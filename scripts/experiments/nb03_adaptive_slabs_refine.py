"""Refina una corrida NB03 por bloques sin usar etiquetas interiores.

Cada bloque se reconstruye con la frontera de Cauchy producida por el bloque
anterior ya refinado. Los pesos entrenables de la corrida de origen sirven
como inicializacion, pero los buffers de frontera se recalculan para conservar
continuidad dura. La seleccion sigue dependiendo solo del residuo de
Helmholtz; el espectro angular se consulta al finalizar.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.experiments import nb03_adaptive_slabs as slabs  # noqa: E402
from scripts.experiments import nb03_modal_refinement as refinement  # noqa: E402
from scripts.experiments import nb03_modal_slabs_pilot as slab_tools  # noqa: E402
from scripts.experiments import nb03_pinn_slabs as base  # noqa: E402


def load_trainable_state(model: torch.nn.Module, path: Path) -> None:
    """Carga pesos aprendidos, preservando la nueva frontera dura."""
    old = torch.load(path, map_location="cpu", weights_only=True)
    state = model.state_dict()
    missing = []
    for name in state:
        if name in slabs.BUFFER_NAMES:
            continue
        if name not in old:
            missing.append(name)
            continue
        state[name] = old[name].detach().clone()
    if missing:
        raise ValueError(f"Faltan parametros entrenables: {missing}")
    model.load_state_dict(state)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--adam-seconds", type=float, default=60.0)
    parser.add_argument("--lbfgs-seconds", type=float, default=120.0)
    parser.add_argument("--n-train", type=int, default=1024)
    parser.add_argument("--threads", type=int, default=2)
    parser.add_argument(
        "--start-block",
        type=int,
        default=1,
        help="Primer bloque que se reentrena; los anteriores se reconstruyen sin optimizar.",
    )
    args = parser.parse_args()
    if min(args.adam_seconds, args.lbfgs_seconds, args.n_train, args.threads) <= 0:
        parser.error("Los presupuestos, puntos y threads deben ser positivos.")

    source_dir = Path(args.source_dir)
    if not source_dir.is_absolute():
        source_dir = ROOT / source_dir
    source_summary = json.loads(
        (source_dir / "summary.json").read_text(encoding="utf-8")
    )
    config = source_summary["configuration"]
    target_distance = int(config["target_distance"])
    if not 1 <= args.start_block < target_distance:
        raise ValueError(
            "start-block debe estar entre 1 y target_distance-1."
        )

    output_dir = ROOT / "results" / "nb03_distance_pilot" / args.name
    output_dir.mkdir(parents=True, exist_ok=False)
    torch.set_num_threads(args.threads)
    torch.manual_seed(int(config["network_seed"]))
    np.random.seed(int(config["network_seed"]))

    reference_path = ROOT / "results" / (
        f"nb03_angular_spectrum_reference{config['reference_suffix']}.npz"
    )
    reference = dict(np.load(reference_path))
    first_path = Path(config["first_model"])
    if not first_path.is_absolute():
        first_path = ROOT / first_path
    slope_multiplier = float(config["slope_multiplier"])
    first, field_scale, kx_active, source_format = slabs.first_model(
        reference, first_path, slope_multiplier
    )
    first.load_state_dict(torch.load(
        source_dir / "slab0.pt", map_location="cpu", weights_only=True
    ))
    models = [first]
    torch.save(first.state_dict(), output_dir / "slab0.pt")
    blocks = [{
        "index": 0,
        "global_interval_lambda": [0.0, 1.0],
        "source_model": first_path.as_posix(),
        "source_format": source_format,
        "source_slab": (source_dir / "slab0.pt").as_posix(),
        "prevalidated": True,
        "adaptive_scale": float(first.adaptive_scale.detach()),
    }]

    active = reference["propagating_mask"].astype(bool)
    kz2 = torch.tensor(
        np.maximum(base.K ** 2 - reference["kx"][active] ** 2, 0),
        dtype=torch.float32,
    )
    for index in range(1, target_distance):
        model = slabs.next_model(models[-1], slope_multiplier)
        load_trainable_state(model, source_dir / f"slab{index}.pt")
        interface_before = slabs.interface_errors(models[-1], model)
        if index >= args.start_block:
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
        else:
            adam_training = {"skipped": True}
            lbfgs_training = {"skipped": True}
        interface_after = slabs.interface_errors(models[-1], model)
        if max(interface_after.values()) > 1e-6:
            raise RuntimeError(f"Fallo de continuidad en interfaz {index}.")
        models.append(model)
        torch.save(model.state_dict(), output_dir / f"slab{index}.pt")
        blocks.append({
            "index": index,
            "global_interval_lambda": [float(index), float(index + 1)],
            "source_slab": (source_dir / f"slab{index}.pt").as_posix(),
            "hard_boundary_recomputed": True,
            "interface_before_training": interface_before,
            "interface_after_training": interface_after,
            "adaptive_scale": float(model.adaptive_scale.detach()),
            "refinement_skipped": index < args.start_block,
            "adam": adam_training,
            "lbfgs": lbfgs_training,
        })
        if index >= args.start_block:
            print(
                f"Bloque {index}: escala={float(model.adaptive_scale.detach()):.5f} "
                f"res_sel={lbfgs_training['selection_best_mse']**0.5:.3e}",
                flush=True,
            )
        else:
            print(f"Bloque {index}: reconstruido sin reentrenar", flush=True)

    metrics, arrays = slab_tools.evaluate(
        models,
        reference,
        field_scale,
        kx_active,
        float(target_distance),
        kz2,
    )
    np.savez_compressed(
        output_dir / f"adaptive_slabs_z{target_distance}.npz", **arrays
    )
    acceptance = {
        "full_final_below_5pct": metrics["l2_full_final"] < 0.05,
        "propagating_final_below_5pct": (
            metrics["l2_propagating_final"] < 0.05
        ),
        "propagating_all_201_planes_below_5pct": (
            metrics["l2_propagating_max"] < 0.05
        ),
        "coherence_above_0_99": metrics["coherence_full_final"] > 0.99,
        "intensity_correlation_above_0_99": (
            metrics["intensity_correlation_full_final"] > 0.99
        ),
        "contrast_reference_error_below_0_05": (
            metrics["contrast_difference"] < 0.05
        ),
    }
    output = {
        "experiment": "NB03 adaptive-frequency slab residual refinement",
        "configuration": {
            **config,
            "source_dir": source_dir.as_posix(),
            "adam_refinement_seconds": args.adam_seconds,
            "lbfgs_refinement_seconds": args.lbfgs_seconds,
            "n_train_refinement": args.n_train,
            "threads_refinement": args.threads,
            "name": args.name,
        },
        "protocol": {
            "coordinates": "Cartesian x,z; local coordinate per one-lambda slab",
            "equation": "complete modal Helmholtz",
            "hard_cauchy_each_interface": True,
            "training_labels": False,
            "selection_uses_reference_field": False,
            "reference": "angular spectrum used only after all slabs",
            "refinement": "warm-start weights; hard boundary recomputed downstream",
        },
        "blocks": blocks,
        "metrics": metrics,
        "acceptance": acceptance,
        "accepted": all(acceptance.values()),
    }
    (output_dir / "summary.json").write_text(
        json.dumps(output, indent=2), encoding="utf-8"
    )
    print(
        f"z={target_distance} lambda: "
        f"prop={100*metrics['l2_propagating_final']:.4f}% "
        f"max_prop={100*metrics['l2_propagating_max']:.4f}% "
        f"full={100*metrics['l2_full_final']:.4f}% "
        f"accepted={output['accepted']}",
        flush=True,
    )
    print(f"Resultado: {output_dir}", flush=True)


if __name__ == "__main__":
    main()
