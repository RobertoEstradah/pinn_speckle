"""
measure_inference.py
Mide el tiempo de inferencia de PINN_2D_SIREN para 10,000 puntos (malla 100x100).
Usa el modelo guardado en results/models/nb02_helmholtz2d.pt
"""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import torch
import numpy as np
from src.models import PINN_2D_SIREN

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'models', 'nb02_helmholtz2d.pt')

# Cargar modelo
model = PINN_2D_SIREN.load(MODEL_PATH, hidden_dim=128, num_layers=5, omega_0=1.0, device=DEVICE)
model.eval()

# Malla 100x100 = 10,000 puntos
x_lin = np.linspace(0, 1, 100)
y_lin = np.linspace(0, 1, 100)
XX, YY = np.meshgrid(x_lin, y_lin)
XY = np.stack([XX.ravel(), YY.ravel()], axis=1).astype(np.float32)
xy_tensor = torch.tensor(XY, device=DEVICE)

# Warm-up (compilación JIT, primeros kernels CUDA)
with torch.no_grad():
    for _ in range(5):
        _ = model(xy_tensor)
if DEVICE == 'cuda':
    torch.cuda.synchronize()

# Medición (30 repeticiones para estabilidad)
N_REPS = 30
times = []
with torch.no_grad():
    for _ in range(N_REPS):
        if DEVICE == 'cuda':
            torch.cuda.synchronize()
        t0 = time.perf_counter()
        E_pred = model(xy_tensor)
        if DEVICE == 'cuda':
            torch.cuda.synchronize()
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1000)  # ms

times_arr = np.array(times)
mean_ms = times_arr.mean()
std_ms  = times_arr.std()
min_ms  = times_arr.min()

print(f"Device     : {DEVICE} ({torch.cuda.get_device_name(0) if DEVICE=='cuda' else 'CPU'})")
print(f"Model      : PINN_2D_SIREN 5x128 (66,690 params)")
print(f"Grid       : 100x100 = 10,000 puntos")
print(f"Repetitions: {N_REPS}")
print(f"Mean time  : {mean_ms:.3f} ms")
print(f"Std time   : {std_ms:.3f} ms")
print(f"Min time   : {min_ms:.3f} ms")
print(f"\nResultado para el paper: inferencia en {mean_ms:.1f} ms ± {std_ms:.1f} ms (GPU)")
