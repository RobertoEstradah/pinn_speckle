"""Piloto NB03 con frecuencia SIREN global adaptativa en una prueba reservada.

La modificación sigue la idea de activación escalable de Jagtap, Kawaguchi y
Karniadakis (JCP 2020): un escalar entrenable multiplica las activaciones. La
ecuación modal de Helmholtz, la condición de Cauchy dura y el protocolo de
evaluación permanecen sin cambios.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.experiments import nb03_modal_multiseed_summary as modal_summary  # noqa: E402
from scripts.experiments import nb03_modal_pinn_siren as modal  # noqa: E402
from scripts.experiments import nb03_modal_refinement as refinement  # noqa: E402


class AdaptiveSineLayer(nn.Module):
    def __init__(self, in_features, out_features, omega, first=False):
        super().__init__()
        self.linear = nn.Linear(in_features, out_features)
        self.omega = float(omega)
        with torch.no_grad():
            bound = (
                1.0 / in_features
                if first
                else np.sqrt(6.0 / in_features) / self.omega
            )
            self.linear.weight.uniform_(-bound, bound)
            nn.init.zeros_(self.linear.bias)

    def forward(self, values, adaptive_scale):
        return torch.sin(self.omega * adaptive_scale * self.linear(values))


class AdaptiveOmegaModalSiren(nn.Module):
    def __init__(
        self,
        coefficient0,
        derivative0,
        correction_scale,
        distance,
        slope_multiplier=10.0,
    ):
        super().__init__()
        self.distance = float(distance)
        self.slope_multiplier = float(slope_multiplier)
        # n*a=1 al inicio: la función inicial coincide con la SIREN fija.
        self.activation_a = nn.Parameter(
            torch.tensor(1.0 / self.slope_multiplier, dtype=coefficient0.dtype)
        )
        self.hidden = nn.ModuleList(
            [AdaptiveSineLayer(1, 128, 30.0, first=True)]
            + [AdaptiveSineLayer(128, 128, 1.0) for _ in range(3)]
        )
        self.final = nn.Linear(128, int(coefficient0.numel()))
        nn.init.zeros_(self.final.weight)
        nn.init.zeros_(self.final.bias)
        self.register_buffer("coefficient0", coefficient0.reshape(1, -1))
        self.register_buffer("derivative0", derivative0.reshape(1, -1))
        self.register_buffer("correction_scale", correction_scale.reshape(1, -1))

    @property
    def adaptive_scale(self):
        return self.slope_multiplier * self.activation_a

    def forward(self, z):
        values = 2.0 * z / self.distance - 1.0
        scale = self.adaptive_scale
        for layer in self.hidden:
            values = layer(values, scale)
        correction = self.correction_scale * self.final(values)
        return self.coefficient0 + z * self.derivative0 + z.square() * correction


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference-suffix", default="_z1_seed31415_corr0.10")
    parser.add_argument("--screen-seed", type=int, default=31415)
    parser.add_argument("--network-seed", type=int, default=73)
    parser.add_argument("--adam-seconds", type=float, default=180.0)
    parser.add_argument("--lbfgs-seconds", type=float, default=60.0)
    parser.add_argument("--n-train", type=int, default=1024)
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--slope-multiplier", type=float, default=10.0)
    parser.add_argument("--resume-model", default="")
    parser.add_argument("--name", default="screen31415_net73_adaptiveomega_v1")
    args = parser.parse_args()
    if args.adam_seconds < 0 or min(args.lbfgs_seconds, args.slope_multiplier) <= 0:
        parser.error("Adam debe ser no negativo; los demás valores deben ser positivos.")

    torch.set_num_threads(args.threads)
    np.random.seed(args.network_seed)
    torch.manual_seed(args.network_seed)
    modal.HIDDEN_DIM, modal.NUM_LAYERS = 128, 4
    modal.FIRST_OMEGA, modal.HIDDEN_OMEGA = 30.0, 1.0

    reference_path = ROOT / "results" / (
        f"nb03_angular_spectrum_reference{args.reference_suffix}.npz"
    )
    reference = dict(np.load(reference_path))
    recorded_seed = int(reference.get("reference_seed", args.screen_seed))
    if recorded_seed != args.screen_seed:
        raise ValueError("La semilla declarada no coincide con la referencia.")

    # Se reutiliza exclusivamente la preparación física de los coeficientes.
    fixed_shell, field_scale, kx_active = modal_summary.build_model(reference)
    torch.manual_seed(args.network_seed)
    model = AdaptiveOmegaModalSiren(
        fixed_shell.coefficient0.detach().flatten(),
        fixed_shell.derivative0.detach().flatten(),
        fixed_shell.correction_scale.detach().flatten(),
        1.0,
        slope_multiplier=args.slope_multiplier,
    )
    if args.resume_model:
        resume_path = Path(args.resume_model)
        if not resume_path.is_absolute():
            resume_path = ROOT / resume_path
        model.load_state_dict(torch.load(
            resume_path, map_location="cpu", weights_only=True
        ))
    initial_scale = float(model.adaptive_scale.detach())

    if args.adam_seconds > 0:
        kz2_adam, adam_training = refinement.train(
            model,
            reference,
            "adam32",
            args.adam_seconds,
            args.n_train,
            learning_rate=2e-4,
            selection_interval=50,
        )
    else:
        active = reference["propagating_mask"].astype(bool)
        kz2_adam = torch.tensor(
            np.maximum((2 * np.pi) ** 2 - reference["kx"][active] ** 2, 0),
            dtype=torch.float32,
        )
        adam_training = {"skipped": True, "resume_model": args.resume_model}
    adam_metrics, adam_arrays = refinement.evaluate(
        model, reference, field_scale, kx_active, kz2_adam
    )
    adam_scale = float(model.adaptive_scale.detach())

    kz2_lbfgs, lbfgs_training = refinement.train(
        model,
        reference,
        "lbfgs32",
        args.lbfgs_seconds,
        args.n_train,
    )
    final_metrics, final_arrays = refinement.evaluate(
        model, reference, field_scale, kx_active, kz2_lbfgs
    )
    final_scale = float(model.adaptive_scale.detach())

    output_dir = ROOT / "results" / "nb03_holdout" / args.name
    output_dir.mkdir(parents=True, exist_ok=False)
    torch.save(model.state_dict(), output_dir / "adaptiveomega_lbfgs32.pt")
    np.savez_compressed(output_dir / "adam32.npz", **adam_arrays)
    np.savez_compressed(output_dir / "adaptiveomega_lbfgs32.npz", **final_arrays)
    result = {
        "experiment": "NB03 global adaptive SIREN frequency holdout",
        "literature_basis": {
            "citation": "Jagtap, Kawaguchi and Karniadakis, JCP 404 (2020) 109136",
            "doi": "10.1016/j.jcp.2019.109136",
            "adaptation": "shared trainable n*a multiplier applied to every sine activation",
        },
        "configuration": vars(args),
        "protocol": {
            "training_labels": False,
            "selection_uses_reference_field": False,
            "hard_cauchy": True,
            "equation": "complete modal Helmholtz equation",
            "fixed_training_points": args.n_train,
            "fixed_selection_points": 997,
            "independent_residual_test_points": 2001,
            "field_test_planes": 201,
        },
        "activation_scale": {
            "initial": initial_scale,
            "after_adam": adam_scale,
            "after_lbfgs": final_scale,
        },
        "adam32": {"training": adam_training, "metrics": adam_metrics},
        "lbfgs32": {"training": lbfgs_training, "metrics": final_metrics},
        "acceptance": {
            "propagating_final_below_1pct": final_metrics["l2_propagating_final"] < 0.01,
            "propagating_all_201_planes_below_1pct": final_metrics["l2_propagating_max"] < 0.01,
            "full_final_below_5pct": final_metrics["l2_full_final"] < 0.05,
            "contrast_reference_error_below_0_05": final_metrics["contrast_difference"] < 0.05,
        },
    }
    (output_dir / "summary.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    print(
        f"Adam: prop={100*adam_metrics['l2_propagating_final']:.4f}% "
        f"full={100*adam_metrics['l2_full_final']:.4f}% "
        f"scale={adam_scale:.5f}",
        flush=True,
    )
    print(
        f"L-BFGS: prop={100*final_metrics['l2_propagating_final']:.4f}% "
        f"max_prop={100*final_metrics['l2_propagating_max']:.4f}% "
        f"full={100*final_metrics['l2_full_final']:.4f}% "
        f"res={final_metrics['test_residual']['rmse']:.3e} "
        f"scale={final_scale:.5f}",
        flush=True,
    )
    print(f"Resultado: {output_dir}", flush=True)


if __name__ == "__main__":
    main()
