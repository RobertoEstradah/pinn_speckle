# -*- coding: utf-8 -*-
"""
NB03-A — Referencia física de speckle por espectro angular
===========================================================

Esta corrida constituye la referencia independiente de NB03. No entrena una
PINN. Propaga una pantalla de fase aleatoria en un medio homogéneo mediante
el método de espectro angular:

    U(x,z) = F^{-1}{ A(k_x) exp(i k_z z) }
    k_z = sqrt(k^2 - k_x^2)

Las coordenadas están expresadas en longitudes de onda. Por ello el dominio
de 20 lambda se escribe como x/lambda in [-10,10] y z/lambda in [0,20],
con k=2*pi. La periodicidad lateral es la hipótesis explícita del espectro
angular y evita introducir paredes reflectantes artificiales.

Salidas:
    results/nb03_angular_spectrum_reference.json
    results/nb03_angular_spectrum_reference.npz
    results/figures/nb03_angular_spectrum_reference.png
"""

from pathlib import Path
import json
import os
import sys

import numpy as np

# El script se ejecuta sin ventana gráfica (servidor/entorno automatizado).
os.environ.setdefault("MPLBACKEND", "Agg")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


SEED = int(os.environ.get("NB03_REFERENCE_SEED", 42))
LAMBDA_LASER = 638e-9
K = 2.0 * np.pi
WIDTH_LAMBDA = 20.0
DISTANCE_LAMBDA = float(os.environ.get("NB03_DISTANCE_LAMBDA", 20.0))
N_X = 1024
N_Z = int(os.environ.get("NB03_REFERENCE_N_Z", 201))
N_REALIZATIONS = int(os.environ.get("NB03_REFERENCE_N_REALIZATIONS", 64))
TARGET_Z_LAMBDA = float(os.environ.get(
    "NB03_TARGET_Z_LAMBDA", DISTANCE_LAMBDA
))
PHASE_CORRELATION_LAMBDA = float(os.environ.get(
    "NB03_PHASE_CORRELATION_LAMBDA", 0.50
))
PHASE_STD_RAD = float(os.environ.get("NB03_PHASE_STD_RAD", 2.0))
OUTPUT_SUFFIX = os.environ.get("NB03_REFERENCE_SUFFIX", "")


def angular_spectrum_coordinates(width_lambda=WIDTH_LAMBDA, n_x=N_X):
    """Devuelve la malla transversal periódica y sus frecuencias kx."""
    x = np.linspace(-width_lambda / 2.0, width_lambda / 2.0, n_x,
                    endpoint=False)
    dx = width_lambda / n_x
    kx = 2.0 * np.pi * np.fft.fftfreq(n_x, d=dx)
    return x, kx, dx


def propagate_phase_screen(phase, z_lambda, k=K, width_lambda=WIDTH_LAMBDA):
    """Propaga una pantalla de fase en coordenadas normalizadas por lambda."""
    n_x = phase.size
    _, kx, _ = angular_spectrum_coordinates(width_lambda, n_x)
    amplitude = np.exp(1j * phase)
    spectrum = np.fft.fft(amplitude)

    # Se conservan los modos evanescentes: su decaimiento exponencial es la
    # continuación exacta del espectro angular y evita alterar artificialmente
    # la condición z=0. Para z=20 lambda son numéricamente despreciables.
    kz = np.sqrt((k**2 - kx**2).astype(complex))
    field = np.fft.ifft(spectrum * np.exp(1j * kz * z_lambda))
    return field, spectrum, kx


def correlated_phase_screen(rng, n_x=N_X, width_lambda=WIDTH_LAMBDA,
                            correlation_lambda=PHASE_CORRELATION_LAMBDA,
                            phase_std=PHASE_STD_RAD):
    """Genera una pantalla de fase gaussiana correlacionada y periódica.

    Una fase independiente por píxel contiene una gran proporción de modos
    evanescentes cuando la malla resuelve muchas muestras por lambda. La
    correlación espacial limita el espectro de la pantalla a un régimen
    físicamente propagante y hace explícita la escala de rugosidad del difusor.
    La fase se conserva como variable continua; la envolvente exp(i*phi) es la
    condición compleja que se propaga.
    """
    _, kx, _ = angular_spectrum_coordinates(width_lambda, n_x)
    white = rng.normal(size=n_x)
    phase_spectrum = np.fft.fft(white)
    gaussian_filter = np.exp(-0.5 * (kx * correlation_lambda) ** 2)
    phase = np.fft.ifft(phase_spectrum * gaussian_filter).real
    phase -= phase.mean()
    std = phase.std()
    if std == 0.0:
        raise RuntimeError("La pantalla de fase degeneró a una constante.")
    return phase * (phase_std / std)


def statistics(intensity):
    """Métricas de contraste y ajuste a exponencial de intensidad."""
    values = np.asarray(intensity, dtype=float).ravel()
    mean = float(values.mean())
    std = float(values.std())
    normalized = values / mean
    ks_stat, ks_pvalue = ks_exponential(normalized)
    return {
        "n_samples": int(values.size),
        "mean_intensity": mean,
        "std_intensity": std,
        "contrast": float(std / mean),
        "ks_statistic": float(ks_stat),
        "ks_pvalue": float(ks_pvalue),
        "fraction_intensity_gt_2mean": float(np.mean(values > 2.0 * mean)),
        "expected_fraction_gt_2mean": float(np.exp(-2.0)),
    }


def ks_exponential(values):
    """Estadístico KS y p-valor asintótico para Exp(1), sin SciPy.

    El p-valor se incluye como referencia descriptiva. Las muestras espaciales
    de un campo propagado están correlacionadas, por lo que no se usa como
    único criterio de aceptación del speckle.
    """
    values = np.sort(np.asarray(values, dtype=float).ravel())
    n = values.size
    cdf = 1.0 - np.exp(-values)
    i = np.arange(1, n + 1, dtype=float)
    d_plus = np.max(i / n - cdf)
    d_minus = np.max(cdf - (i - 1.0) / n)
    statistic = float(max(d_plus, d_minus))

    # Aproximación de Stephens para la distribución asintótica de KS.
    root_n = np.sqrt(float(n))
    lam = (root_n + 0.12 + 0.11 / root_n) * statistic
    terms = [(-1.0) ** (j - 1) * np.exp(-2.0 * (j * lam) ** 2)
             for j in range(1, 101)]
    pvalue = float(np.clip(2.0 * np.sum(terms), 0.0, 1.0))
    return statistic, pvalue


def main():
    output_dir = Path(__file__).resolve().parents[2] / "results"
    figure_dir = output_dir / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(output_dir / ".matplotlib_cache"))

    rng = np.random.RandomState(SEED)
    x, kx, dx = angular_spectrum_coordinates()
    z_values = np.linspace(0.0, DISTANCE_LAMBDA, N_Z)
    target_index = int(np.argmin(np.abs(z_values - TARGET_Z_LAMBDA)))
    if not 0.0 <= TARGET_Z_LAMBDA <= DISTANCE_LAMBDA:
        raise ValueError("TARGET_Z_LAMBDA debe estar dentro de la distancia.")

    phase = correlated_phase_screen(rng)
    target_field, spectrum, kx = propagate_phase_screen(
        phase, TARGET_Z_LAMBDA
    )
    propagating = np.abs(kx) <= K + 1e-12
    n_propagating = int(propagating.sum())
    energy_fraction = float(
        np.sum(np.abs(spectrum[propagating]) ** 2)
        / np.sum(np.abs(spectrum) ** 2)
    )

    fields_at_distance = []
    for z_lambda in z_values:
        field, _, _ = propagate_phase_screen(phase, z_lambda)
        fields_at_distance.append(field)
    fields_at_distance = np.asarray(fields_at_distance)
    intensities = np.abs(fields_at_distance) ** 2

    # Estadística de la realización principal y una estadística de conjunto.
    # El conjunto evita decidir la validez física a partir de una sola pantalla.
    target_intensity = intensities[target_index]
    ensemble_target = np.empty((N_REALIZATIONS, N_X), dtype=float)
    for i in range(N_REALIZATIONS):
        phase_i = correlated_phase_screen(rng)
        field_i, _, _ = propagate_phase_screen(phase_i, TARGET_Z_LAMBDA)
        ensemble_target[i] = np.abs(field_i) ** 2

    stats_single = statistics(target_intensity)
    stats_ensemble = statistics(ensemble_target)

    result = {
        "experiment": "NB03-A angular-spectrum physical reference",
        "seed": SEED,
        "lambda_laser_m": LAMBDA_LASER,
        "coordinates": {
            "unit": "lambda_laser",
            "x_interval_lambda": [-WIDTH_LAMBDA / 2.0, WIDTH_LAMBDA / 2.0],
            "z_interval_lambda": [0.0, DISTANCE_LAMBDA],
            "width_lambda": WIDTH_LAMBDA,
            "distance_lambda": DISTANCE_LAMBDA,
            "dx_lambda": dx,
            "boundary_x": "periodic",
            "propagation_axis": "z",
        },
        "physics": {
            "k_normalized": K,
            "k_real_m_inverse": float(K / LAMBDA_LASER),
            "screen": "U(x,0)=exp(i phi(x)), phi correlacionada y gaussiana",
            "phase_model": {
                "distribution": "zero-mean Gaussian process before exp(i phi)",
                "standard_deviation_rad": PHASE_STD_RAD,
                "correlation_length_lambda": PHASE_CORRELATION_LAMBDA,
                "periodic": True,
            },
            "method": "angular spectrum with propagating and evanescent modes",
            "propagating_modes": n_propagating,
            "total_spectral_modes": N_X,
            "propagating_energy_fraction": energy_fraction,
        },
        "sampling": {
            "n_x": N_X,
            "n_z": N_Z,
            "n_realizations": N_REALIZATIONS,
            "target_z_lambda": TARGET_Z_LAMBDA,
        },
        "target_statistics_single_realization": stats_single,
        "target_statistics_ensemble": stats_ensemble,
        "acceptance_guidance": {
            "contrast_target": "near 1; report observed value rather than a universal pass/fail rule",
            "ks_warning": "KS is reported descriptively; spatial samples are correlated, so it is not the sole acceptance criterion",
            "next_step": "use this field and boundary convention as the reference for the NB03 PINN",
        },
    }

    (output_dir / f"nb03_angular_spectrum_reference{OUTPUT_SUFFIX}.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    np.savez_compressed(
        output_dir / f"nb03_angular_spectrum_reference{OUTPUT_SUFFIX}.npz",
        x_lambda=x,
        z_lambda=z_values,
        phase=phase,
        field_target=target_field,
        field_all_z=fields_at_distance,
        intensity_target=target_intensity,
        intensity_ensemble=ensemble_target,
        kx=kx,
        propagating_mask=propagating,
        reference_seed=np.asarray(SEED, dtype=np.int64),
    )

    # La figura se importa solo al ejecutar el experimento, para que el módulo
    # siga siendo utilizable en entornos sin backend gráfico.
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 3, figsize=(16, 8), constrained_layout=True)
    extent = [x[0], x[-1], 0.0, DISTANCE_LAMBDA]
    axes[0, 0].plot(x, phase, lw=0.7, color="#2166ac")
    axes[0, 0].set_title("Pantalla de fase en z=0")
    axes[0, 0].set_xlabel("x / λ")
    axes[0, 0].set_ylabel("φ(x) [rad]")
    axes[0, 0].set_ylim(0.0, 2.0 * np.pi)
    axes[0, 0].grid(alpha=0.25)

    snapshot_distances = (
        DISTANCE_LAMBDA / 4.0, DISTANCE_LAMBDA / 2.0
    )
    for ax, z_lambda in zip(axes[0, 1:], snapshot_distances):
        index = int(np.argmin(np.abs(z_values - z_lambda)))
        image = ax.imshow(
            intensities[index][None, :], aspect="auto", origin="lower",
            extent=[x[0], x[-1], 0.0, 1.0], cmap="inferno"
        )
        ax.set_title(f"Intensidad en z={z_lambda:g}λ")
        ax.set_xlabel("x / λ")
        ax.set_yticks([])
        fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)

    image = axes[1, 0].imshow(
        intensities, aspect="auto", origin="lower", extent=extent,
        cmap="inferno"
    )
    axes[1, 0].set_title("Propagación de intensidad |U|²")
    axes[1, 0].set_xlabel("x / λ")
    axes[1, 0].set_ylabel("z / λ")
    fig.colorbar(image, ax=axes[1, 0], fraction=0.046, pad=0.04)

    normalized_intensity = target_intensity / target_intensity.mean()
    bins = np.linspace(0.0, 5.0, 60)
    axes[1, 1].hist(normalized_intensity, bins=bins, density=True,
                    alpha=0.72, color="#4575b4", label="Referencia")
    q = np.linspace(0.0, 5.0, 300)
    axes[1, 1].plot(q, np.exp(-q), "r-", lw=2,
                    label="Exponencial teórica")
    axes[1, 1].set_title(
        f"Distribución en z={TARGET_Z_LAMBDA:g}λ "
        f"(C={stats_single['contrast']:.3f})"
    )
    axes[1, 1].set_xlabel("I / ⟨I⟩")
    axes[1, 1].set_ylabel("Densidad")
    axes[1, 1].legend()
    axes[1, 1].grid(alpha=0.25)

    axes[1, 2].plot(
        np.fft.fftshift(kx), np.fft.fftshift(np.abs(spectrum) ** 2),
        color="#762a83", lw=0.8
    )
    axes[1, 2].axvline(K, color="red", ls="--", lw=1.2)
    axes[1, 2].axvline(-K, color="red", ls="--", lw=1.2,
                       label="límite propagante |kx|=k")
    axes[1, 2].set_title(f"Espectro inicial ({n_propagating} modos propagantes)")
    axes[1, 2].set_xlabel("kx")
    axes[1, 2].set_ylabel("|A(kx)|²")
    axes[1, 2].set_yscale("log")
    axes[1, 2].legend(fontsize=8)
    axes[1, 2].grid(alpha=0.25)

    fig.suptitle("NB03-A — Referencia física por espectro angular", fontsize=14)
    fig.savefig(
        figure_dir / f"nb03_angular_spectrum_reference{OUTPUT_SUFFIX}.png",
                dpi=160, bbox_inches="tight")
    plt.close(fig)

    print("NB03-A: referencia física completada")
    print(f"  Dominio: {WIDTH_LAMBDA:.0f}λ de ancho × {DISTANCE_LAMBDA:.0f}λ de propagación")
    print(f"  Malla: {N_X} puntos x, {N_Z} puntos z")
    print(f"  Modos propagantes: {n_propagating} de {N_X}")
    print(f"  Energía espectral propagante: {100.0 * energy_fraction:.2f}%")
    print(f"  C (una realización, z={TARGET_Z_LAMBDA:g}λ): "
          f"{stats_single['contrast']:.4f}")
    print(f"  C (conjunto de {N_REALIZATIONS}, z={TARGET_Z_LAMBDA:g}λ): "
          f"{stats_ensemble['contrast']:.4f}")
    print(f"  JSON: {output_dir / f'nb03_angular_spectrum_reference{OUTPUT_SUFFIX}.json'}")
    print(f"  NPZ : {output_dir / f'nb03_angular_spectrum_reference{OUTPUT_SUFFIX}.npz'}")
    print(f"  PNG : {figure_dir / f'nb03_angular_spectrum_reference{OUTPUT_SUFFIX}.png'}")


if __name__ == "__main__":
    main()
