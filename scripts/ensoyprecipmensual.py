# ONI ERSSTv6: tabla adjunta contrastada con NOAA/CPC el 2026-10-21.
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 15:15:11 2026

@author: bcomi
"""

# -*- coding: utf-8 -*-
"""Análisis mensual exploratorio de precipitación y ENSO para Spyder.
Dependencias: pandas, numpy, matplotlib, openpyxl.
No modifica la base original. ONI del adjunto integrado, sin descarga web.
"""
from pathlib import Path
import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="replace")
from figuras_publicacion import guardar_publicacion
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# ================= CAMBIAR AQUÍ RUTAS Y PERIODO =================
CARPETA_BASE = Path(os.environ.get("ENSO_DATOS", r"G:\ENSO Y PRECIP"))
ARCHIVO = CARPETA_BASE / 'gdl_completo_precip_meses.xlsx'
SALIDA = Path(__file__).resolve().parent / 'resultados' / 'ensoyprecipmensual'
INICIO, FIN = 1991, 2025
BASE_INICIO, BASE_FIN = 1991, 2020
ESTACION = 'Guadalajara'
# Opcional: años que el usuario confirme que no deben entrar en estadísticas.
ANIOS_EXCLUIDOS = []
MOSTRAR_GRAFICAS = False
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


def main():
    SALIDA.mkdir(parents=True,exist_ok=True)
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
    fig.subplots_adjust(left=.065,right=.985,top=.84,bottom=.10,hspace=.37)
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
    handles=[Patch(color=c,alpha=.65,label=f) for f,c in COLORES.items()]+[
        Line2D([0],[0],color='#14648b',label='Acumulado mensual'),
        Line2D([0],[0],color='#207647',ls='--',label='Climatología mensual'),
        Line2D([0],[0],color='#bb660b',marker='D',lw=0,label='Acumulado parcial')]
    fig.legend(handles=handles,loc='upper left',bbox_to_anchor=(.06,.905),ncol=6,frameon=False,fontsize=10)
    fig.text(.065,.047,'Fondo: fase ONI del trimestre centrado en cada mes. Meses parciales fuera de las estadísticas.',fontsize=10,color='#4c5967')
    fig.text(.065,.025,'2021–2023: acumulados IAM observados; la presencia de un valor diario no garantiza cobertura intradiaria completa.',fontsize=10,color='#4c5967')
    guardar_publicacion(fig, SALIDA/'01_Precipitacion_mensual_ENSO.png', estudio=f'{INICIO}–{FIN}', climatologia=f'{BASE_INICIO}–{BASE_FIN}')

    # Figura 2: tendencia de anomalías, sin confundir estacionalidad y tendencia.
    fig2,ax=plt.subplots(figsize=(18,6));fig2.subplots_adjust(left=.065,right=.985,top=.78,bottom=.20)
    for fecha,fila in m.iterrows():
        ax.axvspan(fecha,fecha+pd.offsets.MonthBegin(1),color=COLORES[fila.FASE],alpha=.40,lw=0)
    ax.plot(m.index,m.ANOMALIA_MM,color='#14648b',lw=1,label='Anomalía mensual')
    ax.axhline(0,color='#64748b',lw=1)
    ax.plot(m.index,m.TENDENCIA_ANOMALIA_MM,color='#7439a0',lw=2.4,
            label=f'Tendencia: {pendiente*10:+.2f} mm/década')
    ax.set(xlim=(m.index.min(),pd.Timestamp(FIN+1,1,1)),ylabel='Anomalía de precipitación mensual (mm)',xlabel='Año')
    ax.xaxis.set_major_locator(mdates.YearLocator(2));ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.grid(axis='y',alpha=.2);ax.spines[['top','right']].set_visible(False);ax.legend(frameon=False,loc='upper left',bbox_to_anchor=(0,1.16),ncol=2)
    fig2.suptitle(f'{ESTACION} · Anomalías mensuales y tendencia, {INICIO}–{FIN}',fontsize=21,y=.98)
    fig2.text(.065,.065,'Anomalía = acumulado mensual − climatología de ese mes. Tendencia lineal descriptiva; no es atribución a ENSO.',fontsize=10,color='#4c5967')
    fig2.text(.065,.027,'La pendiente corresponde a lluvia mensual, no al acumulado anual. Fondo ENSO: mismos colores de la figura 1.',fontsize=10,color='#4c5967')
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
    fig3.text(.09,.045,'Diferencias descriptivas: no implican causalidad ni significancia estadística. IAM 2021–2023 conserva limitaciones de cobertura.',fontsize=9.5,color='#4c5967')
    guardar_publicacion(fig3, SALIDA/'03_Lluvia_por_mes_y_fase_ENSO.png', estudio=f'{INICIO}–{FIN}', climatologia=f'{BASE_INICIO}–{BASE_FIN}')

    # Sensibilidad: misma climatología, excluyendo años IAM no verificados.
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

LIMITACIONES
Los datos IAM 2021–2023 pueden tener intervalos ausentes aunque exista suma diaria.
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
    if MOSTRAR_GRAFICAS: plt.show()
    else: plt.close('all')

if __name__=='__main__':
    main()
