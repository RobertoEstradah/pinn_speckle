"""
build_nb04_speckle_distancias.py
Construye notebooks/04_speckle_distancias_estadistico.ipynb a partir de la
logica ya verificada en scripts/experiments/run_speckle_distances.py.
Genera el .ipynb con celdas markdown+codigo (sin ejecutar) via nbformat;
la ejecucion real se hace despues con:
    jupyter nbconvert --to notebook --execute --inplace notebooks/04_speckle_distancias_estadistico.ipynb
"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

cells.append(nbf.v4.new_markdown_cell(
"""# Speckle Óptico a Distancias Reales — Generación Estadística (Goodman)
### Proyecto: Simulación Acelerada de Speckle Óptico
**Roberto Hernández Estrada** | Maestría en Ciencias de la Computación — UJAT
**Director:** Dr. José Adán Hernández Nolasco

---

Complementa a NB03: genera imágenes del patrón de speckle a **10 distancias físicas
reales** (2–20 cm, paso 2cm), acordado con el asesor en la reunión del 2026-09-08
("máximo unos 20cm... 10 lambdas... busca en internet qué distancia manejan
[los experimentos reales]").

**Importante — qué es y qué NO es este notebook:**
- **NO** es una propagación de onda (no resuelve la ecuación de Helmholtz, no usa
  el PINN de NB03). Es una **generación estadística**: se construye directamente
  un campo con las propiedades que la teoría de Goodman predice (contraste C=1,
  tamaño de grano = λz/D), sin derivarlas de la física de difracción.
- Se descartó la propagación de onda exacta (método del espectro angular) tras
  comprobar que, sin una apertura con borde finito (margen oscuro alrededor de
  la zona iluminada), la FFT trata el campo como periódico infinito y elimina el
  mecanismo de difracción que genera el grano — arreglarlo bien habría requerido
  ~16× más puntos de cómputo por esta única figura ilustrativa.
- Es una figura de **contexto/ilustración**, no un resultado que sostenga una
  hipótesis de tesis — debe citarse como "generación estadística (Goodman)", no
  como "simulación PINN" ni "propagación física exacta"."""
))

cells.append(nbf.v4.new_markdown_cell(
"""## 0. Imports y configuración"""
))

cells.append(nbf.v4.new_code_cell(
"""import os, json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import Image, display

import sys
sys.path.insert(0, os.path.join('..'))
from src.utils import get_figures_dir

LAMBDA = 638e-9       # laser diodo rojo, m (CLAUDE.md)
D = 2e-3              # ancho de iluminacion, m (Andres-Zarate/Hernandez-Nolasco 2019: aberturas ~1-1.5mm de radio)
SEED = 42             # misma semilla global del proyecto
DISTANCES_CM = list(range(2, 21, 2))  # 2,4,...,20 cm (10 distancias, acordadas con el asesor)
WINDOW_M = D
N_GRID = 1024

IMG_DIR = get_figures_dir() / 'speckle_distances'
IMG_DIR.mkdir(parents=True, exist_ok=True)
print('Figuras en:', IMG_DIR)"""
))

cells.append(nbf.v4.new_markdown_cell(
"""## 1. Tamaño de grano teórico (Goodman, 2007)

$$\\text{grano} \\approx \\frac{\\lambda z}{D}$$

donde $D$ es el ancho de la zona iluminada y $z$ la distancia de propagación.
Esta es la misma fórmula ya citada en `Cap2-Marcos.tex` / `goodman2007speckle` —
aquí se usa para *fijar* el ancho del filtro que genera el campo, no para
validar una simulación de propagación."""
))

cells.append(nbf.v4.new_code_cell(
"""def grain_size_theoretical(z_m, D_m=D, wavelength=LAMBDA):
    \"\"\"Tamano de grano de speckle objetivo, Goodman (2007): ~ lambda*z / D.\"\"\"
    return wavelength * z_m / D_m

for z_cm in DISTANCES_CM:
    g = grain_size_theoretical(z_cm * 1e-2)
    print(f'  z={z_cm:2d}cm  grano teorico = {g*1e6:.2f} um')"""
))

cells.append(nbf.v4.new_markdown_cell(
"""## 2. Generación del campo de speckle

Ruido blanco complejo gaussiano ($a+ib$, $a,b\\sim\\mathcal{N}(0,1)$ i.i.d.) filtrado
en frecuencia con un filtro gaussiano cuyo ancho fija el grano deseado. El
filtrado lineal de ruido gaussiano produce un campo gaussiano circular (Goodman,
2007) — por construcción, $I=|u|^2$ sigue la exponencial negativa y el
contraste $C=\\sigma_I/\\langle I\\rangle = 1$, el mismo criterio de
`Cap2-Marcos.tex` ec. `contraste`."""
))

cells.append(nbf.v4.new_code_cell(
"""def generate_speckle(grain_size_m, window_m=WINDOW_M, n=N_GRID, seed=SEED):
    \"\"\"Campo de speckle generado estadisticamente (ver celda markdown de arriba).\"\"\"
    rng = np.random.default_rng(seed)
    g = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    dx = window_m / n
    fx = np.fft.fftfreq(n, d=dx)
    FX, FY = np.meshgrid(fx, fx)
    sigma_f = 1.0 / (2 * np.pi * grain_size_m)  # par de Fourier de un kernel gaussiano
    H = np.exp(-(FX**2 + FY**2) / (2 * sigma_f**2))
    u = np.fft.ifft2(np.fft.fft2(g) * H)
    return np.abs(u) ** 2"""
))

cells.append(nbf.v4.new_markdown_cell(
"""## 3. Generar las 10 distancias, guardar imágenes y verificar contraste"""
))

cells.append(nbf.v4.new_code_cell(
"""dx = WINDOW_M / N_GRID
results_log = []
frames = []

for z_cm in DISTANCES_CM:
    z_m = z_cm * 1e-2
    grain = grain_size_theoretical(z_m)
    I = generate_speckle(grain)
    I_norm = I / I.mean()
    contrast = I_norm.std() / I_norm.mean()
    pixels_per_grain = grain / dx

    results_log.append({
        'z_cm': z_cm, 'grain_size_um': round(grain * 1e6, 3),
        'pixels_per_grain': round(pixels_per_grain, 2),
        'contrast_C': round(float(contrast), 4),
    })

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(I_norm, cmap='gray', interpolation='nearest',
              vmin=0, vmax=np.percentile(I_norm, 99))
    ax.set_title(f'z={z_cm}cm  (C={contrast:.3f}, grano={grain*1e6:.1f}um)')
    ax.axis('off')
    fig.tight_layout()
    fig.savefig(IMG_DIR / f'z{z_cm}cm.png', dpi=120)
    plt.close(fig)
    frames.append(I_norm)
    print(f'  z={z_cm}cm  C={contrast:.3f}  grano={grain*1e6:.2f}um  px/grano={pixels_per_grain:.2f}')"""
))

cells.append(nbf.v4.new_markdown_cell(
"""## 4. Vista previa — grano creciendo con la distancia

Se espera que el grano se vea más fino a 2cm y más grueso a 20cm — es la
"dinámica de difracción" que pidió Adán poder visualizar."""
))

cells.append(nbf.v4.new_code_cell(
"""fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for ax, idx in zip(axes, [0, 4, 9]):  # z=2cm, 10cm, 20cm
    ax.imshow(frames[idx], cmap='gray', interpolation='nearest',
              vmin=0, vmax=np.percentile(frames[idx], 99))
    ax.set_title(f'z={DISTANCES_CM[idx]}cm')
    ax.axis('off')
fig.tight_layout()
plt.show()"""
))

cells.append(nbf.v4.new_markdown_cell(
"""## 5. Animación (GIF) — las 10 distancias en secuencia"""
))

cells.append(nbf.v4.new_code_cell(
"""fig, ax = plt.subplots(figsize=(5, 5))
im = ax.imshow(frames[0], cmap='gray', interpolation='nearest',
                vmin=0, vmax=np.percentile(frames[0], 99))
title = ax.set_title(f'z={DISTANCES_CM[0]}cm')
ax.axis('off')

def update(i):
    im.set_data(frames[i])
    im.set_clim(0, np.percentile(frames[i], 99))
    title.set_text(f'z={DISTANCES_CM[i]}cm')
    return im, title

ani = animation.FuncAnimation(fig, update, frames=len(frames), interval=600)
gif_path = IMG_DIR / 'animacion.gif'
ani.save(gif_path, writer=animation.PillowWriter(fps=2))
plt.close(fig)
print('Animacion guardada:', gif_path)
display(Image(filename=str(gif_path)))"""
))

cells.append(nbf.v4.new_markdown_cell(
"""## 6. Guardar parámetros y resultados"""
))

cells.append(nbf.v4.new_code_cell(
"""out_json = os.path.join('..', 'results', 'speckle_distances.json')
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump({
        'lambda_m': LAMBDA, 'D_m': D, 'window_m': WINDOW_M, 'n_grid': N_GRID,
        'seed': SEED, 'distances_cm': DISTANCES_CM,
        'metodo': 'estadistico (ruido blanco gaussiano filtrado), NO propagacion de onda exacta',
        'resultados': results_log,
    }, f, indent=2, ensure_ascii=False)
print('Guardado:', out_json)"""
))

cells.append(nbf.v4.new_markdown_cell(
"""## ¿Qué sigue?

- Confirmar con Adán si esta ilustración (estadística) es suficiente para el
  avance, o si se justifica invertir el tiempo de cómputo en la propagación de
  onda exacta (ver discusión en el docstring de
  `scripts/experiments/run_speckle_distances.py`, versión previa a este notebook).
- Aclarar con Adán la reconciliación de escala: tu dominio PINN actual
  (NB01–03) está normalizado a ≈1λ, mientras que estas distancias reales son
  de cm — son dos ejercicios distintos, no directamente comparables sin
  reescalar el dominio del PINN."""
))

nb['cells'] = cells
nb['metadata'] = {
    'kernelspec': {'display_name': 'Python 3 (pinn_speckle)', 'language': 'python', 'name': 'python3'},
    'language_info': {'name': 'python', 'version': '3.11'},
}

import os
out_path = os.path.join(os.path.dirname(__file__), '..', '..', 'notebooks', '04_speckle_distancias_estadistico.ipynb')
with open(out_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print('Notebook creado:', out_path)
