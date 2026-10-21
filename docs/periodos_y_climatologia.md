# Periodos de estudio y climatología

## Series y fechas

- Estudio mensual de precipitación: enero de 1991 a diciembre de 2025, según INICIO y FIN.
- Análisis anual: el intervalo se obtiene de los años presentes en zap6024.csv; además se representa 1991–2020. No se deduce la estación a partir del nombre del archivo.
- Eventos RUEMAG: cada panel identifica el año y las fechas extremas de los registros de ese año. El pie general se calcula con la primera y última fecha del catálogo leído. Estas fechas no acreditan observación continua ni homogeneidad espacial.
- ONI ERSSTv6: enero de 1950 (DJF) a agosto de 2026 (JAS, trimestre julio–septiembre), asignado por el mes central. JAS 2026 = 2.2 °C. La extensión del ONI no amplía automáticamente el periodo de precipitación ni convierte 2026 en año completo.

## Climatología de precipitación

Referencia: 1991–2020. En el análisis mensual se calcula una media para cada mes del calendario usando meses sin faltantes diarios y no excluidos por configuración. Anomalía mensual = precipitación mensual válida menos la media de ese mes en 1991–2020. La tabla exportada informa cuántos años aportan a cada mes; el intervalo nominal no garantiza 30 observaciones válidas.

En el análisis anual, la referencia es la media de los acumulados anuales disponibles y no excluidos en 1991–2020. Se indica n. El CSV anual no permite comprobar cobertura diaria. Las dos formas de calcular la referencia no son intercambiables cuando hay faltantes.

La referencia de precipitación es distinta de los periodos base móviles utilizados por NOAA para el ONI. No se recalcula ONI con la climatología local de lluvia.

## Fases ENSO

Se aplica el criterio histórico de umbrales ±0.5 °C durante al menos cinco trimestres móviles consecutivos, cruzando años. DJF se asigna a enero, JFM a febrero, etc. El ONI conserva su naturaleza trimestral. La fase anual predominante es un resumen propio, no una clasificación anual oficial. Los valores recientes son revisables.

Fuente: https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/oni/v6/ . Tabla adjunta contrastada el 21/10/2026. Actualización respecto de los scripts originales: JAS 2026 pasó de ausente a 2.2 °C; se conserva lo demás. Esta modificación no cambia por sí sola los resultados mensuales que terminan en 2025.

## Presentación de figuras

Cada figura generada por los programas incluye periodo de estudio y referencia climatológica en un pie adicional, exportado dentro del archivo. El detalle de eventos añade las fechas del catálogo y el intervalo de la serie mensual de referencia. Se exportan PNG a 400 dpi y PDF vectorial. Las notas sobre cobertura y exclusiones se conservan.

Para una siguiente revisión editorial: paneles separados para ONI y lluvia; colores uniformes; anomalías por mes y fase con tamaños de muestra; incertidumbre que tenga en cuenta la dependencia temporal; frecuencia e intensidad de tormentas por separado. Las afectaciones quedan para una segunda etapa.

Las dos imágenes originales del repositorio se conservan como antecedentes. Las nuevas salidas se identifican por programa. Los resultados previos no quedan validados retrospectivamente por documentar estos programas.

## Verificación del 21/10/2026

Los programas anual y mensual se ejecutaron con las fuentes locales: se obtuvieron dos figuras anuales (1960–2025 y 1991–2020) y tres mensuales (1991–2025), en PNG y PDF. La serie mensual contiene 420 meses, de los cuales 415 cumplen el criterio de ausencia de faltantes diarios. La referencia anual incluye 30 acumulados disponibles de 1991–2020.

El programa de eventos queda pendiente de ejecución completa: eventos.xlsx, hoja 2026, evento 90, contiene solo una hora en fecha y un valor de tipo fecha en precipitación. Se requiere corregir la fuente; no se ha eliminado ni reinterpretado el registro. El programa ahora explica este error y detiene el análisis.
