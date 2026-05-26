"""
models.py — Arquitecturas de red extraídas de NB01 y NB02
==========================================================
Proyecto : Simulación Acelerada de Speckle Óptico mediante PINNs
Autor    : Roberto Hernández Estrada
Director : Dr. José Adán Hernández Nolasco — UJAT

Clases:
    Sine          — activación sinusoidal SIREN
    PINN_1D_SIREN — red para Helmholtz 1D  (NB01)
    PINN_2D_SIREN — red para Helmholtz 2D  (NB02, NB03, NB04)

Uso:
    from src.models import PINN_1D_SIREN, PINN_2D_SIREN
"""

import numpy as np
import torch
import torch.nn as nn


# ─────────────────────────────────────────────────────────────────────────────
class Sine(nn.Module):
    """Capa de activación sinusoidal con escalamiento de frecuencia (omega_0)."""

    def __init__(self, omega_0=1.0):
        super().__init__()
        self.omega_0 = omega_0

    def forward(self, x):
        return torch.sin(self.omega_0 * x)


# ─────────────────────────────────────────────────────────────────────────────
class PINN_1D_SIREN(nn.Module):
    """
    Red Neuronal de Representación Sinusoidal (SIREN) para Helmholtz 1D.
    Entrada : x  — coordenada espacial escalar
    Salida  : E  — campo eléctrico real E(x) = cos(kx)
    Usado en NB01.
    """

    def __init__(self, hidden_dim=64, num_layers=5, omega_0=1.0):
        super().__init__()
        self.omega_0    = omega_0
        self.hidden_dim = hidden_dim

        layers = [nn.Linear(1, hidden_dim), Sine(omega_0=self.omega_0)]
        for _ in range(num_layers - 1):
            layers += [nn.Linear(hidden_dim, hidden_dim), Sine(omega_0=self.omega_0)]
        layers.append(nn.Linear(hidden_dim, 1))

        self.net = nn.Sequential(*layers)
        self._init_weights()

    def _init_weights(self):
        """Inicialización específica para SIREN (Sitzmann et al., 2020)."""
        with torch.no_grad():
            for i, layer in enumerate(self.net):
                if isinstance(layer, nn.Linear):
                    if i == 0:
                        layer.weight.uniform_(-1 / 1, 1 / 1)
                    else:
                        layer.weight.uniform_(
                            -np.sqrt(6 / self.hidden_dim) / self.omega_0,
                             np.sqrt(6 / self.hidden_dim) / self.omega_0
                        )
                    nn.init.zeros_(layer.bias)

    def forward(self, x):
        return self.net(x)


# ─────────────────────────────────────────────────────────────────────────────
class PINN_2D_SIREN(nn.Module):
    """
    SIREN para resolver Helmholtz 2D: nabla^2 E + k^2 E = 0
    Entrada : (x, y) — coordenadas espaciales 2D
    Salida  : (E_real, E_imag) — partes real e imaginaria del campo complejo
    Usado en NB02, NB03, NB04.
    """

    def __init__(self, hidden_dim=128, num_layers=5, omega_0=1.0):
        super().__init__()
        self.omega_0    = omega_0
        self.hidden_dim = hidden_dim

        layers = [nn.Linear(2, hidden_dim), Sine(omega_0=omega_0)]
        for _ in range(num_layers - 1):
            layers += [nn.Linear(hidden_dim, hidden_dim), Sine(omega_0=omega_0)]
        layers.append(nn.Linear(hidden_dim, 2))

        self.net = nn.Sequential(*layers)
        self._init_weights()

    def _init_weights(self):
        """Inicializacion de Sitzmann et al. (2020) — necesaria para SIREN."""
        with torch.no_grad():
            for i, layer in enumerate(self.net):
                if isinstance(layer, nn.Linear):
                    n_in = layer.weight.shape[1]
                    if i == 0:
                        layer.weight.uniform_(-1 / n_in, 1 / n_in)
                    else:
                        layer.weight.uniform_(
                            -np.sqrt(6 / n_in) / self.omega_0,
                             np.sqrt(6 / n_in) / self.omega_0
                        )
                    nn.init.zeros_(layer.bias)

    def forward(self, xy):
        return self.net(xy)

    def save(self, path):
        torch.save(self.state_dict(), path)

    @classmethod
    def load(cls, path, hidden_dim=128, num_layers=5, omega_0=1.0, device='cpu'):
        model = cls(hidden_dim=hidden_dim, num_layers=num_layers, omega_0=omega_0)
        model.load_state_dict(torch.load(path, map_location=device))
        return model.to(device)
