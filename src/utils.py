"""
utils.py — Metricas, muestreo LHS y utilidades
===============================================
Proyecto : Simulacion Acelerada de Speckle Optico mediante PINNs
Autor    : Roberto Hernandez Estrada
Director : Dr. Jose Adan Hernandez Nolasco — UJAT

Funciones:
    l2_rel         — error L2 relativo (metrica principal de tesis)
    get_figures_dir — ruta a results/figures/ (la crea si no existe)
    get_models_dir  — ruta a results/models/ (la crea si no existe)
    save_model      — guarda pesos del modelo en results/models/
    load_model      — carga pesos guardados para reusar en otro NB

Uso:
    from src.utils import get_figures_dir, save_model, load_model
"""

import os
import numpy as np
import torch
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
def l2_rel(pred, exact):
    """
    Error L2 relativo — metrica principal de la tesis.
        L2 = ||pred - exact||_2 / ||exact||_2
    """
    return np.linalg.norm(pred.ravel() - exact.ravel()) / \
           np.linalg.norm(exact.ravel())


# ─────────────────────────────────────────────────────────────────────────────
def get_figures_dir(notebook_dir=None):
    """
    Retorna la ruta a results/figures/ y la crea si no existe.

    Uso en el notebook:
        from src.utils import get_figures_dir
        IMG_DIR = get_figures_dir()
        plt.savefig(str(IMG_DIR / 'resultados_nb01.png'), dpi=150)
    """
    if notebook_dir is None:
        notebook_dir = os.getcwd()
    fig_dir = Path(notebook_dir).parent / 'results' / 'figures'
    fig_dir.mkdir(parents=True, exist_ok=True)
    return fig_dir


def get_models_dir(notebook_dir=None):
    """
    Retorna la ruta a results/models/ y la crea si no existe.
    """
    if notebook_dir is None:
        notebook_dir = os.getcwd()
    models_dir = Path(notebook_dir).parent / 'results' / 'models'
    models_dir.mkdir(parents=True, exist_ok=True)
    return models_dir


# ─────────────────────────────────────────────────────────────────────────────
def save_model(model, name, notebook_dir=None):
    """
    Guarda los pesos de un modelo entrenado en results/models/.

    Uso al final de NB01:
        save_model(model_1d, 'nb01_helmholtz1d')
        # guarda en: results/models/nb01_helmholtz1d.pt

    Uso al final de NB02:
        save_model(model_2d, 'nb02_helmholtz2d')
        # guarda en: results/models/nb02_helmholtz2d.pt
    """
    models_dir = get_models_dir(notebook_dir)
    path = str(models_dir / f'{name}.pt')
    torch.save(model.state_dict(), path)
    print(f'Modelo guardado en: {path}')
    return path


def load_model(model, name, notebook_dir=None, device=None):
    """
    Carga pesos de un modelo guardado previamente.

    Uso al inicio de NB03 para reusar el modelo de NB02:
        from src.models import PINN_2D_SIREN
        from src.utils  import load_model

        model_2d = PINN_2D_SIREN(hidden_dim=128).to(device)
        model_2d = load_model(model_2d, 'nb02_helmholtz2d', device=device)
    """
    models_dir = get_models_dir(notebook_dir)
    path = models_dir / f'{name}.pt'

    if not path.exists():
        raise FileNotFoundError(
            f'No se encontro el modelo en: {path}\n'
            f'Asegurate de haber ejecutado el notebook correspondiente '
            f'y llamado save_model() al final.'
        )

    map_loc = device if device else 'cpu'
    model.load_state_dict(torch.load(str(path), map_location=map_loc))
    if device:
        model.to(device)
    print(f'Modelo cargado desde: {path}')
    return model
