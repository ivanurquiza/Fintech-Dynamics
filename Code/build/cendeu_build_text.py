"""Parse the two fixed-width files that carry free text (latin-1, with control
bytes DuckDB refuses). The name field is read and thrown away on purpose: the
key is the CUIT, and names are personal data we have no use for.

    python3 build_text.py rect
    python3 build_text.py padron
"""

import os
import sys
import pathlib
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = pathlib.Path(__file__).resolve().parents[2]
RAW = ROOT / "Data" / "raw" / "bcra_cendeu" / "extracted"
OUT = ROOT / "Data" / "processed" / "cendeu"
BATCH = 500_000

# (name, width, kind). kind: i = int, s = string, x = read and discard
RECT = [("ent", 5, "i"), ("period", 6, "i"), ("id_type", 2, "i"), ("cuit", 11, "s"),
        ("name", 55, "x"), ("status", 2, "i"), ("amount_ars", 12, "m")]

PADRON = [("cuit", 11, "s"), ("name", 160, "x"), ("activity", 6, "i"),
          ("dropped", 1, "s"), ("cuit_replacement", 11, "s"), ("birth_date", 10, "s"),
          ("sex", 1, "s"), ("zip", 10, "s"), ("province", 2, "i"), ("death_date", 8, "s")]

TYPE = {"i": pa.int32(), "s": pa.string(), "m": pa.int64()}


def convert(src_name, spec, out_name):
    src = RAW / src_name
    if not src.exists():
        sys.exit(f"missing: {src}")
    OUT.mkdir(parents=True, exist_ok=True)

    off, pos = [], 0
    for name, width, kind in spec:
        off.append((name, pos, pos + width, kind))
        pos += width
    reclen = pos
    keep = [(n, a, b, k) for n, a, b, k in off if k != "x"]
    schema = pa.schema([pa.field(n, TYPE[k]) for n, _, _, k in keep])
    names = [f.name for f in schema]

    cols = {n: [] for n in names}
    writer = pq.ParquetWriter(OUT / out_name, schema, compression="zstd")
    n = bad = 0

    def flush():
        writer.write_table(pa.table([cols[k] for k in names], schema=schema))
        for k in cols:
            cols[k].clear()

    with open(src, "rb") as f:
        for raw in f:
            line = raw.rstrip(b"\r\n").decode("latin-1", errors="replace")
            if len(line) < reclen:
                bad += 1
                continue
            for name, a, b, kind in keep:
                v = line[a:b].strip()
                if kind == "s":
                    cols[name].append(v)
                elif kind == "m":
                    t = v.replace(",", "")
                    cols[name].append(int(t) * 100 if t and t.lstrip("-").isdigit() else 0)
                else:
                    cols[name].append(int(v) if v and v.lstrip("-").isdigit() else 0)
            n += 1
            if n % BATCH == 0:
                flush()
                print(f"  {n:,} rows", flush=True)

    if cols[names[0]]:
        flush()
    writer.close()
    mb = (OUT / out_name).stat().st_size / 1e6
    print(f"{out_name}: {n:,} rows, {bad:,} skipped, {mb:,.0f} MB")


JOBS = {
    "rect":   lambda: convert("inf_retparc.txt", RECT, "rectifications.parquet"),
    "padron": lambda: convert("Padron_ARCA.txt", PADRON, "padron.parquet"),
}

if __name__ == "__main__":
    JOBS[sys.argv[1]]()
