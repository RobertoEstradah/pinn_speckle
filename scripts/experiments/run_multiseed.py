"""
run_multiseed.py
Entrena NB02 (Helmholtz 2D, lambda=0.1) con semillas 42, 123, 777.
Guarda resultados en results/multiseed_results.json
"""
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np
import torch
from scipy.stats import qmc
from src.models import PINN_2D_SIREN
from src.losses  import pinn_loss_2d

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
print("Device:", DEVICE, flush=True)

LAMBDA_PHYS     = 0.1
K               = 2 * np.pi
KX = KY         = K / np.sqrt(2)
NC, NB          = 3000, 300
ADAM_MAX_EPOCHS = 15000
ADAM_LR         = 1e-3
PATIENCE        = 800
DELTA           = 1e-7
LBFGS_MAX_ITER  = 1000

def make_data(seed):
    rng = np.random.default_rng(seed)
    sampler = qmc.LatinHypercube(d=2, seed=rng)
    xy_int  = sampler.random(NC).astype(np.float32)
    t = np.linspace(0, 1, NB, dtype=np.float32)
    z = np.zeros(NB, dtype=np.float32)
    o = np.ones(NB, dtype=np.float32)
    xy_bc, E_bc = [], []
    for side in ['bottom', 'top', 'left', 'right']:
        if side == 'bottom':  pts = np.column_stack([t, z])
        elif side == 'top':   pts = np.column_stack([t, o])
        elif side == 'left':  pts = np.column_stack([z, t])
        else:                 pts = np.column_stack([o, t])
        xy_bc.append(pts)
        x_s, y_s = pts[:, 0], pts[:, 1]
        E_bc.append(np.column_stack([
            np.cos(float(KX)*x_s + float(KY)*y_s).astype(np.float32),
            np.sin(float(KX)*x_s + float(KY)*y_s).astype(np.float32)
        ]))
    return (torch.tensor(xy_int.astype(np.float32), device=DEVICE),
            torch.tensor(np.concatenate(xy_bc).astype(np.float32), device=DEVICE),
            torch.tensor(np.concatenate(E_bc).astype(np.float32),  device=DEVICE))

def compute_l2(model):
    x = np.linspace(0, 1, 100, dtype=np.float32)
    y = np.linspace(0, 1, 100, dtype=np.float32)
    XX, YY = np.meshgrid(x, y)
    xy = torch.tensor(np.column_stack([XX.ravel(), YY.ravel()]).astype(np.float32), device=DEVICE)
    with torch.no_grad():
        E_pred = model(xy).cpu().numpy()
    l2_r = (np.linalg.norm(E_pred[:,0] - np.cos(float(KX)*XX.ravel()+float(KY)*YY.ravel())) /
            np.linalg.norm(np.cos(float(KX)*XX.ravel()+float(KY)*YY.ravel()))) * 100
    l2_i = (np.linalg.norm(E_pred[:,1] - np.sin(float(KX)*XX.ravel()+float(KY)*YY.ravel())) /
            np.linalg.norm(np.sin(float(KX)*XX.ravel()+float(KY)*YY.ravel()))) * 100
    return (l2_r + l2_i) / 2, l2_r, l2_i

def train_one(seed):
    torch.manual_seed(seed); np.random.seed(seed)
    if DEVICE == 'cuda': torch.cuda.manual_seed(seed)

    xy_int, xy_bc, E_bc = make_data(seed)
    model = PINN_2D_SIREN(hidden_dim=128, num_layers=5, omega_0=1.0).to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=ADAM_LR)

    best_loss = float('inf'); patience_counter = 0; epoch = 0
    t0 = time.time()
    for epoch in range(ADAM_MAX_EPOCHS):
        optimizer.zero_grad()
        loss, _, _ = pinn_loss_2d(model, xy_int, xy_bc, E_bc, K, LAMBDA_PHYS)
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
    print("  seed=%d Adam: %d epochs, loss=%.6e" % (seed, adam_epochs, best_loss), flush=True)

    lbfgs = torch.optim.LBFGS(model.parameters(), max_iter=LBFGS_MAX_ITER,
                                line_search_fn='strong_wolfe', history_size=100)
    iters = [0]
    def closure():
        lbfgs.zero_grad()
        loss, _, _ = pinn_loss_2d(model, xy_int, xy_bc, E_bc, K, LAMBDA_PHYS)
        loss.backward(); iters[0] += 1
        return loss
    lbfgs.step(closure)
    t_total = time.time() - t0

    l2_avg, l2_r, l2_i = compute_l2(model)
    print("  seed=%d L2_avg=%.4f%%  time=%ds" % (seed, l2_avg, t_total), flush=True)
    return {'seed': seed, 'l2_avg': round(l2_avg,4), 'l2_real': round(l2_r,4),
            'l2_imag': round(l2_i,4), 'adam_epochs': adam_epochs,
            'lbfgs_iters': iters[0], 'time_s': round(t_total,1)}

# Seed 42 already known from NB02
results = [
    {'seed': 42, 'l2_avg': 0.171, 'l2_real': 0.214, 'l2_imag': 0.127,
     'adam_epochs': 8737, 'lbfgs_iters': 1035, 'time_s': 299,
     'note': 'resultado original NB02'},
]

for seed in [123, 777]:
    print("\n=== Training seed=%d ===" % seed, flush=True)
    try:
        results.append(train_one(seed))
    except Exception as e:
        print("  ERROR:", str(e), flush=True)
        results.append({'seed': seed, 'error': str(e)})

out = os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'multiseed_results.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

l2s = [r['l2_avg'] for r in results if 'l2_avg' in r]
print("\n=== RESUMEN MULTI-SEMILLA (lambda=0.1) ===", flush=True)
for r in results:
    if 'l2_avg' in r:
        print("  seed=%d: L2=%.4f%%" % (r['seed'], r['l2_avg']), flush=True)
if len(l2s) > 1:
    print("  Media: %.4f%% +/- %.4f%%" % (np.mean(l2s), np.std(l2s)), flush=True)
print("\nGuardado en:", out, flush=True)
