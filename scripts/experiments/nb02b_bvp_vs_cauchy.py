# -*- coding: utf-8 -*-
"""NB02b: misma solucion analitica, dos planteamientos de frontera.

Aisla una sola variable —el buen planteamiento del problema— manteniendo
identicos la geometria, la solucion exacta y la arquitectura de red.

Campo de prueba (solucion cerrada de Helmholtz 2D):

    E(x,y) = sum_n c_n exp(i(kx_n x + kz_n y)),
    n in {-2,-1,0,1,2},  kx_n = 2*pi*n,  kz_n = 2*pi*sqrt(5-n^2),  k = 2*pi*sqrt(5)

Los cinco modos propagan (kz_n real), son periodicos en x sobre [0,1] y
cumplen kx_n^2 + kz_n^2 = 20*pi^2 = k^2 de forma exacta.

Tres celdas:
  A. BVP Dirichlet en los cuatro lados, formulacion directa   -> bien puesto
  B. Cauchy (valor y derivada) solo en y=0, formulacion directa -> mal puesto
  C. Cauchy identico al de B, formulacion modal con Cauchy dura -> regularizado

B y C reciben exactamente los mismos datos. La unica diferencia es la
representacion, de modo que cualquier brecha de error es atribuible a ella.
"""

from pathlib import Path
import json
import os
import sys
import time

import numpy as np

os.environ.setdefault("MPLBACKEND", "Agg")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import torch
import torch.nn as nn
from torch.func import jvp

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.models import PINN_2D_SIREN

SEED = 42

# q = (k/2pi)^2. Debe cumplir dos condiciones:
#   (1) q > max(n^2) para que todos los modos propaguen (kz real);
#   (2) 4q no entero, para que k^2 = 4q*pi^2 no sea autovalor de Dirichlet
#       en [0,1]^2 (los autovalores son pi^2(m^2+n^2), m,n >= 1 enteros).
# Con q = 1.625 se tiene k^2 = 6.5*pi^2, a distancia 1.5*pi^2 de los
# autovalores vecinos 5*pi^2 (1,2) y 8*pi^2 (2,2). Una eleccion resonante
# volveria singular el BVP de la celda A y arruinaria la comparacion.
Q = 1.625
K = 2.0 * np.pi * np.sqrt(Q)
OMEGA_0 = float(np.sqrt(Q))            # regla omega_0 ~ k/(2*pi)
MODES = np.array([-1, 0, 1])
KX = 2.0 * np.pi * MODES
KZ = 2.0 * np.pi * np.sqrt(Q - MODES ** 2)

N_BOUNDARY = 300                       # por lado, como NB02
N_COLLOC = 3000                        # LHS, como NB02
LAMBDA_PHYS = 0.1                      # como NB02
EPOCHS_ADAM = 8000
LBFGS_ITER = 500
EPOCHS_MODAL = 5000
N_EVAL = 256

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
OUT = PROJECT_ROOT / "results" / "nb02b" / "bien_vs_mal_puesto"


def coefficients():
    rng = np.random.RandomState(SEED)
    c = rng.randn(len(MODES)) + 1j * rng.randn(len(MODES))
    return c / np.sqrt(np.sum(np.abs(c) ** 2))   # RMS|E| = 1 sobre el dominio


C = coefficients()


def field(x, y):
    """Solucion analitica exacta."""
    x, y = np.asarray(x), np.asarray(y)
    return sum(C[i] * np.exp(1j * (KX[i] * x + KZ[i] * y))
               for i in range(len(MODES)))


def field_dy(x, y):
    """Derivada normal exacta en la direccion de propagacion."""
    x, y = np.asarray(x), np.asarray(y)
    return sum(C[i] * 1j * KZ[i] * np.exp(1j * (KX[i] * x + KZ[i] * y))
               for i in range(len(MODES)))


def latin_hypercube(n, rng):
    cut = (np.arange(n) + rng.rand(n)) / n
    return np.column_stack((rng.permutation(cut), rng.permutation(cut)))


def to_t(a):
    return torch.tensor(np.asarray(a, dtype=np.float32), device=DEVICE)


def helmholtz_residual(model, xy):
    """Residuo normalizado por k^2: R = lap(E)/k^2 + E.

    Sin esta normalizacion el termino fisico escala como O(k^4) frente a un
    termino de datos O(1); a k = 2*pi*sqrt(5) eso lo hace dominar por ~4e3 y
    el optimizador colapsa hacia E = 0, que satisface la ecuacion homogenea
    de forma exacta.
    """
    xy = xy.clone().requires_grad_(True)
    out = model(xy)
    residuals = []
    for component in (0, 1):
        f = out[:, component:component + 1]
        grad = torch.autograd.grad(f, xy, torch.ones_like(f),
                                   create_graph=True)[0]
        lap = 0.0
        for axis in (0, 1):
            g = grad[:, axis:axis + 1]
            second = torch.autograd.grad(g, xy, torch.ones_like(g),
                                         create_graph=True)[0]
            lap = lap + second[:, axis:axis + 1]
        residuals.append(lap / (K ** 2) + f)
    return residuals[0], residuals[1]


def evaluation_grid():
    g = np.linspace(0.0, 1.0, N_EVAL)
    xx, yy = np.meshgrid(g, g, indexing="ij")
    return xx.reshape(-1), yy.reshape(-1)


def relative_l2(pred_complex, exact_complex):
    return float(np.linalg.norm(pred_complex - exact_complex)
                 / np.linalg.norm(exact_complex))


def evaluate_direct(model):
    x, y = evaluation_grid()
    with torch.no_grad():
        out = model(to_t(np.column_stack((x, y)))).cpu().numpy()
    return relative_l2(out[:, 0] + 1j * out[:, 1], field(x, y))


def train_direct(case, verbose=True):
    """case 'A' = Dirichlet en los 4 lados; case 'B' = Cauchy solo en y=0."""
    torch.manual_seed(SEED)
    rng = np.random.RandomState(SEED)
    model = PINN_2D_SIREN(hidden_dim=128, num_layers=5,
                          omega_0=OMEGA_0).to(DEVICE)

    xy_c = to_t(latin_hypercube(N_COLLOC, rng))
    s = np.linspace(0.0, 1.0, N_BOUNDARY)

    if case == "A":
        xb = np.concatenate([s, s, np.zeros_like(s), np.ones_like(s)])
        yb = np.concatenate([np.zeros_like(s), np.ones_like(s), s, s])
        xy_b = to_t(np.column_stack((xb, yb)))
        e_b = field(xb, yb)
        target_b = to_t(np.column_stack((e_b.real, e_b.imag)))
        xy_d = target_d = None
    else:
        xb, yb = s, np.zeros_like(s)
        xy_b = to_t(np.column_stack((xb, yb)))
        e_b = field(xb, yb)
        target_b = to_t(np.column_stack((e_b.real, e_b.imag)))
        xy_d = xy_b.clone()                       # mismos puntos, dato de Cauchy
        d_b = field_dy(xb, yb)
        target_d = to_t(np.column_stack((d_b.real, d_b.imag)))

    mse = nn.MSELoss()

    def total_loss():
        loss = mse(model(xy_b), target_b)
        if xy_d is not None:
            xy = xy_d.clone().requires_grad_(True)
            out = model(xy)
            dy = torch.cat([
                torch.autograd.grad(out[:, c:c + 1], xy,
                                    torch.ones_like(out[:, c:c + 1]),
                                    create_graph=True)[0][:, 1:2]
                for c in (0, 1)], dim=1)
            loss = loss + mse(dy, target_d)
        r_re, r_im = helmholtz_residual(model, xy_c)
        return loss + LAMBDA_PHYS * (r_re.pow(2).mean() + r_im.pow(2).mean())

    start = time.time()
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    for epoch in range(1, EPOCHS_ADAM + 1):
        opt.zero_grad()
        loss = total_loss()
        loss.backward()
        opt.step()
        if verbose and epoch % 2000 == 0:
            print(f"    Adam {epoch}/{EPOCHS_ADAM}: loss={loss.item():.3e}")

    lbfgs = torch.optim.LBFGS(model.parameters(), max_iter=LBFGS_ITER,
                              history_size=100, line_search_fn="strong_wolfe")

    def closure():
        lbfgs.zero_grad()
        loss = total_loss()
        loss.backward()
        return loss

    lbfgs.step(closure)
    seconds = time.time() - start

    def predict(x, y):
        with torch.no_grad():
            out = model(to_t(np.column_stack((x, y)))).cpu().numpy()
        return out[:, 0] + 1j * out[:, 1]

    return {
        "l2_relative": evaluate_direct(model),
        "final_loss": float(total_loss().item()),
        "seconds": seconds,
        "profile": spectral_profile(predict),
    }


class ModalSiren(nn.Module):
    """Identica en estructura a la usada en NB03 (Cauchy dura + escala modal)."""

    def __init__(self, a0, da0, scale, omega_first, hidden=128, layers=4):
        super().__init__()
        blocks = []
        in_features = 1
        for index in range(layers):
            omega = omega_first if index == 0 else 1.0
            linear = nn.Linear(in_features, hidden)
            with torch.no_grad():
                bound = (1.0 / in_features if index == 0
                         else np.sqrt(6.0 / in_features) / omega)
                linear.weight.uniform_(-bound, bound)
                nn.init.zeros_(linear.bias)
            blocks.append((linear, omega))
            in_features = hidden
        self.blocks = nn.ModuleList([b[0] for b in blocks])
        self.omegas = [b[1] for b in blocks]
        self.final = nn.Linear(hidden, a0.numel())
        nn.init.zeros_(self.final.weight)
        nn.init.zeros_(self.final.bias)
        self.register_buffer("a0", a0.reshape(1, -1))
        self.register_buffer("da0", da0.reshape(1, -1))
        self.register_buffer("scale", scale.reshape(1, -1))

    def forward(self, z):
        h = 2.0 * z - 1.0
        for linear, omega in zip(self.blocks, self.omegas):
            h = torch.sin(omega * linear(h))
        correction = self.scale * self.final(h)
        return self.a0 + z * self.da0 + z.square() * correction


def train_modal(verbose=True):
    torch.manual_seed(SEED)
    a0 = np.column_stack((C.real, C.imag)).astype(np.float32).reshape(-1)
    d0c = 1j * KZ * C
    da0 = np.column_stack((d0c.real, d0c.imag)).astype(np.float32).reshape(-1)
    amplitude = np.maximum(np.abs(C), np.abs(d0c) / K)
    amplitude = np.maximum(amplitude, max(amplitude.max() * 1e-4, 1e-8))
    scale = np.repeat((K ** 2 * amplitude).astype(np.float32), 2)

    model = ModalSiren(to_t(a0), to_t(da0), to_t(scale),
                       omega_first=OMEGA_0).to(DEVICE)
    kz2 = to_t(KZ ** 2)

    start = time.time()
    opt = torch.optim.Adam(model.parameters(), lr=2e-4)
    generator = torch.Generator(device="cpu").manual_seed(SEED)
    for epoch in range(1, EPOCHS_MODAL + 1):
        z = torch.rand(256, 1, generator=generator).to(DEVICE)
        # jvp por salida: autograd.grad sumaria las derivadas de las 10
        # salidas contra la unica entrada en vez de darlas por separado.
        tangent = torch.ones_like(z)

        def first_derivative(values):
            return jvp(model, (values,), (torch.ones_like(values),))[1]

        a, _ = jvp(model, (z,), (tangent,))
        _, second = jvp(first_derivative, (z,), (tangent,))
        # a'' + kz^2 a = 0, normalizado por la escala modal
        res = (second.reshape(-1, len(MODES), 2)
               + kz2.reshape(1, -1, 1) * a.reshape(-1, len(MODES), 2))
        loss = (res / to_t(scale).reshape(1, len(MODES), 2)).pow(2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        if verbose and epoch % 1000 == 0:
            print(f"    modal {epoch}/{EPOCHS_MODAL}: loss={loss.item():.3e}")
    seconds = time.time() - start

    def predict(x, y):
        x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
        with torch.no_grad():
            coeff = model(to_t(y.reshape(-1, 1))).cpu().numpy()
        coeff = coeff.reshape(len(y), len(MODES), 2)
        a = coeff[..., 0] + 1j * coeff[..., 1]
        return np.sum(a * np.exp(1j * (x[:, None] * KX[None, :])), axis=1)

    x, y = evaluation_grid()
    return {
        "l2_relative": relative_l2(predict(x, y), field(x, y)),
        "final_loss": float(loss.item()),
        "seconds": seconds,
        "profile": spectral_profile(predict),
    }


def diagnostic_grid():
    """Malla con x sin repetir el extremo, para que la FFT en x sea limpia."""
    xs = np.linspace(0.0, 1.0, N_EVAL, endpoint=False)
    ys = np.linspace(0.0, 1.0, 65)
    return xs, ys


def spectral_profile(predict):
    """Perfil en y del error y de la energia evanescente de la prediccion.

    La prediccion se descompone en modos e^{i 2 pi m x}. Los modos con
    |kx| <= k propagan; el resto son evanescentes y no pueden formar parte
    de la solucion fisica. Su presencia es la firma del modo de fallo del
    problema de Cauchy: crecen como e^{+|kappa| y} y por eso contaminan
    cada vez mas al alejarse de la frontera con datos.
    """
    xs, ys = diagnostic_grid()
    m = np.fft.fftfreq(len(xs), d=1.0 / len(xs))
    propagating = np.abs(2.0 * np.pi * m) <= K + 1e-9
    l2_of_y, evanescent_of_y = [], []
    for y in ys:
        xx = xs
        yy = np.full_like(xs, y)
        pred = predict(xx, yy)
        exact = field(xx, yy)
        l2_of_y.append(float(np.linalg.norm(pred - exact)
                             / np.linalg.norm(exact)))
        spectrum = np.fft.fft(pred)
        total = float(np.sum(np.abs(spectrum) ** 2))
        evan = float(np.sum(np.abs(spectrum[~propagating]) ** 2))
        evanescent_of_y.append(evan / max(total, 1e-30))
    return {
        "y": ys.tolist(),
        "l2_of_y": l2_of_y,
        "evanescent_energy_fraction_of_y": evanescent_of_y,
        "n_propagating_modes": int(propagating.sum()),
    }


def check_not_resonant(margin=0.5):
    """k^2 no debe coincidir con un autovalor de Dirichlet de [0,1]^2.

    Si lo hiciera, el BVP de la celda A seria singular y su error alto no
    diria nada sobre la formulacion directa.
    """
    ratio = (K / np.pi) ** 2
    grid = np.arange(1, 12)
    eigen = np.unique((grid[:, None] ** 2 + grid[None, :] ** 2).ravel())
    distance = float(np.min(np.abs(eigen - ratio)))
    assert distance > margin, (
        f"k^2 = {ratio:.3f}*pi^2 esta a {distance:.3f} del autovalor mas "
        f"cercano; el BVP seria (casi) resonante."
    )
    assert np.all(KZ > 0), "algun modo no propaga: kz no real."
    assert np.allclose(KX ** 2 + KZ ** 2, K ** 2), "los modos no cumplen Helmholtz."
    return ratio, distance


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ratio, distance = check_not_resonant()
    print(f"  k^2 = {ratio:.4f}*pi^2, a {distance:.4f} del autovalor vecino")
    print(f"NB02b — dispositivo: {DEVICE}; k = {K:.4f}; omega_0 = {OMEGA_0:.4f}")
    print(f"  modos kx: {KX.round(3)}")
    print(f"  modos kz: {KZ.round(3)}")

    def report(tag, result):
        p = result["profile"]
        print(f"    L2 global = {100*result['l2_relative']:.4f}%"
              f"   ({result['seconds']:.0f}s)")
        print(f"    L2 en y=0 -> y=1 : {100*p['l2_of_y'][0]:.3f}%"
              f" -> {100*p['l2_of_y'][-1]:.3f}%")
        print(f"    energia evanescente y=0 -> y=1 : "
              f"{100*p['evanescent_energy_fraction_of_y'][0]:.4f}%"
              f" -> {100*p['evanescent_energy_fraction_of_y'][-1]:.4f}%")

    print("\n[A] BVP Dirichlet en los 4 lados, formulacion directa")
    a = train_direct("A")
    report("A", a)

    print("\n[B] Cauchy (valor+derivada) en y=0, formulacion directa")
    b = train_direct("B")
    report("B", b)

    print("\n[C] Cauchy identico, formulacion modal con Cauchy dura")
    c = train_modal()
    report("C", c)

    result = {
        "experiment": "NB02b: bien puesto vs mal puesto con solucion analitica",
        "seed": SEED,
        "k": K,
        "omega_0": OMEGA_0,
        "modes_n": MODES.tolist(),
        "kx": KX.tolist(),
        "kz": KZ.tolist(),
        "coefficients_real": C.real.tolist(),
        "coefficients_imag": C.imag.tolist(),
        "protocol": {
            "n_boundary_per_side": N_BOUNDARY,
            "n_collocation": N_COLLOC,
            "lambda_phys": LAMBDA_PHYS,
            "epochs_adam": EPOCHS_ADAM,
            "lbfgs_max_iter": LBFGS_ITER,
            "epochs_modal": EPOCHS_MODAL,
            "note": "B y C reciben exactamente los mismos datos de Cauchy",
        },
        "cells": {
            "A_dirichlet_directa": a,
            "B_cauchy_directa": b,
            "C_cauchy_modal": c,
        },
    }
    path = OUT / "nb02b_bvp_vs_cauchy.json"
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False),
                    encoding="utf-8")
    print(f"\nJSON: {path}")


if __name__ == "__main__":
    main()
