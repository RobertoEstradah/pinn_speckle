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

import numpy as np
import torch
from pathlib import Path


# La raíz se obtiene desde la ubicación de este módulo y no desde el directorio
# de trabajo del kernel. Así, los notebooks guardan siempre dentro del proyecto
# que contiene este archivo, aunque Jupyter se inicie desde otra carpeta.
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _resolve_project_root(notebook_dir=None):
    """Resuelve la raíz del proyecto de forma estable.

    ``notebook_dir`` se conserva por compatibilidad. Puede apuntar a la raíz
    del proyecto o a su carpeta ``notebooks``.
    """
    if notebook_dir is None:
        return PROJECT_ROOT

    candidate = Path(notebook_dir).resolve()
    if candidate.name == 'notebooks':
        candidate = candidate.parent
    if not (candidate / 'src').is_dir():
        raise ValueError(
            f'No se encontró src/ en la raíz indicada: {candidate}'
        )
    return candidate


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
    fig_dir = _resolve_project_root(notebook_dir) / 'results' / 'figures'
    fig_dir.mkdir(parents=True, exist_ok=True)
    return fig_dir


def get_models_dir(notebook_dir=None):
    """
    Retorna la ruta a results/models/ y la crea si no existe.
    """
    models_dir = _resolve_project_root(notebook_dir) / 'results' / 'models'
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
    path = models_dir / f'{name}.pt'
    torch.save(model.state_dict(), str(path))
    # Se imprime relativa a la raiz: la absoluta delata la maquina local.
    print(f'Modelo guardado en: {path.relative_to(models_dir.parents[1]).as_posix()}')
    return str(path)


def load_model(model, name, notebook_dir=None, device=None):
    """
    Carga pesos de un modelo guardado previamente.

    Nota: no se recomienda para transferir pesos entre problemas con condicion
    de frontera distinta (p. ej. onda plana -> frontera estocastica): los
    pesos quedan calibrados para la fisica del problema original y pueden
    sesgar el entrenamiento del problema nuevo. Util para recargar el mismo
    modelo en una sesion posterior o para evaluacion posterior al
    entrenamiento.

    Uso:
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
    model.load_state_dict(torch.load(str(path), map_location=map_loc, weights_only=True))
    if device:
        model.to(device)
    print(f'Modelo cargado desde: {path}')
    return model
