"""
run_multiseed.py
================
Reproducibilidad multi-semilla de NB02 (Helmholtz 2D, campo complejo, lambda=0.1).

Este script replica EXACTAMENTE el camino de codigo de
`notebooks/02_pinn_helmholtz_2d_complex_field.ipynb`, de modo que la semilla 42
debe devolver el mismo resultado que el notebook (L2_avg = 0.171 %). Esa
coincidencia es la prueba de que notebook y script son equivalentes y que los
valores de las tres semillas son comparables entre si.

Puntos donde una version anterior de este script divergia del notebook, y que
hacian que la semilla 42 no fuera reproducible (por eso estaba escrita a mano):

  1. LHS sembrado con un Generator (`default_rng(seed)`) en lugar del entero.
     Produce una secuencia de puntos distinta.
  2. Casteo a float32 antes del muestreo en lugar de despues.
  3. No se restauraba el mejor modelo tras el early stopping, asi que L-BFGS
     partia de los pesos de 800 epocas despues del optimo, no del optimo.

Salida: results/multiseed_results.json
"""
import sys, os, json, time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np
import torch
from scipy.stats import qmc

from src.models import PINN_2D_SIREN
from src.losses import pinn_loss_2d
from src.utils  import l2_rel

# ── Hiperparametros: identicos al CONFIG de NB02 ─────────────────────────────
K               = 2 * np.pi
KX = KY         = K / np.sqrt(2)
N_COLLOC        = 3000
N_BOUNDARY      = 300          # por borde -> 1200 total
HIDDEN_DIM      = 128
NUM_LAYERS      = 5
OMEGA_0         = 1.0
ADAM_MAX_EPOCHS = 15000
ADAM_LR         = 1e-3
LAMBDA_PHYS     = 0.1
PATIENCE        = 800
MIN_DELTA       = 1e-7
LBFGS_MAX_ITER  = 1000
LBFGS_HISTORY   = 100
N_EVAL          = 100

SEEDS = [42, 123, 777]

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def make_data(seed):
    """Datos de entrenamiento, identicos a la celda 13 de NB02."""
    # LHS sembrado con el ENTERO, como el notebook
    sampler   = qmc.LatinHypercube(d=2, seed=seed)
    lhs_pts   = sampler.random(n=N_COLLOC)                     # float64
    xy_colloc = torch.tensor(lhs_pts, dtype=torch.float32).to(DEVICE)

    t = np.linspace(0, 1, N_BOUNDARY)                          # float64
    x_bot = np.stack([t,                      np.zeros(N_BOUNDARY)], axis=1)
    x_top = np.stack([t,                      np.ones(N_BOUNDARY)],  axis=1)
    x_lft = np.stack([np.zeros(N_BOUNDARY),   t],                    axis=1)
    x_rgt = np.stack([np.ones(N_BOUNDARY),    t],                    axis=1)
    xy_bc_np = np.vstack([x_bot, x_top, x_lft, x_rgt])

    phase_bc = KX * xy_bc_np[:, 0] + KY * xy_bc_np[:, 1]
    E_bc_np  = np.stack([np.cos(phase_bc), np.sin(phase_bc)], axis=1)

    xy_bc = torch.tensor(xy_bc_np, dtype=torch.float32).to(DEVICE)
    E_bc  = torch.tensor(E_bc_np,  dtype=torch.float32).to(DEVICE)
    return xy_colloc, xy_bc, E_bc


def evaluate(model):
    """Metricas, identicas a la celda 21 de NB02. Devuelve fracciones, no %."""
    x_lin = np.linspace(0, 1, N_EVAL)                          # float64
    y_lin = np.linspace(0, 1, N_EVAL)
    XX, YY = np.meshgrid(x_lin, y_lin)

    xy_test = torch.tensor(np.stack([XX.ravel(), YY.ravel()], axis=1),
                           dtype=torch.float32).to(DEVICE)
    model.eval()
    with torch.no_grad():
        E_pred = model(xy_test).cpu().numpy()

    E_real_pred = E_pred[:, 0].reshape(N_EVAL, N_EVAL)
    E_imag_pred = E_pred[:, 1].reshape(N_EVAL, N_EVAL)

    phase = KX * XX + KY * YY
    return l2_rel(E_real_pred, np.cos(phase)), l2_rel(E_imag_pred, np.sin(phase))


def train_one(seed):
    """Entrenamiento Adam -> L-BFGS, identico a la celda 19 de NB02."""
    xy_colloc, xy_bc, E_bc = make_data(seed)

    # Semillas justo antes de instanciar, como el notebook
    torch.manual_seed(seed)
    if DEVICE.type == 'cuda':
        torch.cuda.manual_seed(seed)

    model = PINN_2D_SIREN(hidden_dim=HIDDEN_DIM, num_layers=NUM_LAYERS,
                          omega_0=OMEGA_0).to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=ADAM_LR)

    best_loss  = float('inf')
    best_state = None
    sin_mejora = 0
    epoch_final = ADAM_MAX_EPOCHS

    t0 = time.time()
    for epoch in range(ADAM_MAX_EPOCHS):
        optimizer.zero_grad()
        loss, _, _ = pinn_loss_2d(model, xy_colloc, xy_bc, E_bc,
                                  k=K, lambda_phys=LAMBDA_PHYS)
        loss.backward()
        optimizer.step()

        current_loss = loss.item()
        if current_loss < best_loss - MIN_DELTA:
            best_loss  = current_loss
            best_state = {k_: v.clone() for k_, v in model.state_dict().items()}
            sin_mejora = 0
        else:
            sin_mejora += 1

        if sin_mejora >= PATIENCE:
            epoch_final = epoch + 1
            model.load_state_dict(best_state)      # <- restaurar el mejor
            break
    t_adam = time.time() - t0

    print("  seed=%d  Adam: %d epocas, mejor L_total=%.3e, %.1f s"
          % (seed, epoch_final, best_loss, t_adam), flush=True)

    lbfgs = torch.optim.LBFGS(model.parameters(), lr=1.0,
                              max_iter=LBFGS_MAX_ITER,
                              history_size=LBFGS_HISTORY,
                              line_search_fn='strong_wolfe')
    calls = [0]

    def closure():
        lbfgs.zero_grad()
        loss, _, _ = pinn_loss_2d(model, xy_colloc, xy_bc, E_bc,
                                  k=K, lambda_phys=LAMBDA_PHYS)
        loss.backward()
        calls[0] += 1
        return loss

    t1 = time.time()
    lbfgs.step(closure)
    t_lbfgs = time.time() - t1

    l2_r, l2_i = evaluate(model)
    l2_avg = (l2_r + l2_i) / 2

    print("  seed=%d  L-BFGS: %d evaluaciones, %.1f s  |  L2_avg=%.4f %%  total=%.1f s"
          % (seed, calls[0], t_lbfgs, l2_avg * 100, t_adam + t_lbfgs), flush=True)

    return {
        'seed'               : seed,
        'l2_avg'             : round(l2_avg * 100, 4),
        'l2_real'            : round(l2_r   * 100, 4),
        'l2_imag'            : round(l2_i   * 100, 4),
        'adam_epochs'        : epoch_final,
        'adam_best_loss'     : float('%.6e' % best_loss),
        'lbfgs_closure_calls': calls[0],
        'time_adam_s'        : round(t_adam,  1),
        'time_lbfgs_s'       : round(t_lbfgs, 1),
        'time_total_s'       : round(t_adam + t_lbfgs, 1),
    }


def main():
    # Reproducibilidad global, como la celda 2 de NB02
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark     = False
    np.random.seed(SEEDS[0])

    print("Dispositivo:", DEVICE, flush=True)
    if DEVICE.type == 'cuda':
        print("GPU        :", torch.cuda.get_device_name(0), flush=True)
    print("PyTorch    :", torch.__version__, "| Python", sys.version.split()[0], flush=True)
    print()

    results = {}
    for seed in SEEDS:
        print("=== semilla %d ===" % seed, flush=True)
        results[str(seed)] = train_one(seed)
        print(flush=True)

    l2s = [results[str(s)]['l2_avg'] for s in SEEDS]
    results['summary'] = {
        'seeds'   : SEEDS,
        'l2_values': l2s,
        'mean'    : round(float(np.mean(l2s)), 4),
        'std'     : round(float(np.std(l2s)),  4),
        'entorno' : {
            'python' : sys.version.split()[0],
            'torch'  : torch.__version__,
            'cuda'   : torch.version.cuda,
            'gpu'    : torch.cuda.get_device_name(0) if DEVICE.type == 'cuda' else 'cpu',
        },
        'nota': ('Las tres semillas se entrenan con el mismo camino de codigo, '
                 'identico al de NB02, y se miden en la misma sesion. '
                 '"lbfgs_closure_calls" cuenta evaluaciones de la funcion objetivo, '
                 'no iteraciones de L-BFGS: la busqueda de linea strong_wolfe llama '
                 'al closure varias veces por iteracion, por eso el valor puede '
                 'superar max_iter=1000.'),
    }

    out = os.path.join(os.path.dirname(__file__), '..', '..', 'results',
                       'multiseed_results.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("=== RESUMEN MULTI-SEMILLA (lambda=0.1) ===", flush=True)
    for s in SEEDS:
        r = results[str(s)]
        print("  seed=%-4d L2=%.4f %%  | Adam %5d ep | L-BFGS %4d eval | %6.1f s"
              % (s, r['l2_avg'], r['adam_epochs'],
                 r['lbfgs_closure_calls'], r['time_total_s']), flush=True)
    print("  Media: %.4f %% +/- %.4f %%" % (results['summary']['mean'],
                                            results['summary']['std']), flush=True)
    print()
    print("Prueba de equivalencia notebook <-> script:", flush=True)
    print("  NB02 reporta L2_avg = 0.1710 %% para la semilla 42", flush=True)
    print("  este script         = %.4f %%" % results['42']['l2_avg'], flush=True)
    print("  ->", "COINCIDE" if abs(results['42']['l2_avg'] - 0.171) < 0.001
          else "NO COINCIDE, quedan diferencias por localizar", flush=True)
    print()
    print("Guardado en:", out, flush=True)


if __name__ == '__main__':
    main()
