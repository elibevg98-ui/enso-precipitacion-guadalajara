# ONI ERSSTv6: tabla adjunta contrastada con NOAA/CPC el 2026-10-21.

    # -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 11:08:57 2026

@author: bcomi
"""

# -*- coding: utf-8 -*-
"""Análisis mensual exploratorio de precipitación y ENSO para Spyder.
Dependencias: pandas, numpy, matplotlib, openpyxl, scipy.
Versión integrada: ejecutar este archivo completo con F5.
No modifica la base original. ONI del adjunto integrado, sin descarga web.
"""
from pathlib import Path
import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="replace")
from figuras_publicacion import guardar_publicacion
import json
import html
from scipy.stats import spearmanr, norm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# ================= CAMBIAR AQUÍ RUTAS Y PERIODO =================
CARPETA_BASE = Path(os.environ.get("ENSO_DATOS", r"G:\ENSO Y PRECIP"))
ARCHIVO = CARPETA_BASE / 'gdl_completo_precip_meses.xlsx'
SALIDA = Path(__file__).resolve().parent / 'resultados' / 'ensoyprecipeventos'
CARPETA_EVENTOS = Path(os.environ.get("ENSO_EVENTOS", r"G:\RUEMAG2\TEMPORAL 2026"))
ARCHIVO_EVENTOS = CARPETA_EVENTOS / 'eventos.xlsx'  # Ajustar si tiene otro nombre.
INICIO, FIN = 1991, 2025
BASE_INICIO, BASE_FIN = 1991, 2020
ESTACION = 'Guadalajara'
# Opcional: años que el usuario confirme que no deben entrar en estadísticas.
ANIOS_EXCLUIDOS = []
MOSTRAR_GRAFICAS = False

# Los seis gráficos y tablas adicionales se guardan aquí.
SALIDA_ESTUDIOS = Path(__file__).resolve().parent / 'resultados' / 'estudios'
ENTRADA = ARCHIVO  # Fuente del informe: usa la serie calculada en memoria.
ANIOS_SENSIBILIDAD = [2022, 2023]
MAX_DESFASE = 6
HAC_MESES = 24
FASES = ['El Niño', 'La Niña', 'Neutral']
COLORES_ESTUDIOS = {'El Niño': '#c85a45', 'La Niña': '#2287bd', 'Neutral': '#707784'}

# ===============================================================
COLORES = {'El Niño':'#f2ae9e', 'La Niña':'#a3d1eb', 'Neutral':'#e2e4e8'}
TRIMESTRES = 'DJF JFM FMA MAM AMJ MJJ JJA JAS ASO SON OND NDJ'.split()
MESES = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
ONI = json.loads(r'''{
  "1950": [
    -1.3,
    -1.2,
    -1.1,
    -1.1,
    -1.1,
    -0.9,
    -0.6,
    -0.6,
    -0.6,
    -0.6,
    -0.7,
    -0.8
  ],
  "1951": [
    -0.7,
    -0.4,
    0.0,
    0.2,
    0.3,
    0.5,
    0.7,
    0.9,
    1.0,
    1.0,
    1.0,
    0.7
  ],
  "1952": [
    0.5,
    0.3,
    0.3,
    0.2,
    -0.1,
    -0.4,
    -0.4,
    -0.2,
    0.0,
    0.0,
    -0.1,
    0.1
  ],
  "1953": [
    0.3,
    0.5,
    0.5,
    0.6,
    0.8,
    0.7,
    0.6,
    0.7,
    0.6,
    0.8,
    0.5,
    0.6
  ],
  "1954": [
    0.4,
    0.4,
    0.0,
    -0.3,
    -0.5,
    -0.5,
    -0.7,
    -0.8,
    -0.7,
    -0.5,
    -0.4,
    -0.4
  ],
  "1955": [
    -0.5,
    -0.5,
    -0.6,
    -0.8,
    -0.8,
    -0.9,
    -0.7,
    -0.9,
    -1.1,
    -1.4,
    -1.6,
    -1.5
  ],
  "1956": [
    -1.2,
    -0.8,
    -0.6,
    -0.5,
    -0.5,
    -0.5,
    -0.5,
    -0.5,
    -0.4,
    -0.4,
    -0.4,
    -0.4
  ],
  "1957": [
    -0.3,
    -0.1,
    0.3,
    0.6,
    0.7,
    0.8,
    1.0,
    1.0,
    1.1,
    1.2,
    1.4,
    1.6
  ],
  "1958": [
    1.7,
    1.6,
    1.2,
    0.8,
    0.6,
    0.5,
    0.4,
    0.3,
    0.3,
    0.3,
    0.4,
    0.6
  ],
  "1959": [
    0.6,
    0.6,
    0.5,
    0.4,
    0.2,
    0.0,
    -0.2,
    -0.2,
    0.0,
    0.1,
    0.2,
    0.1
  ],
  "1960": [
    0.0,
    0.0,
    0.1,
    0.2,
    0.0,
    0.0,
    0.0,
    0.2,
    0.2,
    0.1,
    -0.1,
    -0.1
  ],
  "1961": [
    0.0,
    0.0,
    0.0,
    0.1,
    0.2,
    0.2,
    0.1,
    -0.2,
    -0.3,
    -0.2,
    -0.1,
    0.0
  ],
  "1962": [
    -0.2,
    -0.2,
    -0.1,
    -0.2,
    -0.2,
    -0.1,
    0.0,
    -0.1,
    -0.2,
    -0.2,
    -0.2,
    -0.3
  ],
  "1963": [
    -0.3,
    -0.2,
    0.0,
    0.1,
    0.1,
    0.5,
    0.8,
    1.1,
    1.1,
    1.1,
    1.2,
    1.1
  ],
  "1964": [
    0.9,
    0.5,
    0.1,
    -0.3,
    -0.6,
    -0.7,
    -0.7,
    -0.7,
    -0.7,
    -0.8,
    -0.8,
    -0.7
  ],
  "1965": [
    -0.5,
    -0.2,
    0.0,
    0.2,
    0.5,
    0.8,
    1.1,
    1.3,
    1.6,
    1.7,
    1.8,
    1.6
  ],
  "1966": [
    1.2,
    1.0,
    0.8,
    0.4,
    0.2,
    0.2,
    0.3,
    0.1,
    -0.1,
    -0.1,
    -0.2,
    -0.3
  ],
  "1967": [
    -0.5,
    -0.5,
    -0.5,
    -0.4,
    -0.1,
    0.1,
    0.0,
    -0.3,
    -0.4,
    -0.4,
    -0.4,
    -0.4
  ],
  "1968": [
    -0.6,
    -0.7,
    -0.6,
    -0.5,
    -0.1,
    0.2,
    0.4,
    0.4,
    0.3,
    0.5,
    0.7,
    0.9
  ],
  "1969": [
    1.0,
    1.0,
    0.8,
    0.7,
    0.6,
    0.5,
    0.4,
    0.4,
    0.6,
    0.7,
    0.8,
    0.7
  ],
  "1970": [
    0.5,
    0.2,
    0.2,
    0.3,
    0.1,
    -0.3,
    -0.5,
    -0.7,
    -0.7,
    -0.7,
    -0.8,
    -1.1
  ],
  "1971": [
    -1.3,
    -1.4,
    -1.1,
    -0.8,
    -0.7,
    -0.7,
    -0.7,
    -0.6,
    -0.7,
    -0.8,
    -0.9,
    -0.8
  ],
  "1972": [
    -0.6,
    -0.3,
    0.0,
    0.3,
    0.5,
    0.7,
    1.0,
    1.3,
    1.5,
    1.7,
    1.8,
    1.8
  ],
  "1973": [
    1.6,
    1.1,
    0.6,
    0.0,
    -0.5,
    -0.8,
    -1.0,
    -1.1,
    -1.3,
    -1.6,
    -1.9,
    -2.0
  ],
  "1974": [
    -1.9,
    -1.6,
    -1.2,
    -1.0,
    -0.7,
    -0.6,
    -0.5,
    -0.4,
    -0.5,
    -0.7,
    -0.9,
    -0.7
  ],
  "1975": [
    -0.6,
    -0.5,
    -0.6,
    -0.7,
    -0.8,
    -0.9,
    -1.1,
    -1.1,
    -1.3,
    -1.3,
    -1.5,
    -1.6
  ],
  "1976": [
    -1.5,
    -1.1,
    -0.6,
    -0.4,
    -0.2,
    0.0,
    0.2,
    0.4,
    0.6,
    0.8,
    0.8,
    0.8
  ],
  "1977": [
    0.7,
    0.7,
    0.3,
    0.3,
    0.3,
    0.5,
    0.4,
    0.4,
    0.5,
    0.7,
    0.8,
    0.8
  ],
  "1978": [
    0.7,
    0.5,
    0.2,
    -0.1,
    -0.3,
    -0.2,
    -0.4,
    -0.4,
    -0.4,
    -0.3,
    -0.1,
    0.1
  ],
  "1979": [
    0.2,
    0.2,
    0.3,
    0.3,
    0.3,
    0.1,
    0.1,
    0.2,
    0.3,
    0.5,
    0.5,
    0.6
  ],
  "1980": [
    0.6,
    0.5,
    0.4,
    0.3,
    0.5,
    0.4,
    0.2,
    -0.1,
    -0.2,
    -0.1,
    0.1,
    0.0
  ],
  "1981": [
    -0.3,
    -0.4,
    -0.4,
    -0.3,
    -0.3,
    -0.3,
    -0.3,
    -0.2,
    -0.1,
    -0.2,
    -0.2,
    -0.1
  ],
  "1982": [
    0.0,
    0.0,
    0.1,
    0.3,
    0.7,
    0.7,
    0.8,
    1.0,
    1.5,
    1.8,
    2.0,
    2.1
  ],
  "1983": [
    2.1,
    1.9,
    1.5,
    1.2,
    1.0,
    0.6,
    0.3,
    -0.1,
    -0.4,
    -0.8,
    -1.0,
    -0.9
  ],
  "1984": [
    -0.6,
    -0.5,
    -0.4,
    -0.5,
    -0.5,
    -0.5,
    -0.4,
    -0.2,
    -0.3,
    -0.6,
    -0.9,
    -1.1
  ],
  "1985": [
    -1.0,
    -0.9,
    -0.8,
    -0.8,
    -0.8,
    -0.6,
    -0.4,
    -0.3,
    -0.3,
    -0.3,
    -0.3,
    -0.4
  ],
  "1986": [
    -0.4,
    -0.4,
    -0.2,
    -0.2,
    -0.1,
    0.0,
    0.2,
    0.5,
    0.6,
    0.9,
    1.1,
    1.2
  ],
  "1987": [
    1.2,
    1.1,
    1.0,
    0.9,
    1.0,
    1.1,
    1.3,
    1.5,
    1.5,
    1.4,
    1.2,
    1.0
  ],
  "1988": [
    0.6,
    0.4,
    0.0,
    -0.4,
    -1.0,
    -1.3,
    -1.3,
    -1.1,
    -1.3,
    -1.5,
    -1.8,
    -1.8
  ],
  "1989": [
    -1.6,
    -1.4,
    -1.1,
    -0.8,
    -0.6,
    -0.4,
    -0.4,
    -0.4,
    -0.3,
    -0.2,
    -0.1,
    0.0
  ],
  "1990": [
    0.2,
    0.2,
    0.3,
    0.3,
    0.3,
    0.3,
    0.3,
    0.3,
    0.3,
    0.3,
    0.3,
    0.3
  ],
  "1991": [
    0.4,
    0.3,
    0.2,
    0.3,
    0.5,
    0.6,
    0.8,
    0.7,
    0.7,
    0.8,
    1.2,
    1.4
  ],
  "1992": [
    1.5,
    1.5,
    1.4,
    1.3,
    1.1,
    0.7,
    0.4,
    0.1,
    -0.1,
    -0.2,
    -0.2,
    0.0
  ],
  "1993": [
    0.1,
    0.3,
    0.5,
    0.7,
    0.8,
    0.6,
    0.3,
    0.2,
    0.2,
    0.2,
    0.2,
    0.2
  ],
  "1994": [
    0.1,
    0.0,
    0.0,
    0.2,
    0.3,
    0.2,
    0.3,
    0.3,
    0.5,
    0.7,
    0.9,
    1.0
  ],
  "1995": [
    0.9,
    0.7,
    0.5,
    0.2,
    0.0,
    -0.1,
    -0.3,
    -0.5,
    -0.8,
    -1.0,
    -1.0,
    -1.0
  ],
  "1996": [
    -0.9,
    -0.7,
    -0.5,
    -0.4,
    -0.2,
    -0.2,
    -0.2,
    -0.3,
    -0.3,
    -0.3,
    -0.4,
    -0.4
  ],
  "1997": [
    -0.4,
    -0.3,
    0.0,
    0.3,
    0.7,
    1.1,
    1.5,
    1.8,
    2.0,
    2.2,
    2.3,
    2.4
  ],
  "1998": [
    2.2,
    1.9,
    1.4,
    1.0,
    0.4,
    -0.1,
    -0.6,
    -0.8,
    -1.0,
    -1.1,
    -1.3,
    -1.5
  ],
  "1999": [
    -1.5,
    -1.2,
    -0.9,
    -0.8,
    -0.8,
    -0.8,
    -0.9,
    -0.9,
    -1.0,
    -1.1,
    -1.3,
    -1.5
  ],
  "2000": [
    -1.5,
    -1.3,
    -1.0,
    -0.8,
    -0.7,
    -0.6,
    -0.5,
    -0.4,
    -0.4,
    -0.5,
    -0.8,
    -0.8
  ],
  "2001": [
    -0.8,
    -0.5,
    -0.4,
    -0.3,
    -0.2,
    -0.1,
    0.0,
    -0.1,
    -0.1,
    -0.3,
    -0.3,
    -0.3
  ],
  "2002": [
    -0.1,
    0.1,
    0.1,
    0.2,
    0.3,
    0.5,
    0.6,
    0.6,
    0.8,
    1.0,
    1.2,
    1.1
  ],
  "2003": [
    0.9,
    0.6,
    0.4,
    0.0,
    -0.2,
    -0.1,
    0.1,
    0.1,
    0.2,
    0.2,
    0.3,
    0.3
  ],
  "2004": [
    0.3,
    0.3,
    0.2,
    0.1,
    0.1,
    0.2,
    0.4,
    0.5,
    0.6,
    0.6,
    0.6,
    0.7
  ],
  "2005": [
    0.6,
    0.6,
    0.4,
    0.4,
    0.3,
    0.1,
    0.0,
    -0.1,
    -0.1,
    -0.3,
    -0.6,
    -0.8
  ],
  "2006": [
    -0.9,
    -0.8,
    -0.6,
    -0.4,
    -0.2,
    0.0,
    0.1,
    0.3,
    0.5,
    0.7,
    0.9,
    0.9
  ],
  "2007": [
    0.6,
    0.2,
    -0.1,
    -0.3,
    -0.3,
    -0.4,
    -0.5,
    -0.8,
    -1.0,
    -1.4,
    -1.6,
    -1.7
  ],
  "2008": [
    -1.8,
    -1.6,
    -1.4,
    -1.0,
    -0.8,
    -0.6,
    -0.3,
    -0.2,
    -0.2,
    -0.4,
    -0.6,
    -0.8
  ],
  "2009": [
    -0.9,
    -0.8,
    -0.6,
    -0.3,
    0.0,
    0.3,
    0.5,
    0.6,
    0.7,
    0.9,
    1.3,
    1.5
  ],
  "2010": [
    1.5,
    1.2,
    0.9,
    0.4,
    -0.2,
    -0.7,
    -1.0,
    -1.2,
    -1.4,
    -1.5,
    -1.6,
    -1.5
  ],
  "2011": [
    -1.3,
    -1.1,
    -0.8,
    -0.7,
    -0.5,
    -0.3,
    -0.4,
    -0.5,
    -0.8,
    -0.9,
    -1.0,
    -0.9
  ],
  "2012": [
    -0.7,
    -0.6,
    -0.4,
    -0.3,
    -0.2,
    0.0,
    0.3,
    0.4,
    0.4,
    0.3,
    0.1,
    0.0
  ],
  "2013": [
    -0.2,
    -0.3,
    -0.2,
    -0.2,
    -0.3,
    -0.4,
    -0.4,
    -0.3,
    -0.3,
    -0.1,
    -0.1,
    -0.1
  ],
  "2014": [
    -0.2,
    -0.2,
    0.0,
    0.3,
    0.4,
    0.2,
    0.1,
    0.1,
    0.2,
    0.5,
    0.7,
    0.8
  ],
  "2015": [
    0.7,
    0.7,
    0.7,
    0.9,
    1.0,
    1.2,
    1.4,
    1.7,
    2.0,
    2.3,
    2.5,
    2.6
  ],
  "2016": [
    2.5,
    2.2,
    1.7,
    1.1,
    0.6,
    0.1,
    -0.2,
    -0.3,
    -0.4,
    -0.5,
    -0.5,
    -0.4
  ],
  "2017": [
    -0.1,
    0.1,
    0.3,
    0.3,
    0.4,
    0.3,
    0.1,
    -0.1,
    -0.2,
    -0.4,
    -0.6,
    -0.8
  ],
  "2018": [
    -0.7,
    -0.7,
    -0.5,
    -0.3,
    -0.1,
    0.1,
    0.2,
    0.3,
    0.5,
    0.8,
    1.0,
    1.1
  ],
  "2019": [
    1.0,
    0.9,
    0.9,
    0.8,
    0.7,
    0.6,
    0.4,
    0.2,
    0.3,
    0.5,
    0.7,
    0.8
  ],
  "2020": [
    0.7,
    0.7,
    0.6,
    0.3,
    0.0,
    -0.2,
    -0.3,
    -0.4,
    -0.8,
    -1.0,
    -1.1,
    -1.1
  ],
  "2021": [
    -1.0,
    -0.9,
    -0.7,
    -0.6,
    -0.4,
    -0.3,
    -0.3,
    -0.5,
    -0.6,
    -0.8,
    -0.9,
    -0.8
  ],
  "2022": [
    -0.8,
    -0.7,
    -0.8,
    -0.9,
    -0.8,
    -0.7,
    -0.7,
    -0.8,
    -0.9,
    -0.9,
    -0.8,
    -0.7
  ],
  "2023": [
    -0.5,
    -0.3,
    -0.1,
    0.2,
    0.5,
    0.7,
    1.0,
    1.3,
    1.5,
    1.7,
    1.9,
    2.0
  ],
  "2024": [
    1.8,
    1.5,
    1.2,
    0.8,
    0.4,
    0.2,
    0.1,
    0.0,
    -0.1,
    -0.2,
    -0.3,
    -0.4
  ],
  "2025": [
    -0.5,
    -0.2,
    -0.1,
    0.0,
    0.0,
    0.0,
    -0.1,
    -0.3,
    -0.4,
    -0.6,
    -0.6,
    -0.6
  ],
  "2026": [
    -0.4,
    -0.2,
    0.1,
    0.5,
    0.9,
    1.4,
    1.8,
    2.2,
    null,
    null,
    null,
    null
  ]
}''')

def clasificar_oni():
    """Umbral ±0.5 en 5 trimestres móviles consecutivos, cruzando años.
    Fase anual: moda de los 12 trimestres, no clasificación oficial anual.
    Se preservan los valores del adjunto; HIJO se interpreta como SON.
    """
    registros = [(int(a), t, v) for a, valores in sorted(ONI.items())
                 for t, v in zip(TRIMESTRES, valores)]
    tabla = pd.DataFrame(registros, columns=['ANIO', 'TRIMESTRE', 'ONI'])
    v = tabla.ONI.to_numpy(dtype=float)
    signos = np.where(v >= .5, 1, np.where(v <= -.5, -1, 0))
    fase = np.full(len(v), 'Neutral', dtype=object)
    inicio = 0
    while inicio < len(v):
        fin = inicio + 1
        while fin < len(v) and signos[fin] == signos[inicio]:
            fin += 1
        if signos[inicio] != 0 and fin - inicio >= 5:
            fase[inicio:fin] = 'El Niño' if signos[inicio] == 1 else 'La Niña'
        inicio = fin
    fase[~np.isfinite(v)] = 'S/D'
    tabla['FASE'] = fase
    anuales = []
    for anio, g in tabla.groupby('ANIO'):
        if g.ONI.notna().sum() != 12:
            anuales.append((anio, 'S/D', np.nan))
            continue
        cuentas = g.FASE.value_counts()
        ganadoras = [f for f in COLORES if cuentas.get(f, 0) == cuentas.max()]
        anuales.append((anio, ' / '.join(ganadoras), g.ONI.mean()))
    return tabla, pd.DataFrame(anuales, columns=['ANIO', 'FASE_ANUAL', 'ONI_MEDIO'])



def ajustar(tabla):
    d=tabla.dropna(subset=['ANOMALIA_MM','ONI'])
    if len(d)<3:
        return np.nan,np.nan,np.nan
    tiempo=d.index.year+(d.index.month-1)/12
    pendiente,intercepto=np.polyfit(tiempo-INICIO,d.ANOMALIA_MM,1)
    correlacion=d.ANOMALIA_MM.corr(d.ONI)
    return pendiente,intercepto,correlacion


def leer_eventos():
    if not ARCHIVO_EVENTOS.exists():
        raise FileNotFoundError(f'No se encuentra el archivo de eventos: {ARCHIVO_EVENTOS}')
    libro=pd.ExcelFile(ARCHIVO_EVENTOS)
    tablas=[]
    for hoja in libro.sheet_names:
        nombre_hoja = str(hoja).strip()
        if not (nombre_hoja.isdigit() and len(nombre_hoja)==4):
            continue  # No contar nuevamente la hoja consolidada "todo".
        e=pd.read_excel(libro,sheet_name=hoja).dropna(how='all')
        e.columns=e.columns.astype(str).str.strip().str.lower()
        if not {'evento','fecha','precip'}.issubset(e.columns):
            raise ValueError(f'Faltan columnas de eventos en {hoja}.')
        # Rechazar horas sin fecha antes de interpretar el calendario.
        from datetime import time, date, datetime
        horas = e.fecha.map(lambda v: isinstance(v, time))
        if horas.any():
            eventos_invalidos = e.loc[horas, 'evento'].astype(str).tolist()
            raise ValueError(f'Hoja {hoja}: fecha contiene solo una hora en eventos {eventos_invalidos}. Corregir en la fuente; no se excluyen registros automáticamente.')
        e['fecha']=pd.to_datetime(e.fecha,errors='raise').dt.normalize()
        e['evento']=pd.to_numeric(e.evento,errors='raise')
        if e.fecha.isna().any() or e.evento.isna().any() or (e.evento%1!=0).any():
            raise ValueError(f'Fechas o números de evento inválidos en {hoja}.')
        if not e.fecha.dt.year.eq(int(nombre_hoja)).all():
            raise ValueError(f'Fechas fuera del año de la hoja {hoja}.')
        e['anio']=int(nombre_hoja)
        e['precip']=pd.to_numeric(e.precip,errors='raise')
        if e.precip.dropna().lt(0).any() or np.isinf(e.precip).any():
            raise ValueError('Precipitación de evento negativa o infinita.')
        e['mes_fecha']=e.fecha.dt.to_period('M').dt.to_timestamp()
        tablas.append(e)
    if not tablas:
        raise ValueError('No se encontraron hojas por año en eventos.')
    e=pd.concat(tablas,ignore_index=True).sort_values(['fecha','evento'])
    if e.duplicated(['anio','evento']).any():
        raise ValueError('Se repite un número de evento dentro del mismo año. Revisar antes de contar.')
    conteos=[]
    for anio,g in e.groupby('anio'):
        idx=pd.date_range(g.mes_fecha.min(),g.mes_fecha.max(),freq='MS',name='FECHA')
        tabla=g.groupby('mes_fecha').size().reindex(idx,fill_value=0).rename('EVENTOS_REGISTRADOS').to_frame()
        tabla['ANIO']=anio
        conteos.append(tabla)
    c=pd.concat(conteos).sort_index()
    e.to_csv(SALIDA/'Eventos_RUEMAG_sin_duplicar.csv',index=False,encoding='utf-8-sig')
    c.to_csv(SALIDA/'Eventos_RUEMAG_por_mes.csv',encoding='utf-8-sig')
    return e,c


def superponer_conteos(ax,conteos,inicio,fin):
    c=conteos.loc[str(inicio):str(fin)]
    if c.empty:
        return
    derecha=ax.twinx()
    derecha.bar(c.index+pd.Timedelta(days=14),c.EVENTOS_REGISTRADOS,width=19,
                 color='#783ca0',alpha=.45,label='Eventos registrados / mes',zorder=1)
    derecha.set_ylim(0,max(5,conteos.EVENTOS_REGISTRADOS.max()*1.35))
    derecha.set_ylabel('Eventos registrados / mes',color='#783ca0',fontsize=10)
    derecha.tick_params(axis='y',labelcolor='#783ca0')
    derecha.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    derecha.spines[['top','left']].set_visible(False)
    derecha.grid(False)


def graficar_detalle_eventos(m,base,oni,eventos,conteos):
    anios=sorted(eventos.anio.unique())
    fig,axes=plt.subplots(len(anios),1,figsize=(16,3.4*len(anios)+2),squeeze=False,sharey=True)
    fig.subplots_adjust(left=.07,right=.91,top=.84,bottom=.105,hspace=.43)
    fig.suptitle(f'{ESTACION} · Eventos de tormenta, precipitación y ENSO',fontsize=21,x=.07,ha='left',y=.975)
    handles=[Patch(color=c,alpha=.6,label=f) for f,c in COLORES.items()]+[
        Patch(facecolor='white',edgecolor='#999999',hatch='///',label='ONI sin dato'),
        Line2D([0],[0],color='#14648b',label='Lluvia mensual de la base'),
        Line2D([0],[0],color='#207647',ls='--',label='Climatología mensual'),
        Line2D([0],[0],color='#8b1a76',marker='o',lw=0,label='Lluvia por evento RUEMAG'),
        Patch(color='#783ca0',alpha=.45,label='Eventos registrados / mes')]
    fig.legend(handles=handles,loc='upper left',bbox_to_anchor=(.065,.936),ncol=4,frameon=False,fontsize=10)
    for ax,anio in zip(axes[:,0],anios):
        idx=pd.date_range(f'{anio}-01-01',f'{anio}-12-01',freq='MS')
        for fecha in idx:
            fase=oni.FASE.get(fecha,'S/D')
            if fase in COLORES:
                ax.axvspan(fecha,fecha+pd.offsets.MonthBegin(1),color=COLORES[fase],alpha=.38,lw=0)
            else:
                ax.axvspan(fecha,fecha+pd.offsets.MonthBegin(1),facecolor='white',edgecolor='#dddddd',hatch='///',lw=0)
        d=m.reindex(idx)
        ax.plot(idx,d.PRECIP_ANALISIS_MM,color='#14648b',lw=2)
        ax.plot(idx,[base.CLIMATOLOGIA_MM.loc[t.month] for t in idx],color='#207647',ls='--',lw=1.5)
        g=eventos[eventos.anio.eq(anio)]
        ax.scatter(g.fecha,g.precip,color='#8b1a76',s=22,alpha=.8,zorder=4,edgecolors='white',linewidths=.3)
        ax.set_title(f'{anio}: {len(g)} eventos registrados | {g.fecha.min():%d/%m}–{g.fecha.max():%d/%m}',loc='left',fontsize=12,fontweight='bold')
        ax.set_xlim(pd.Timestamp(int(anio),1,1),pd.Timestamp(int(anio)+1,1,1))
        ax.set_xticks(idx+pd.Timedelta(days=14));ax.set_xticklabels(MESES)
        ax.set_ylim(0,max(m.PRECIP_ANALISIS_MM.max(),eventos.precip.max())*1.08)
        ax.set_ylabel('Precipitación (mm)');ax.grid(axis='y',alpha=.17)
        ax.spines[['top','right']].set_visible(False)
        superponer_conteos(ax,conteos,anio,anio)
        if d.PRECIP_OBSERVADA_MM.isna().all():
            ax.text(.02,.9,'Sin precipitación mensual en la base para este año',transform=ax.transAxes,fontsize=10,color='#4c5967')
    fig.text(.07,.055,'Los puntos son registros individuales RUEMAG, con zonas distintas; no se suman a la precipitación mensual de la base.',fontsize=10,color='#4c5967')
    fig.text(.07,.030,'Barras: eventos registrados. Fuera del periodo del catálogo no se asume cero eventos. ONI ERSSTv6 disponible hasta JAS de 2026 (últimos valores revisables).',fontsize=10,color='#4c5967')
    guardar_publicacion(fig, SALIDA/'04_Detalle_eventos_RUEMAG_ENSO.png', estudio=f'catálogo de eventos {eventos.fecha.min():%d/%m/%Y}–{eventos.fecha.max():%d/%m/%Y}', climatologia=f'{BASE_INICIO}–{BASE_FIN}', detalle=f'Serie mensual de referencia: {INICIO}–{FIN}. Fechas extremas del catálogo; no acreditan cobertura continua.')


def main():
    SALIDA.mkdir(parents=True,exist_ok=True)
    eventos,conteos_eventos=leer_eventos()
    print('Archivo de eventos leído:', ARCHIVO_EVENTOS.resolve())
    print('Eventos por año:', eventos.groupby('anio').size().to_dict())
    if 2023 not in eventos.anio.values:
        raise ValueError('Falta 2023 en el Excel leído. Revisa ARCHIVO_EVENTOS y guarda la copia actualizada.')
    x=pd.read_excel(ARCHIVO,sheet_name='PRECIP')
    x.columns=x.columns.str.strip().str.upper()
    x['FECHA']=pd.to_datetime(x.FECHA,errors='raise')
    if x.FECHA.isna().any() or x.FECHA.duplicated().any():
        raise ValueError('Fechas vacías o duplicadas: resolver antes del análisis.')
    if not x.FECHA.eq(x.FECHA.dt.normalize()).all():
        raise ValueError('Se esperaba una base diaria sin horas.')
    x['PRECIP']=pd.to_numeric(x.PRECIP,errors='raise')
    if (x.PRECIP.dropna()<0).any() or np.isinf(x.PRECIP).any():
        raise ValueError('Precipitación negativa o infinita.')
    # Conservar todas las fechas: las ausentes se vuelven NaN, nunca cero.
    diario=x.set_index('FECHA').PRECIP.sort_index().reindex(
        pd.date_range(f'{INICIO}-01-01',f'{FIN}-12-31',name='FECHA'))
    m=pd.DataFrame({'PRECIP_OBSERVADA_MM':diario.resample('MS').sum(min_count=1),
                    'DIAS_VALIDOS':diario.resample('MS').count(),
                    'DIAS_ESPERADOS':diario.resample('MS').size()})
    m['DIAS_FALTANTES']=m.DIAS_ESPERADOS-m.DIAS_VALIDOS
    m['ESTADO']=np.where(m.DIAS_VALIDOS.eq(0),'SIN_DATOS',
                          np.where(m.DIAS_FALTANTES.eq(0),'SIN_FALTANTES_DIARIOS','PARCIAL'))
    m['MES']=m.index.month
    m['PRECIP_ANALISIS_MM']=m.PRECIP_OBSERVADA_MM.where(
        m.DIAS_FALTANTES.eq(0)&~m.index.year.isin(ANIOS_EXCLUIDOS))
    # Cada mes usa su propio promedio 1991–2020, omitiendo meses parciales.
    base=m.loc[f'{BASE_INICIO}':f'{BASE_FIN}'].groupby('MES').PRECIP_ANALISIS_MM.agg(['mean','count'])
    base=base.reindex(range(1,13)).rename(columns={'mean':'CLIMATOLOGIA_MM','count':'N_ANIOS'})
    if base.CLIMATOLOGIA_MM.isna().any():
        raise ValueError('Falta climatología para algún mes del año.')
    m['CLIMATOLOGIA_MM']=m.MES.map(base.CLIMATOLOGIA_MM)
    m['ANOMALIA_MM']=m.PRECIP_ANALISIS_MM-m.CLIMATOLOGIA_MM
    # ONI es trimestral móvil. Se asigna por el mes central, no se convierte
    # en índice mensual independiente: DJF→enero, JFM→febrero, ..., NDJ→diciembre.
    oni,_=clasificar_oni()
    oni['MES']=oni.TRIMESTRE.map({t:i+1 for i,t in enumerate(TRIMESTRES)})
    oni['FECHA']=pd.to_datetime(dict(year=oni.ANIO,month=oni.MES,day=1))
    oni=oni.set_index('FECHA')
    m=m.join(oni[['TRIMESTRE','ONI','FASE']])
    m=m.join(conteos_eventos[['EVENTOS_REGISTRADOS']])
    eventos=eventos.join(oni[['ONI','FASE']],on='mes_fecha')
    eventos.to_csv(SALIDA/'Eventos_RUEMAG_con_ONI.csv',index=False,encoding='utf-8-sig')
    if m.ONI.isna().any():
        raise ValueError('El periodo solicitado no tiene ONI completo en la tabla adjunta.')
    pendiente,intercepto,r=ajustar(m)
    m['TENDENCIA_ANOMALIA_MM']=intercepto+pendiente*(m.index.year+(m.index.month-1)/12-INICIO)
    m['REFERENCIA_CLIMA_MAS_TENDENCIA_MM']=m.CLIMATOLOGIA_MM+m.TENDENCIA_ANOMALIA_MM
    # Esta referencia puede ser negativa en meses secos: no se grafica como
    # precipitación pronosticada. La tendencia se muestra aparte en anomalías.
    comp=m.dropna(subset=['PRECIP_ANALISIS_MM']).groupby(['MES','FASE']).agg(
        PRECIP_MEDIA_MM=('PRECIP_ANALISIS_MM','mean'),
        ANOMALIA_MEDIA_MM=('ANOMALIA_MM','mean'),N_MESES=('PRECIP_ANALISIS_MM','count'))
    fases=m.dropna(subset=['ANOMALIA_MM']).groupby('FASE').agg(
        N_MESES=('ANOMALIA_MM','count'),ANOMALIA_MEDIA_MM=('ANOMALIA_MM','mean'))
    m.to_csv(SALIDA/'Serie_mensual_ONI_1991_2025.csv',encoding='utf-8-sig',float_format='%.4f')
    base.to_csv(SALIDA/'Climatologia_mensual_1991_2020.csv',encoding='utf-8-sig',float_format='%.4f')
    comp.to_csv(SALIDA/'Comparacion_por_mes_y_fase.csv',encoding='utf-8-sig',float_format='%.4f')
    fases.to_csv(SALIDA/'Resumen_por_fase.csv',encoding='utf-8-sig',float_format='%.4f')
    diario[diario.isna()].rename('PRECIP').to_csv(SALIDA/'Fechas_sin_dato.csv',encoding='utf-8-sig')

    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11})
    # Figura 1: serie completa con fondos por fase; no unir meses parciales.
    fig,axes=plt.subplots(3,1,figsize=(18,11),sharey=True)
    fig.subplots_adjust(left=.065,right=.91,top=.84,bottom=.10,hspace=.37)
    fig.suptitle(f'{ESTACION} · Precipitación mensual y ENSO',x=.065,ha='left',y=.98,fontsize=24)
    fig.text(.065,.935,f'{INICIO}–{FIN} | Climatología {BASE_INICIO}–{BASE_FIN}',fontsize=14,color='#4c5967')
    bloques=np.array_split(np.arange(INICIO,FIN+1),3)
    for ax,anios in zip(axes,bloques):
        d=m.loc[str(anios[0]):str(anios[-1])]
        for fecha,fila in d.iterrows():
            ax.axvspan(fecha,fecha+pd.offsets.MonthBegin(1),color=COLORES[fila.FASE],alpha=.48,lw=0)
        ax.plot(d.index,d.PRECIP_ANALISIS_MM,color='#14648b',lw=1.5,zorder=3)
        ax.plot(d.index,d.CLIMATOLOGIA_MM,color='#207647',lw=1.3,ls='--',zorder=2)
        parcial=d[d.DIAS_FALTANTES.gt(0)]
        ax.scatter(parcial.index,parcial.PRECIP_OBSERVADA_MM,color='#bb660b',marker='D',s=32,zorder=4)
        ax.set_title(f'{anios[0]}–{anios[-1]}',loc='left',fontweight='bold',fontsize=12)
        ax.set_xlim(pd.Timestamp(int(anios[0]),1,1),pd.Timestamp(int(anios[-1])+1,1,1))
        ax.set_ylim(0,m.PRECIP_OBSERVADA_MM.max()*1.10)
        ax.set_ylabel('Precipitación (mm)')
        ax.xaxis.set_major_locator(mdates.YearLocator());ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax.grid(axis='y',alpha=.18);ax.spines[['top','right']].set_visible(False)
        ev=eventos[eventos.anio.between(int(anios[0]),int(anios[-1]))]
        ax.scatter(ev.fecha,ev.precip,color='#0087df',s=22,alpha=.85,
                   edgecolors='white',linewidths=.25,zorder=5)
        ax.set_ylim(0,max(m.PRECIP_OBSERVADA_MM.max(),
                          eventos.loc[eventos.anio.between(INICIO,FIN),'precip'].max())*1.10)
    handles=[Patch(color=c,alpha=.65,label=f) for f,c in COLORES.items()]+[
        Line2D([0],[0],color='#14648b',label='Acumulado mensual'),
        Line2D([0],[0],color='#207647',ls='--',label='Climatología mensual'),
        Line2D([0],[0],color='#bb660b',marker='D',lw=0,label='Acumulado parcial'),
        Line2D([0],[0],color='#0087df',marker='o',lw=0,label='Lluvia por tormenta RUEMAG (mm)')]
    fig.legend(handles=handles,loc='upper left',bbox_to_anchor=(.06,.905),ncol=4,frameon=False,fontsize=10)
    fig.text(.065,.047,'Puntos: lluvia por tormenta RUEMAG en su fecha real (2023–2025); no se suma al acumulado mensual histórico.',fontsize=10,color='#4c5967')
    fig.text(.065,.025,'2022–2023: acumulados IAM observados; la presencia de un valor diario no garantiza cobertura intradiaria completa.',fontsize=10,color='#4c5967')
    guardar_publicacion(fig, SALIDA/'01_Precipitacion_mensual_ENSO.png', estudio=f'{INICIO}–{FIN}', climatologia=f'{BASE_INICIO}–{BASE_FIN}')

    # Figura 2: tendencia de anomalías, sin confundir estacionalidad y tendencia.
    fig2,ax=plt.subplots(figsize=(18,6));fig2.subplots_adjust(left=.065,right=.91,top=.78,bottom=.20)
    for fecha,fila in m.iterrows():
        ax.axvspan(fecha,fecha+pd.offsets.MonthBegin(1),color=COLORES[fila.FASE],alpha=.40,lw=0)
    ax.plot(m.index,m.ANOMALIA_MM,color='#14648b',lw=1,label='Anomalía mensual')
    ax.axhline(0,color='#64748b',lw=1)
    ax.plot(m.index,m.TENDENCIA_ANOMALIA_MM,color='#7439a0',lw=2.4,
            label=f'Tendencia: {pendiente*10:+.2f} mm/década')
    ax.set(xlim=(m.index.min(),pd.Timestamp(FIN+1,1,1)),ylabel='Anomalía de precipitación mensual (mm)',xlabel='Año')
    ax.xaxis.set_major_locator(mdates.YearLocator(2));ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.grid(axis='y',alpha=.2);ax.spines[['top','right']].set_visible(False);ax.legend(frameon=False,loc='upper left',bbox_to_anchor=(0,1.16),ncol=2)
    superponer_conteos(ax,conteos_eventos,INICIO,FIN)
    fig2.suptitle(f'{ESTACION} · Anomalías mensuales y tendencia, {INICIO}–{FIN}',fontsize=21,y=.98)
    fig2.text(.065,.065,'Anomalía = acumulado mensual − climatología de ese mes. Tendencia lineal descriptiva; no es atribución a ENSO.',fontsize=10,color='#4c5967')
    fig2.text(.065,.027,'La pendiente corresponde a lluvia mensual. Barras moradas: eventos/mes (eje derecho); fondo ENSO: colores de la figura 1.',fontsize=10,color='#4c5967')
    guardar_publicacion(fig2, SALIDA/'02_Anomalias_mensuales_tendencia.png', estudio=f'{INICIO}–{FIN}', climatologia=f'{BASE_INICIO}–{BASE_FIN}')

    # Figura 3: comparar el mismo mes entre fases para no mezclar estaciones.
    fig3,ax=plt.subplots(figsize=(13,7));fig3.subplots_adjust(left=.09,right=.97,top=.80,bottom=.19)
    for fase,color in [('El Niño','#c85a45'),('La Niña','#2287bd'),('Neutral','#707784')]:
        serie=comp.xs(fase,level='FASE').PRECIP_MEDIA_MM.reindex(range(1,13))
        ax.plot(range(1,13),serie,'-o',color=color,lw=2,label=fase)
    ax.plot(range(1,13),base.CLIMATOLOGIA_MM,'--',color='#207647',lw=2,label='Climatología 1991–2020')
    ax.set(xticks=range(1,13),xticklabels=MESES,ylabel='Precipitación mensual media (mm)',ylim=(0,None))
    ax.grid(axis='y',alpha=.2);ax.spines[['top','right']].set_visible(False)
    ax.legend(ncol=4,frameon=False,loc='upper center',bbox_to_anchor=(.5,1.17))
    fig3.suptitle(f'{ESTACION} · Lluvia mensual según fase ENSO',fontsize=21,y=.96)
    fig3.text(.09,.082,f'Medias de {INICIO}–{FIN}; se compara cada mes del calendario. Tamaños de muestra en el CSV por mes y fase.',fontsize=10,color='#4c5967')
    fig3.text(.09,.045,'Diferencias descriptivas: no implican causalidad ni significancia estadística. IAM 2022–2023 conserva limitaciones de cobertura.',fontsize=9.5,color='#4c5967')
    guardar_publicacion(fig3, SALIDA/'03_Lluvia_por_mes_y_fase_ENSO.png', estudio=f'{INICIO}–{FIN}', climatologia=f'{BASE_INICIO}–{BASE_FIN}')

    graficar_detalle_eventos(m,base,oni,eventos,conteos_eventos)

    # Sensibilidad histórica 2021–2023; IAM corresponde a 2022–2023.
    ps,_,rs=ajustar(m[~m.index.year.isin([2021,2022,2023])])
    texto=f'''ANÁLISIS EXPLORATORIO MENSUAL: {ESTACION}, {INICIO}–{FIN}
Fuente de precipitación: {ARCHIVO.name}
ONI: valores de la tabla adjunta del usuario, sin sustituirlos por otra versión.
Criterio histórico: umbral ±0.5 °C durante al menos 5 trimestres móviles consecutivos.
Fuente del criterio: https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/oni/v6/
El encabezado traducido HIJO se interpreta como SON. Clasificación calculada cruzando límites de año.
DJF→enero; JFM→febrero; ...; NDJ→diciembre. ONI sigue siendo una media trimestral.

Días sin dato: {int(diario.isna().sum())}. Meses: {len(m)}.
Meses sin faltantes diarios: {int(m.DIAS_FALTANTES.eq(0).sum())}.
Meses usados en estadísticas: {int(m.PRECIP_ANALISIS_MM.notna().sum())}.
Climatología: promedio separado por mes de {BASE_INICIO}–{BASE_FIN}, excluyendo meses parciales.
Suma de las 12 climatologías mensuales: {base.CLIMATOLOGIA_MM.sum():.2f} mm.
Esta suma no es el promedio de acumulados anuales parciales.
Tendencia de anomalías mensuales: {pendiente*10:+.3f} mm/década.
Correlación Pearson ONI–anomalía mensual, sin desfase: r={r:.3f}.
Sensibilidad excluyendo 2021–2023: pendiente {ps*10:+.3f} mm/década; r={rs:.3f}.

RESUMEN POR FASE (meses válidos disponibles; mezcla de meses puede variar entre fases)
{fases.to_string(float_format=lambda v:f'{v:.2f}')}

EVENTOS RUEMAG
Fuente: {ARCHIVO_EVENTOS.name}. Se leen solo hojas por año; se omite todo para evitar doble conteo.
Eventos por año: {eventos.groupby("anio").size().to_dict()}.
Conteos por fecha de evento, sin sumar la lluvia de diferentes zonas al total mensual de la base.
La base termina en 2025: los eventos 2026 se muestran en una figura de detalle independiente.
ONI 2026 del adjunto termina en JJA; meses posteriores figuran sin dato.
No se infiere ausencia de tormentas fuera del periodo con registros en el catálogo.

LIMITACIONES
Los datos IAM 2022–2023 pueden tener intervalos ausentes aunque exista suma diaria.
No se ha confirmado aquí la equivalencia de estación/instrumento/corte diario respecto de la serie histórica.
No se rellenan faltantes, no se convierten a cero, no se estiman totales de meses parciales.
La correlación y tendencia son descriptivas. No se calcula significancia con supuestos de independencia:
ONI usa trimestres superpuestos y las series pueden tener autocorrelación.
La tendencia temporal no mide por sí misma el efecto de ENSO. No se atribuye causalidad.
Para interpretar diferencias estacionales usar Comparacion_por_mes_y_fase.csv y sus tamaños de muestra.
ANIOS_EXCLUIDOS configurados: {ANIOS_EXCLUIDOS}
'''
    (SALIDA/'LEEME_resultados.txt').write_text(texto,encoding='utf-8')
    print(texto)
    print('Resultados en:',SALIDA)
    # La visualización se hace una sola vez, después de generar todo.
    if not MOSTRAR_GRAFICAS:
        plt.close('all')
    return m


# ================= ESTUDIOS ESTADÍSTICOS ENSO =================
def holm(p):
    """Ajuste Holm: controla error familiar sin exigir pruebas independientes."""
    p = np.asarray(p, float)
    q = np.full(p.shape, np.nan)
    validos = np.flatnonzero(np.isfinite(p))
    orden = validos[np.argsort(p[validos])]
    if len(orden):
        q[orden] = np.minimum(1, np.maximum.accumulate(
            p[orden] * np.arange(len(orden), 0, -1)))
    return q


def correlaciones(d, x):
    v = pd.DataFrame({'x': x, 'y': d.ANOMALIA_MM}).dropna()
    r = rho = np.nan
    if len(v) >= 3 and v.x.nunique() > 1 and v.y.nunique() > 1:
        r = v.x.corr(v.y)
        rho = float(spearmanr(v.x, v.y).statistic)
    return {'N': len(v), 'Pearson_r': r, 'Spearman_rho': rho,
            'r2_bivariado': r*r if np.isfinite(r) else np.nan}


def modelo(d, predictores, ventana=HAC_MESES):
    """OLS con efectos de mes y tendencia; HAC sobre el calendario completo.

    Las filas sin observación tienen score cero; NO se imputa su lluvia.
    Esto evita tratar dos observaciones separadas por un hueco como contiguas.
    Bartlett/Newey-West, corrección n/(n-k), aproximación normal asintótica.
    """
    ncal = len(d)
    x = pd.DataFrame({'constante': np.ones(ncal)}, index=d.index)
    for c in predictores:
        x[c] = predictores[c]
    x['tiempo_decadas'] = np.arange(ncal) / 120
    presentes = sorted(d.loc[d.ANOMALIA_MM.notna(), 'MES'].unique())
    for mes in presentes[1:]:
        x[f'mes_{mes}'] = (d.MES == mes).astype(float)
    y = d.ANOMALIA_MM.to_numpy(float)
    X = x.to_numpy(float)
    ok = np.isfinite(y) & np.isfinite(X).all(axis=1)
    A, b = X[ok], y[ok]
    n, k = A.shape
    vacio = {c: {'N': n, 'beta_mm': np.nan, 'IC95_inf': np.nan,
                  'IC95_sup': np.nan, 'p_HAC': np.nan,
                  'R2_modelo': np.nan, 'estado': 'Muestra insuficiente o diseño singular'}
             for c in predictores}
    if n < max(30, k + 10) or np.linalg.matrix_rank(A) < k:
        return vacio
    beta = np.linalg.lstsq(A, b, rcond=None)[0]
    residuo = b - A @ beta
    scores = np.zeros((ncal, k))
    scores[ok] = A * residuo[:, None]
    S = scores.T @ scores
    for lag in range(1, min(ventana, ncal-1) + 1):
        cruz = scores[lag:].T @ scores[:-lag]
        S += (1 - lag/(ventana+1)) * (cruz + cruz.T)
    bread = np.linalg.inv(A.T @ A)
    cov = bread @ S @ bread * n/(n-k)
    se = np.sqrt(np.maximum(np.diag(cov), 0))
    total = np.sum((b - b.mean())**2)
    r2 = 1 - np.sum(residuo**2)/total if total > 0 else np.nan
    resultado = {}
    for c in predictores:
        j = x.columns.get_loc(c)
        p = 2*norm.sf(abs(beta[j]/se[j])) if se[j] > 0 else np.nan
        resultado[c] = dict(N=n, beta_mm=beta[j], IC95_inf=beta[j]-1.96*se[j],
                            IC95_sup=beta[j]+1.96*se[j], p_HAC=p,
                            R2_modelo=r2, estado='Estimado; inferencia aproximada')
    return resultado


def tabla_relacion(d, grupos):
    filas = []
    for nombre, meses in grupos.items():
        for lag in range(MAX_DESFASE+1):
            # El ONI de t-lag se calcula ANTES de seleccionar meses.
            x = d.ONI.shift(lag)
            sub = d.copy()
            sub.loc[~sub.MES.isin(meses), 'ANOMALIA_MM'] = np.nan
            fila = dict(grupo=nombre, desfase_meses=lag, HAC_meses=HAC_MESES)
            fila.update(correlaciones(sub, x))
            fila.update(modelo(sub, pd.DataFrame({'ONI': x}))['ONI'])
            filas.append(fila)
    return pd.DataFrame(filas)


def guardar_fig(fig, nombre, salida):
    guardar_publicacion(fig, salida / f'{nombre}.png', estudio=f'{INICIO}–{FIN}', climatologia=f'{BASE_INICIO}–{BASE_FIN}')
    if not MOSTRAR_GRAFICAS:
        plt.close(fig)


def ejecutar(d, salida):
    salida = Path(salida)
    salida.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'axes.spines.top': False, 'axes.spines.right': False})
    grupos = {'Todos los meses': list(range(1, 13)), 'Jun-Sep': [6, 7, 8, 9],
              'Nov-Abr': [11, 12, 1, 2, 3, 4]}
    relacion = tabla_relacion(d, grupos)
    mensual = tabla_relacion(d, {MESES[i-1]: [i] for i in range(1, 13)})
    # Contrastes de fases, controlando composición mensual y tendencia.
    fases = []
    for nombre, meses in grupos.items():
        sub = d.copy()
        sub.loc[~sub.MES.isin(meses) | ~sub.FASE.isin(FASES), 'ANOMALIA_MM'] = np.nan
        for referencia in ['Neutral', 'La Niña']:
            otros = [f for f in FASES if f != referencia]
            pred = pd.DataFrame({f: (sub.FASE == f).astype(float) for f in otros}, index=sub.index)
            ajustes = modelo(sub, pred)
            for fase in otros:
                if referencia == 'La Niña' and fase != 'El Niño':
                    continue
                fila = dict(grupo=nombre, contraste=f'{fase} − {referencia}',
                            n_fase=int((sub.ANOMALIA_MM.notna() & sub.FASE.eq(fase)).sum()),
                            n_referencia=int((sub.ANOMALIA_MM.notna() & sub.FASE.eq(referencia)).sum()))
                fila.update(ajustes[fase])
                fases.append(fila)
    fases = pd.DataFrame(fases)
    # Una sola familia: todos los coeficientes ONI y contrastes de fase principales.
    tablas = [relacion, mensual, fases]
    q = holm(np.concatenate([t.p_HAC.to_numpy() for t in tablas]))
    inicio = 0
    for t in tablas:
        t['p_Holm'] = q[inicio:inicio+len(t)]
        t['evidencia_ajustada_005'] = t.p_Holm.lt(.05)
        inicio += len(t)

    sensibilidad = []
    for nombre, excluidos in [('Serie disponible', []), ('Sin años IAM', ANIOS_SENSIBILIDAD),
                              ('Sin 2021-2023', [2021, 2022, 2023])]:
        sub = d.copy()
        sub.loc[sub.index.year.isin(excluidos), 'ANOMALIA_MM'] = np.nan
        for ventana in [12, 24, 36]:
            fila = dict(escenario=nombre, excluidos=str(excluidos), HAC_meses=ventana)
            fila.update(correlaciones(sub, sub.ONI))
            fila.update(modelo(sub, sub[['ONI']], ventana)['ONI'])
            sensibilidad.append(fila)
    sensibilidad = pd.DataFrame(sensibilidad)
    # Sensibilidades se informan aparte, sin seleccionar la variante con menor p.
    sensibilidad['p_Holm_sensibilidad'] = holm(sensibilidad.p_HAC)
    resumen = d.dropna(subset=['ANOMALIA_MM']).groupby(['MES', 'FASE']).agg(
        N=('ANOMALIA_MM', 'size'), precip_media_mm=('PRECIP_ANALISIS_MM', 'mean'),
        anomalia_media_mm=('ANOMALIA_MM', 'mean'), anomalia_mediana_mm=('ANOMALIA_MM', 'median'),
        desviacion_mm=('ANOMALIA_MM', 'std'), minimo_mm=('ANOMALIA_MM', 'min'),
        maximo_mm=('ANOMALIA_MM', 'max')).reset_index()
    cobertura = d.groupby(d.index.year).agg(
        meses_validos=('ANOMALIA_MM', 'count'), meses_ONI=('ONI', 'count'))
    archivos = {'01_Relacion_general_temporadas': relacion, '02_Relacion_por_mes': mensual,
                '03_Comparacion_fases_ajustada': fases, '04_Sensibilidad': sensibilidad,
                '05_Resumen_mes_fase': resumen, '06_Cobertura_anual': cobertura.reset_index()}
    for nombre, tabla in archivos.items():
        tabla.to_csv(salida/f'{nombre}.csv', index=False, encoding='utf-8-sig', float_format='%.6g')
    d.to_csv(salida/'00_Datos_utilizados.csv', encoding='utf-8-sig')

    fig, ax = plt.subplots(figsize=(9, 6), constrained_layout=True)
    for fase in FASES:
        g = d[d.FASE.eq(fase)].dropna(subset=['ONI', 'ANOMALIA_MM'])
        ax.scatter(g.ONI, g.ANOMALIA_MM, s=22, alpha=.6, color=COLORES_ESTUDIOS[fase], label=f'{fase} (n={len(g)})')
    ax.axhline(0, color='gray', lw=.8)
    fila = relacion.iloc[0]
    ax.set(title=f'ONI y anomalía mensual | r={fila.Pearson_r:.2f}, rho={fila.Spearman_rho:.2f}',
           xlabel='ONI del trimestre centrado en el mes (°C)', ylabel='Anomalía mensual (mm)')
    ax.legend(frameon=False)
    guardar_fig(fig, '01_Dispersion_ONI_anomalia', salida)

    fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True, constrained_layout=True)
    for ax, nombre in zip(axes, grupos):
        g = relacion[relacion.grupo.eq(nombre)]
        ax.errorbar(g.desfase_meses, g.beta_mm,
                    yerr=np.array([g.beta_mm-g.IC95_inf, g.IC95_sup-g.beta_mm]), fmt='o-', capsize=4)
        ax.axhline(0, color='gray', lw=.8)
        ax.set(title=nombre, ylabel='Cambio ajustado (mm/°C)')
        ax.grid(alpha=.15)
    axes[-1].set(xlabel='Desfase: ONI antecede a la lluvia (meses)', xticks=range(MAX_DESFASE+1))
    fig.suptitle('Efecto lineal estimado con IC 95% HAC puntuales\nAjuste por mes y tendencia; consultar p_Holm en tablas')
    guardar_fig(fig, '02_Desfases_ONI', salida)

    fig, ax = plt.subplots(figsize=(10, 7), constrained_layout=True)
    matriz = mensual.pivot(index='grupo', columns='desfase_meses', values='Pearson_r').reindex(MESES)
    im = ax.imshow(matriz, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
    for i in range(12):
        for j in range(MAX_DESFASE+1):
            val = matriz.iloc[i, j]
            ax.text(j, i, f'{val:.2f}' if np.isfinite(val) else 'S/D', ha='center', va='center',
                    color='white' if abs(val) > .6 else '#202020')
    ax.set(yticks=range(12), yticklabels=MESES, xticks=range(MAX_DESFASE+1),
           xlabel='Desfase: ONI antecede a la lluvia (meses)', title='Correlación Pearson por mes y desfase (descriptiva)')
    fig.colorbar(im, ax=ax, label='r')
    guardar_fig(fig, '03_Correlaciones_mes_desfase', salida)

    fig, axes = plt.subplots(3, 4, figsize=(15, 10), constrained_layout=True)
    for mes, ax in enumerate(axes.flat, 1):
        vals = [d.loc[d.MES.eq(mes) & d.FASE.eq(f), 'ANOMALIA_MM'].dropna().to_numpy() for f in FASES]
        boxes = ax.boxplot([v if len(v) else [np.nan] for v in vals], patch_artist=True)
        for box, fase in zip(boxes['boxes'], FASES):
            box.set_facecolor(COLORES_ESTUDIOS[fase]); box.set_alpha(.6)
        ax.set_xticks([1, 2, 3]); ax.set_xticklabels([f'{f}\nn={len(v)}' for f, v in zip(FASES, vals)], fontsize=8)
        ax.axhline(0, color='gray', lw=.6); ax.set_title(MESES[mes-1])
        if mes in [1, 5, 9]: ax.set_ylabel('Anomalía (mm)')
    fig.suptitle('Distribución de anomalías por mes y fase ENSO\nCaja: percentiles 25–75; línea: mediana; bigotes: 1.5 × rango intercuartílico')
    guardar_fig(fig, '04_Distribuciones_por_fase', salida)

    fig, ax = plt.subplots(figsize=(11, 6), constrained_layout=True)
    g = mensual[mensual.desfase_meses.eq(0)].set_index('grupo').reindex(MESES)
    ax.errorbar(range(12), g.beta_mm, yerr=np.array([g.beta_mm-g.IC95_inf, g.IC95_sup-g.beta_mm]),
                fmt='o', capsize=4, color='#14648b')
    ax.axhline(0, color='gray', lw=.8)
    ax.set(xticks=range(12), xticklabels=MESES, ylabel='Cambio ajustado (mm/°C)',
           title='Relación simultánea por mes | IC 95% HAC puntuales\nAjuste por tendencia; tamaños de muestra y p_Holm en tabla 02')
    guardar_fig(fig, '05_Efecto_ONI_por_mes', salida)

    fig, ax = plt.subplots(figsize=(11, 6), constrained_layout=True)
    g = sensibilidad
    ax.errorbar(g.beta_mm, np.arange(len(g)),
                xerr=np.array([g.beta_mm-g.IC95_inf, g.IC95_sup-g.beta_mm]), fmt='o', capsize=4)
    ax.axvline(0, color='gray', lw=.8)
    ax.set(yticks=np.arange(len(g)), yticklabels=[f'{r.escenario} · HAC {r.HAC_meses} meses' for r in g.itertuples()],
           xlabel='Cambio ajustado (mm/°C), con IC 95% puntual', title='Sensibilidad a cobertura y dependencia temporal')
    guardar_fig(fig, '06_Sensibilidad', salida)

    principal = relacion.iloc[0]
    significativo = int(sum(t.evidencia_ajustada_005.sum() for t in tablas))
    texto = f'''ESTUDIOS EXPLORATORIOS ENSO–PRECIPITACIÓN
Periodo: {d.index.min():%Y-%m} a {d.index.max():%Y-%m}.
Fuente: {ENTRADA}. Se conserva el ONI y la clasificación del análisis original.
Meses con anomalía válida: {d.ANOMALIA_MM.notna().sum()} de {len(d)}.

RESULTADO GLOBAL SIN DESFASE
Pearson r: {principal.Pearson_r:.4f}; Spearman rho: {principal.Spearman_rho:.4f}.
Coeficiente ONI ajustado: {principal.beta_mm:.3f} mm/°C.
IC 95% puntual: [{principal.IC95_inf:.3f}, {principal.IC95_sup:.3f}].
p HAC aproximado: {principal.p_HAC:.5g}; p ajustado Holm: {principal.p_Holm:.5g}.
Contrastes principales con p Holm < 0.05: {significativo} de {sum(len(t) for t in tablas)}.
Un resultado no significativo indica evidencia insuficiente, no demuestra ausencia de relación.

QUÉ SE CALCULA
Pearson: relación lineal; Spearman: relación monótona mediante rangos. Son descriptivos.
r2_bivariado = r²; no es porcentaje de lluvia causado por ENSO.
OLS: anomalía = intercepto + ONI + tendencia temporal + indicadores de mes.
En análisis de un solo mes, solo se controla tendencia. Cada desfase es un modelo separado.
Desfase k: ONI(t-k) frente a anomalía(t). El índice sigue siendo trimestral móvil;
desfase cero no es un predictor operativo anticipado, pues incluye el mes siguiente.
Jun-Sep es la temporada principal de lluvias; Nov-Abr el periodo seco predefinido.
Mayo y octubre siguen incluidos en el análisis global y por mes.
Contrastes de fase: diferencias en mm ajustadas por mes y tendencia (no mm/°C).
R2_modelo corresponde al modelo completo, no exclusivamente al ONI.

INCERTIDUMBRE Y PRUEBAS MÚLTIPLES
Covarianza HAC Newey-West con pesos Bartlett y ventana {HAC_MESES} meses.
Los productos de scores usan distancias mensuales reales, conservando huecos.
Los ceros en scores no son precipitaciones imputadas.
Corrección n/(n-k); p bilateral e IC con aproximación normal asintótica.
Holm se aplica conjuntamente a los {sum(len(t) for t in tablas)} contrastes principales,
incluyendo todos los meses, desfases, temporadas y diferencias de fase.
Los IC 95% graficados son puntuales, NO simultáneos: para significancia múltiple usar p_Holm.
Las nueve sensibilidades tienen su propia corrección y no se usan para elegir resultados.
Fuente HAC: https://www.statsmodels.org/stable/generated/statsmodels.stats.sandwich_covariance.cov_hac.html
Pearson: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html

LIMITACIONES
HAC permite heterocedasticidad y dependencia temporal dentro de una aproximación asintótica.
No garantiza inferencia exacta en muestras pequeñas, especialmente por mes (unos 35 años).
ENSO puede persistir más que la ventana; revisar sensibilidades HAC 12, 24 y 36 meses.
Los desfases están correlacionados. Un pico no demuestra un mecanismo físico ni capacidad predictiva.
No se rellenan meses parciales ni años excluidos. Su ausencia puede sesgar las asociaciones.
Sensibilidad IAM configurable: {ANIOS_SENSIBILIDAD}; también se muestra 2021–2023 por comparación.
No se verifica aquí homogeneidad entre estaciones, instrumentos, fuentes ni cobertura intradiaria.
Cambiar exclusiones no recalcula la climatología: se conserva la del análisis original.
Los eventos RUEMAG no se suman a la precipitación mensual y no intervienen en estas pruebas.
La corta serie de eventos no basta para equiparar conteos observados con frecuencia climática ENSO.
Estos resultados evalúan asociación, no causalidad. Requieren interpretación física y de calidad de datos.

ARCHIVOS
CSV: tablas que se abren en Excel (UTF-8); PNG y PDF: seis figuras.
INFORME_ENSO.html: informe conjunto para abrir en navegador e imprimir.
No se eliminan archivos preexistentes; una nueva ejecución reemplaza salidas del mismo nombre.
'''
    (salida/'LEEME_interpretacion.txt').write_text(texto, encoding='utf-8')
    secciones = ['<h1>Estudios ENSO y precipitación</h1>', '<pre>'+html.escape(texto)+'</pre>']
    for p in sorted(salida.glob('0[1-6]_*.png')):
        secciones.append(f'<h2>{html.escape(p.stem.replace("_", " "))}</h2><img src="{p.name}">')
    for nombre, tabla in archivos.items():
        secciones.append(f'<h2>{nombre.replace("_", " ")}</h2>'+tabla.to_html(index=False, float_format=lambda x: f'{x:.4g}'))
    (salida/'INFORME_ENSO.html').write_text(
        '<!doctype html><html lang="es"><meta charset="utf-8"><title>Estudios ENSO</title>'
        '<style>body{font:15px Arial;margin:40px;color:#183247}pre{white-space:pre-wrap;line-height:1.5}'
        'img{width:100%;max-width:1100px}table{border-collapse:collapse;font-size:12px}'
        'td,th{padding:7px;border:1px solid #ccc}h2{margin-top:40px}</style>' + ''.join(secciones) + '</html>', encoding='utf-8')
    (salida/'configuracion.json').write_text(json.dumps(dict(entrada=str(ENTRADA),
        ventana_HAC=HAC_MESES, desfase_maximo=MAX_DESFASE,
        anios_sensibilidad=ANIOS_SENSIBILIDAD), ensure_ascii=False, indent=2), encoding='utf-8')
    print(texto)
    print('Resultados guardados en:', salida.resolve())
    if MOSTRAR_GRAFICAS:
        plt.show()
    return archivos



if __name__ == '__main__':
    # Todo se ejecuta en orden; no necesita el script complementario ni un CSV previo.
    serie_mensual = main()
    ejecutar(serie_mensual, SALIDA_ESTUDIOS)
