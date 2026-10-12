"""Genera Data/docs/diccionario_bases.md a partir de las bases .dta de Data/processed.

Lee nombre, tipo, etiqueta y cobertura de cada variable directamente de los
archivos, de modo que el diccionario no se desactualiza a mano. Se corre después
de rearmar cualquier base:

    python3 Code/build/documentar_bases.py

Además escribe Data/docs/catalogo_caracteristicas.csv con los códigos de
caracteristicas_bancos.dta (fuente, código, descripción, primer y último mes).
"""
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
PROC = RAIZ / "Data" / "processed"
DOCS = RAIZ / "Data" / "docs"

# unidad de observación, llave y nota breve de cada base (lo demás sale del archivo)
BASES = [
    ("balances_bancos.dta", "entidad × mes", "ent, ym",
     "Balance de saldos (balhist/baldet del IEF), resultados, tipo de entidad e IPC. "
     "Saldos en miles de pesos nominales; sufijo `_r`: pesos de enero de 2026. "
     "`*_acum`: resultado acumulado en el ejercicio; `*_flow`: resultado del mes (desacumulado)."),
    ("caracteristicas_bancos.dta", "entidad × mes × código (formato largo)", "ent, ym, fuente, codigo",
     "Indicadores (`indicad`), información adicional (`inf_adi`) y estado de situación de deudores (`esd`) del IEF. "
     "El catálogo de códigos está en `catalogo_caracteristicas.csv`. El centinela 99999 de `indicad` ya está en missing."),
    ("prestamos_depositos_prov.dta", "entidad × provincia × mes", "ent, provincia, ym",
     "Red de atención por provincia (mensual) y préstamos y depósitos por provincia (sólo cierres trimestrales)."),
    ("inclusion_prov.dta", "provincia × mes", "provincia, ym",
     "Informe de Inclusión Financiera del BCRA. Las variables de personas con cuenta son trimestrales."),
    ("ipc.dta", "mes", "ym", "IPC del INDEC, nivel general, dic-2016 = 100."),
    ("pda_provincia.dta", "provincia × mes", "cod_prov_indec, ym",
     "Puntos de acceso del BCRA agregados a provincia. `ym` es el índice `%tm` guardado como entero, sin formato."),
    ("pda_depto.dta", "departamento × mes", "cod_depto, ym",
     "Puntos de acceso agregados a departamento INDEC. `ym` es el índice `%tm` guardado como entero."),
    ("pda_lender_depto.dta", "entidad × departamento × tipo × mes", "entidad, cod_depto, tipo_pda, ym",
     "Puntos de acceso por entidad. La entidad viene por nombre, no por código BCRA."),
    ("FondosCNV/panel_fondo_semana.dta", "fondo money market × semana", "cod_cnv, semana",
     "Planillas diarias CNV/CAFCI llevadas a semana y cruzadas con la cartera semanal de la ficha CNV. "
     "Detalle de construcción en `diccionario_fondoscnv.md`."),
]


def cobertura(df: pd.DataFrame) -> str:
    for c in ("ym", "semana"):
        if c in df:
            s = df[c].dropna()
            if s.empty:
                return ""
            if pd.api.types.is_datetime64_any_dtype(s):
                f = "%Y-%m" if c == "ym" else "%Y-%m-%d"
                return f"{s.min():{f}} a {s.max():{f}}"
            lo, hi = int(s.min()), int(s.max())
            if lo > 20000:  # convención CENDEU: anio*12 + mes - 1
                return f"{lo // 12}-{lo % 12 + 1:02d} a {hi // 12}-{hi % 12 + 1:02d}"
            # índice %tm de Stata guardado como entero
            return f"{1960 + lo // 12}-{lo % 12 + 1:02d} a {1960 + hi // 12}-{hi % 12 + 1:02d}"
    return ""


def tipo(s: pd.Series) -> str:
    if pd.api.types.is_datetime64_any_dtype(s):
        return "fecha"
    if pd.api.types.is_numeric_dtype(s):
        return "num"
    return "texto"


def una_base(nombre, unidad, llave, nota) -> list[str]:
    ruta = PROC / nombre
    with pd.io.stata.StataReader(ruta) as r:
        etiquetas = r.variable_labels()
        titulo = r.data_label
        df = r.read(convert_categoricals=False)
    out = [f"## `{nombre}`", ""]
    if titulo:
        out.append(f"_{titulo}_")
        out.append("")
    filas = f"{len(df):,}".replace(",", ".")
    out += [f"Unidad: {unidad}. Llave: `{llave}`. Filas: {filas}. Variables: {df.shape[1]}. "
            f"Cobertura: {cobertura(df)}.", "", nota, "",
            "| Variable | Tipo | % no faltante | Descripción |", "|---|---|---:|---|"]
    for c in df.columns:
        nn = 100 * df[c].notna().mean()
        if tipo(df[c]) == "texto":
            nn = 100 * df[c].astype(str).str.strip().ne("").mean()
        out.append(f"| `{c}` | {tipo(df[c])} | {nn:.0f} | {etiquetas.get(c, '') or ''} |")
    out.append("")
    if nombre == "caracteristicas_bancos.dta":
        cat = (df.groupby(["fuente", "codigo"])
                 .agg(descripcion=("descripcion", "first"), ym_desde=("ym", "min"),
                      ym_hasta=("ym", "max"), n_obs=("valor", "count"))
                 .reset_index())
        cat.to_csv(DOCS / "catalogo_caracteristicas.csv", index=False)
        out.append(f"Códigos por fuente: " + ", ".join(
            f"`{k}` {v}" for k, v in cat.groupby("fuente").size().items()) + ".")
        out.append("")
    return out


def main():
    texto = ["# Diccionario de las bases en `Data/processed`", "",
             "Generado por `Code/build/documentar_bases.py` a partir de los archivos. "
             "No editar a mano: si cambia una base, se vuelve a correr el script. "
             "Las bases de la Central de Deudores están en `diccionario_cendeu.md` y las de "
             "fondos, con su construcción, en `diccionario_fondoscnv.md`.", "",
             "Convención de meses: en los `.dta` `ym` es el índice `%tm` de Stata (en las bases de "
             "puntos de acceso, guardado como entero sin formato). En los parquet de CENDEU es "
             "`anio*12 + mes - 1`; para pasar a `%tm` se resta 23520.", ""]
    for b in BASES:
        texto += una_base(*b)
    (DOCS / "diccionario_bases.md").write_text("\n".join(texto), encoding="utf-8")
    print("escrito", DOCS / "diccionario_bases.md")


if __name__ == "__main__":
    main()
