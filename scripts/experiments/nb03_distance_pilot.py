"""Controlled NB03 distance-extension pilot.

This pilot keeps the modal PINN-SIREN architecture and hard Cauchy
condition, but rescales the longitudinal coordinate for each requested
distance.  Each distance is trained independently from the corresponding
validated z=1 checkpoint; no interior reference field is used for training.

Run from the project root, for example:
  python -u scripts/experiments/nb03_distance_pilot.py \
      --seeds 42 --distances 2 5 --seconds 60 --name pilot_z2_z5
"""

import argparse
import copy
import hashlib
import json
import math
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


def make_model(reference, model_path, distance):
    x = reference["x_lambda"]
    kx = reference["kx"]
    active = reference["propagating_mask"].astype(bool)
    kx_active = kx[active]
    _, field0, dz0 = base.radiative_input(reference)
    field_scale = float(np.sqrt(np.mean(np.abs(field0) ** 2)))
    spectrum0 = np.fft.fft(field0 / field_scale) / len(x)
    spectrum_dz0 = np.fft.fft(dz0 / field_scale) / len(x)
    physical_phase = np.exp(-1j * kx_active * float(x[0]))
    coefficient0_complex = spectrum0[active] * physical_phase
    derivative0_complex = spectrum_dz0[active] * physical_phase
    coefficient0 = np.column_stack((
        coefficient0_complex.real, coefficient0_complex.imag
    )).astype(np.float32).reshape(-1)
    derivative0 = np.column_stack((
        derivative0_complex.real, derivative0_complex.imag
    )).astype(np.float32).reshape(-1)
    modal_amplitude = np.maximum(
        np.abs(coefficient0_complex),
        np.abs(derivative0_complex) / base.K,
    )
    floor = max(float(modal_amplitude.max()) * 1e-4, 1e-8)
    modal_amplitude = np.maximum(modal_amplitude, floor)
    correction_scale = np.repeat(
        (base.K ** 2 * modal_amplitude).astype(np.float32), 2
    )
    model = modal.ModalSiren(
        torch.tensor(coefficient0),
        torch.tensor(derivative0),
        torch.tensor(correction_scale),
        float(distance),
    )
    model.load_state_dict(torch.load(
        model_path, map_location="cpu", weights_only=True
    ))
    model.eval()
    return model, field_scale, kx_active


def residual_values(model, coordinates, kz2):
    scale = model.correction_scale.reshape(1, -1, 2)
    return modal.modal_residual(model, coordinates, kz2) / scale


def residual_score(model, coordinates, kz2):
    chunks = []
    for chunk in coordinates.split(256):
        chunks.append(residual_values(model, chunk, kz2).detach())
    values = torch.cat(chunks).cpu().numpy()
    absolute = np.abs(values)
    return {
        "mse": float(np.mean(values ** 2)),
        "rmse": float(np.sqrt(np.mean(values ** 2))),
        "max_abs": float(np.max(absolute)),
        "p99_abs": float(np.quantile(absolute, 0.99)),
    }


def evaluate(model, reference, field_scale, kx_active, distance, kz2):
    dtype = next(model.parameters()).dtype
    z = np.linspace(0.0, distance, 201)
    with torch.no_grad():
        values = model(torch.tensor(z, dtype=dtype).reshape(-1, 1))
    values = values.cpu().numpy().reshape(len(z), -1, 2)
    coefficients = values[..., 0] + 1j * values[..., 1]
    phase_x = np.exp(1j * np.outer(reference["x_lambda"], kx_active))
    prediction = field_scale * (coefficients @ phase_x.T)

    spectrum = np.fft.fft(np.exp(1j * reference["phase"]))
    all_kz = np.sqrt((base.K ** 2 - reference["kx"] ** 2).astype(complex))
    full = np.fft.ifft(
        spectrum[None, :] * np.exp(1j * z[:, None] * all_kz), axis=1
    )
    active = reference["propagating_mask"].astype(bool)
    spectrum_prop = np.where(active, spectrum, 0.0)
    prop_kz = np.where(active, all_kz, 0.0)
    propagating = np.fft.ifft(
        spectrum_prop[None, :] * np.exp(1j * z[:, None] * prop_kz), axis=1
    )

    full_norm = np.linalg.norm(full, axis=1)
    prop_norm = np.linalg.norm(propagating, axis=1)
    l2_full = np.linalg.norm(prediction - full, axis=1) / full_norm
    l2_prop = np.linalg.norm(prediction - propagating, axis=1) / prop_norm
    evanescent_floor = np.linalg.norm(full - propagating, axis=1) / full_norm
    neural_common = np.linalg.norm(prediction - propagating, axis=1) / full_norm
    identity = np.max(
        np.abs(l2_full ** 2 - evanescent_floor ** 2 - neural_common ** 2)
    )
    assert identity < 1e-10, identity
    assert np.isfinite(prediction).all()

    z0 = torch.zeros((1, 1), dtype=dtype)
    value0, dz0 = jvp(model, (z0,), (torch.ones_like(z0),))
    boundary_error = float((value0 - model.coefficient0).abs().max().detach())
    derivative_error = float((dz0 - model.derivative0).abs().max().detach())
    assert boundary_error < 1e-6 and derivative_error < 1e-6

    metrics = base.complex_field_metrics(prediction[-1], full[-1])
    contrast_reference = base.intensity_statistics(full[-1])["contrast"]
    contrast_prediction = base.intensity_statistics(prediction[-1])["contrast"]
    return {
        "distance_lambda": float(distance),
        "l2_full_final": float(l2_full[-1]),
        "l2_propagating_final": float(l2_prop[-1]),
        "l2_propagating_max": float(l2_prop.max()),
        "l2_propagating_max_z": float(z[np.argmax(l2_prop)]),
        "l2_full_max": float(l2_full.max()),
        "evanescent_floor_final": float(evanescent_floor[-1]),
        "coherence_full_final": metrics["target_complex_coherence"],
        "intensity_correlation_full_final": metrics[
            "target_intensity_pearson_correlation"
        ],
        "contrast_full": contrast_reference,
        "contrast_pinn": contrast_prediction,
        "contrast_difference": abs(contrast_prediction - contrast_reference),
        "reference_fidelity_pass": bool(
            l2_full[-1] < 0.05 and
            abs(contrast_prediction - contrast_reference) < 0.05
        ),
        "test_residual": None,
        "cauchy_field_max_abs": boundary_error,
        "cauchy_derivative_max_abs": derivative_error,
        "spectral_error_identity_max_abs": float(identity),
    }, {
        "z_lambda": z,
        "l2_full": l2_full,
        "l2_propagating": l2_prop,
        "evanescent_floor": evanescent_floor,
        "field_pred": prediction,
        "field_full": full,
        "field_propagating": propagating,
    }


def train(model, reference, distance, seconds, n_train, seed):
    dtype = next(model.parameters()).dtype
    active = reference["propagating_mask"].astype(bool)
    kz2 = torch.tensor(
        np.maximum(base.K ** 2 - reference["kx"][active] ** 2, 0),
        dtype=dtype,
    )
    z_train = torch.tensor(
        (np.arange(n_train) + 0.5) / n_train * distance,
        dtype=dtype,
    ).reshape(-1, 1)
    z_selection = torch.tensor(
        np.random.default_rng(1717 + seed).uniform(0.0, distance, size=997),
        dtype=dtype,
    ).reshape(-1, 1)
    initial = residual_score(model, z_selection, kz2)
    best_mse = initial["mse"]
    best_state = copy.deepcopy(model.state_dict())
    best_step = 0
    history = [{"step": 0, "seconds": 0.0, "selection_mse": best_mse}]
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
        history.append({
            "step": step,
            "seconds": time.perf_counter() - t0,
            "selection_mse": score["mse"],
        })
    elapsed = time.perf_counter() - t0
    model.load_state_dict(best_state)
    verified = residual_score(model, z_selection, kz2)["mse"]
    assert np.isclose(verified, best_mse, rtol=1e-6, atol=1e-12)
    return kz2, {
        "seconds": elapsed,
        "budget_seconds": seconds,
        "steps": step,
        "closure_calls": closure_calls,
        "best_step": best_step,
        "selection_initial_mse": initial["mse"],
        "selection_best_mse": verified,
        "history": history,
        "optimizer": "LBFGS_float32",
        "optimizer_state_resumed": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=int, nargs="+", default=[42])
    parser.add_argument("--distances", type=float, nargs="+", default=[2.0, 5.0])
    parser.add_argument("--seconds", type=float, default=60.0)
    parser.add_argument("--n-train", type=int, default=1024)
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--name", default="pilot_z2_z5")
    args = parser.parse_args()
    if args.seconds <= 0 or args.n_train < 2 or args.threads < 1:
        parser.error("seconds, n-train and threads must be positive")
    if any(distance <= 1.0 for distance in args.distances):
        parser.error("distances must be greater than 1 lambda")
    if len(set(args.distances)) != len(args.distances):
        parser.error("distances must be unique")
    if not args.name.replace("_", "").replace("-", "").isalnum():
        parser.error("name must be an alphanumeric label")

    out = ROOT / "results" / "nb03_distance_pilot" / args.name
    out.mkdir(parents=True, exist_ok=False)
    torch.set_num_threads(args.threads)
    torch.manual_seed(42)
    modal.HIDDEN_DIM, modal.NUM_LAYERS = 128, 4
    modal.FIRST_OMEGA, modal.HIDDEN_OMEGA = 30.0, 1.0

    summary = {
        "experiment": "NB03 distance-extension pilot",
        "scope": "Independent retraining at each distance; same modal PINN-SIREN architecture",
        "configuration": vars(args),
        "source_dirs": {
            "42": "results/nb03_refinement/pilot1",
            "123": "results/nb03_refinement/pilot1",
            "321": "results/nb03_refinement/confirmation3",
            "777": "results/nb03_refinement/confirmation3",
            "2026": "results/nb03_refinement/confirmation3",
        },
        "runtime": {
            "python": sys.version,
            "torch": torch.__version__,
            "numpy": np.__version__,
            "platform": platform.platform(),
            "device": "cpu",
            "threads": torch.get_num_threads(),
        },
        "source_script_sha256": digest(Path(__file__)),
        "protocol": (
            "Load the validated z=1 L-BFGS float32 checkpoint for each screen, "
            "reinstantiate the same hard-Cauchy model with distance z_max, "
            "train only on the normalized Helmholtz residual, select by 997 "
            "fixed residual points, and test on 201 field planes."
        ),
        "cases": [],
    }

    for seed in args.seeds:
        case = next(c for c in previous.CASES if c[0] == seed)
        reference_path = ROOT / "results" / (
            f"nb03_angular_spectrum_reference{case[1]}.npz"
        )
        source_dir = ROOT / "results" / "nb03_refinement" / (
            "pilot1" if seed in (42, 123) else "confirmation3"
        )
        source_model = source_dir / f"seed{seed}_lbfgs32.pt"
        if not source_model.exists():
            raise FileNotFoundError(source_model)
        reference = dict(np.load(reference_path))
        case_entry = {
            "seed": seed,
            "reference_path": str(reference_path),
            "reference_sha256": digest(reference_path),
            "source_model": str(source_model),
            "source_model_sha256": digest(source_model),
            "distances": {},
        }
        summary["cases"].append(case_entry)
        for distance in args.distances:
            label = f"z{distance:g}"
            model, field_scale, kx_active = make_model(
                reference, source_model, distance
            )
            kz2, training = train(
                model, reference, distance, args.seconds, args.n_train, seed
            )
            metrics, arrays = evaluate(
                model, reference, field_scale, kx_active, distance, kz2
            )
            selection_z = torch.tensor(
                np.random.default_rng(1717 + seed).uniform(
                    0.0, distance, size=997
                ), dtype=torch.float32
            ).reshape(-1, 1)
            metrics["test_residual"] = residual_score(model, torch.tensor(
                np.linspace(0.0, distance, 2001), dtype=torch.float32
            ).reshape(-1, 1), kz2)
            metrics["selection_residual"] = residual_score(
                model, selection_z, kz2
            )
            training["seconds"] = float(training["seconds"])
            case_entry["distances"][label] = {
                "distance_lambda": float(distance),
                "training": training,
                "metrics": metrics,
            }
            torch.save(model.state_dict(), out / f"seed{seed}_{label}.pt")
            np.savez_compressed(out / f"seed{seed}_{label}.npz", **arrays)
            summary_path = out / "summary.json"
            summary_path.write_text(
                json.dumps(summary, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            print(
                f"Seed {seed}, z={distance:g} lambda: "
                f"prop={100*metrics['l2_propagating_final']:.4f}% "
                f"full={100*metrics['l2_full_final']:.4f}% "
                f"max_prop={100*metrics['l2_propagating_max']:.4f}% "
                f"residual={metrics['test_residual']['rmse']:.3e} "
                f"seconds={training['seconds']:.1f}",
                flush=True,
            )

    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(
        len(args.seeds), len(args.distances),
        figsize=(6 * len(args.distances), 4 * len(args.seeds)),
        squeeze=False,
    )
    for row_index, entry in enumerate(summary["cases"]):
        seed = entry["seed"]
        for col_index, distance in enumerate(args.distances):
            label = f"z{distance:g}"
            data = np.load(out / f"seed{seed}_{label}.npz")
            ax = axes[row_index][col_index]
            ax.plot(data["z_lambda"], data["l2_propagating"] * 100)
            ax.axhline(1.0, color="black", linestyle="--", alpha=0.65)
            ax.set(
                title=f"Pantalla {seed}, z_max={distance:g} lambda",
                xlabel="z/lambda", ylabel="L2 propagante (%)",
            )
            ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(out / "comparison.png", dpi=150)
    plt.close(fig)
    print(f"Completed: {out}", flush=True)


if __name__ == "__main__":
    main()
