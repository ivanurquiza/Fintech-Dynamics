"""Turn the BCRA Central de Deudores fixed-width files into parquet.

Run from anywhere. Expects the .7z files already extracted into
Data/raw/bcra_cendeu/extracted/.
DuckDB streams the text and writes parquet; nothing is held in memory.

    python build.py deudores
    python build.py padron
    python build.py dsf24
    python build.py all
"""

import sys
import pathlib
import duckdb

ROOT = pathlib.Path(__file__).resolve().parents[2]
RAW = ROOT / "Data" / "raw" / "bcra_cendeu" / "extracted"
OUT = ROOT / "Data" / "processed" / "cendeu"

# (name, width). Fixed-width layouts from the BCRA "LEAME" files.
DEUDORES = [
    ("ent", 5), ("period", 6), ("id_type", 2), ("cuit", 11), ("activity", 3),
    ("status", 2), ("loans", 12), ("unused", 12), ("guarantees_given", 12),
    ("other_items", 12), ("pref_guar_a", 12), ("pref_guar_b", 12),
    ("no_pref_guar", 12), ("counter_guar_a", 12), ("counter_guar_b", 12),
    ("no_counter_guar", 12), ("provisions", 12), ("covered", 1),
    ("legal_review", 1), ("refinanced", 1), ("forced_reclass", 1),
    ("legal_status", 1), ("uncollectible", 1), ("days_past_due", 4),
]

PADRON = [
    ("cuit", 11), ("name", 160), ("activity", 6), ("dropped", 1),
    ("cuit_replacement", 11), ("birth_date", 10), ("sex", 1),
    ("zip", 10), ("province", 2), ("death_date", 8),
]

DSF1 = [("id_type", 2), ("cuit", 11), ("normal_since", 6)]

RECT = [("ent", 5), ("period", 6), ("id_type", 2), ("cuit", 11),
        ("name", 55), ("status", 2), ("amount", 12)]

# amounts arrive as "238,0" and mean thousands of pesos, one decimal.
MONEY = {"loans", "unused", "guarantees_given", "other_items", "pref_guar_a",
         "pref_guar_b", "no_pref_guar", "counter_guar_a", "counter_guar_b",
         "no_counter_guar", "provisions", "amount"}
TEXT = {"cuit", "name", "zip", "birth_date", "death_date", "sex",
        "dropped", "cuit_replacement"}


def col(name, start, width):
    """One output column, cast according to its kind."""
    raw = f"trim(substr(line, {start}, {width}))"
    if name in MONEY:
        # "238,0" -> 2380 -> 238000 pesos. exact integer arithmetic.
        return (f"CASE WHEN {raw} IN ('', ',0') THEN 0 "
                f"ELSE TRY_CAST(replace({raw}, ',', '') AS BIGINT) * 100 END "
                f"AS {name}_ars")
    if name in TEXT:
        return f"{raw} AS {name}"
    return f"TRY_CAST({raw} AS INTEGER) AS {name}"


def wide_block(n):
    """The 24 repeated {status, amount, legal_review} blocks of 24DSF."""
    out = []
    for i in range(n):
        base = 19 + i * 15
        out.append(f"TRY_CAST(trim(substr(line, {base}, 2)) AS INTEGER) AS status_{i:02d}")
        out.append(
            f"CASE WHEN trim(substr(line, {base+2}, 12)) IN ('', ',0') THEN 0 "
            f"ELSE TRY_CAST(replace(trim(substr(line, {base+2}, 12)), ',', '') AS BIGINT) * 100 END "
            f"AS amount_{i:02d}_ars")
        out.append(f"TRY_CAST(trim(substr(line, {base+14}, 1)) AS INTEGER) AS legal_{i:02d}")
    return out


def convert(txt, spec, out_name, wide=0):
    src = RAW / txt
    if not src.exists():
        sys.exit(f"missing: {src}\nextract the .7z into {RAW} first")
    OUT.mkdir(parents=True, exist_ok=True)

    cols, pos = [], 1
    for name, width in spec:
        cols.append(col(name, pos, width))
        pos += width
    if wide:
        cols += wide_block(wide)

    con = duckdb.connect()
    con.execute("SET preserve_insertion_order = false")
    con.execute(f"""
        COPY (
            SELECT {', '.join(cols)}
            FROM (
                SELECT rtrim(line, chr(13)) AS line
                FROM read_csv('{src}',
                     columns = {{'line': 'VARCHAR'}},
                     delim = '\\x07', quote = '', escape = '', header = false,
                     encoding = 'latin-1')
            )
        ) TO '{OUT / out_name}' (FORMAT parquet, COMPRESSION zstd);
    """)
    n = con.execute(f"SELECT count(*) FROM '{OUT / out_name}'").fetchone()[0]
    mb = (OUT / out_name).stat().st_size / 1e6
    print(f"{out_name}: {n:,} rows, {mb:,.0f} MB")


JOBS = {
    "deudores": lambda: convert("deudores.txt", DEUDORES, "deudores.parquet"),
    "padron":   lambda: convert("Padron_ARCA.txt", PADRON, "padron.parquet"),
    "dsf1":     lambda: convert("1DSF.txt", DSF1, "normal_since.parquet"),
    "rect":     lambda: convert("inf_retparc.txt", RECT, "rectifications.parquet"),
    "dsf24":    lambda: convert("24DSF.txt", [("ent", 5), ("id_type", 2), ("cuit", 11)],
                                "panel24_wide.parquet", wide=24),
}

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    for k in (JOBS if which == "all" else [which]):
        JOBS[k]()
