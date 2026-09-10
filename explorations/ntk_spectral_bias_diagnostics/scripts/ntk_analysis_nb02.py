# Analisis NTK (Wang et al. 2022, ya citado en Cap2-Marcos.tex) sobre el
# modelo FINAL de NB02 ya entrenado (results/models/nb02_helmholtz2d_gpu.pt).
# No se reentrena nada -- se cargan los pesos guardados y solo se evalua.
#
# Idea: comparar el espectro de autovalores del kernel tangente neuronal (NTK)
# del termino de datos (frontera) contra el del termino de fisica (residuo de
# Helmholtz). Wang et al. argumentan que un termino con autovalores NTK mucho
# mas grandes converge (y domina el gradiente) mas rapido que el otro -- esto
# es la explicacion teorica de por que lambda_fis=0.1 (no 1.0) fue necesario
# en la ablacion de NB02 (Cap4-Resultados.tex, Seccion de ablacion).
import sys, json
sys.path.insert(0, r"C:\roberto\Tesis_Maestria")
import numpy as np, torch
from scipy.stats import qmc
from src.models import PINN_2D_SIREN
from src.utils import load_model

SEED = 42
torch.manual_seed(SEED); np.random.seed(SEED)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

K = 2*np.pi
KX = KY = K/np.sqrt(2)
N_NTK = 80   # puntos muestreados por termino -- suficiente para el espectro, barato en memoria

model = PINN_2D_SIREN(hidden_dim=128, num_layers=5, omega_0=1.0).to(device)
model = load_model(model, 'nb02_helmholtz2d_gpu', notebook_dir=r"C:\roberto\Tesis_Maestria\notebooks", device=device)
model.eval()
params = [p for p in model.parameters() if p.requires_grad]
n_params = sum(p.numel() for p in params)
print(f"Modelo NB02 cargado: {n_params:,} parametros")

def flat_grad(scalar_output, params):
    grads = torch.autograd.grad(scalar_output, params, retain_graph=True, create_graph=False)
    return torch.cat([g.reshape(-1) for g in grads])

def jacobian_scalar_field(fn, xy_points, params):
    """Jacobiano (N_puntos x N_params) de un campo escalar fn(xy) respecto a params."""
    J = torch.zeros(len(xy_points), n_params)
    for i in range(len(xy_points)):
        xy_i = xy_points[i:i+1].clone().requires_grad_(True)
        out = fn(xy_i)
        J[i] = flat_grad(out.squeeze(), params).detach().cpu()
    return J

# ── Termino de datos: E_real en puntos de frontera (4 bordes, onda plana) ──
t = np.linspace(0, 1, N_NTK // 4)
x_bot = np.stack([t, np.zeros_like(t)], axis=1)
x_top = np.stack([t, np.ones_like(t)], axis=1)
x_lft = np.stack([np.zeros_like(t), t], axis=1)
x_rgt = np.stack([np.ones_like(t), t], axis=1)
xy_bc_np = np.vstack([x_bot, x_top, x_lft, x_rgt])
xy_bc = torch.tensor(xy_bc_np, dtype=torch.float32).to(device)

def data_fn(xy):
    return model(xy)[:, 0:1]   # E_real como representante del termino de datos

J_data = jacobian_scalar_field(data_fn, xy_bc, params)

# ── Termino de fisica: residuo real de Helmholtz en puntos de colocacion LHS ──
sampler = qmc.LatinHypercube(d=2, seed=SEED)
xy_colloc_np = sampler.random(n=N_NTK)
xy_colloc = torch.tensor(xy_colloc_np, dtype=torch.float32).to(device)

def phys_fn(xy):
    xy = xy.clone().requires_grad_(True)
    E_out = model(xy)
    E_real = E_out[:, 0:1]
    ones = torch.ones_like(E_real)
    g = torch.autograd.grad(E_real, xy, grad_outputs=ones, create_graph=True)[0]
    fxx = torch.autograd.grad(g[:,0:1], xy, grad_outputs=ones, create_graph=True)[0][:,0:1]
    fyy = torch.autograd.grad(g[:,1:2], xy, grad_outputs=ones, create_graph=True)[0][:,1:2]
    return fxx + fyy + K**2 * E_real

J_phys = torch.zeros(N_NTK, n_params)
for i in range(N_NTK):
    xy_i = xy_colloc[i:i+1]
    out = phys_fn(xy_i)
    J_phys[i] = flat_grad(out.squeeze(), params).detach().cpu()

# ── NTK = J J^T, autovalores ──
NTK_data = (J_data @ J_data.T).numpy()
NTK_phys = (J_phys @ J_phys.T).numpy()
eig_data = np.sort(np.linalg.eigvalsh(NTK_data))[::-1]
eig_phys = np.sort(np.linalg.eigvalsh(NTK_phys))[::-1]

trace_data = float(np.trace(NTK_data))
trace_phys = float(np.trace(NTK_phys))

result = {
    'n_params': n_params, 'N_NTK': N_NTK, 'k': K,
    'trace_data': trace_data, 'trace_phys': trace_phys,
    'ratio_phys_sobre_data': trace_phys / trace_data,
    'max_eig_data': float(eig_data[0]), 'max_eig_phys': float(eig_phys[0]),
    'eig_data_top10': eig_data[:10].tolist(),
    'eig_phys_top10': eig_phys[:10].tolist(),
}
out_path = r"C:\roberto\Tesis_Maestria\explorations\ntk_spectral_bias_diagnostics\output\ntk_nb02.json"
with open(out_path, 'w') as f:
    json.dump(result, f, indent=2)
print(json.dumps(result, indent=2))
print()
print(f"Traza NTK fisica / Traza NTK datos = {result['ratio_phys_sobre_data']:.2f}x")
print("Si este ratio es >> 1, el termino de fisica domina el gradiente en igualdad")
print("de peso (lambda=1.0) -- consistente con por que lambda_fis=0.1 fue necesario.")
