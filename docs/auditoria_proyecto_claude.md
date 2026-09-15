# Auditoría del proyecto equivalente de Claude

Fecha de revisión: 2026-09-13.

## Alcance y protección del original

La ruta indicada `C:\roberto\Tesis\_Maestria` no existe en este equipo. El
proyecto equivalente localizado fue:

`C:\roberto\Tesis_Maestria`

Se utilizó únicamente como fuente de lectura. No se modificaron, eliminaron ni
sobrescribieron archivos en esa ruta. Todas las implementaciones y salidas de
esta auditoría están en:

`C:\roberto\Tesis_Maestria - codex`

NB01 y NB02 tampoco fueron modificados; se cargaron sus artefactos existentes
solo para diagnóstico.

## Resultado ejecutivo

El proyecto de Claude no contiene una sustitución mejor que la NB03 modal
actual. Sus experimentos cartesianos con envolvente, Fourier y curriculum de
frecuencia obtuvieron errores altos en la configuración de 20 lambda o no
reportaron una métrica de campo comparable. Por eso no se sustituyó la NB03
validada.

Sí se incorporaron tres elementos seguros:

1. Diagnóstico reproducible de la sensibilidad NTK de NB02.
2. Barrido reproducible de `omega_0` de NB01, sin cambiar NB01.
3. Literatura adicional relevante para Helmholtz, condiciones duras,
   sesgo espectral, subdominios y propagación por espectro angular.

## Qué se analizó y decisión

| Elemento encontrado en Claude | Resultado o utilidad | Decisión en Codex |
|---|---|---|
| Referencia por espectro angular | Referencia independiente exacta; el código principal ya coincidía por hash | Conservar y usar como referencia de NB03 |
| PINN cartesiana con campo crudo | Aproximadamente 96–100 % de L2 en los pilotos de larga distancia | No sustituir la NB03 modal |
| PINN con factor de envolvente | Mejor resultado reportado ≈35.77 % de L2 a 20 lambda | No adoptar; es peor que 1–2 lambda modal |
| Fourier + envolvente | Inestabilidad numérica y ≈98.57 % de L2 en el piloto | No adoptar |
| Curriculum de frecuencia | ≈47.39 % de L2 a 1 lambda en el experimento de Claude | No adoptar |
| Muestreo concentrado / dominio mayor | No produjo una validación de campo comparable | No adoptar como solución principal |
| Diagnóstico NTK de NB02 | La física tiene una escala mucho mayor que los datos | Incorporar como diagnóstico explicativo |
| Barrido de `omega_0` | Sirve para detectar sensibilidad espectral, pero el resultado numérico no se reproduce idéntico sin fijar el protocolo | Incorporar como diagnóstico, no cambiar NB01 |
| Literatura adicional | Aporta soporte metodológico y óptico, no prueba por sí sola el modelo | Copiar PDFs y documentar su uso |

## Diagnósticos ejecutados en la copia

### NTK de NB02

Archivo de salida: `results/diagnostics/ntk_nb02.json`.

| Magnitud | Valor |
|---|---:|
| Parámetros entrenables | 66,690 |
| Puntos por término | 80 |
| Traza NTK de datos | 14,487.64 |
| Traza NTK física | 12,175,811.00 |
| Cociente física/datos | 840.43× |
| Mayor autovalor de datos | 5,292.83 |
| Mayor autovalor físico | 8,271,311.50 |

La lectura correcta es que, con igual peso, el residuo físico puede dominar el
gradiente. Esto respalda estudiar el balance de pérdidas de NB02, pero no
autoriza a cambiar los pesos de la validación ya cerrada.

### Barrido de `omega_0` de NB01

Archivo de salida: `results/diagnostics/nb01_omega0_sweep.json`.

Se conservaron el problema, la arquitectura, semilla, puntos y presupuesto de
entrenamiento de NB01. Los valores probados fueron 1, 5, 15 y 30.

| `omega_0` | Pérdida total final | L2 final | Tiempo |
|---:|---:|---:|---:|
| 1 | 0.268711 | 63.02 % | 31.31 s |
| 5 | 0.184970 | 54.34 % | 29.67 s |
| 15 | 0.409955 | 82.58 % | 30.80 s |
| 30 | 0.603025 | 100.10 % | 29.92 s |

En esta reproducción `omega_0=5` fue el mejor de los cuatro, aunque las
cifras no coinciden exactamente con el JSON de Claude. Por ello el barrido se
considera una alerta de sensibilidad y no una modificación de NB01 ni una
afirmación final de la tesis.

## Estado que debe conservarse para la tesis

- NB01: conservar su validación oficial y sus archivos originales.
- NB02: conservar su validación analítica y sus archivos originales.
- NB03: conservar la formulación modal PINN-SIREN como línea principal.
- La validación modal actual a 1 lambda sigue siendo la referencia principal;
  la extensión a 2 lambda es prometedora, pero no equivale a generalidad para
  cualquier distancia.
- Los resultados de Claude a 5–20 lambda no deben presentarse como mejora:
  tienen errores altos, referencias no homogéneas o criterios no comparables.

## Siguiente paso recomendado

Antes de sustituir la arquitectura, corregir el protocolo de selección de
pesos y comparar Adam, Adam+L-BFGS y eventualmente float64 con las mismas
pantallas, una malla fija de validación y una prueba reservada. Si se exige
precisión frente al campo completo a z pequeño, debe estudiarse la inclusión
convergente de modos evanescentes; aumentar épocas o Fourier no elimina el
límite físico de truncar esos modos.

No se reemplazó ningún capítulo de la tesis en esta fase: el texto de Claude
no contiene todavía los resultados más recientes de la NB03 modal de Codex.

## Prueba reservada posterior a la auditoría

Como continuación del protocolo corregido se generó una pantalla nueva
(semilla 31415) y se entrenó una inicialización neuronal distinta (semilla
73). Después de 7360 pasos Adam acumulados y dos etapas L-BFGS, el mejor
resultado fue 6.4492 % de L2 propagante, 6.7397 % frente al campo completo,
máximo propagante de 8.0298 % y residuo RMSE de 0.04265.

La coherencia 0.9985 y el error de contraste 0.0068 fueron buenos, pero no
sustituyen el criterio de campo `L2 < 5 %`. El resultado se clasifica como
prueba reservada negativa y evidencia sensibilidad a la inicialización. Los
detalles están en `results/nb03_holdout/README.md`.

Una modificación posterior, fundamentada en Jagtap, Kawaguchi y Karniadakis
(2020), hizo entrenable un multiplicador global de las activaciones SIREN. Con
la misma pantalla 31415 y semilla neuronal 73 obtuvo 0.7548 % propagante,
0.8854 % máximo propagante, 2.1018 % completo y residuo 0.00577. La escala
efectiva aprendida fue 0.46684.

La confirmación predefinida con semillas neuronales 73, 101 y 211 aprobó el
criterio primario de L2 completo menor que 5 % en 2 de 3 casos. La semilla 101
falló con 134.9440 %, por lo que la modificación se conserva como candidata y
no como sustitución incondicional de NB03.
