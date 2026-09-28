"""
utils.py — Metricas, muestreo LHS y utilidades
===============================================
Proyecto : Simulacion Acelerada de Speckle Optico mediante PINNs
Autor    : Roberto Hernandez Estrada
Director : Dr. Jose Adan Hernandez Nolasco — UJAT

Funciones:
    l2_rel         — error L2 relativo (metrica principal de tesis)
    get_figures_dir — ruta a results/<notebook>/figures/ (la crea si no existe)
    get_models_dir  — ruta a results/<notebook>/models/ (la crea si no existe)
    save_model      — guarda pesos del modelo en results/<notebook>/models/
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
def _results_dir(notebook_dir=None, notebook=None):
    """results/<notebook>/ si se indica el notebook; si no, results/_exploracion/."""
    base = _resolve_project_root(notebook_dir) / 'results'
    return base / (notebook or '_exploracion')


def get_figures_dir(notebook_dir=None, notebook=None):
    """
    Retorna la ruta a results/<notebook>/figures/ y la crea si no existe.

    Cada notebook escribe solo en su carpeta de results/. Sin ``notebook``
    devuelve results/_exploracion/figures/: lo que no es de un notebook es prueba.

    Uso en el notebook:
        from src.utils import get_figures_dir
        IMG_DIR = get_figures_dir(notebook='nb01')
        plt.savefig(str(IMG_DIR / 'resultados_nb01.png'), dpi=150)
    """
    fig_dir = _results_dir(notebook_dir, notebook) / 'figures'
    fig_dir.mkdir(parents=True, exist_ok=True)
    return fig_dir


def get_models_dir(notebook_dir=None, notebook=None):
    """
    Retorna la ruta a results/<notebook>/models/ y la crea si no existe.
    """
    models_dir = _results_dir(notebook_dir, notebook) / 'models'
    models_dir.mkdir(parents=True, exist_ok=True)
    return models_dir


# ─────────────────────────────────────────────────────────────────────────────
def save_model(model, name, notebook_dir=None, notebook=None):
    """
    Guarda los pesos de un modelo entrenado en results/<notebook>/models/.

    Uso al final de NB01:
        save_model(model_1d, 'nb01_helmholtz1d', notebook='nb01')
        # guarda en: results/nb01/models/nb01_helmholtz1d.pt

    Uso al final de NB02:
        save_model(model_2d, 'nb02_helmholtz2d', notebook='nb02')
        # guarda en: results/nb02/models/nb02_helmholtz2d.pt
    """
    models_dir = get_models_dir(notebook_dir, notebook)
    path = models_dir / f'{name}.pt'
    torch.save(model.state_dict(), str(path))
    # Se imprime relativa a la raiz: la absoluta delata la maquina local.
    raiz = _resolve_project_root(notebook_dir)
    print(f'Modelo guardado en: {path.relative_to(raiz).as_posix()}')
    return str(path)


def load_model(model, name, notebook_dir=None, device=None, notebook=None):
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
        model_2d = load_model(model_2d, 'nb02_helmholtz2d', device=device, notebook='nb02')
    """
    models_dir = get_models_dir(notebook_dir, notebook)
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
    print(f'Modelo cargado desde: {path.relative_to(_resolve_project_root(notebook_dir)).as_posix()}')
    return model
