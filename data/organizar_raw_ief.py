"""
Copia lo esencial de cada mes del IEF crudo (repo Fintech_Dynamics) a
data/raw/ief/AAAAMM/ de este repo, con nombres estables. Re-ejecutable:
saltea meses ya organizados y completa los nuevos a medida que se descargan.
Tambien copia balhist.txt (panel historico de balances) desde el mes mas reciente.

Uso: python organizar_raw_ief.py   (desde cualquier lado)
"""
import os
import re
import glob
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "..", "..", "Fintech_Dynamics",
                                    "data", "Balances_bancos_BCRA", "bcra_ief"))
DST = os.path.join(HERE, "raw", "ief")

MAP = {
    "Entfin/Tec_Cont/distribgeo": ("prestamos_depositos_prov.xlsx", "*.xlsx"),
    "Entfin/Distrib/Suc_pcia":    ("suc_pcia.txt",  "COMPLETO*"),
    "Entfin/Tec_Cont/baldet":     ("baldet.txt",    "COMPLETO*"),
    "Entfin/Tec_Cont/inf_adi":    ("inf_adi.txt",   "COMPLETO*"),
    "Entfin/Tec_Cont/indicad":    ("indicad.txt",   "COMPLETO*"),
    "Entfin/Tec_Cont/esd":        ("esd.txt",       "COMPLETO*"),
    "Entfin/Tec_Cont/entidad":    ("entidad.txt",   "COMPLETO*"),
    "Entfin/Tec_Cont/entint":     ("entint.txt",    "COMPLETO*"),
}

def find_one(folder, pattern):
    hits = sorted(glob.glob(os.path.join(folder, pattern)) +
                  glob.glob(os.path.join(folder, pattern.lower())))
    return hits[0] if hits else None

months = sorted(d for d in os.listdir(SRC) if re.fullmatch(r"20\d{4}", d)
                and os.path.isdir(os.path.join(SRC, d)))
def month_root(m):
    """Algunos 7z envuelven todo en una subcarpeta (p.ej. 202005/202005d/)."""
    base = os.path.join(SRC, m)
    if os.path.isdir(os.path.join(base, "Entfin")):
        return base
    for d in sorted(os.listdir(base)):
        cand = os.path.join(base, d)
        if os.path.isdir(os.path.join(cand, "Entfin")):
            return cand
    return base

done, partial = [], []
for m in months:
    dst = os.path.join(DST, m)
    os.makedirs(dst, exist_ok=True)
    missing = []
    root = month_root(m)
    for sub, (name, pat) in MAP.items():
        out = os.path.join(dst, name)
        if os.path.exists(out):
            continue
        src = find_one(os.path.join(root, sub), pat)
        if src:
            shutil.copy2(src, out)
        else:
            missing.append(name)
    (partial if missing else done).append(m)
    if missing:
        print(f"{m}: faltan {missing}")

# balhist del mes mas reciente que lo tenga (los ultimos pueden estar a medio descargar)
for m in reversed(months):
    src = find_one(os.path.join(month_root(m), "Entfin", "Tec_Cont", "bal_hist"), "balhist*")
    if src and os.path.getsize(src) > 1e6:
        dst = os.path.join(HERE, "raw", "balhist.txt")
        if not os.path.exists(dst) or os.path.getsize(src) > os.path.getsize(dst):
            shutil.copy2(src, dst)
            print(f"balhist.txt actualizado desde {m} ({os.path.getsize(src)/1e6:.0f} MB)")
        break

print(f"\n{len(done)} meses completos, {len(partial)} con faltantes, "
      f"de {len(months)} descargados en el repo crudo.")
