"""Distance extension with chained one-lambda modal PINN-SIREN slabs.

The first slab uses the validated z=1 checkpoint.  Each following slab is a
fresh local PINN-SIREN with the same architecture and hard Cauchy condition;
its value and derivative at the left interface come from the previous slab.
No interior angular-spectrum values are used during training.
"""

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import time

os.environ.setdefault("MPLBACKEND", "Agg")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import numpy as np
import torch
from torch.func import jvp

from scripts.experiments import nb03_modal_multiseed_summary as previous
from scripts.experiments import nb03_modal_pinn_siren as modal
from scripts.experiments import nb03_pinn_slabs as base


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def modal_boundary_scale(coeff0, derivative0):
    coeff = coeff0.reshape(-1, 2)
    deriv = derivative0.reshape(-1, 2)
    coeff_complex = coeff[:, 0] + 1j * coeff[:, 1]
    deriv_complex = deriv[:, 0] + 1j * deriv[:, 1]
    amplitude = np.maximum(np.abs(coeff_complex), np.abs(deriv_complex) / base.K)
    amplitude = np.maximum(amplitude, max(float(amplitude.max()) * 1e-4, 1e-8))
    return np.repeat((base.K ** 2 * amplitude).astype(np.float32), 2)


def make_first_model(reference, model_path):
    x = reference["x_lambda"]
    kx = reference["kx"]
    active = reference["propagating_mask"].astype(bool)
    kx_active = kx[active]
    _, field0, dz0 = base.radiative_input(reference)
    field_scale = float(np.sqrt(np.mean(np.abs(field0) ** 2)))
    spectrum0 = np.fft.fft(field0 / field_scale) / len(x)
    spectrum_dz0 = np.fft.fft(dz0 / field_scale) / len(x)
    physical_phase = np.exp(-1j * kx_active * float(x[0]))
    c0 = spectrum0[active] * physical_phase
    d0 = spectrum_dz0[active] * physical_phase
    coefficient0 = np.column_stack((c0.real, c0.imag)).astype(np.float32).reshape(-1)
    derivative0 = np.column_stack((d0.real, d0.imag)).astype(np.float32).reshape(-1)
    model = modal.ModalSiren(
        torch.tensor(coefficient0), torch.tensor(derivative0),
        torch.tensor(modal_boundary_scale(coefficient0, derivative0)), 1.0,
    )
    model.load_state_dict(torch.load(model_path, map_location="cpu", weights_only=True))
    model.eval()
    return model, field_scale, kx_active


def new_slab_from_boundary(previous_model, width):
    dtype = next(previous_model.parameters()).dtype
    z_left = torch.zeros((1, 1), dtype=dtype)
    with torch.no_grad():
        coefficient0 = previous_model(torch.tensor([[width]], dtype=dtype))
    _, derivative0 = jvp(
        previous_model, (torch.tensor([[width]], dtype=dtype),),
        (torch.ones((1, 1), dtype=dtype),),
    )
    coefficient0 = coefficient0.detach().reshape(-1)
    derivative0 = derivative0.detach().reshape(-1)
    model = modal.ModalSiren(
        coefficient0, derivative0,
        torch.tensor(modal_boundary_scale(
            coefficient0.cpu().numpy(), derivative0.cpu().numpy()
        )), width,
    )
    return model


def residual_values(model, coordinates, kz2):
    scale = model.correction_scale.reshape(1, -1, 2)
    return modal.modal_residual(model, coordinates, kz2) / scale


def residual_score(model, coordinates, kz2):
    values = torch.cat([
        residual_values(model, chunk, kz2).detach()
        for chunk in coordinates.split(256)
    ]).cpu().numpy()
    absolute = np.abs(values)
    return {
        "mse": float(np.mean(values ** 2)),
        "rmse": float(np.sqrt(np.mean(values ** 2))),
        "max_abs": float(np.max(absolute)),
        "p99_abs": float(np.quantile(absolute, 0.99)),
    }


def train_slab(model, kz2, seconds, n_train, seed, slab_index):
    dtype = next(model.parameters()).dtype
    width = model.distance
    z_train = torch.tensor(
        (np.arange(n_train) + 0.5) / n_train * width, dtype=dtype
    ).reshape(-1, 1)
    z_selection = torch.tensor(
        np.random.default_rng(2701 + seed + slab_index).uniform(
            0.0, width, size=997
        ), dtype=dtype
    ).reshape(-1, 1)
    initial = residual_score(model, z_selection, kz2)
    best_mse = initial["mse"]
    best_state = copy.deepcopy(model.state_dict())
    best_step = 0
    optimizer = torch.optim.LBFGS(
        model.parameters(), lr=1.0, max_iter=10, max_eval=15,
        history_size=50, tolerance_grad=1e-10, tolerance_change=1e-12,
        line_search_fn="strong_wolfe",
    )
    closure_calls = 0
    step = 0
    t0 = time.perf_counter()

    def closure():
        nonlocal closure_calls
        optimizer.zero_grad(set_to_none=True)
        loss = residual_values(model, z_train, kz2).square().mean()
        if not torch.isfinite(loss):
            raise FloatingPointError("Nonfinite physical loss")
        loss.backward()
        closure_calls += 1
        return loss

    while time.perf_counter() - t0 < seconds:
        optimizer.step(closure)
        step += 1
        score = residual_score(model, z_selection, kz2)
        if score["mse"] < best_mse:
            best_mse = score["mse"]
            best_state = copy.deepcopy(model.state_dict())
            best_step = step
    elapsed = time.perf_counter() - t0
    model.load_state_dict(best_state)
    verified = residual_score(model, z_selection, kz2)["mse"]
    assert np.isclose(verified, best_mse, rtol=1e-6, atol=1e-12)
    return {
        "slab_index": slab_index,
        "width_lambda": width,
        "seconds": elapsed,
        "budget_seconds": seconds,
        "steps": step,
        "closure_calls": closure_calls,
        "selection_initial_mse": initial["mse"],
        "selection_best_mse": verified,
        "optimizer": "LBFGS_float32",
    }


def predict_chained(models, z_values):
    values = []
    width = models[0].distance
    for z in z_values:
        index = min(int(np.floor(z / width)), len(models) - 1)
        local_z = float(z - index * width)
        local_z = min(max(local_z, 0.0), width)
        dtype = next(models[index].parameters()).dtype
        with torch.no_grad():
            value = models[index](torch.tensor([[local_z]], dtype=dtype))
        values.append(value.cpu().numpy().reshape(-1, 2))
    return np.asarray(values)


def evaluate(models, reference, field_scale, kx_active, distance, kz2):
    z = np.linspace(0.0, distance, 201)
    values = predict_chained(models, z)
    coefficients = values[..., 0] + 1j * values[..., 1]
    phase_x = np.exp(1j * np.outer(reference["x_lambda"], kx_active))
    prediction = field_scale * (coefficients @ phase_x.T)
    spectrum = np.fft.fft(np.exp(1j * reference["phase"]))
    all_kz = np.sqrt((base.K ** 2 - reference["kx"] ** 2).astype(complex))
    full = np.fft.ifft(
        spectrum[None, :] * np.exp(1j * z[:, None] * all_kz), axis=1
    )
    active = reference["propagating_mask"].astype(bool)
    prop = np.fft.ifft(
        np.where(active, spectrum, 0.0)[None, :]
        * np.exp(1j * z[:, None] * np.where(active, all_kz, 0.0)), axis=1
    )
    l2_full = np.linalg.norm(prediction - full, axis=1) / np.linalg.norm(full, axis=1)
    l2_prop = np.linalg.norm(prediction - prop, axis=1) / np.linalg.norm(prop, axis=1)
    floor = np.linalg.norm(full - prop, axis=1) / np.linalg.norm(full, axis=1)
    neural_common = np.linalg.norm(prediction - prop, axis=1) / np.linalg.norm(full, axis=1)
    identity = np.max(np.abs(l2_full ** 2 - floor ** 2 - neural_common ** 2))
    assert identity < 1e-10, identity
    metrics = base.complex_field_metrics(prediction[-1], full[-1])
    c_ref = base.intensity_statistics(full[-1])["contrast"]
    c_pred = base.intensity_statistics(prediction[-1])["contrast"]
    residuals = []
    for model in models:
        local_z = torch.linspace(0.0, model.distance, 1001).reshape(-1, 1)
        residuals.append(residual_score(model, local_z, kz2))
    return {
        "distance_lambda": distance,
        "n_slabs": len(models),
        "l2_full_final": float(l2_full[-1]),
        "l2_propagating_final": float(l2_prop[-1]),
        "l2_propagating_max": float(l2_prop.max()),
        "l2_propagating_max_z": float(z[np.argmax(l2_prop)]),
        "l2_full_max": float(l2_full.max()),
        "evanescent_floor_final": float(floor[-1]),
        "coherence_full_final": metrics["target_complex_coherence"],
        "intensity_correlation_full_final": metrics["target_intensity_pearson_correlation"],
        "contrast_full": c_ref,
        "contrast_pinn": c_pred,
        "contrast_difference": abs(c_pred - c_ref),
        "reference_fidelity_pass": bool(
            l2_full[-1] < 0.05 and abs(c_pred - c_ref) < 0.05
        ),
        "slab_residuals": residuals,
    }, {
        "z_lambda": z,
        "l2_full": l2_full,
        "l2_propagating": l2_prop,
        "evanescent_floor": floor,
        "field_pred": prediction,
        "field_full": full,
        "field_propagating": prop,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=int, nargs="+", default=[42])
    parser.add_argument("--distances", type=int, nargs="+", default=[2])
    parser.add_argument("--seconds", type=float, default=60.0)
    parser.add_argument("--n-train", type=int, default=1024)
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--name", default="pilot_z2_slabs")
    args = parser.parse_args()
    if args.seconds <= 0 or args.n_train < 2 or args.threads < 1:
        parser.error("seconds, n-train and threads must be positive")
    if any(distance < 2 for distance in args.distances):
        parser.error("distances must be integer values >= 2 lambda")

    out = ROOT / "results" / "nb03_distance_pilot" / args.name
    out.mkdir(parents=True, exist_ok=False)
    torch.set_num_threads(args.threads)
    modal.HIDDEN_DIM, modal.NUM_LAYERS = 128, 4
    modal.FIRST_OMEGA, modal.HIDDEN_OMEGA = 30.0, 1.0
    summary = {
        "experiment": "NB03 chained modal PINN-SIREN distance pilot",
        "scope": "One-lambda slabs; first slab is the validated z=1 model",
        "configuration": vars(args),
        "runtime": {
            "python": sys.version, "torch": torch.__version__,
            "numpy": np.__version__, "platform": platform.platform(),
            "device": "cpu", "threads": torch.get_num_threads(),
        },
        "source_script_sha256": digest(Path(__file__)),
        "protocol": (
            "Each slab solves the modal Helmholtz residual locally. The next "
            "slab receives value and derivative from the previous slab. "
            "Angular spectrum is used only for independent evaluation."
        ),
        "cases": [],
    }
    source_dir_map = {
        42: "pilot1", 123: "pilot1", 321: "confirmation3",
        777: "confirmation3", 2026: "confirmation3",
    }
    for seed in args.seeds:
        case = next(c for c in previous.CASES if c[0] == seed)
        reference_path = ROOT / "results" / (
            f"nb03_angular_spectrum_reference{case[1]}.npz"
        )
        source_model = ROOT / "results" / "nb03_refinement" / (
            source_dir_map[seed]
        ) / f"seed{seed}_lbfgs32.pt"
        reference = dict(np.load(reference_path))
        first, field_scale, kx_active = make_first_model(reference, source_model)
        active = reference["propagating_mask"].astype(bool)
        kz2 = torch.tensor(
            np.maximum(base.K ** 2 - reference["kx"][active] ** 2, 0),
            dtype=torch.float32,
        )
        seed_entry = {"seed": seed, "distances": {}}
        summary["cases"].append(seed_entry)
        for distance in args.distances:
            models = [copy.deepcopy(first)]
            slab_training = []
            for slab_index in range(1, distance):
                slab = new_slab_from_boundary(models[-1], 1.0)
                training = train_slab(
                    slab, kz2, args.seconds, args.n_train, seed, slab_index
                )
                models.append(slab)
                slab_training.append(training)
                torch.save(slab.state_dict(), out / f"seed{seed}_z{distance}_slab{slab_index}.pt")
                print(
                    f"Seed {seed}, z={distance} lambda, slab {slab_index}: "
                    f"residual={training['selection_best_mse']:.3e} "
                    f"seconds={training['seconds']:.1f}", flush=True
                )
            metrics, arrays = evaluate(
                models, reference, field_scale, kx_active, float(distance), kz2
            )
            label = f"z{distance}"
            seed_entry["distances"][label] = {
                "training": slab_training,
                "metrics": metrics,
            }
            np.savez_compressed(out / f"seed{seed}_{label}.npz", **arrays)
            (out / "summary.json").write_text(
                json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            print(
                f"Seed {seed}, z={distance} lambda: "
                f"prop={100*metrics['l2_propagating_final']:.4f}% "
                f"full={100*metrics['l2_full_final']:.4f}% "
                f"max_prop={100*metrics['l2_propagating_max']:.4f}%",
                flush=True,
            )
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 5))
    for entry in summary["cases"]:
        for label in entry["distances"]:
            data = np.load(out / f"seed{entry['seed']}_{label}.npz")
            ax.plot(data["z_lambda"], data["l2_propagating"] * 100,
                    label=f"semilla {entry['seed']}, {label}")
    ax.axhline(1.0, color="black", linestyle="--", label="1 %")
    ax.set(xlabel="z/lambda", ylabel="L2 propagante (%)",
           title="NB03: bloques modales de una longitud de onda")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / "comparison.png", dpi=150)
    plt.close(fig)
    print(f"Completed: {out}", flush=True)


if __name__ == "__main__":
    main()
