"""24DSF -> parquet, straight from the .7z, without writing the 22.5 GB text.

    bsdtar -xOf Data/raw/bcra_cendeu/24DSF202607.7Z 24DSF.txt | python3 Code/build/cendeu_build_panel.py

One row per borrower-lender, 24 monthly blocks of {status, amount, legal}.
Block 00 is the current month, 01..23 go backwards. Amounts in pesos.
"""

import sys
import pathlib
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = str(ROOT / "Data" / "processed" / "cendeu" / "panel24_wide.parquet")
HEAD = [("ent", 5), ("id_type", 2), ("cuit", 11)]
BATCH = 250_000

fields = [pa.field("ent", pa.int32()), pa.field("id_type", pa.int8()),
          pa.field("cuit", pa.string())]
for i in range(24):
    fields += [pa.field(f"status_{i:02d}", pa.int8()),
               pa.field(f"amount_{i:02d}_ars", pa.int64()),
               pa.field(f"legal_{i:02d}", pa.int8())]
schema = pa.schema(fields)
names = [f.name for f in fields]


def money(s):
    """'238,0' means 238.0 thousand pesos. exact integer arithmetic."""
    t = s.replace(",", "").strip()
    return int(t) * 100 if t and t.lstrip("-").isdigit() else 0


def num(s):
    t = s.strip()
    return int(t) if t and t.lstrip("-").isdigit() else 0


cols = {n: [] for n in names}
writer = pq.ParquetWriter(OUT, schema, compression="zstd")
n = bad = 0

for raw in sys.stdin.buffer:
    line = raw.rstrip(b"\r\n").decode("latin-1")
    if len(line) < 378:
        bad += 1
        continue
    cols["ent"].append(num(line[0:5]))
    cols["id_type"].append(num(line[5:7]))
    cols["cuit"].append(line[7:18].strip())
    for i in range(24):
        b = 18 + i * 15
        cols[f"status_{i:02d}"].append(num(line[b:b + 2]))
        cols[f"amount_{i:02d}_ars"].append(money(line[b + 2:b + 14]))
        cols[f"legal_{i:02d}"].append(num(line[b + 14:b + 15]))
    n += 1
    if n % BATCH == 0:
        writer.write_table(pa.table([cols[k] for k in names], schema=schema))
        for k in cols:
            cols[k].clear()
        print(f"{n:,} rows", file=sys.stderr, flush=True)

if cols["ent"]:
    writer.write_table(pa.table([cols[k] for k in names], schema=schema))
writer.close()
print(f"done: {n:,} rows, {bad:,} skipped", file=sys.stderr)
