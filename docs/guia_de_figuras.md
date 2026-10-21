# Guía de figuras

## 01. Correlación ONI–lluvia por desfase

Archivo: [`01_correlacion_oni_lluvia_desfases.png`](../figuras/01_correlacion_oni_lluvia_desfases.png)

- Cada fila corresponde al mes de lluvia.
- Cada columna corresponde al desfase del ONI respecto a la lluvia.
- `0` significa ONI y lluvia del mismo mes.
- `1` significa que el ONI corresponde al mes anterior.
- Los valores son coeficientes de correlación de Pearson (`r`).
- Rojo: relación positiva; azul: relación negativa; cerca de cero: poca relación lineal.

Para hacer el gráfico más accesible en una siguiente versión, se recomienda nombrar las columnas como: **Mismo mes**, **1 mes antes**, **2 meses antes**, …, **6 meses antes**.

## 02. Anomalías de lluvia por mes y fase ENSO

Archivo: [`02_anomalias_lluvia_por_fase_enso.png`](../figuras/02_anomalias_lluvia_por_fase_enso.png)

- Cada panel es un mes.
- Cada color representa una fase ENSO: El Niño, La Niña o neutral.
- La línea dentro de la caja representa el valor central.
- La caja señala el rango donde se encuentran la mayoría de los años del grupo.
- Los puntos separados son años poco frecuentes o extremos.
- `n` indica cuántos años integran cada grupo.
