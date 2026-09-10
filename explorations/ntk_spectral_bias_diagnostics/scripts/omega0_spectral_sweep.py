# Barrido de omega_0 sobre el problema de NB01 (k=2pi, fresh runs cortos,
# NO se toca el modelo final de NB01 ni sus resultados reportados). Objetivo:
# mostrar cuantitativamente el sesgo espectral (Rahaman et al. 2019, ya
# citado en Cap2-Marcos.tex) que motiva la regla de calibracion omega_0=k/(2pi):
# un omega_0 mal calibrado desajusta el espectro nativo de la red SIREN
# respecto a la frecuencia objetivo k, degradando o rompiendo la convergencia.
# Documentado hasta ahora solo como hallazgo puntual (omega_0=30 explota);
# aqui se agrega un barrido con varios valores para verlo como tendencia.
import sys, time, json
sys.path.insert(0, r"C:\roberto\Tesis_Maestria")
import numpy as np, torch
from src.models import PINN_1D_SIREN

SEED = 42
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

K = 2*np.pi
N_COLLOC = 2000
N_EPOCHS = 3000   # barrido corto -- no busca convergencia final, solo la tendencia
OMEGA_0_VALUES = [1.0, 5.0, 15.0, 30.0]

x_bc_vals = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
E_bc_vals = np.cos(K * x_bc_vals)

results = {}
for omega_0 in OMEGA_0_VALUES:
    torch.manual_seed(SEED); torch.cuda.manual_seed(SEED); np.random.seed(SEED)
    x_colloc = torch.linspace(0, 1, N_COLLOC).reshape(-1, 1).to(device)
    x_bc = torch.tensor(x_bc_vals.reshape(-1, 1), dtype=torch.float32).to(device)
    E_bc = torch.tensor(E_bc_vals.reshape(-1, 1), dtype=torch.float32).to(device)

    model = PINN_1D_SIREN(hidden_dim=64, num_layers=5, omega_0=omega_0).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)

    def residual(model, x, k):
        x = x.clone().requires_grad_(True)
        E = model(x)
        dE = torch.autograd.grad(E, x, grad_outputs=torch.ones_like(E), create_graph=True)[0]
        d2E = torch.autograd.grad(dE, x, grad_outputs=torch.ones_like(dE), create_graph=True)[0]
        return d2E + k**2 * E

    loss_hist = []
    t0 = time.time()
    diverged = False
    for epoch in range(N_EPOCHS):
        opt.zero_grad()
        E_pred_bc = model(x_bc)
        loss_data = torch.mean((E_pred_bc - E_bc)**2)
        res = residual(model, x_colloc, K)
        loss_phys = torch.mean(res**2)
        loss = loss_data + 1.0 * loss_phys   # lambda_phys=1.0, igual que NB01 real
        if not torch.isfinite(loss):
            diverged = True
            break
        loss.backward()
        opt.step()
        loss_hist.append(loss.item())
    t_total = time.time() - t0

    final_loss = loss_hist[-1] if loss_hist else float('nan')
    results[str(omega_0)] = {
        'omega_0': omega_0,
        'diverged': diverged,
        'epochs_completed': len(loss_hist),
        'loss_inicial': loss_hist[0] if loss_hist else None,
        'loss_final': final_loss,
        'loss_hist_muestreado': loss_hist[::100],   # cada 100 epocas, para graficar liviano
        'time_s': round(t_total, 1),
    }
    estado = "DIVERGIO" if diverged else f"loss_final={final_loss:.3e}"
    print(f"omega_0={omega_0:5.1f} | {estado} | {len(loss_hist)}/{N_EPOCHS} epocas | {t_total:.1f}s")

out_path = r"C:\roberto\Tesis_Maestria\explorations\ntk_spectral_bias_diagnostics\output\omega0_sweep.json"
with open(out_path, 'w') as f:
    json.dump(results, f, indent=2)
print()
print("Regla de calibracion omega_0 ~ k/(2pi): con k=2pi, omega_0=1.0 es el calibrado.")
print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != 'loss_hist_muestreado'}
                   for k, v in results.items()}, indent=2))
