# NB03D — validación hasta 10 lambda

Este directorio consolida cinco realizaciones conocidas de speckle propagadas
hasta `z=10λ` mediante diez PINN-SIREN modales locales de ancho `1λ`.

## Resultado validado

- Pantallas aceptadas: `5/5`.
- Error L2 complejo final medio: `2.6173 %`.
- Peor error propagante en 201 planos: `3.7265 %`.
- Coherencia compleja media: `0.999716`.
- Correlación de intensidad media: `0.999475`.
- Diferencia de contraste media: `0.003731`.
- Continuidad de campo y derivada: impuesta de forma dura en nueve interfaces.

Las pantallas 321 y 2026 requirieron una segunda optimización de los bloques
5–9. El tramo validado 0–5λ se reconstruyó sin reentrenarlo.

## Archivos principales

- `validation_summary.json`: métricas consolidadas y criterios por pantalla.
- `../../../notebooks/03d_validacion_speckle_2d_z10lambda.ipynb`: explicación,
  tablas y figuras ejecutadas.
- `../../../scripts/experiments/nb03d_z10_summary.py`: consolidación verificable.

## Reproducibilidad

Desde la raíz del proyecto:

```powershell
python scripts/experiments/nb03d_z10_summary.py
python scripts/build/build_nb03d_z10_notebook.py
python -m jupyter nbconvert --to notebook --execute --inplace `
  notebooks/03d_validacion_speckle_2d_z10lambda.ipynb
```

## Alcance

El resultado valida cinco pantallas conocidas y una cadena de diez redes
locales. No demuestra generalización a pantallas nuevas, una PINN global única,
distancias arbitrarias ni aceleración frente a FEM.
