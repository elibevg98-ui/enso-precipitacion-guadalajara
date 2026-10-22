# Metodología y alcance

## Pregunta exploratoria

Se explora si las condiciones del ENSO, representadas por el Índice Oceánico de El Niño (ONI), guardan una relación lineal con la precipitación mensual de Guadalajara y si esa relación cambia cuando el ONI antecede a la lluvia por varios meses.

## Variables analizadas

- **ONI:** indicador usado como referencia de las condiciones ENSO.
- **Precipitación mensual:** lluvia observada o estimada para Guadalajara.
- **Anomalía de precipitación:** diferencia de la lluvia mensual respecto a un valor de referencia de ese mismo mes, expresada en milímetros en la figura disponible.
- **Fase ENSO:** en los programas incorporados, fase del trimestre ONI asignada al mes central; la fase anual predominante es un resumen propio separado.

## Correlaciones por desfase

Para cada mes de lluvia se calculó la correlación de Pearson con el ONI del mismo mes y con el ONI de hasta seis meses anteriores:

| Desfase | Comparación para la lluvia de junio |
| --- | --- |
| 0 | ONI de junio y lluvia de junio |
| 1 | ONI de mayo y lluvia de junio |
| 2 | ONI de abril y lluvia de junio |
| 3 | ONI de marzo y lluvia de junio |
| 4 a 6 | ONI de dos a seis meses antes de junio |

El desfase permite explorar si las condiciones ENSO previas presentan una asociación más clara con la precipitación posterior. No implica que un valor anterior del ONI provoque por sí mismo la lluvia de un mes posterior.

## Comparación por fase ENSO

Las anomalías mensuales se agruparon por fase ENSO. Cada caja de la figura resume la distribución de los años disponibles en ese grupo:

- La línea dentro de la caja muestra el valor central del grupo.
- La caja representa el rango donde se encuentran la mayoría de los años del grupo.
- Los puntos separados señalan años poco frecuentes o extremos.
- `n` es el número de años incluidos en cada grupo.

## Límites de interpretación

Este análisis es descriptivo. Las correlaciones bajas, el traslape entre grupos, los valores atípicos y tamaños de muestra reducidos en algunos meses limitan las conclusiones. Los resultados muestran asociaciones; no demuestran causalidad ni sustituyen un análisis de significancia, incertidumbre, control de otras variables o validación fuera de la muestra.

## Información pendiente para reproducción

Los programas y periodos se documentan en [periodos y climatología](periodos_y_climatologia.md). Las figuras originales se conservan como antecedentes. Para vincularlas con una ejecución reproducible aún debe comprobarse:

1. La fuente y periodo de la precipitación.
2. La versión, fuente y periodo del ONI.
3. El cálculo exacto de la anomalía de precipitación.
4. La regla aplicada para clasificar El Niño, La Niña y neutral.
5. El tratamiento de valores faltantes y los criterios de inclusión de años.
6. El software, paquetes y scripts empleados.

## Versión documentada del 21/10/2026

Los programas mensual y de eventos están configurados para 1991–2025, con climatología de precipitación 1991–2020. El programa anual obtiene de su CSV el intervalo disponible, actualmente 1960–2025. El ONI es ERSSTv6 y se conserva hasta JAS de 2026; ese periodo disponible no amplía el estudio de lluvia. Las fases se calculan con ±0.5 °C durante cinco trimestres móviles consecutivos, cruzando años. Véase la documentación de periodos para fórmulas, exclusiones, cobertura, verificación y el dato pendiente del catálogo de eventos.
