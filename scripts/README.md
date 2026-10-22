# Ejecución de los programas

Instalar con `python -m pip install -r requirements.txt` y ejecutar uno de los tres programas dentro de scripts/. Mantener figuras_publicacion.py junto a ellos. También pueden abrirse en Spyder. MOSTRAR_GRAFICAS controla la visualización; las figuras se guardan siempre.

Fuentes locales predeterminadas: G:/ENSO Y PRECIP para zap6024.csv y gdl_completo_precip_meses.xlsx (hoja PRECIP, datos diarios FECHA/PRECIP), y G:/RUEMAG2/TEMPORAL 2026 para eventos.xlsx (hojas por año con evento, fecha, precip). Se pueden configurar las carpetas con las variables de entorno ENSO_DATOS y ENSO_EVENTOS, o editarlas al principio del programa.

Salidas: scripts/resultados/, separadas por programa; los estudios adicionales del análisis de eventos se guardan en resultados/estudios. No se modifican las fuentes. Los archivos de datos locales no se incluyen en esta actualización del repositorio.

Periodo mensual configurado: 1991–2025. Referencia de precipitación: 1991–2020. No ampliar FIN sin verificar precipitación y ONI disponibles para todo el intervalo. Los meses incompletos se excluyen de las estadísticas, no se rellenan con cero.

Los programas se entregan como la versión documentada de los archivos proporcionados. Las figuras antiguas del repositorio no se identifican automáticamente como salidas reproducidas de esta versión. Consulte docs/periodos_y_climatologia.md.
