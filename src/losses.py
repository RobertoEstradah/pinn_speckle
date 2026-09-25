"""
losses.py — Funciones de perdida extraidas de NB01 y NB02
==========================================================
Proyecto : Simulacion Acelerada de Speckle Optico mediante PINNs
Autor    : Roberto Hernandez Estrada
Director : Dr. Jose Adan Hernandez Nolasco — UJAT

Funciones:
    helmholtz_residual_1d — residuo EDP Helmholtz 1D
    pinn_loss_1d          — perdida total PINN para NB01
    helmholtz_residual_2d — laplaciano 2D + residuo EDP
    pinn_loss_2d          — perdida total PINN para NB02, NB03
    helmholtz_residual_3d — laplaciano 3D complejo para NB_3D_01
    pinn_loss_3d          — perdida total PINN para NB_3D_01
    helmholtz_envelope_transfer_residual_3d — Helmholtz fisica en envolvente

Uso:
    from src.losses import pinn_loss_1d, pinn_loss_2d
"""

import torch
from torch.func import jvp


# ─────────────────────────────────────────────────────────────────────────────
# 1D
# ─────────────────────────────────────────────────────────────────────────────

def helmholtz_residual_1d(model, x_dominio, k):
    """
    Calcula el residuo de Helmholtz 1D: R = E''(x) + k^2 * E(x)
    Si la red es perfecta -> R = 0 en todo el dominio.
    """
    x_dominio = x_dominio.clone().requires_grad_(True)

    E = model(x_dominio)

    E_x = torch.autograd.grad(
        E, x_dominio,
        grad_outputs=torch.ones_like(E),
        create_graph=True
    )[0]

    E_xx = torch.autograd.grad(
        E_x, x_dominio,
        grad_outputs=torch.ones_like(E_x),
        create_graph=True
    )[0]

    residual = E_xx + float(k)**2 * E
    return residual, E


def pinn_loss_1d(model, x_colloc, x_bc, E_bc, k, lambda_phys):
    """
    Perdida total PINN para Helmholtz 1D.
        L_total = L_datos + lambda * L_fisica
    """
    E_pred_bc    = model(x_bc)
    loss_data    = torch.mean((E_pred_bc - E_bc) ** 2)

    residual, _  = helmholtz_residual_1d(model, x_colloc, k)
    loss_physics = torch.mean(residual ** 2)

    loss_total = loss_data + lambda_phys * loss_physics
    return loss_total, loss_data, loss_physics


# ─────────────────────────────────────────────────────────────────────────────
# 2D
# ─────────────────────────────────────────────────────────────────────────────

def helmholtz_residual_2d(model, xy_colloc, k):
    """
    Residuo de Helmholtz 2D para ambas partes del campo:
        R_real = d2E_real/dx2 + d2E_real/dy2 + k^2 * E_real
        R_imag = d2E_imag/dx2 + d2E_imag/dy2 + k^2 * E_imag
    Si la red es perfecta -> R_real = R_imag = 0 en todo el dominio.
    """
    xy = xy_colloc.clone().requires_grad_(True)

    E_out  = model(xy)
    E_real = E_out[:, 0:1]
    E_imag = E_out[:, 1:2]
    ones   = torch.ones_like(E_real)

    def laplacian(field):
        grad_f = torch.autograd.grad(field, xy, grad_outputs=ones,
                                     create_graph=True)[0]
        f_xx = torch.autograd.grad(grad_f[:, 0:1], xy, grad_outputs=ones,
                                   create_graph=True)[0][:, 0:1]
        f_yy = torch.autograd.grad(grad_f[:, 1:2], xy, grad_outputs=ones,
                                   create_graph=True)[0][:, 1:2]
        return f_xx + f_yy

    k_sq = float(k) ** 2
    res_real = laplacian(E_real) + k_sq * E_real
    res_imag = laplacian(E_imag) + k_sq * E_imag

    return res_real, res_imag, E_real, E_imag


def pinn_loss_2d(model, xy_colloc, xy_bc, E_bc, k, lambda_phys):
    """
    Perdida total PINN para Helmholtz 2D con campo complejo.
        L_total = L_datos + lambda * (L_fisica_real + L_fisica_imag)
    """
    E_pred_bc    = model(xy_bc)
    loss_data    = torch.mean((E_pred_bc - E_bc) ** 2)

    res_real, res_imag, _, _ = helmholtz_residual_2d(model, xy_colloc, k)
    loss_physics = torch.mean(res_real ** 2) + torch.mean(res_imag ** 2)

    loss_total = loss_data + lambda_phys * loss_physics
    return loss_total, loss_data, loss_physics


# ─────────────────────────────────────────────────────────────────────────────
# 3D
# ─────────────────────────────────────────────────────────────────────────────

def helmholtz_residual_3d(model, xyz_colloc, k):
    """
    Residuo de Helmholtz escalar 3D para un campo complejo:

        R_real = E_real,xx + E_real,yy + E_real,zz + k^2 E_real
        R_imag = E_imag,xx + E_imag,yy + E_imag,zz + k^2 E_imag
    """
    xyz = xyz_colloc.clone().requires_grad_(True)

    field = model(xyz)
    field_real = field[:, 0:1]
    field_imag = field[:, 1:2]

    def laplacian(component):
        grad_component = torch.autograd.grad(
            component,
            xyz,
            grad_outputs=torch.ones_like(component),
            create_graph=True,
        )[0]
        second_derivatives = []
        for axis in range(3):
            derivative = grad_component[:, axis:axis + 1]
            second = torch.autograd.grad(
                derivative,
                xyz,
                grad_outputs=torch.ones_like(derivative),
                create_graph=True,
            )[0][:, axis:axis + 1]
            second_derivatives.append(second)
        return sum(second_derivatives)

    k_squared = float(k) ** 2
    residual_real = laplacian(field_real) + k_squared * field_real
    residual_imag = laplacian(field_imag) + k_squared * field_imag
    return residual_real, residual_imag, field_real, field_imag


def pinn_loss_3d(model, xyz_colloc, xyz_boundary, field_boundary, k, lambda_phys):
    """Pérdida para Helmholtz 3D: seis caras de Dirichlet más residuo físico."""
    field_predicted = model(xyz_boundary)
    loss_boundary = torch.mean((field_predicted - field_boundary) ** 2)

    residual_real, residual_imag, _, _ = helmholtz_residual_3d(
        model, xyz_colloc, k
    )
    loss_physics = (
        torch.mean(residual_real ** 2)
        + torch.mean(residual_imag ** 2)
    )

    loss_total = loss_boundary + lambda_phys * loss_physics
    return loss_total, loss_boundary, loss_physics


def helmholtz_modal_residual_3d(model, z, kz_squared):
    """Residuo de cada modo transversal de la Helmholtz escalar 3D.

    Para ``E = sum_m a_m(z) exp(i(kx_m x + ky_m y))`` se evalúa

        a_m''(z) + (k^2 - kx_m^2 - ky_m^2) a_m(z).

    La salida se devuelve con forma ``(n_z, n_modes, 2)``.
    """
    tangent = torch.ones_like(z)

    def first_derivative(values):
        return jvp(model, (values,), (torch.ones_like(values),))[1]

    coefficients, _ = jvp(model, (z,), (tangent,))
    _, second_derivative = jvp(first_derivative, (z,), (tangent,))
    batch_size = z.shape[0]
    coefficients = coefficients.reshape(batch_size, -1, 2)
    second_derivative = second_derivative.reshape(batch_size, -1, 2)
    return (
        second_derivative
        + kz_squared.reshape(1, -1, 1) * coefficients
    )


def helmholtz_envelope_transfer_residual_3d(model, points):
    """Residuo exacto de Helmholtz para la transferencia de la envolvente.

    Tras escribir ``E=exp(i*k*z)*psi`` y usar ``s=z/Z``, cada modo satisface

        epsilon*h_ss + i*h_s - alpha*h = 0,

    con ``epsilon=1/(2*k*Z)`` y ``alpha=q_perp**2*Z/(2*k)``. ``points``
    contiene ``(s, alpha/alpha_max)``. La derivación automática se realiza
    sólo en la dirección ``s``.
    """
    tangent = torch.zeros_like(points)
    tangent[:, 0] = 1.0

    def first_derivative(values):
        local_tangent = torch.zeros_like(values)
        local_tangent[:, 0] = 1.0
        return jvp(model, (values,), (local_tangent,))[1]

    transfer, first = jvp(model, (points,), (tangent,))
    _, second = jvp(first_derivative, (points,), (tangent,))
    alpha = model.physical_alpha(points)
    real = model.epsilon * second[:, 0:1] - first[:, 1:2] - alpha * transfer[:, 0:1]
    imag = model.epsilon * second[:, 1:2] + first[:, 0:1] - alpha * transfer[:, 1:2]
    return torch.cat((real, imag), dim=1)
