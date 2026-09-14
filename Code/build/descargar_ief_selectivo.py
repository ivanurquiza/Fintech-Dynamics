"""
Descarga la IEF del BCRA mes a mes y extrae SOLO lo esencial directo a
data/raw/ief/AAAAMM/ (~5 MB/mes en vez de ~160 MB extraidos):
  baldet.txt, suc_pcia.txt, inf_adi.txt, indicad.txt, esd.txt,
  entidad.txt, entint.txt, prestamos_depositos_prov.xlsx
  + balhist.txt (panel historico completo; solo viene en meses recientes,
    se sobreescribe con el del mes mas nuevo).
El 7z se borra despues de extraer. Re-ejecutable: saltea meses ya completos.

Uso:      python descargar_ief_selectivo.py            # 2018-01 a 2026-06
Requiere: pip install requests py7zr
"""
import io
import os
import pathlib
import re
import sys
import shutil
import tempfile
import requests
import py7zr

BASE = "https://www.bcra.gob.ar/archivos/Pdfs/PublicacionesEstadisticas/Entidades/"
HEADERS = {"User-Agent": "Mozilla/5.0 (research; Fintech-Dynamics repo)"}
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = pathlib.Path(__file__).resolve().parents[2]
RAW = str(ROOT / "Data" / "raw" / "bcra_ief")

# (nombre destino, regex sobre la ruta interna del 7z, case-insensitive)
WANTED = [
    ("baldet.txt",   r"Entfin/Tec_Cont/baldet/completo\.txt$"),
    ("suc_pcia.txt", r"Entfin/Distrib/Suc_pcia/completo\.txt$"),
    ("inf_adi.txt",  r"Entfin/Tec_Cont/inf_adi/completo\.txt$"),
    ("indicad.txt",  r"Entfin/Tec_Cont/indicad/completo\.txt$"),
    ("esd.txt",      r"Entfin/Tec_Cont/esd/completo\.txt$"),
    ("entidad.txt",  r"Entfin/Tec_Cont/entidad/completo\.txt$"),
    ("entint.txt",   r"Entfin/Tec_Cont/entint/completo\.txt$"),
    ("prestamos_depositos_prov.xlsx", r"Entfin/Tec_Cont/distribgeo/.*\.xlsx?$"),
]
BALHIST = r"Entfin/Tec_Cont/bal_hist/balhist.*\.txt$"

y0, y1 = 2018, 2026
if len(sys.argv) > 2:
    y0, y1 = int(sys.argv[1]), int(sys.argv[2])

ok = skip = 0
sin_publicar = {}
for year in range(y0, y1 + 1):
    for month in range(1, 13):
        per = f"{year}{month:02d}"
        dest = os.path.join(RAW, per)
        os.makedirs(dest, exist_ok=True)
        if all(os.path.exists(os.path.join(dest, n)) for n, _ in WANTED[:1]) and \
           sum(os.path.exists(os.path.join(dest, n)) for n, _ in WANTED) >= 7:
            skip += 1
            continue
        r = requests.get(f"{BASE}{per}d.7z", headers=HEADERS, timeout=300)
        if r.status_code != 200 or len(r.content) < 1000:
            print(f"{per}: 7z no disponible ({r.status_code})")
            continue
        try:
            z = py7zr.SevenZipFile(io.BytesIO(r.content))
            names = z.getnames()
            targets, rename = [], {}
            for outname, pat in WANTED + [("balhist.txt", BALHIST)]:
                hits = [n for n in names if re.search(pat, n.replace("\\", "/"), re.I)]
                if hits:
                    targets.append(hits[0])
                    rename[hits[0]] = outname
                elif outname != "balhist.txt":
                    sin_publicar.setdefault(per, []).append(outname)
            with tempfile.TemporaryDirectory() as tmp:
                z.extract(path=tmp, targets=targets)
                for member in targets:
                    outname = rename[member]
                    srcf = os.path.join(tmp, member.replace("\\", "/"))
                    if not os.path.exists(srcf):
                        continue
                    # balhist va a raw/, no a la carpeta del mes (siempre el mas nuevo)
                    out = os.path.join(HERE, "raw", "balhist.txt") if outname == "balhist.txt" \
                          else os.path.join(dest, outname)
                    shutil.move(srcf, out)
            ok += 1
            faltan = sin_publicar.get(per, [])
            print(f"{per}: OK ({len(r.content)/1e6:.0f} MB bajados)" +
                  (f" — sin publicar: {faltan}" if faltan else ""))
        except Exception as e:
            print(f"{per}: ERROR {e}")

print(f"\nListo: {ok} meses nuevos, {skip} ya estaban. Meses con conceptos sin publicar: {len(sin_publicar)}")
