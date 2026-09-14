"""
Mapa provincial de adopcion de billeteras: personas con solo cuenta de
pago (CVU) como % de las personas con alguna cuenta, ultimo trimestre.
Insumos: Data/processed/inclusion_prov.dta y Data/raw/geo/ar_provincias.geojson
         (Natural Earth admin-1, filtrado a Argentina).
Salida:  Code/output/figuras/f5_mapa_adopcion.png
Requiere: pip install geopandas pandas matplotlib
"""
import os
import unicodedata
import pandas as pd
import geopandas as gpd
import matplotlib
import pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
matplotlib.use("Agg")
import matplotlib.pyplot as plt

here = os.path.dirname(os.path.abspath(__file__))
TRIM = "2025-12-01"   # fin del trimestre a mapear

def norm(p):
    p = unicodedata.normalize("NFD", str(p).strip().upper())
    p = "".join(c for c in p if not unicodedata.combining(c))
    if "CIUDAD" in p or "CAPITAL" in p:
        p = "CABA"
    return p

g = gpd.read_file(os.path.join(here, "..", "data", "raw", "geo", "ar_provincias.geojson"))
g["provincia"] = g["name"].map(norm)

i = pd.read_stata(os.path.join(here, "..", "data", "processed", "inclusion_prov.dta"))
x = i[i.ym == TRIM].copy()
x["share"] = 100 * x.n_pers_min1_cta_pago / x.n_pers_min1_cta
m = g.merge(x[["provincia", "share"]], on="provincia", how="left")
assert m.share.notna().all(), "provincias sin match"

fig, ax = plt.subplots(figsize=(7.5, 10))
m.plot(column="share", cmap="Blues", linewidth=0.6, edgecolor="white", ax=ax,
       legend=True, legend_kwds={"shrink": 0.5, "label": "%"})
for _, r in m.iterrows():
    if r["provincia"] == "CABA":
        continue
    pt = r.geometry.representative_point()
    col = "white" if r["share"] > 82 else "0.15"
    ax.annotate(f"{r['share']:.0f}", (pt.x, pt.y), ha="center", fontsize=7.5, color=col)
ax.set_xlim(-74, -53)
ax.set_ylim(-56, -21)
ax.set_axis_off()
ax.set_title("Personas con al menos una cuenta de pago (CVU),\n"
             "como % de las personas con alguna cuenta. 2025q4",
             fontsize=11, color="0.1")
plt.tight_layout()
out = os.path.join(here, "..", "output", "figuras", "f5_mapa_adopcion.png")
plt.savefig(out, dpi=220, facecolor="white", bbox_inches="tight")
print("ok:", out)
