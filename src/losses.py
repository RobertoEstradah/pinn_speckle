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
    pinn_loss_2d          — perdida total PINN para NB02, NB03, NB04

Uso:
    from src.losses import pinn_loss_1d, pinn_loss_2d
"""

import torch


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

    residual = E_xx + k**2 * E
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

    res_real = laplacian(E_real) + k**2 * E_real
    res_imag = laplacian(E_imag) + k**2 * E_imag

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
