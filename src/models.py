"""
models.py — Arquitecturas de red extraídas de NB01 y NB02
==========================================================
Proyecto : Simulación Acelerada de Speckle Óptico mediante PINNs
Autor    : Roberto Hernández Estrada
Director : Dr. José Adán Hernández Nolasco — UJAT

Clases:
    Sine          — activación sinusoidal SIREN
    PINN_1D_SIREN — red para Helmholtz 1D  (NB01)
    PINN_2D_SIREN — red para Helmholtz 2D  (NB02, NB03)
    PINN_3D_SIREN — red directa para Helmholtz 3D (NB_3D_01)
    PINN_3D_MODAL_SIREN — coeficientes transversales para NB_3D_01B
    PINN_3D_ENVELOPE_TRANSFER_SIREN — propagador modal fisico (NB_3D_03)

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
    Salida  : E  — campo eléctrico real E(x)
    Usado en NB01 para validar las soluciones fundamentales cos(kx) y sin(kx).
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
    Usado en NB02, NB03.
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


# ─────────────────────────────────────────────────────────────────────────────
class PINN_3D_SIREN(nn.Module):
    """
    SIREN directa para Helmholtz escalar 3D: nabla^2 E + k^2 E = 0.

    Entrada : (x, y, z) — coordenadas espaciales cartesianas normalizadas.
    Salida  : (E_real, E_imag) — partes real e imaginaria del campo complejo.
    Usado en NB_3D_01 como validación analítica previa a la formulación modal.
    """

    def __init__(self, hidden_dim=96, num_layers=4, omega_0=1.0):
        super().__init__()
        self.omega_0 = omega_0
        self.hidden_dim = hidden_dim

        layers = [nn.Linear(3, hidden_dim), Sine(omega_0=omega_0)]
        for _ in range(num_layers - 1):
            layers += [nn.Linear(hidden_dim, hidden_dim), Sine(omega_0=omega_0)]
        layers.append(nn.Linear(hidden_dim, 2))

        self.net = nn.Sequential(*layers)
        self._init_weights()

    def _init_weights(self):
        """Inicialización SIREN de Sitzmann et al. (2020)."""
        with torch.no_grad():
            for i, layer in enumerate(self.net):
                if isinstance(layer, nn.Linear):
                    n_in = layer.weight.shape[1]
                    if i == 0:
                        layer.weight.uniform_(-1 / n_in, 1 / n_in)
                    else:
                        bound = np.sqrt(6 / n_in) / self.omega_0
                        layer.weight.uniform_(-bound, bound)
                    nn.init.zeros_(layer.bias)

    def forward(self, xyz):
        return self.net(xyz)

    def save(self, path):
        torch.save(self.state_dict(), path)

    @classmethod
    def load(cls, path, hidden_dim=96, num_layers=4, omega_0=1.0, device='cpu'):
        model = cls(hidden_dim=hidden_dim, num_layers=num_layers, omega_0=omega_0)
        model.load_state_dict(torch.load(path, map_location=device))
        return model.to(device)


# ─────────────────────────────────────────────────────────────────────────────
class PINN_3D_MODAL_SIREN(nn.Module):
    """SIREN para la evolución longitudinal de modos transversales 3D.

    La entrada es únicamente ``z`` y la salida contiene las partes real e
    imaginaria de todos los coeficientes modales. La transformación de salida
    impone exactamente las condiciones de Cauchy en ``z=0``:

        a(z) = a(0) + z a'(0) + z^2 N_theta(z).
    """

    def __init__(
        self,
        coefficient0,
        derivative0,
        correction_scale,
        distance=1.0,
        hidden_dim=128,
        num_layers=4,
        first_omega=1.0,
        hidden_omega=1.0,
    ):
        super().__init__()
        self.distance = float(distance)
        self.hidden_dim = int(hidden_dim)
        self.first_omega = float(first_omega)
        self.hidden_omega = float(hidden_omega)

        n_outputs = int(coefficient0.numel())
        layers = [
            nn.Linear(1, hidden_dim),
            Sine(omega_0=first_omega),
        ]
        for _ in range(num_layers - 1):
            layers += [
                nn.Linear(hidden_dim, hidden_dim),
                Sine(omega_0=hidden_omega),
            ]
        final = nn.Linear(hidden_dim, n_outputs)
        layers.append(final)
        self.net = nn.Sequential(*layers)
        self._init_weights()

        # La salida correctiva empieza en cero para no introducir energía
        # espuria antes del primer paso de optimización.
        nn.init.zeros_(final.weight)
        nn.init.zeros_(final.bias)

        self.register_buffer("coefficient0", coefficient0.reshape(1, -1))
        self.register_buffer("derivative0", derivative0.reshape(1, -1))
        self.register_buffer(
            "correction_scale", correction_scale.reshape(1, -1)
        )

    def _init_weights(self):
        linear_index = 0
        with torch.no_grad():
            for layer in self.net:
                if not isinstance(layer, nn.Linear):
                    continue
                n_in = layer.weight.shape[1]
                omega = self.first_omega if linear_index == 0 else self.hidden_omega
                if linear_index == 0:
                    bound = 1.0 / n_in
                else:
                    bound = np.sqrt(6.0 / n_in) / omega
                layer.weight.uniform_(-bound, bound)
                nn.init.zeros_(layer.bias)
                linear_index += 1

    def forward(self, z):
        normalized_z = 2.0 * z / self.distance - 1.0
        correction = self.correction_scale * self.net(normalized_z)
        return (
            self.coefficient0
            + z * self.derivative0
            + z.square() * correction
        )


# ─────────────────────────────────────────────────────────────────────────────
class PINN_3D_ENVELOPE_TRANSFER_SIREN(nn.Module):
    """SIREN compartida para el propagador modal exacto de Helmholtz.

    El campo se factoriza como ``E=exp(i*k*z)*psi`` y la red aproxima la
    transferencia de la envolvente de cada modo transversal. La entrada es
    ``(s, alpha/alpha_max)``, donde ``s=z/Z`` y

        alpha = (kx**2 + ky**2) * Z / (2*k).

    La transformación de salida impone exactamente ``h(0)=1`` y
    ``dh/ds(0)=i*delta``, con ``delta=(kz-k)Z`` calculado de forma estable.
    Esta representación conserva la ecuación completa de Helmholtz y evita
    pedir a la red que aprenda el portador óptico de millones de radianes.
    """

    def __init__(
        self,
        epsilon,
        alpha_max,
        hidden_dim=128,
        num_layers=4,
        first_omega=12.0,
        hidden_omega=1.0,
    ):
        super().__init__()
        self.epsilon = float(epsilon)
        self.alpha_max = float(alpha_max)
        self.hidden_dim = int(hidden_dim)
        self.first_omega = float(first_omega)
        self.hidden_omega = float(hidden_omega)

        layers = [nn.Linear(2, hidden_dim), Sine(omega_0=first_omega)]
        for _ in range(num_layers - 1):
            layers += [
                nn.Linear(hidden_dim, hidden_dim),
                Sine(omega_0=hidden_omega),
            ]
        final = nn.Linear(hidden_dim, 2)
        layers.append(final)
        self.net = nn.Sequential(*layers)
        self._init_weights()
        nn.init.zeros_(final.weight)
        nn.init.zeros_(final.bias)

    def _init_weights(self):
        linear_index = 0
        with torch.no_grad():
            for layer in self.net:
                if not isinstance(layer, nn.Linear):
                    continue
                n_in = layer.weight.shape[1]
                omega = (
                    self.first_omega if linear_index == 0 else self.hidden_omega
                )
                if linear_index == 0:
                    bound = 1.0 / n_in
                else:
                    bound = np.sqrt(6.0 / n_in) / omega
                layer.weight.uniform_(-bound, bound)
                nn.init.zeros_(layer.bias)
                linear_index += 1

    def physical_alpha(self, points):
        return points[:, 1:2] * self.alpha_max

    def longitudinal_phase(self, points):
        alpha = self.physical_alpha(points)
        radicand = torch.clamp(1.0 - 4.0 * self.epsilon * alpha, min=0.0)
        # Forma estable de (sqrt(1-4*epsilon*alpha)-1)/(2*epsilon).
        return -2.0 * alpha / (1.0 + torch.sqrt(radicand))

    def forward(self, points):
        s = points[:, 0:1]
        alpha_normalized = points[:, 1:2]
        network_input = torch.cat(
            (2.0 * s - 1.0, 2.0 * alpha_normalized - 1.0), dim=1
        )
        correction = self.net(network_input)
        delta = self.longitudinal_phase(points)
        correction_factor = s.square() * delta.square()
        real = 1.0 + correction_factor * correction[:, 0:1]
        imag = delta * s + correction_factor * correction[:, 1:2]
        return torch.cat((real, imag), dim=1)
