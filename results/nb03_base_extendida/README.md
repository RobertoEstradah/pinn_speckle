# ¿El piso evanescente es evitable ampliando la base modal?

**Fecha:** 2026-09-16
**Respuesta corta:** el piso **sí** se elimina, pero el error total **empeora 5.7 veces**.
El truncamiento al cono propagante está justificado — aunque **no por la razón que da Cap3**.

---

## La pregunta

`Cap3` descarta los modos evanescentes así:

> «Los modos evanescentes se descartan porque su rama creciente $e^{+|\kappa_m|\tilde z}$
> hace que la solución no dependa de forma continua de los datos; el truncamiento
> espectral es la regularización de este problema de Cauchy.»

El árbitro de dominio objetó que esa justificación está anulada por otra ecuación
de la propia tesis. `Cap3:90-96` fija la derivada de entrada como

```
∂z E(x,0) = F⁻¹[ i·√(k² − kx²) · Ê(kx,0) ]
```

y para un modo evanescente `√(k² − kx²) = i|κ|`, de modo que
`a'(0) = −|κ|·a(0)`: **la rama decreciente ya está seleccionada por
construcción**. La creciente no es admisible, así que no hay un problema de
Cauchy mal planteado que regularizar.

Si eso es correcto, el piso de 3.818 % no sería una limitación fundamental sino
una decisión evitable, y el resultado principal de la tesis pasaría de
«3.161 %, dominado por algo irrepresentable» a algo mucho menor.

## El experimento

Una sola cosa cambia: cuántos modos entran en la base. Todo lo demás es
idéntico — clase `ModalSiren` de NB03, ω₀ = 1, Cauchy dura, escalamiento por
modo, normalización del residuo por `k²·amplitud`, mismo protocolo
(5 000 épocas Adam con recocido coseno + 3 000 de refinamiento), misma semilla,
pantalla 42.

Para los modos evanescentes, `kz² < 0` entra **sin recortar**: la EDO modal pasa
a ser `a'' − |κ|²a = 0`, que es justo lo que debe resolver.

```bash
python explorations/nb03_base_extendida/nb03_base_extendida.py --m-max 20   # control, 41 modos
python explorations/nb03_base_extendida/nb03_base_extendida.py --m-max 35   # extendida, 71 modos
```

## Resultados

| | Control, 41 modos | Extendida, 71 modos |
|---|---:|---:|
| Modos propagantes | 41 | 41 |
| Modos evanescentes | 0 | 30 |
| **Piso fuera de la base** | **3.8184 %** | **0.0020 %** |
| Error dentro de la base | 1.979 % | **24.695 %** |
| **L² total** | **4.300 %** | **24.695 %** |
| Coherencia | 0.999135 | 0.970882 |

## Qué se concluye

**La premisa del árbitro era correcta.** La energía evanescente es
representable: el piso cae de 3.82 % a 0.002 %, tres órdenes de magnitud. No
hay ningún impedimento matemático para incluirla.

**Pero la optimización no lo soporta.** Con la base extendida el error dentro de
la banda se multiplica por 12, y el total por 5.7. La causa razonable es el
rango dinámico: la red debe representar `e^{-κz}` con κ entre 0 y 9.02 en el
mismo dominio, un problema multiescala que una SIREN de un solo ω₀ maneja mal.
Es el mismo fenómeno que el barrido de ω₀ ya mostraba, llevado al extremo.

**Por tanto el truncamiento está justificado, pero la justificación de Cap3 debe
cambiar:** no es que el problema esté mal planteado en el sentido de Hadamard
--no lo está, porque el dato de Cauchy no es libre--, sino que **incluir los
modos evanescentes vuelve el ajuste numéricamente intratable con esta
arquitectura**. Es una razón de método, no de matemáticas.

## Salvedad importante

**Las cifras absolutas no son las de NB03.** El control reproduce el piso dígito
a dígito (3.8184 % frente a 3.8184 %), lo que valida la máscara de modos, la
referencia y la evaluación. Pero su error dentro de la banda es 1.979 % frente
al 0.090 % que reporta NB03, unas 22 veces peor, pese a alcanzar una pérdida
**menor** (2.90e-06 frente a 3.41e-06).

El motivo es que los modelos validados de NB03 no salen de una corrida limpia:
`..._omega1_finetune.pt` reanuda desde `..._omega1.pt`, que viene a su vez de
otra corrida. Hay un linaje más largo detrás del 0.090 % que este script no
reproduce.

Es otra instancia de la regla que ya está en la memoria anti-errores del
proyecto: **residuo bajo no acredita solución correcta**.

Por eso la comparación válida aquí es **41 modos frente a 71 dentro de este
mismo script**, que sí comparten protocolo, semilla y presupuesto. La
conclusión es relativa y en esos términos es sólida; no debe compararse el
4.300 % con el 3.819 % de la tesis, porque son pipelines distintos.

## Qué haría falta para cerrarlo del todo

1. Repetir la extendida partiendo del modelo validado de 41 modos, ampliando la
   base sobre él, en vez de entrenar desde cero.
2. Probar un ω₀ distinto para el bloque de modos evanescentes, o un
   escalamiento por modo que absorba `e^{-κ}`.
3. Si alguna de las dos recupera el error, la conclusión cambia y el piso sí
   sería evitable en la práctica.

Mientras eso no se haga, lo que la tesis puede afirmar es lo de arriba: el piso
es eliminable en principio pero no con esta arquitectura y este entrenamiento.
