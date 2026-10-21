# ENSO y precipitación en Guadalajara

Este repositorio reúne el material de trabajo sobre la relación descriptiva entre el ENSO —medida mediante el **ONI**— y la precipitación en Guadalajara. Su propósito es conservar las figuras, las explicaciones en lenguaje claro, la metodología documentada y las conclusiones provisionales elaboradas hasta ahora.

## Contenido

- [`docs/`](docs/): metodología, explicación de los desfases y resultados interpretados.
- [`figuras/`](figuras/): gráficas usadas en el análisis y una guía de lectura.
- [`scripts/`](scripts/): programas anual, mensual y de eventos, con exportación PNG/PDF y periodos explícitos.
- [`datos/`](datos/): guía para documentar y añadir datos; no contiene datos originales todavía.

## Hallazgos principales

- La relación entre el ONI y la lluvia cambia según el mes y es, en general, baja en esta serie.
- Sin desfase, las correlaciones positivas más altas son marzo (`r = 0.34`), octubre (`r = 0.32`) y noviembre (`r = 0.32`).
- La asociación negativa más marcada aparece en junio con el ONI de un mes anterior (`r = -0.17`).
- No se identifica un único desfase que funcione de forma consistente durante todo el año.
- La comparación por fases ENSO sugiere contrastes en algunos meses, pero hay traslapes, valores atípicos y grupos con pocos años; los resultados son descriptivos, no reglas fijas ni pruebas de causalidad.

## Figuras disponibles

| Figura | Descripción |
| --- | --- |
| [`01_correlacion_oni_lluvia_desfases.png`](figuras/01_correlacion_oni_lluvia_desfases.png) | Correlación de Pearson por mes y desfase entre el ONI y la lluvia. |
| [`02_anomalias_lluvia_por_fase_enso.png`](figuras/02_anomalias_lluvia_por_fase_enso.png) | Distribución mensual de anomalías de lluvia por fase ENSO. |

## Uso responsable

Estas figuras y textos resumen asociaciones estadísticas de una serie analizada. No deben interpretarse como pronósticos, relaciones causales demostradas ni como una regla aplicable a todos los eventos de El Niño o La Niña.

## Estado de reproducibilidad

Se incorporaron los tres programas proporcionados por la autora y su ONI ERSSTv6 actualizado hasta JAS de 2026. Los datos locales de precipitación y eventos no están incluidos. Consulte [periodos y climatología](docs/periodos_y_climatologia.md) y [ejecución de programas](scripts/README.md). Las dos figuras originales y sus hallazgos se conservan como resultados previos; no se consideran automáticamente recalculados por agregar los programas.


Actualización del 21/10/2026: [cinco figuras verificadas en PNG y PDF](figuras/actualizadas_2026-10-21/), con sus periodos y climatología explícitos. El análisis de eventos está pendiente de corregir la fecha y precipitación del evento 90 de 2026 en la fuente local.
