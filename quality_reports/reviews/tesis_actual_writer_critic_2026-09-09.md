# Revisión writer-critic — tesis/Tesis_Actual

**Fecha:** 2026-09-09 · **Severidad:** ALTA (fase de ejecución) · **Score:** 0/100 (piso; deducciones crudas −168)

El score está en el piso igual que la ronda anterior, pero el documento mejoró de forma
real: 14 hallazgos de la revisión de agosto están corregidos, incluidos los dos bloqueadores
de compilación, los cuatro desajustes numéricos, la violación INV-12 y el sobrerreclamo
×415/×11.2. El cero lo domina **un hallazgo científico nuevo (C-1)** que la revisión anterior
no podía ver, más una regresión introducida por una corrección (C-3) y dos huecos
estructurales nunca atendidos (C-6, C-14).

---

## C-1 (CRÍTICO). El campo de NB03 colapsó: la condición de frontera nunca se ajustó

**Verificado de forma independiente contra la salida almacenada del propio notebook**
(`notebooks/03_pinn_optical_speckle_simulation.ipynb`, celda 14):

```
E_real : min=-0.0280, max=0.0432
E_imag : min=-0.0364, max=0.0374
I=|E|² : min=0.0000, max=0.0032
⟨I⟩    : 0.0005
σ_I    : 0.0005
```

`Cap3-Modelo.tex:59` impone `E(x,0) = e^{iψ(x)}`, es decir `|E| = 1` en la frontera.
El campo entrenado tiene `|E| ≲ 0.05` en todo el dominio: alrededor del 4 % de la amplitud
impuesta, y `⟨I⟩ = 0.0005` frente a `|E|² = 1` en `y = 0`.

Evidencia concurrente en las figuras:

- `resultados_speckle_nb03.png`, Paneles A y B: `E_real` y `E_imag` se ven en blanco contra
  una barra de color de ±1.0.
- Panel I: la **pérdida de datos (BC, azul) queda plana en ≈0.5 durante las 8 000 épocas**;
  nunca baja. Para un MSE promediado sobre partes real e imaginaria contra objetivos
  `cos ψ` / `sin ψ`, el campo `E ≡ 0` da exactamente 0.5. La frontera nunca se ajustó.
- Panel D: cuatro o cinco lóbulos suaves, no un patrón granular.
- `estadistica_speckle_nb03.png`, Panel B: `σ = 0.023`. Panel C: el diagrama de fase
  `E_real` vs `E_imag` es filamentoso y anisótropo, no una nube gaussiana circular. La
  precondición de Goodman (`Cap2-Marcos.tex:55-59`) queda contradicha por la figura misma.

El contraste `C = σ_I/⟨I⟩` es **invariante de escala**, así que `C = 1.0253` es
perfectamente compatible con un campo colapsado. No se reporta en ninguna parte una métrica
sensible a la amplitud: ni `L_datos` de NB03, ni error de ajuste en frontera, ni `⟨I⟩`.
`Cap4-Resultados.tex:336-339` toma `C` como confirmación de speckle completamente
desarrollado; no lo es.

Dato concurrente: `Cap4:319` reporta L-BFGS **8 / 1 000** iteraciones. Una terminación a las
8 iteraciones es señal de fallo, y `CLAUDE.md` documenta ese síntoma exacto en su tabla de
problemas resueltos. Es coherente con el mismo colapso.

**Consecuencia:** el capítulo de speckle no necesita reescritura, necesita re-ejecución o una
re-validación que demuestre que la frontera sí se satisface. Todo lo demás está aguas abajo
de esta respuesta.

## C-2 (CRÍTICO). Entrada de ablación fabricada, y nota fabricada

`Cap4-Resultados.tex:249` reporta `$>5.0$` para λ=1.0. `results/ablation_lambda.json`
registra `"l2_avg": null, "converged": false`. Nunca se midió ningún error.

La nota que lo acompaña (`Cap4:254-256`) es una **segunda fabricación independiente**:

> *"No converge indica que Adam no alcanzó la condición de parada antes de las 15 000 épocas
> con ε_L2 < 5 %."*

El JSON dice: `"Crash CUDA nivel-C; gradiente explota con lambda=1.0 (float32)"`, corroborado
por `CLAUDE.md`. La corrida **se cayó**; no llegó a 15 000 épocas ni falló un criterio de
parada. La nota describe un experimento que no ocurrió.

El propio `ablation_lambda.json` arrastra la cadena `"Documentado como >5%."` — la fabricación
es anterior al manuscrito y hay que corregirla también en el JSON.

Propaga a: `paper/fuente_validacion1D2D/sections/03_metodologia.tex:106` y al paper de CyS.

## C-3 (CRÍTICO). Las cinco leyendas de figura de Cap4 describen figuras que ya no existen

Las figuras se regeneraron para corregir INV-12; las leyendas no se actualizaron.

| Leyenda | Dice | La figura muestra |
|---|---|---|
| `Cap4:92-96` | *"curva de pérdida total... caída abrupta en la época 15 000"* | `metricas_adicionales_1d.png` **no tiene curva de pérdida**. A/B/C = histograma de error, error puntual relativo, dispersión PINN-vs-exacta |
| `Cap4:185-190` | *"Panel izquierdo: curva de pérdida... errores en las esquinas del dominio"* | **No hay curva de pérdida**; son 6 paneles (A–F). D/E muestran error en **bandas antidiagonales** (donde la solución exacta cruza cero), no en las esquinas. Tres afirmaciones falsas en una leyenda |
| `Cap4:169-175` | *"Fila superior: analítica. Fila inferior: PINN"* | Rejilla 3×3: fila 1 = `E_real` exacta/PINN/error; fila 2 = igual para `E_imag`; fila 3 = intensidad, puntos LHS, curvas de pérdida |
| `Cap4:78-82` | *"Panel izquierdo... Panel derecho"* | Panel A ocupa todo el ancho superior; B y C van debajo. Panel C no se menciona |
| `Cap4:389-392` | *"Panel derecho: CDF"* | 6 paneles (A–F); la CDF es el Panel **A**, arriba a la izquierda |

## C-4 (CRÍTICO). La hipótesis (i) se declara verificada "en todos los casos"

`Cap1-Generalidades.tex:162-164` enuncia (i) como error `L² < 5 %` **respecto a la solución
analítica de referencia** para el speckle. No existe referencia analítica para speckle: la
tesis lo dice ella misma (`Cap3:214-225`).

`Cap4-Resultados.tex:489` afirma: *"(i) el error L² < 5 % se supera con amplitud en todos los
casos."* `L²` se midió solo para NB01 y NB02. Tal como está redactada en Cap1, la hipótesis (i)
no es contrastable en NB03.

## C-5 (CRÍTICO). El test KS fallido se explica con un argumento que su propio estadístico refuta

`Cap4-Resultados.tex:357-361` dice que el rechazo se debe a que *"desviaciones menores al 1 %
resultan estadísticamente significativas"* con `N = 10 000`. Pero `D = 0.0487` **es** la
desviación máxima de la CDF: ≈4.9 %, no menor al 1 %. La frase se contradice con el
estadístico que ella misma reporta.

Además, el argumento de alta potencia requiere `N` grande, mientras que `Cap4:346-349`
argumenta lo contrario dos párrafos antes (píxeles correlacionados, `N_eff ≪ 10 000`). Ambos
no pueden sostenerse. Y `\parencite{goodman2007speckle}` se cita para una afirmación sobre la
potencia del test de Kolmogorov-Smirnov, que la monografía de Goodman no respalda.

Punto aparte: `Cap3-Modelo.tex:220-222` establece *"Criterio formal: p > 0.05"* como criterio
de aceptación declarado para NB03. Ese criterio **falló**, y el resumen de `Cap4:488-492` y la
tabla de `Cap4:461-486` (NB03 = "Completo") lo omiten. Es reporte selectivo de un criterio
predeclarado.

`Resumen.tex:18-20` y `Abstract.tex:17-19` van más lejos: *"distribución de intensidades
exponencial negativa, **confirmando** speckle completamente desarrollado."* La hipótesis de
exponencialidad se rechazó con `p < 0.0001`, y ningún resumen menciona el test.

## C-6 (CRÍTICO). Sin mapa claim-source (INV-22)

`quality_reports/` solo contiene `research_journal.md`. Ninguno de los ~40 números de Cap3/Cap4
es trazable a una línea de script y un archivo de salida. C-2 es exactamente el error que un
mapa así existe para atrapar.

Números de NB03 **sin archivo de respaldo en `results/`**: `C=1.0253`, `KS=0.0487`,
`p<0.0001`, `0.1207`, `7 976`, `8/1 000`, `195 s`.
Números de NB01 sin archivo: `0.006 %`, MSE/RMSE/MAE/error máx., `R²`, `202/500`, `142 s`.
Reclamo con única fuente en markdown de notebook: `0.436 %` (`notebooks/02_...ipynb:1253`).

---

## Hallazgos mayores

- **C-7.** "Simulación acelerada" se afirma en título, objetivo general y Resumen mientras
  `S > 1` sigue sin probarse. Cap1/Cap4 lo declaran pendiente con honestidad, pero
  Resumen/Abstract nunca mencionan que una de las tres hipótesis está sin verificar.
- **C-8.** `Cap3:66` — `σ_ψ > 2π` es falso. Para `ψ ~ U(0, 2π)`, `σ_ψ = 2π/√12 ≈ 1.81`. Lo
  que se quiso decir es que el *rango* abarca `2π`, que es lo que `Cap2:49` sí dice
  (`Δψ ≫ 2π`). Tal como está, la condición suficiente enunciada la viola la propia frontera
  de la tesis.
- **C-9.** `Cap3:149-152` dice que *"En NB01 y NB02, los N_b = 300 puntos de frontera por
  borde se distribuyen... sobre cada uno de los cuatro lados"*. NB01 es 1D con 5 puntos de
  frontera, enunciado 130 líneas antes en el mismo capítulo.
- **C-10.** `Cap4:143` y `tab:multiseed:209` reportan **1 035** iteraciones L-BFGS contra un
  máximo declarado de **1 000** (`Cap3:179`). El valor coincide con el JSON, no está
  fabricado, pero es contradictorio y no se explica.
- **C-11.** `Cap4:157-159` atribuye la mejora a `d=64 → d=128` como *"determinante"*. El
  0.436 % de referencia sale de una corrida que difiere además en iteraciones L-BFGS y en el
  manejo de λ: atribución de un factor a partir de una comparación de dos factores. Cerca de
  ahí, dos reclamos huérfanos: LHS *"redujo el error respecto a mallas cartesianas"* (no
  existe ese experimento) y Resumen/Abstract *"Adam + L-BFGS y LHS son clave"* (sin ablación,
  y en NB03 L-BFGS corrió 8 iteraciones).
- **C-12.** `Cap4:399-407` afirma evaluar *"cualquier condición de frontera sin reentrenamiento
  de la arquitectura"*. `CLAUDE.md` establece que NB03 inicializa desde cero y no reutiliza
  pesos de NB02. El modelo se reentrenó por completo.
- **C-13.** λ=0.1 se etiqueta *"Configuración óptima"* y se elige *"por su estabilidad y
  precisión"*, pero la misma tabla muestra λ=0.01 en **0.163 %** contra **0.171 %**. El
  argumento de estabilidad se sostiene solo; el de precisión contradice la tabla.
- **C-14.** No hay capítulo de Conclusiones (`main.tex:131-134`).
- **C-15.** Los *Alcances* (`Cap1:120-122`) prometen el benchmark FEM que `Cap1:262-266`
  clasifica como trabajo futuro.
- **C-16.** *"supera el umbral"* invierte el sentido del resultado principal en tres lugares
  (`Cap4:65`, `Cap4:152`, `Cap4:489`). `Resumen.tex:12-14` lo dice bien
  (*"por debajo del umbral"*), lo que además lo vuelve inconsistente con el resumen.
- **C-17.** Tres títulos distintos: `main.tex:66-67` (14 palabras, dentro del límite UJAT de
  15), `pdftitle` en `main.tex:87`, y el de `CLAUDE.md`. Además el título dice *"redes
  neuronales físicamente informadas"* mientras el cuerpo usa *"Redes Neuronales Informadas por
  Física"*. Propaga vía `\Titulo` a portada, declaración de autoría y cesión de derechos.
- **C-18.** El estatus no arbitrado de `panagiotakopoulos2026helmholtz` está anotado con
  honestidad en `references.bib:251-262` pero nunca llega al lector, y toda la novedad se
  posiciona contra ese trabajo. Divulgarlo en `Cap4:442-445`.

## Hallazgos menores

`Cap2:194-202` contradice la tabla por notebook de Cap3 · inicialización de Sitzmann sin el
divisor `ω₀` · `d` colisiona con el diferencial en `d²E/dx²` · `Cap3:195-199` dice malla
100×100 para NB01, que es 1D con 1 000 puntos · NB04 aparece solo en una nota al pie fuera de
la numeración, con "Goodman 2007" en texto plano y `2-20cm` sin `--` · Panel F de
`estadistica_speckle_nb03.png` es un marcador vacío con una referencia cruzada quemada en el
ráster · etiqueta verde suelta fuera de los ejes en `resultados_pinn_1d.png` · figuras de 9 y
6 paneles a `0.48\textwidth` cada una, ilegibles impresas · tres overfull hbox por encima de
10 pt · aviso de `headheight` · `.aux` obsoletos en el árbol de fuentes, incluido el huérfano
`PortadaBlanca.aux` · encabezado "Método" sobre celdas con citas de autor · "varianza de
±0.020 %" es una desviación estándar, y el "13 % relativo" un coeficiente de variación ·
reclamo de novedad sin matizar en Cap2 frente a la versión matizada de Cap1.

---

## Lo que sí verifica bien

NB02 `L²` real 0.214 / imag 0.127 / prom 0.171 · Adam 8 737 · 299 s · multiseed 0.171 /
0.1264 / 0.1675, media 0.155 ± 0.020 · ablación λ=0.01 → 0.163 · `|C−1| = 0.0253` ·
diferencia relativa de cola 10.8 % · `5/0.006 ≈ 833` · `5/0.171 ≈ 29` · `0.436/0.171 = 2.55` ·
16 833 / 66 690 parámetros · `N_ψ = 256` consistente en las cuatro apariciones.

Formato UJAT correcto y consistente: `report` / 11 pt / helvet / `biblatex style=apa` + biber.
Las 7 tablas usan `threeparttable` con notas sustantivas (INV-1). Cero `\hline` (INV-3).
Compila limpio: cero errores, cero referencias o citas indefinidas, 26/26 citekeys resueltos.
Prosa sin marcas de IA.

---

## Orden de atención

1. **C-1** — determinar si el campo de NB03 satisface `|E| ≈ 1` en `y = 0`. Si no, el capítulo
   de speckle se re-ejecuta, no se reescribe. Todo lo demás depende de esta respuesta.
2. **C-2** — sustituir `>5.0` por "no converge (crash)" y reescribir la nota. Corregir también
   `ablation_lambda.json`, y propagar a `paper/fuente_validacion1D2D` y CyS.
3. **C-3** — reescribir las cinco leyendas contra los PNG actuales.
4. **C-4, C-5, C-16** — acotar el alcance de la hipótesis (i); reportar el fallo del KS contra
   el criterio declarado en `Cap3:222`, en Cap4 y en Resumen/Abstract; corregir la inversión
   semántica.
5. **C-6, C-14** — mapa claim-source y capítulo de Conclusiones.
6. El resto de mayores y menores.
