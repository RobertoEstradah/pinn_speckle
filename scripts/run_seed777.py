"""Single-seed run: seed=777, lambda=0.1, writes to results/seed777_result.json"""
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import numpy as np, torch
from scipy.stats import qmc
from src.models import PINN_2D_SIREN
from src.losses import pinn_loss_2d

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
print("Device:", DEVICE, flush=True)
K = 2 * np.pi; KX = KY = K / np.sqrt(2)
NC, NB = 3000, 300; SEED = 777
LAMBDA = 0.1; ADAM_LR = 1e-3; PATIENCE = 800; DELTA = 1e-7
LBFGS_MAX_ITER = 1000

torch.manual_seed(SEED); np.random.seed(SEED)
if DEVICE == 'cuda': torch.cuda.manual_seed(SEED)

rng = np.random.default_rng(SEED)
sampler = qmc.LatinHypercube(d=2, seed=rng)
xy_int = torch.tensor(sampler.random(NC).astype(np.float32), device=DEVICE)
t = np.linspace(0, 1, NB, dtype=np.float32)
pts_list = [np.column_stack([t, np.zeros(NB, dtype=np.float32)]),
            np.column_stack([t, np.ones(NB, dtype=np.float32)]),
            np.column_stack([np.zeros(NB, dtype=np.float32), t]),
            np.column_stack([np.ones(NB, dtype=np.float32), t])]
bc_xy = np.concatenate(pts_list).astype(np.float32)
E_bc_np = np.concatenate([np.column_stack([
    np.cos(float(KX)*p[:, 0]+float(KY)*p[:, 1]).astype(np.float32),
    np.sin(float(KX)*p[:, 0]+float(KY)*p[:, 1]).astype(np.float32)
]) for p in pts_list]).astype(np.float32)
xy_bc = torch.tensor(bc_xy, device=DEVICE)
E_bc  = torch.tensor(E_bc_np, device=DEVICE)

model = PINN_2D_SIREN(128, 5, 1.0).to(DEVICE)
opt = torch.optim.Adam(model.parameters(), lr=ADAM_LR)
best = float('inf'); patience_c = 0; epoch = 0
t0 = time.time()
for epoch in range(15000):
    opt.zero_grad()
    loss, _, _ = pinn_loss_2d(model, xy_int, xy_bc, E_bc, K, LAMBDA)
    loss.backward(); opt.step()
    lv = loss.item()
    if lv < best - DELTA: best = lv; patience_c = 0
    else: patience_c += 1
    if patience_c >= PATIENCE: break
adam_epochs = epoch + 1
print("Adam: %d epochs, loss=%.6e" % (adam_epochs, best), flush=True)

lbfgs = torch.optim.LBFGS(model.parameters(), max_iter=LBFGS_MAX_ITER,
                            line_search_fn='strong_wolfe', history_size=100)
iters = [0]
def closure():
    lbfgs.zero_grad()
    loss, _, _ = pinn_loss_2d(model, xy_int, xy_bc, E_bc, K, LAMBDA)
    loss.backward(); iters[0] += 1
    return loss
lbfgs.step(closure)
t_total = time.time() - t0
print("L-BFGS: %d iters, time=%.0fs" % (iters[0], t_total), flush=True)

x = np.linspace(0, 1, 100, dtype=np.float32); y = np.linspace(0, 1, 100, dtype=np.float32)
XX, YY = np.meshgrid(x, y)
xy_eval = torch.tensor(np.column_stack([XX.ravel(), YY.ravel()]).astype(np.float32), device=DEVICE)
with torch.no_grad():
    E_pred = model(xy_eval).cpu().numpy()
E_r_exact = np.cos(float(KX)*XX.ravel()+float(KY)*YY.ravel())
E_i_exact = np.sin(float(KX)*XX.ravel()+float(KY)*YY.ravel())
l2_r = np.linalg.norm(E_pred[:, 0]-E_r_exact)/np.linalg.norm(E_r_exact)*100
l2_i = np.linalg.norm(E_pred[:, 1]-E_i_exact)/np.linalg.norm(E_i_exact)*100
l2_avg = (l2_r + l2_i) / 2
print("L2_avg=%.4f%% (real=%.4f%%, imag=%.4f%%)" % (l2_avg, l2_r, l2_i), flush=True)

out = os.path.join(os.path.dirname(__file__), '..', 'results', 'seed777_result.json')
with open(out, 'w') as f:
    json.dump({'seed': SEED, 'l2_avg': round(l2_avg, 4), 'l2_real': round(l2_r, 4),
               'l2_imag': round(l2_i, 4), 'adam_epochs': adam_epochs,
               'lbfgs_iters': iters[0], 'time_s': round(t_total, 1)}, f, indent=2)
print("Saved to", out, flush=True)
