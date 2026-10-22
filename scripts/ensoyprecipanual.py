# ONI ERSSTv6: tabla adjunta contrastada con NOAA/CPC el 2026-10-21.
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 10:22:19 2026

@author: bcomi
"""


"""Ejecutar en Spyder. Dependencias: pandas, numpy, matplotlib y scipy.
Fuente: zap6024.csv (ANIO, PRECIP en mm) y tabla ONI proporcionada.
No se infiere la estación a partir del nombre del archivo.
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
from matplotlib.patches import Patch
from scipy.stats import linregress

CARPETA_BASE = Path(os.environ.get("ENSO_DATOS", r"G:\ENSO Y PRECIP"))
ARCHIVO_PRECIP = CARPETA_BASE / "zap6024.csv"
CARPETA_SALIDA = Path(__file__).resolve().parent / "resultados" / "anual"
NOMBRE_ESTACION = "Serie zap6024"  # Cambiar por el nombre confirmado de la estación.
BASE_INICIO, BASE_FIN = 1991, 2020
# Añadir aquí SOLO los años que se hayan confirmado como incompletos.
ANIOS_INCOMPLETOS = []
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
COLORES = {'El Niño': '#f2ae9e', 'La Niña': '#a3d1eb', 'Neutral': '#e2e4e8'}
TRIMESTRES = 'DJF JFM FMA MAM AMJ MJJ JJA JAS ASO SON OND NDJ'.split()


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


def graficar(datos, climatologia, nbase, inicio, fin, salida):
    d = datos.set_index('ANIO').reindex(range(inicio, fin + 1)).reset_index()
    validos = d.PRECIP.notna() & ~d.ANIO.isin(ANIOS_INCOMPLETOS)
    if validos.sum() < 3:
        raise ValueError('Se necesitan al menos tres años válidos para la tendencia.')
    ajuste = linregress(d.loc[validos, 'ANIO'], d.loc[validos, 'PRECIP'])
    fig, ax = plt.subplots(figsize=(19, 8.5))
    fig.subplots_adjust(left=.07, right=.985, bottom=.21, top=.79)
    for _, fila in d.iterrows():
        fases = str(fila.FASE_ANUAL).split(' / ')
        for i, f in enumerate(fases):
            ax.axvspan(fila.ANIO-.5+i/len(fases), fila.ANIO-.5+(i+1)/len(fases),
                       color=COLORES.get(f, 'white'), alpha=.65, lw=0, zorder=0)
    linea, = ax.plot(d.ANIO, d.PRECIP.where(validos), '-o', color='#176c98',
                    lw=2, ms=4, label='Acumulado anual', zorder=3)
    if (~validos & d.PRECIP.notna()).any():
        ax.scatter(d.loc[~validos, 'ANIO'], d.loc[~validos, 'PRECIP'], marker='v',
                   facecolors='none', edgecolors='#176c98', label='Acumulado parcial')
    normal = ax.axhline(climatologia, color='#227d4e', lw=2.3, ls='--',
             label=f'Climatología {BASE_INICIO}–{BASE_FIN}: {climatologia:.1f} mm')
    tendencia, = ax.plot(d.ANIO, ajuste.intercept + ajuste.slope*d.ANIO,
                      color='#8548a3', lw=2.5, ls='-.',
                      label=f'Tendencia: {ajuste.slope*10:+.1f} mm/década')
    ax.set(xlim=(inicio-.5, fin+.5), ylim=(0, max(d.PRECIP.max()*1.17, climatologia*1.2)),
           xlabel='Año', ylabel='Precipitación acumulada (mm)')
    ax.set_xticks(np.arange(inicio, fin+1, 1 if fin-inicio <= 35 else 2))
    ax.tick_params(axis='x', rotation=55)
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='y', color='#9299a3', alpha=.2)
    fig.suptitle(f'{NOMBRE_ESTACION} · Precipitación anual y fases ENSO', fontsize=22, y=.97)
    ax.set_title(f'{inicio}–{fin}', fontsize=17, pad=14)
    handles = [Patch(color=c, label=f) for f,c in COLORES.items()]+[linea,normal,tendencia]
    fig.legend(handles=handles, loc='upper center', bbox_to_anchor=(.52,.918),
               ncol=3, frameon=False, fontsize=11)
    fig.text(.07,.093, 'Fondo: fase predominante en los 12 trimestres ONI; los empates dividen la franja anual.', fontsize=10, color='#46505c')
    fig.text(.07,.064, f'Climatología: media de {nbase} acumulados anuales disponibles en {BASE_INICIO}–{BASE_FIN}. '
             f'Ajuste lineal: R² = {ajuste.rvalue**2:.3f}; p = {ajuste.pvalue:.3f}.', fontsize=10, color='#46505c')
    fig.text(.07,.035, 'Fuente: zap6024.csv y tabla ONI adjunta. El CSV anual no permite verificar la cobertura diaria.', fontsize=10, color='#46505c')
    archivo = salida / f'Precipitacion_ENSO_{inicio}_{fin}.png'
    guardar_publicacion(fig, archivo, estudio=f'{inicio}–{fin}', climatologia=f'{BASE_INICIO}–{BASE_FIN} (n={nbase} años disponibles)')
    plt.close(fig)
    return {'periodo':f'{inicio}–{fin}', 'n':int(validos.sum()), 'mm_decada':ajuste.slope*10,
            'r2':ajuste.rvalue**2, 'p':ajuste.pvalue}


def main():
    CARPETA_SALIDA.mkdir(parents=True, exist_ok=True)
    datos = pd.read_csv(ARCHIVO_PRECIP, encoding='utf-8-sig')
    datos.columns = datos.columns.str.strip().str.upper()
    if not {'ANIO', 'PRECIP'}.issubset(datos.columns):
        raise ValueError('El CSV debe contener ANIO y PRECIP (mm).')
    datos['ANIO'] = pd.to_numeric(datos.ANIO, errors='raise')
    if datos.ANIO.isna().any() or (datos.ANIO % 1 != 0).any():
        raise ValueError('Años vacíos o no enteros.')
    datos['ANIO'] = datos.ANIO.astype(int)
    datos['PRECIP'] = pd.to_numeric(datos.PRECIP, errors='raise')
    if datos.ANIO.duplicated().any() or (datos.PRECIP.dropna() < 0).any():
        raise ValueError('Revisar años duplicados o precipitación negativa.')
    if np.isinf(datos.PRECIP).any():
        raise ValueError('Precipitación infinita no válida.')
    datos = datos.sort_values('ANIO')
    trimestral, anual = clasificar_oni()
    datos = datos.merge(anual, on='ANIO', how='left', validate='one_to_one')
    datos['FASE_ANUAL'] = datos.FASE_ANUAL.fillna('S/D')
    base = datos[datos.ANIO.between(BASE_INICIO,BASE_FIN) & ~datos.ANIO.isin(ANIOS_INCOMPLETOS)].PRECIP.dropna()
    if base.empty:
        raise ValueError('No hay datos válidos en el periodo climatológico.')
    climatologia = base.mean()
    datos['CLIMATOLOGIA_MM'] = climatologia
    datos['ANOMALIA_MM'] = datos.PRECIP-climatologia
    datos['EXCLUIDO_ESTADISTICA'] = datos.ANIO.isin(ANIOS_INCOMPLETOS)
    datos.to_csv(CARPETA_SALIDA/'Resumen_anual_ENSO.csv', index=False, encoding='utf-8-sig')
    trimestral.to_csv(CARPETA_SALIDA/'ONI_trimestral_clasificado.csv', index=False, encoding='utf-8-sig')
    periodos = list(dict.fromkeys([(int(datos.ANIO.min()),int(datos.ANIO.max())),(BASE_INICIO,BASE_FIN)]))
    resultados = [graficar(datos,climatologia,len(base),a,b,CARPETA_SALIDA) for a,b in periodos]
    texto = f'Climatología {BASE_INICIO}–{BASE_FIN}: {climatologia:.2f} mm ({len(base)} años).\n'
    for r in resultados:
        texto += f"{r['periodo']}: {r['mm_decada']:+.2f} mm/década; R²={r['r2']:.4f}; p={r['p']:.4f}; n={r['n']}.\n"
    texto += '\nLa climatología se calcula con los acumulados suministrados. No hay información de cobertura diaria.\n'
    texto += 'La tendencia es un ajuste OLS descriptivo; p corresponde al contraste convencional de pendiente cero.\n'
    texto += 'La superposición con ENSO no demuestra causalidad. La fase predominante anual es un resumen propio.\n'
    texto += 'Clasificación por ±0.5 °C durante al menos cinco trimestres móviles consecutivos, sin cortar entre años.\n'
    texto += 'Criterio: https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/oni/v6/\n'
    texto += 'ONI ERSSTv6 del adjunto, contrastado con NOAA/CPC el 21/10/2026.\n'
    (CARPETA_SALIDA/'Resultados.txt').write_text(texto, encoding='utf-8')
    print(texto)
    print('Archivos guardados en:',CARPETA_SALIDA)

if __name__ == '__main__':
    main()
