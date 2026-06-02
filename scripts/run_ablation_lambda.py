"""
run_ablation_lambda.py
Ablacion del peso de fisica lambda_phys in {0.01, 0.1, 1.0} para NB02.
Arquitectura fija: SIREN 5x128, omega_0=1.0, SEED=42, LHS N_c=3000, N_b=300.
Guarda resultados en results/ablation_lambda.json
"""
import sys, os, json, time, gc
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import torch
from scipy.stats import qmc
from src.models import PINN_2D_SIREN
from src.losses  import pinn_loss_2d

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
print("Device:", DEVICE, flush=True)

K     = 2 * np.pi
KX    = KY = K / np.sqrt(2)
SEED  = 42
NC    = 3000
NB    = 300
ADAM_MAX_EPOCHS = 15000
ADAM_LR         = 1e-3
PATIENCE        = 800
DELTA           = 1e-7
LBFGS_MAX_ITER  = 1000
HIDDEN_DIM      = 128
NUM_LAYERS      = 5
OMEGA_0         = 1.0

def make_data(seed=42):
    sampler = qmc.LatinHypercube(d=2, seed=seed)
    xy_int  = sampler.random(NC).astype(np.float32)

    t = np.linspace(0, 1, NB, dtype=np.float32)
    xy_bc, E_bc = [], []
    z = np.zeros(NB, dtype=np.float32)
    o = np.ones(NB, dtype=np.float32)
    for side in ['bottom', 'top', 'left', 'right']:
        if side == 'bottom':  pts = np.column_stack([t, z])
        elif side == 'top':   pts = np.column_stack([t, o])
        elif side == 'left':  pts = np.column_stack([z, t])
        else:                 pts = np.column_stack([o, t])
        xy_bc.append(pts)
        x_s, y_s = pts[:, 0], pts[:, 1]
        E_r = np.cos(KX*x_s + KY*y_s).astype(np.float32)
        E_i = np.sin(KX*x_s + KY*y_s).astype(np.float32)
        E_bc.append(np.column_stack([E_r, E_i]))

    xy_bc  = torch.tensor(np.concatenate(xy_bc).astype(np.float32),  device=DEVICE)
    E_bc   = torch.tensor(np.concatenate(E_bc).astype(np.float32),   device=DEVICE)
    xy_int = torch.tensor(xy_int.astype(np.float32), device=DEVICE)
    return xy_int, xy_bc, E_bc

def compute_l2(model):
    x = np.linspace(0, 1, 100, dtype=np.float32)
    y = np.linspace(0, 1, 100, dtype=np.float32)
    XX, YY = np.meshgrid(x, y)
    xy = torch.tensor(np.column_stack([XX.ravel(), YY.ravel()]).astype(np.float32), device=DEVICE)
    with torch.no_grad():
        E_pred = model(xy).cpu().numpy()
    E_r_exact = np.cos(float(KX)*XX.ravel() + float(KY)*YY.ravel())
    E_i_exact = np.sin(float(KX)*XX.ravel() + float(KY)*YY.ravel())
    l2_r = np.linalg.norm(E_pred[:,0] - E_r_exact) / np.linalg.norm(E_r_exact) * 100
    l2_i = np.linalg.norm(E_pred[:,1] - E_i_exact) / np.linalg.norm(E_i_exact) * 100
    return (l2_r + l2_i) / 2, l2_r, l2_i

def train_one(lambda_phys, seed=42):
    torch.manual_seed(seed); np.random.seed(seed)
    if DEVICE == 'cuda': torch.cuda.manual_seed(seed)

    xy_int, xy_bc, E_bc = make_data(seed)
    model = PINN_2D_SIREN(hidden_dim=HIDDEN_DIM, num_layers=NUM_LAYERS, omega_0=OMEGA_0).to(DEVICE)

    optimizer = torch.optim.Adam(model.parameters(), lr=ADAM_LR)
    best_loss = float('inf'); patience_counter = 0; epoch = 0
    t0 = time.time()
    for epoch in range(ADAM_MAX_EPOCHS):
        optimizer.zero_grad()
        loss, _, _ = pinn_loss_2d(model, xy_int, xy_bc, E_bc, K, lambda_phys)
        loss.backward()
        optimizer.step()
        lv = loss.item()
        if lv < best_loss - DELTA:
            best_loss = lv; patience_counter = 0
        else:
            patience_counter += 1
        if patience_counter >= PATIENCE:
            break
    adam_epochs = epoch + 1
    print("  lam=%.2f Adam: %d epochs, loss=%.6e" % (lambda_phys, adam_epochs, best_loss), flush=True)

    lbfgs = torch.optim.LBFGS(model.parameters(), max_iter=LBFGS_MAX_ITER,
                                line_search_fn='strong_wolfe', history_size=100)
    lbfgs_iters = [0]
    def closure():
        lbfgs.zero_grad()
        loss, _, _ = pinn_loss_2d(model, xy_int, xy_bc, E_bc, K, lambda_phys)
        loss.backward()
        lbfgs_iters[0] += 1
        return loss
    lbfgs.step(closure)
    t_total = time.time() - t0
    print("  lam=%.2f L-BFGS: %d iters, time=%ds" % (lambda_phys, lbfgs_iters[0], t_total), flush=True)

    l2_avg, l2_r, l2_i = compute_l2(model)
    print("  lam=%.2f L2_avg=%.4f%%  (real=%.4f%%, imag=%.4f%%)" % (lambda_phys, l2_avg, l2_r, l2_i), flush=True)
    result = {
        'lambda': lambda_phys,
        'l2_avg': round(l2_avg, 4),
        'l2_real': round(l2_r, 4),
        'l2_imag': round(l2_i, 4),
        'adam_epochs': adam_epochs,
        'lbfgs_iters': lbfgs_iters[0],
        'time_s': round(t_total, 1),
        'converged': l2_avg < 5.0,
    }
    # Explicit cleanup
    del model, optimizer, xy_int, xy_bc, E_bc
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return result

out_path = os.path.join(os.path.dirname(__file__), '..', 'results', 'ablation_lambda.json')
# Pre-fill with known lam=0.01 result from prior run
results = {
    '0.01': {'lambda': 0.01, 'l2_avg': 0.1632, 'l2_real': 0.1873, 'l2_imag': 0.1391,
             'adam_epochs': 6575, 'lbfgs_iters': 320, 'time_s': 801.0, 'converged': True,
             'note': 'run previa (seed=42)'},
    '0.1':  {'lambda': 0.1, 'l2_avg': 0.171, 'l2_real': 0.214, 'l2_imag': 0.127,
             'adam_epochs': 8737, 'lbfgs_iters': 1035, 'time_s': 299, 'converged': True,
             'note': 'resultado original NB02 (seed=42)'},
}
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print("Checkpoint written (lam=0.01 and 0.1 known).", flush=True)

for lam in [1.0]:
    print("\n=== Training lam = %.2f ===" % lam, flush=True)
    try:
        r = train_one(lam)
        results[str(lam)] = r
    except Exception as e:
        print("  ERROR:", str(e), flush=True)
        results[str(lam)] = {'lambda': lam, 'error': str(e), 'converged': False}
    finally:
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    # Save after each lambda
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("Checkpoint saved.", flush=True)

print("\n=== RESUMEN ABLACION ===", flush=True)
for k, v in results.items():
    if 'l2_avg' in v:
        print("  lam=%s: L2=%.4f%%  converge=%s" % (k, v['l2_avg'], v['converged']), flush=True)
print("\nGuardado en:", out_path, flush=True)
