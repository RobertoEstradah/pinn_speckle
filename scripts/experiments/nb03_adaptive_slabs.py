"""Propagación NB03 por bloques locales con SIREN de frecuencia adaptativa.

Cada bloque tiene ancho de una lambda. El campo y su derivada al final del
bloque anterior se imponen como condición de Cauchy dura del siguiente. Los
pesos internos y la frecuencia aprendida se transfieren, pero la referencia de
espectro angular no se usa para entrenamiento ni selección.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch
from torch.func import jvp


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.experiments import nb03_adaptive_omega_holdout as adaptive  # noqa: E402
from scripts.experiments import nb03_modal_multiseed_summary as modal_summary  # noqa: E402
from scripts.experiments import nb03_modal_refinement as refinement  # noqa: E402
from scripts.experiments import nb03_modal_slabs_pilot as slab_tools  # noqa: E402
from scripts.experiments import nb03_pinn_slabs as base  # noqa: E402


BUFFER_NAMES = {"coefficient0", "derivative0", "correction_scale"}


def load_first_state(model, model_path):
    """Carga un checkpoint adaptativo o convierte exactamente la SIREN fija."""
    state = torch.load(model_path, map_location="cpu", weights_only=True)
    if "activation_a" in state:
        model.load_state_dict(state)
        return "adaptive"
    if "net.0.linear.weight" not in state:
        raise ValueError("Formato de checkpoint inicial no reconocido.")
    converted = model.state_dict()
    for name in BUFFER_NAMES:
        converted[name] = state[name].detach().clone()
    for index in range(4):
        for parameter in ("weight", "bias"):
            converted[f"hidden.{index}.linear.{parameter}"] = state[
                f"net.{index}.linear.{parameter}"
            ].detach().clone()
    converted["final.weight"] = state["net.4.weight"].detach().clone()
    converted["final.bias"] = state["net.4.bias"].detach().clone()
    # activation_a conserva 1/n, por lo que n*a=1 y la salida es idéntica.
    model.load_state_dict(converted)
    return "fixed_siren_exact_conversion"


def first_model(reference, model_path, slope_multiplier):
    # ``build_model`` también reconstruye la escala física y los modos activos.
    # Desde la consolidación multisemilla recibe explícitamente el checkpoint;
    # el estado se vuelve a convertir abajo a la variante adaptativa, de modo
    # que esta llamada conserva una única fuente de verdad para la frontera.
    shell, field_scale, kx_active = modal_summary.build_model(
        reference, model_path
    )
    model = adaptive.AdaptiveOmegaModalSiren(
        shell.coefficient0.detach().flatten(),
        shell.derivative0.detach().flatten(),
        shell.correction_scale.detach().flatten(),
        1.0,
        slope_multiplier=slope_multiplier,
    )
    source_format = load_first_state(model, model_path)
    return model, field_scale, kx_active, source_format


def next_model(previous, slope_multiplier):
    dtype = next(previous.parameters()).dtype
    right = torch.ones((1, 1), dtype=dtype) * previous.distance
    value, derivative = jvp(
        previous, (right,), (torch.ones_like(right),)
    )
    coefficient0 = value.detach().flatten()
    derivative0 = derivative.detach().flatten()
    scale = torch.tensor(
        slab_tools.modal_boundary_scale(
            coefficient0.cpu().numpy(), derivative0.cpu().numpy()
        ),
        dtype=dtype,
    )
    model = adaptive.AdaptiveOmegaModalSiren(
        coefficient0,
        derivative0,
        scale,
        1.0,
        slope_multiplier=slope_multiplier,
    )
    destination = model.state_dict()
    for name, value_state in previous.state_dict().items():
        if name not in BUFFER_NAMES:
            destination[name] = value_state.detach().clone()
    model.load_state_dict(destination)
    return model


def interface_errors(left, right):
    dtype = next(left.parameters()).dtype
    z_right = torch.ones((1, 1), dtype=dtype) * left.distance
    left_value, left_derivative = jvp(
        left, (z_right,), (torch.ones_like(z_right),)
    )
    z_left = torch.zeros((1, 1), dtype=dtype)
    right_value, right_derivative = jvp(
        right, (z_left,), (torch.ones_like(z_left),)
    )
    return {
        "field_max_abs": float((left_value - right_value).abs().max().detach()),
        "derivative_max_abs": float(
            (left_derivative - right_derivative).abs().max().detach()
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference-suffix", default="_z1_seed31415_corr0.10")
    parser.add_argument("--first-model", required=True)
    parser.add_argument(
        "--resume-dir",
        help="Directorio de una corrida por bloques que se reutilizara como prefijo.",
    )
    parser.add_argument("--screen-seed", type=int, default=31415)
    parser.add_argument("--network-seed", type=int, default=73)
    parser.add_argument("--target-distance", type=int, default=2)
    parser.add_argument("--adam-seconds", type=float, default=60.0)
    parser.add_argument("--lbfgs-seconds", type=float, default=120.0)
    parser.add_argument("--n-train", type=int, default=1024)
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--slope-multiplier", type=float, default=10.0)
    parser.add_argument("--name", required=True)
    args = parser.parse_args()
    if args.target_distance < 2:
        parser.error("target-distance debe ser un entero >= 2.")
    if min(args.adam_seconds, args.lbfgs_seconds, args.slope_multiplier) <= 0:
        parser.error("Los presupuestos y slope-multiplier deben ser positivos.")

    torch.set_num_threads(args.threads)
    torch.manual_seed(args.network_seed)
    np.random.seed(args.network_seed)
    reference_path = ROOT / "results" / (
        f"nb03_angular_spectrum_reference{args.reference_suffix}.npz"
    )
    source = Path(args.first_model)
    if not source.is_absolute():
        source = ROOT / source
    reference = dict(np.load(reference_path))
    if int(reference.get("reference_seed", args.screen_seed)) != args.screen_seed:
        raise ValueError("La semilla de pantalla no coincide con la referencia.")

    first, field_scale, kx_active, source_format = first_model(
        reference, source, args.slope_multiplier
    )
    models = [first]
    blocks = [{
        "index": 0,
        "global_interval_lambda": [0.0, 1.0],
        "source_model": str(source),
        "source_format": source_format,
        "adaptive_scale": float(first.adaptive_scale.detach()),
        "prevalidated": True,
    }]

    output_dir = ROOT / "results" / "nb03_distance_pilot" / args.name
    output_dir.mkdir(parents=True, exist_ok=False)
    torch.save(first.state_dict(), output_dir / "slab0.pt")

    if args.resume_dir:
        resume_dir = Path(args.resume_dir)
        if not resume_dir.is_absolute():
            resume_dir = ROOT / resume_dir
        previous_summary = json.loads(
            (resume_dir / "summary.json").read_text(encoding="utf-8")
        )
        previous_config = previous_summary["configuration"]
        for key in ("screen_seed", "network_seed", "reference_suffix"):
            if previous_config[key] != getattr(args, key):
                raise ValueError(f"La configuracion reanudada no coincide en {key}.")
        previous_distance = int(previous_config["target_distance"])
        if previous_distance >= args.target_distance:
            raise ValueError("target-distance debe superar la corrida reanudada.")
        blocks = previous_summary["blocks"]
        blocks[0]["resumed_from"] = str(resume_dir)
        for index in range(1, previous_distance):
            model = next_model(models[-1], args.slope_multiplier)
            model.load_state_dict(torch.load(
                resume_dir / f"slab{index}.pt",
                map_location="cpu",
                weights_only=True,
            ))
            continuity = interface_errors(models[-1], model)
            if max(continuity.values()) > 1e-6:
                raise RuntimeError(
                    f"Fallo de continuidad al reanudar interfaz {index}."
                )
            models.append(model)
            torch.save(model.state_dict(), output_dir / f"slab{index}.pt")
            blocks[index]["resumed_from"] = str(resume_dir)
        print(
            f"Prefijo validado reutilizado: 0-{previous_distance} lambda",
            flush=True,
        )

    active = reference["propagating_mask"].astype(bool)
    kz2 = torch.tensor(
        np.maximum(base.K ** 2 - reference["kx"][active] ** 2, 0),
        dtype=torch.float32,
    )
    for index in range(len(models), args.target_distance):
        model = next_model(models[-1], args.slope_multiplier)
        interface_before = interface_errors(models[-1], model)
        kz2, adam_training = refinement.train(
            model,
            reference,
            "adam32",
            args.adam_seconds,
            args.n_train,
            learning_rate=5e-5,
            selection_interval=50,
        )
        kz2, lbfgs_training = refinement.train(
            model,
            reference,
            "lbfgs32",
            args.lbfgs_seconds,
            args.n_train,
        )
        interface_after = interface_errors(models[-1], model)
        if max(interface_after.values()) > 1e-6:
            raise RuntimeError(f"Fallo de continuidad en interfaz {index}.")
        models.append(model)
        torch.save(model.state_dict(), output_dir / f"slab{index}.pt")
        blocks.append({
            "index": index,
            "global_interval_lambda": [float(index), float(index + 1)],
            "transferred_trainable_weights": True,
            "interface_before_training": interface_before,
            "interface_after_training": interface_after,
            "adaptive_scale": float(model.adaptive_scale.detach()),
            "adam": adam_training,
            "lbfgs": lbfgs_training,
        })
        print(
            f"Bloque {index}: escala={float(model.adaptive_scale.detach()):.5f} "
            f"res_sel={lbfgs_training['selection_best_mse']**0.5:.3e}",
            flush=True,
        )

    metrics, arrays = slab_tools.evaluate(
        models,
        reference,
        field_scale,
        kx_active,
        float(args.target_distance),
        kz2,
    )
    np.savez_compressed(
        output_dir / f"adaptive_slabs_z{args.target_distance}.npz", **arrays
    )
    output = {
        "experiment": "NB03 adaptive-frequency transferred-weight slabs",
        "configuration": vars(args),
        "protocol": {
            "coordinates": "Cartesian x,z; local coordinate per one-lambda slab",
            "equation": "complete modal Helmholtz",
            "hard_cauchy_each_interface": True,
            "training_labels": False,
            "selection_uses_reference_field": False,
            "reference": "angular spectrum used only after all slabs",
        },
        "blocks": blocks,
        "metrics": metrics,
        "acceptance": {
            "full_final_below_5pct": metrics["l2_full_final"] < 0.05,
            "propagating_final_below_5pct": metrics["l2_propagating_final"] < 0.05,
            "propagating_all_201_planes_below_5pct": metrics["l2_propagating_max"] < 0.05,
            "contrast_reference_error_below_0_05": metrics["contrast_difference"] < 0.05,
            "goodman_reference_abs_C_minus_1_below_0_1": abs(
                metrics["contrast_full"] - 1.0
            ) < 0.1,
            "goodman_pinn_abs_C_minus_1_below_0_1": abs(
                metrics["contrast_pinn"] - 1.0
            ) < 0.1,
        },
    }
    (output_dir / "summary.json").write_text(
        json.dumps(output, indent=2), encoding="utf-8"
    )
    print(
        f"z={args.target_distance} lambda: prop={100*metrics['l2_propagating_final']:.4f}% "
        f"max_prop={100*metrics['l2_propagating_max']:.4f}% "
        f"full={100*metrics['l2_full_final']:.4f}% "
        f"contrast_diff={metrics['contrast_difference']:.5f}",
        flush=True,
    )
    print(f"Resultado: {output_dir}", flush=True)


if __name__ == "__main__":
    main()
