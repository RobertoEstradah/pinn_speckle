# NB03: piloto PINN-SIREN modal en z = 1 lambda

Fecha de ejecucion: 11 de septiembre de 2026.

## Objetivo

Validar un campo speckle 2D a una distancia normalizada `z = 1 lambda`
manteniendo la ecuacion completa de Helmholtz, una arquitectura SIREN y una
referencia independiente por espectro angular. NB01, NB02 y la tesis no se
modificaron durante esta fase.

## Formulacion aceptada

El campo se representa como una suma de 41 modos transversales propagantes:

`u(x,z) = sum_m a_m(z) exp(i kx_m x)`.

Cada coeficiente complejo satisface la reduccion exacta de Helmholtz:

`a_m''(z) + (k^2-kx_m^2) a_m(z) = 0`.

La SIREN aprende simultaneamente los 41 coeficientes mediante la condicion de
Cauchy dura

`a_m(z) = a_m(0) + z a_m'(0) + z^2 N_theta(z)`.

No se emplean valores del espectro angular dentro del dominio. Esa solucion se
usa solamente al final para evaluar el campo predicho. Para evitar que los
modos debiles adquieran amplitud espuria, la salida y el residuo se escalan con
la amplitud fisica de cada modo.

## Resultados

| Experimento | L2 complejo | Coherencia | C PINN | Residuo normalizado RMSE | Tiempo | Aceptado |
|---|---:|---:|---:|---:|---:|---|
| PINN cartesiana, Cauchy dura + Fourier | 23.57 % | 0.9724 | 0.8697 | 0.0350 aprox. | 359.2 s | No |
| Curriculum de frecuencia | 47.39 % | 0.8984 | 0.9001 | 0.1503 | 156.0 s | No |
| Curriculum + afinacion | 27.65 % | 0.9618 | 0.8223 | 0.0774 | 120.5 s | No |
| PINN modal sin escalado | 232.75 % | 0.5981 | 0.7837 | 0.0986 | 96.4 s | No |
| PINN modal escalada | 4.88 % | 0.9990 | 0.9022 | 0.0548 | 164.4 s | Si |
| PINN modal escalada + afinacion | **4.12 %** | **0.9992** | **0.9019** | **0.0387** | 104.0 s adicionales | **Si** |

Para la corrida final, `|C-1| = 0.0981 < 0.1`. La comprobacion independiente
del archivo NPZ reprodujo `L2 = 0.0411845086` y `coherencia = 0.9991936385`.
El tiempo acumulado del entrenamiento aceptado y su afinacion fue 268.4 s en
CPU.

## Validacion con cinco pantallas

Se congelo la inicializacion de la red en la semilla 42 y se generaron cinco
pantallas fisicas con semillas 42, 123, 321, 777 y 2026. Todas utilizaron la
misma arquitectura y el mismo protocolo de 5000 epocas mas 3000 de afinacion.

| Pantalla | L2 en z=1 | Coherencia | C referencia | C PINN | Error absoluto de C | Residuo RMSE |
|---:|---:|---:|---:|---:|---:|---:|
| 42 | 4.12 % | 0.9992 | 0.9063 | 0.9019 | 0.0044 | 0.0387 |
| 123 | 2.91 % | 0.9996 | 0.8827 | 0.8841 | 0.0014 | 0.0370 |
| 321 | 3.89 % | 0.9993 | 0.9200 | 0.9211 | 0.0011 | 0.0363 |
| 777 | 3.25 % | 0.9995 | 1.2246 | 1.2391 | 0.0144 | 0.0357 |
| 2026 | 3.54 % | 0.9995 | 0.7812 | 0.7822 | 0.0010 | 0.0363 |

El L2 medio final fue 3.54 % con desviacion poblacional de 0.43 puntos
porcentuales; el peor resultado fue 4.12 %. Las cinco pantallas cumplieron
`L2 < 5 %` y `|C_PINN-C_referencia| < 0.05`.

En el intervalo completo, el L2 medio por pantalla estuvo entre 2.61 % y
3.24 %. El maximo fue 5.27 % para la pantalla 123 cerca de un plano interior;
las otras cuatro permanecieron por debajo de 5 % en todos los planos.

## Correccion del criterio de contraste

La condicion `|C-1| < 0.1` solo fue satisfecha por dos de cinco realizaciones,
porque las referencias individuales presentaron contrastes entre 0.7812 y
1.2246. En cambio, los conjuntos de 64 realizaciones tuvieron contraste
cercano a uno. Por ello se conservan dos evaluaciones distintas:

1. Para una pantalla: fidelidad `|C_PINN-C_referencia| < 0.05`.
2. Para el conjunto: contraste speckle cercano a uno.

## Alcance de la conclusion

La prueba demuestra reproducibilidad preliminar en cinco pantallas para
`z = 1 lambda`. Todavia no demuestra propagacion a 5, 10 o 20 lambda,
generalizacion sin reentrenamiento a una pantalla nueva, ni aceleracion frente
a FEM. El umbral formal del residuo de Helmholtz tambien debe fijarse antes de
redactar la conclusion definitiva de la tesis.
