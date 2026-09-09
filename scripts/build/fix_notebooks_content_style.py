"""
fix_notebooks_content_style.py
Aplica correcciones de contenido (nombres de archivo obsoletos, contradiccion
E=0 vs libre en NB03, sobre-promesa en NB02, factor xN sin matiz) y limpieza
de estilo (guiones largos, emojis) a NB01, NB02, NB03 y NB05.
Uso unico -- no se re-ejecuta despues de aplicado.
"""
import json, re, glob, os

os.chdir(os.path.join(os.path.dirname(__file__), '..', '..', 'notebooks'))

EMOJI_RE = re.compile('[✅❌\U0001F504\U0001F51C⚠️]\\s?')

def clean_mechanical(s):
    s = s.replace('—', '-')
    s = EMOJI_RE.sub('', s)
    return s

# ---- Reemplazos de contenido exactos, por notebook ----------------------------

FILENAME_FIXES = [
    ('01_teoria_pinns_completo.ipynb', '01_pinn_helmholtz_1d_validation.ipynb'),
    ('01_helmholtz_1D_tesis.ipynb', '01_pinn_helmholtz_1d_validation.ipynb'),
    ('02_helmholtz_2D_tesis.ipynb', '02_pinn_helmholtz_2d_complex_field.ipynb'),
    ('02_helmholtz_2D.ipynb', '02_pinn_helmholtz_2d_complex_field.ipynb'),
    ('03_speckle_tesis.ipynb', '03_pinn_optical_speckle_simulation.ipynb'),
    ('03_speckle.ipynb', '03_pinn_optical_speckle_simulation.ipynb'),
]

ROADMAP_OLD_BLOCK_MD = """| `04_benchmark.ipynb` | PINN vs FEniCSx (Speed-up Factor) | Pendiente |"""
ROADMAP_NEW_BLOCK_MD = """| `04_benchmark.ipynb` | PINN vs FEniCSx (Speed-up Factor) | Pendiente |
| `05_speckle_distancias_estadistico.ipynb` | Speckle a distancias reales (2-20cm), generacion estadistica de Goodman | Completado |

Nota: el trabajo de medio inhomogeneo/lente (antes planeado como notebooks 05-07)
quedo pospuesto sin numeracion confirmada, segun lo acordado con el asesor
(reunion 2026-09-08) -- ver memoria de proyecto. No se lista aqui hasta que
tenga un plan de desarrollo activo."""

ROADMAP_OLD_TABLE_ESTADO = """| Notebook | Contenido | Estado |
|---|---|---|
| `01_helmholtz_1D_tesis.ipynb` | Helmholtz 1D - SIREN ω₀=1.0, 5×64 | Error L2 = 0.006% |
| `02_helmholtz_2D_tesis.ipynb` | Helmholtz 2D - campo complejo, LHS, 5×128 | Error L2 = 0.171% |
| **`03_speckle_tesis.ipynb`** | **Speckle - frontera rugosa φ~U(0,2π), C ≈ 1** | Completado |
| `04_benchmark.ipynb` | PINN vs FEniCSx - Speed-up Factor | Pendiente |
| `05_inhomogeneo_1D.ipynb` | Inhomogéneo 1D - n(x) gradiente lineal | Pendiente |
| `06_inhomogeneo_2D.ipynb` | Inhomogéneo 2D - perfiles GRIN y bicapa | Pendiente |
| `07_speckle_grin.ipynb` | Speckle en material GRIN - publicable | Pendiente |"""

ROADMAP_NEW_TABLE_ESTADO = """| Notebook | Contenido | Estado |
|---|---|---|
| `01_pinn_helmholtz_1d_validation.ipynb` | Helmholtz 1D - SIREN ω₀=1.0, 5×64 | Error L2 = 0.006% |
| `02_pinn_helmholtz_2d_complex_field.ipynb` | Helmholtz 2D - campo complejo, LHS, 5×128 | Error L2 = 0.171% |
| **`03_pinn_optical_speckle_simulation.ipynb`** | **Speckle - frontera rugosa φ~U(0,2π), C ≈ 1** | Completado |
| `04_benchmark.ipynb` | PINN vs FEniCSx - Speed-up Factor | Pendiente |
| `05_speckle_distancias_estadistico.ipynb` | Speckle a distancias reales (2-20cm), generacion estadistica de Goodman | Completado |

Nota: el trabajo de medio inhomogeneo/lente (antes planeado como notebooks 05-07)
quedo pospuesto sin numeracion confirmada, segun lo acordado con el asesor
(reunion 2026-09-08). No se lista aqui hasta que tenga un plan de desarrollo activo."""

CAVEAT_NOTE = ("\n\n> **Nota de comparabilidad:** Schoder y Kraxberger (2024) resuelven "
               "Helmholtz 3D (acustica) con activacion tanh contra una malla FEM de "
               "referencia -- dominio fisico, dimensionalidad y arquitectura distintos "
               "a este trabajo (1D/2D optico, SIREN, solucion analitica exacta). El "
               "factor xN se reporta como contexto de la literatura, no como linea "
               "base de comparacion cuantitativa directa (ver `Cap2-Marcos.tex`, "
               "seccion \"Literatura relacionada\").")

def fix_nb01(nb):
    for cell in nb['cells']:
        src = ''.join(cell['source'])
        orig = src
        for old, new in FILENAME_FIXES:
            src = src.replace(old, new)
        if ROADMAP_OLD_TABLE_ESTADO in src:
            src = src.replace(ROADMAP_OLD_TABLE_ESTADO, ROADMAP_NEW_TABLE_ESTADO)
        if '| Referencia Schoder & Kraxberger (2024) | 2.490% | Superado ×415 |' in src:
            src = src.replace(
                '| Referencia Schoder & Kraxberger (2024) | 2.490% | Superado ×415 |',
                '| Referencia Schoder & Kraxberger (2024)\\* | 2.490% | ×415 (ver nota) |'
            )
            src = src.rstrip('\n') + CAVEAT_NOTE + '\n'
        if src != orig:
            cell['source'] = src.splitlines(keepends=True)
    return nb

def fix_nb02(nb):
    for cell in nb['cells']:
        src = ''.join(cell['source'])
        orig = src
        for old, new in FILENAME_FIXES:
            src = src.replace(old, new)
        src = src.replace(
            '**Resultado esperado esta versión:** Error L2 < 0.1%',
            '**Resultado esperado esta versión:** reducción sustancial respecto al '
            '0.436% original mediante mayor capacidad de red (resultado obtenido: 0.171%)'
        )
        if '| Notebook | Contenido | Estado |' in src and '04_benchmark.ipynb' in src:
            # tabla "Estado del proyecto" de NB02 (formato distinto al de NB01/NB03)
            src = src.replace(
                '| `04_benchmark.ipynb` | PINN vs FEniCSx - Speed-up Factor | Pendiente |',
                '| `04_benchmark.ipynb` | PINN vs FEniCSx - Speed-up Factor | Pendiente |\n'
                '| `05_speckle_distancias_estadistico.ipynb` | Speckle a distancias reales '
                '(2-20cm), generación estadística de Goodman | Completado |'
            )
        if '| vs Schoder 2024 | ×415 mejor | ×11.2 mejor |' in src:
            src = src.replace(
                '| vs Schoder 2024 | ×415 mejor | ×11.2 mejor |',
                '| vs Schoder 2024\\* | ×415 mejor | ×11.2 mejor |'
            )
            src = src.rstrip('\n') + CAVEAT_NOTE + '\n'
        if src != orig:
            cell['source'] = src.splitlines(keepends=True)
    return nb

def fix_nb03(nb):
    for cell in nb['cells']:
        src = ''.join(cell['source'])
        orig = src
        for old, new in FILENAME_FIXES:
            src = src.replace(old, new)
        src = src.replace(
            '| Bordes restantes | Onda plana exacta | Dirichlet homogéneo ($E = 0$) |',
            '| Bordes restantes | Onda plana exacta | Libres (sin condición impuesta) |'
        )
        src = src.replace(
            '| Bordes restantes con E=0 son suficientes | Para speckle estadístico el confinamiento no altera la distribución interior |',
            '| Bordes restantes libres (sin condición impuesta) no impiden el speckle | La EDP + LHS interior + frontera rugosa en y=0 determinan el campo sin necesidad de confinar el resto |'
        )
        src = src.replace(
            '| Condición de frontera | 5 puntos cos(kx) | Onda plana 4 bordes | Fase rugosa y=0, E=0 resto |',
            '| Condición de frontera | 5 puntos cos(kx) | Onda plana 4 bordes | Fase rugosa y=0, resto libre |'
        )
        if ROADMAP_OLD_TABLE_ESTADO in src:
            src = src.replace(ROADMAP_OLD_TABLE_ESTADO, ROADMAP_NEW_TABLE_ESTADO)
        if src != orig:
            cell['source'] = src.splitlines(keepends=True)
    return nb

FIXERS = {
    '01_pinn_helmholtz_1d_validation.ipynb': fix_nb01,
    '02_pinn_helmholtz_2d_complex_field.ipynb': fix_nb02,
    '03_pinn_optical_speckle_simulation.ipynb': fix_nb03,
}

for path in ['01_pinn_helmholtz_1d_validation.ipynb',
             '02_pinn_helmholtz_2d_complex_field.ipynb',
             '03_pinn_optical_speckle_simulation.ipynb',
             '05_speckle_distancias_estadistico.ipynb']:
    with open(path, encoding='utf-8') as f:
        nb = json.load(f)

    if path in FIXERS:
        nb = FIXERS[path](nb)

    changed_cells = 0
    for cell in nb['cells']:
        src = ''.join(cell['source'])
        cleaned = clean_mechanical(src)
        if cleaned != src:
            cell['source'] = cleaned.splitlines(keepends=True)
            changed_cells += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print(f'{path}: {changed_cells} celdas con limpieza mecanica aplicada')
