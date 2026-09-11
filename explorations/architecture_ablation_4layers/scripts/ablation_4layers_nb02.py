# Ablacion adicional: NB02 (2D) con 4 capas ocultas en vez de 5, todo lo demas
# identico al protocolo real de NB02 (k=2pi, onda plana kx=ky=k/sqrt(2),
# N_colloc=3000 LHS, N_boundary=300/borde, lambda_phys=0.1, patience=800,
# Adam max 15000 + L-BFGS 1000/100, seed=42).
# NO modifica ni reemplaza el NB02 real (5 capas, L2_avg=0.171%, ya verificado).
import sys, time, json
sys.path.insert(0, r"C:\roberto\Tesis_Maestria")
import numpy as np, torch
from scipy.stats import qmc, pearsonr
from src.models import PINN_2D_SIREN
from src.losses import pinn_loss_2d

SEED = 42
torch.manual_seed(SEED); torch.cuda.manual_seed(SEED); np.random.seed(SEED)
torch.backends.cudnn.deterministic = True
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

K = 2*np.pi
KX = KY = K/np.sqrt(2)
N_COLLOC, N_BOUNDARY = 3000, 300
NUM_LAYERS = 4   # unica diferencia vs NB02 real (5 capas)
HIDDEN_DIM = 128
OMEGA_0 = 1.0
LAMBDA_PHYS = 0.1
N_EPOCHS = 15000
PATIENCE = 800
MIN_DELTA = 1e-7

sampler = qmc.LatinHypercube(d=2, seed=SEED)
xy_colloc = torch.tensor(sampler.random(n=N_COLLOC), dtype=torch.float32).to(device)

t = np.linspace(0, 1, N_BOUNDARY)
x_bot = np.stack([t, np.zeros(N_BOUNDARY)], axis=1)
x_top = np.stack([t, np.ones(N_BOUNDARY)], axis=1)
x_lft = np.stack([np.zeros(N_BOUNDARY), t], axis=1)
x_rgt = np.stack([np.ones(N_BOUNDARY), t], axis=1)
xy_bc_np = np.vstack([x_bot, x_top, x_lft, x_rgt])
phase_bc = KX*xy_bc_np[:,0] + KY*xy_bc_np[:,1]
E_bc_np = np.stack([np.cos(phase_bc), np.sin(phase_bc)], axis=1)
xy_bc = torch.tensor(xy_bc_np, dtype=torch.float32).to(device)
E_bc = torch.tensor(E_bc_np, dtype=torch.float32).to(device)

model = PINN_2D_SIREN(hidden_dim=HIDDEN_DIM, num_layers=NUM_LAYERS, omega_0=OMEGA_0).to(device)
n_params = sum(p.numel() for p in model.parameters())
print(f"NB02 ablacion: {NUM_LAYERS} capas x {HIDDEN_DIM} | {n_params:,} parametros "
      f"(NB02 real: 5 capas, 66,690 parametros)")

opt = torch.optim.Adam(model.parameters(), lr=1e-3)
best_loss, best_state, sin_mejora = float('inf'), None, 0
t0 = time.time()
epoch_final = N_EPOCHS
for epoch in range(N_EPOCHS):
    opt.zero_grad()
    loss, loss_data, loss_physics = pinn_loss_2d(model, xy_colloc, xy_bc, E_bc, k=K, lambda_phys=LAMBDA_PHYS)
    loss.backward()
    opt.step()
    cl = loss.item()
    if cl < best_loss - MIN_DELTA:
        best_loss, sin_mejora = cl, 0
        best_state = {k_: v.clone() for k_, v in model.state_dict().items()}
    else:
        sin_mejora += 1
    if sin_mejora >= PATIENCE:
        epoch_final = epoch + 1
        break
model.load_state_dict(best_state)
t_adam = time.time() - t0

lbfgs = torch.optim.LBFGS(model.parameters(), lr=1.0, max_iter=1000, history_size=100, line_search_fn='strong_wolfe')
def closure():
    lbfgs.zero_grad()
    loss, _, _ = pinn_loss_2d(model, xy_colloc, xy_bc, E_bc, k=K, lambda_phys=LAMBDA_PHYS)
    loss.backward()
    return loss
t1 = time.time()
lbfgs.step(closure)
t_lbfgs = time.time() - t1

N_EVAL = 100
XX, YY = np.meshgrid(np.linspace(0,1,N_EVAL), np.linspace(0,1,N_EVAL))
xy_test = torch.tensor(np.stack([XX.ravel(), YY.ravel()], axis=1), dtype=torch.float32).to(device)
model.eval()
with torch.no_grad():
    E_pred = model(xy_test).cpu().numpy()
phase_test = KX*XX + KY*YY
E_real_exact, E_imag_exact = np.cos(phase_test), np.sin(phase_test)
def l2_rel(pred, exact):
    return np.linalg.norm(pred.ravel()-exact.ravel()) / np.linalg.norm(exact.ravel())
l2_real = l2_rel(E_pred[:,0].reshape(N_EVAL,N_EVAL), E_real_exact)
l2_imag = l2_rel(E_pred[:,1].reshape(N_EVAL,N_EVAL), E_imag_exact)
l2_avg = (l2_real + l2_imag) / 2 * 100

result = {
    'num_layers': NUM_LAYERS, 'hidden_dim': HIDDEN_DIM, 'n_params': n_params,
    'epoch_final': epoch_final, 'time_total_s': round(t_adam + t_lbfgs, 1),
    'l2_real_pct': round(float(l2_real*100), 4), 'l2_imag_pct': round(float(l2_imag*100), 4),
    'l2_avg_pct': round(float(l2_avg), 4),
}
out_path = r"C:\roberto\Tesis_Maestria\explorations\architecture_ablation_4layers\output\nb02_4layers.json"
with open(out_path, 'w') as f:
    json.dump(result, f, indent=2)
print(json.dumps(result, indent=2))
print()
print("NB02 real (5 capas, 66,690 params): L2_avg=0.171%")
print(f"NB02 ablacion (4 capas, {n_params:,} params): L2_avg={l2_avg:.4f}%")
