# NB02b — Bien puesto vs. mal puesto, con solución analítica

**Estado:** completado (2026-09-12) · **Script:** `nb02b_bvp_vs_cauchy.py` · **Salida:** `results/nb02b/bien_vs_mal_puesto/nb02b_bvp_vs_cauchy.json`

## Objetivo

Aislar **una sola variable** —el planteamiento del problema de contorno— para
sostener con evidencia por qué NB03 necesitó abandonar la formulación colocada
directa de NB02. Hasta ahora ese cambio se justificaba señalando que NB03 no
convergía, lo que no distingue entre «el método no alcanza» y «el problema no
está bien puesto».

## Diseño

Campo de prueba con solución cerrada de Helmholtz 2D:

```
E(x,y) = Σₙ cₙ·exp(i(kxₙ·x + kzₙ·y)),   n ∈ {−1,0,1}
kxₙ = 2πn,   kzₙ = 2π√(q−n²),   k = 2π√q,   q = 1.625
```

Los tres modos propagan, son exactamente periódicos en x sobre [0,1], y
cumplen `kxₙ² + kzₙ² = k²` de forma exacta.

**Elección de q.** `k² = 6.5π²` no es autovalor del laplaciano de Dirichlet en
[0,1]² (los autovalores son `π²(m²+n²)` con m,n enteros ≥ 1), y queda a `1.5π²`
de los vecinos `5π²` y `8π²`. Una primera versión usó `k² = 20π²` con
`20 = 2²+4²`: resonancia exacta, que vuelve **singular** el BVP de la celda A y
produjo un 58.8% de error sin que el método tuviera la culpa. El script ahora
verifica la no resonancia con `check_not_resonant()` antes de entrenar.

Tres celdas, misma geometría, misma solución exacta, misma arquitectura
SIREN 5×128, mismo `ω₀ = √q = 1.2748` (regla de NB01), misma semilla:

| Celda | Datos | Formulación | Clase de problema |
|---|---|---|---|
| A | Dirichlet en los 4 lados (300/lado) | directa (x,y)→E | BVP elíptico, bien puesto |
| B | Cauchy en y=0: valor **y** derivada | directa (x,y)→E | Cauchy elíptico, mal puesto |
| C | **idénticos a B** | modal, Cauchy dura | Cauchy regularizado |

B y C reciben exactamente la misma información. Cualquier diferencia es
atribuible únicamente a la representación.

## Resultados

| Celda | L² global | L² en y=0 → y=1 | Energía evanescente y=0 → y=1 |
|---|---|---|---|
| A | **0.0770%** | 0.034% → 0.036% | 0.0000% → 0.0000% |
| B | **45.1354%** | 0.209% → 73.717% | 0.0004% → 7.3922% (pico 13.2% en y≈0.8) |
| C | **0.1554%** | 0.000% → 0.406% | 0.0000% → 0.0000% |

## Hallazgos

1. **Con datos idénticos, la formulación modal es ~290× más precisa que la
   directa** (0.155% vs 45.1%). La diferencia no está en la información
   disponible ni en la red, sino en el espacio de funciones representable.

2. **B no falla por optimización.** Ajusta sus datos de Cauchy con 0.209% de
   error en y=0; el error crece a 73.7% en y=1. El fallo es de propagación, no
   de ajuste.

3. **El mecanismo es contaminación evanescente, como predice el análisis de
   Hadamard.** La solución física no tiene ninguna energía fuera del cono
   propagante `|kx| ≤ k`. La predicción de B sí la tiene, y crece
   aproximadamente de forma exponencial con y (cuatro órdenes de magnitud entre
   y=0 y el pico). La tasa ajustada, `d(ln E_ev)/dy ≈ 6.3`, queda por debajo de
   la teórica `2κ ≈ 19.4` del primer modo evanescente (m=2) por dos razones:
   la fracción está normalizada por la energía total, que también crece —por eso
   satura y decae tras el pico—, y la SIREN con ω₀=1.27 tiene contenido de alta
   frecuencia limitado, de modo que el κ efectivo realizado es menor.

4. **A y C tienen energía evanescente nula** (1e-7% y 0%). En C es nula *por
   construcción*: la base modal sólo contiene los modos propagantes. Ése es
   precisamente el truncamiento espectral que regulariza el problema.

5. El error de C crece con y de forma suave y acotada (0% → 0.406%): es
   acumulación del error de integración de la EDO, no inestabilidad.

## Uso en la tesis

Sostiene tres afirmaciones que hasta ahora no tenían evidencia controlada:

- El cambio de formulación en NB03 responde a la clase de problema, no a una
  limitación de la red.
- El truncamiento a modos propagantes es la regularización canónica del
  problema de Cauchy para Helmholtz, no una simplificación de conveniencia.
- Valida la maquinaria modal **contra una solución analítica**, no sólo contra
  el espectro angular — lo que atiende la objeción de que la referencia de NB03
  no es independiente del método.

## Verificaciones incluidas en el script

`check_not_resonant()` comprueba antes de entrenar que `k²` no sea autovalor de
Dirichlet, que todos los `kz` sean reales y que los modos cumplan Helmholtz.
