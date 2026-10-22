"""Exportación de figuras con periodos explícitos y copia vectorial."""
from pathlib import Path

def guardar_publicacion(fig, archivo, *, estudio, climatologia, detalle=None):
    archivo = Path(archivo)
    archivo.parent.mkdir(parents=True, exist_ok=True)
    texto = f"Periodo de estudio: {estudio} | Climatología de precipitación: {climatologia}"
    if detalle:
        texto += "\n" + detalle
    pie = fig.text(.5, -.025, texto, ha="center", va="top", fontsize=9,
                   color="#414b57", linespacing=1.5)
    try:
        opciones = dict(bbox_inches="tight", facecolor="white")
        fig.savefig(archivo.with_suffix(".png"), dpi=400, **opciones)
        fig.savefig(archivo.with_suffix(".pdf"), **opciones)
    finally:
        pie.remove()

