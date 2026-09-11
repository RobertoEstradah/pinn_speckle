# Ablacion adicional: NB01 (1D) con 4 capas ocultas en vez de 5, todo lo demas
# identico al protocolo real de NB01 (k=2pi, N_colloc=2000, 5 puntos de
# frontera conocidos, lambda_phys=1.0, Adam 15000 ep + L-BFGS 500/50, seed=42).
# NO modifica ni reemplaza el NB01 real (5 capas, L2=0.006%, ya verificado).
import sys, time, json
sys.path.insert(0, r"C:\roberto\Tesis_Maestria")
import numpy as np, torch
from scipy.stats import pearsonr
from src.models import PINN_1D_SIREN
from src.losses import pinn_loss_1d

SEED = 42
torch.manual_seed(SEED); torch.cuda.manual_seed(SEED); np.random.seed(SEED)
torch.backends.cudnn.deterministic = True
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

K = 2*np.pi
N_COLLOC = 2000
NUM_LAYERS = 4   # unica diferencia vs NB01 real (5 capas)
HIDDEN_DIM = 64
OMEGA_0 = 1.0
LAMBDA_PHYS = 1.0
N_EPOCHS = 15000
ADAM_STOP_THRESHOLD = 1e-4

x_colloc = torch.linspace(0, 1, N_COLLOC).reshape(-1, 1).to(device)
x_bc_vals = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
E_bc_vals = np.cos(K * x_bc_vals)
x_bc = torch.tensor(x_bc_vals.reshape(-1, 1), dtype=torch.float32).to(device)
E_bc = torch.tensor(E_bc_vals.reshape(-1, 1), dtype=torch.float32).to(device)

model = PINN_1D_SIREN(hidden_dim=HIDDEN_DIM, num_layers=NUM_LAYERS, omega_0=OMEGA_0).to(device)
n_params = sum(p.numel() for p in model.parameters())
print(f"NB01 ablacion: {NUM_LAYERS} capas x {HIDDEN_DIM} | {n_params:,} parametros "
      f"(NB01 real: 5 capas, 16,833 parametros)")

opt = torch.optim.Adam(model.parameters(), lr=1e-3)
best_loss = float('inf')
t0 = time.time()
epoch_final = N_EPOCHS
for epoch in range(N_EPOCHS):
    opt.zero_grad()
    loss, loss_data, loss_physics = pinn_loss_1d(model, x_colloc, x_bc, E_bc, k=K, lambda_phys=LAMBDA_PHYS)
    loss.backward()
    opt.step()
    cl = loss.item()
    if cl < best_loss:
        best_loss = cl
    if cl < ADAM_STOP_THRESHOLD:
        epoch_final = epoch + 1
        break
t_adam = time.time() - t0

lbfgs = torch.optim.LBFGS(model.parameters(), lr=1.0, max_iter=500, history_size=50, line_search_fn='strong_wolfe')
def closure():
    lbfgs.zero_grad()
    loss, _, _ = pinn_loss_1d(model, x_colloc, x_bc, E_bc, k=K, lambda_phys=LAMBDA_PHYS)
    loss.backward()
    return loss
t1 = time.time()
lbfgs.step(closure)
t_lbfgs = time.time() - t1

x_test = torch.linspace(0, 1, 1000).reshape(-1, 1).to(device)
with torch.no_grad():
    u_pred = model(x_test).cpu().numpy().flatten()
x_np = x_test.cpu().numpy().flatten()
u_exact = np.cos(K * x_np)
l2_error = np.linalg.norm(u_pred - u_exact) / np.linalg.norm(u_exact)
r2 = 1 - np.sum((u_pred - u_exact)**2) / np.sum((u_exact - np.mean(u_exact))**2)
corr, _ = pearsonr(u_pred, u_exact)

result = {
    'num_layers': NUM_LAYERS, 'hidden_dim': HIDDEN_DIM, 'n_params': n_params,
    'epoch_final': epoch_final, 'time_total_s': round(t_adam + t_lbfgs, 1),
    'l2_error_pct': round(float(l2_error*100), 4), 'r2': round(float(r2), 6),
    'pearson': round(float(corr), 6),
}
out_path = r"C:\roberto\Tesis_Maestria\explorations\architecture_ablation_4layers\output\nb01_4layers.json"
with open(out_path, 'w') as f:
    json.dump(result, f, indent=2)
print(json.dumps(result, indent=2))
print()
print("NB01 real (5 capas, 16,833 params): L2=0.006%, R2=1.000000")
print(f"NB01 ablacion (4 capas, {n_params:,} params): L2={l2_error*100:.4f}%, R2={r2:.6f}")
