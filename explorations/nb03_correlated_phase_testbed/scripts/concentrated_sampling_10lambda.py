# Testbed: muestreo de colocacion concentrado cerca de y=0 (la frontera con
# la fase aleatoria), informado por Panagiotakopoulos et al. (2026). Se toma
# la MISMA frontera i.i.d. y el MISMO N_colloc=15000 y dominio=10 lambda que
# la prueba original de esta sesion (amp_mean=0.0679, sin colapso) para
# aislar el efecto de la distribucion de puntos: en vez de LHS uniforme en
# [0,1]^2, se deforma la coordenada y con y_new = y_lhs^P_EXP (P_EXP>1
# concentra la densidad de puntos cerca de y=0), manteniendo x sin cambios.
import sys, time, json
sys.path.insert(0, r"C:\roberto\Tesis_Maestria")
import numpy as np, torch
from scipy.stats import qmc
from src.models import PINN_2D_SIREN

SEED = 42
torch.manual_seed(SEED); torch.cuda.manual_seed(SEED); np.random.seed(SEED)
torch.backends.cudnn.deterministic = True
device = torch.device('cuda')

N_LAMBDA = 10
K = 2*np.pi*N_LAMBDA
OMEGA_0 = float(N_LAMBDA)
N_PHI = 256
N_COLLOC = 15000
LAMBDA_PHYS = 0.1
N_EPOCHS = 10000
PATIENCE_DATA = 2500
MIN_DELTA = 1e-7
P_EXP = 4.0   # y_new = y_lhs^P_EXP -- concentra puntos cerca de y=0

np.random.seed(SEED)
x_rough = np.linspace(0, 1, N_PHI)
phi_x = np.random.uniform(0, 2*np.pi, N_PHI)   # misma fase i.i.d. que la prueba original
E_rough_np = np.stack([np.cos(phi_x), np.sin(phi_x)], axis=1)
xy_rough_np = np.stack([x_rough, np.zeros(N_PHI)], axis=1)
xy_rough = torch.tensor(xy_rough_np, dtype=torch.float32).to(device)
E_rough = torch.tensor(E_rough_np, dtype=torch.float32).to(device)

sampler = qmc.LatinHypercube(d=2, seed=SEED)
lhs_pts = sampler.random(n=N_COLLOC)
lhs_pts[:, 1] = lhs_pts[:, 1] ** P_EXP   # deforma solo y, concentra cerca de 0
frac_near_boundary = np.mean(lhs_pts[:, 1] < 0.1)
print(f"N_colloc={N_COLLOC} | P_EXP={P_EXP} | "
      f"fraccion de puntos con y<0.1: {frac_near_boundary:.2%} "
      f"(uniforme seria ~10%)")
xy_colloc = torch.tensor(lhs_pts, dtype=torch.float32).to(device)

def residual_normalized(model, xy, k):
    xy = xy.clone().requires_grad_(True)
    E_out = model(xy)
    E_real, E_imag = E_out[:,0:1], E_out[:,1:2]
    ones = torch.ones_like(E_real)
    def laplacian(f):
        g = torch.autograd.grad(f, xy, grad_outputs=ones, create_graph=True)[0]
        fxx = torch.autograd.grad(g[:,0:1], xy, grad_outputs=ones, create_graph=True)[0][:,0:1]
        fyy = torch.autograd.grad(g[:,1:2], xy, grad_outputs=ones, create_graph=True)[0][:,1:2]
        return fxx + fyy
    k2 = float(k)**2
    return laplacian(E_real)/k2 + E_real, laplacian(E_imag)/k2 + E_imag

def losses(model, k):
    E_pred_rough = model(xy_rough)
    loss_data = torch.mean((E_pred_rough - E_rough)**2)
    res_real, res_imag = residual_normalized(model, xy_colloc, k)
    loss_phys = torch.mean(res_real**2) + torch.mean(res_imag**2)
    return loss_data, loss_phys

model = PINN_2D_SIREN(hidden_dim=128, num_layers=5, omega_0=OMEGA_0).to(device)
opt = torch.optim.Adam(model.parameters(), lr=1e-3)

best_data_loss, best_state, sin_mejora = float('inf'), None, 0
print(f"Muestreo concentrado: k={K:.2f} ({N_LAMBDA} lambda), omega_0={OMEGA_0}, "
      f"N_phi={N_PHI}, bordes libres, residuo/k^2")
t0 = time.time()
epoch_final = N_EPOCHS
for epoch in range(N_EPOCHS):
    opt.zero_grad()
    loss_data, loss_phys = losses(model, K)
    loss = loss_data + LAMBDA_PHYS * loss_phys
    loss.backward()
    opt.step()
    dl = loss_data.item()
    if dl < best_data_loss - MIN_DELTA:
        best_data_loss, sin_mejora = dl, 0
        best_state = {k_: v.clone() for k_, v in model.state_dict().items()}
    else:
        sin_mejora += 1
    if epoch % 500 == 0 or epoch == N_EPOCHS-1:
        print(f"  ep {epoch:5d} | L_datos={dl:.4e} | L_fisica(norm)={loss_phys.item():.4e} | "
              f"mejor={best_data_loss:.4e} | sin_mejora={sin_mejora} | t={time.time()-t0:.0f}s")
    if sin_mejora >= PATIENCE_DATA:
        epoch_final = epoch+1
        print(f"  early stop en {epoch_final}")
        break
model.load_state_dict(best_state)
t_adam = time.time()-t0

lbfgs = torch.optim.LBFGS(model.parameters(), lr=1.0, max_iter=1000,
                          history_size=100, line_search_fn='strong_wolfe')
def closure():
    lbfgs.zero_grad()
    loss_data, loss_phys = losses(model, K)
    loss = loss_data + LAMBDA_PHYS * loss_phys
    loss.backward()
    return loss
t1 = time.time()
lbfgs.step(closure)
t_lbfgs = time.time()-t1
print(f"Adam: {epoch_final}ep {t_adam:.0f}s | L-BFGS: {t_lbfgs:.0f}s")

N_EVAL = 100
XX, YY = np.meshgrid(np.linspace(0,1,N_EVAL), np.linspace(0,1,N_EVAL))
xy_test = torch.tensor(np.stack([XX.ravel(), YY.ravel()],axis=1), dtype=torch.float32).to(device)
model.eval()
with torch.no_grad():
    E_pred = model(xy_test).cpu().numpy()
E_real_field = E_pred[:,0].reshape(N_EVAL,N_EVAL)
E_imag_field = E_pred[:,1].reshape(N_EVAL,N_EVAL)
amp = np.sqrt(E_real_field**2 + E_imag_field**2)
amp_row_far = amp[-1,:]

loss_data_f, loss_phys_f = losses(model, K)
result = {
    'k': K, 'omega_0': OMEGA_0, 'N_phi': N_PHI, 'N_colloc': N_COLLOC,
    'P_EXP': P_EXP, 'frac_y_lt_0.1': round(float(frac_near_boundary),4),
    'adam_epochs': epoch_final, 'time_total_s': round(t_adam+t_lbfgs,1),
    'L_datos_final': loss_data_f.item(), 'L_fisica_norm_final': loss_phys_f.item(),
    'amp_mean': round(float(amp.mean()),4), 'amp_std': round(float(amp.std()),4),
    'amp_min': round(float(amp.min()),4), 'amp_max': round(float(amp.max()),4),
    'amp_mean_y1': round(float(amp_row_far.mean()),4),
}
out_path = r"C:\roberto\Tesis_Maestria\explorations\nb03_correlated_phase_testbed\output\concentrated_sampling_10lambda.json"
with open(out_path, 'w') as f:
    json.dump(result, f, indent=2)
print(); print(json.dumps(result, indent=2))
print()
print("Comparacion (mismo N_colloc=15000, dominio=10 lambda, fase i.i.d.):")
print("  LHS uniforme (prueba original):        amp_mean=0.0679")
print(f"  LHS concentrado cerca de y=0 (P={P_EXP}): amp_mean={amp.mean():.4f}")
