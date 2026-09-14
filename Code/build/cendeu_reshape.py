"""Reshape the wide 24-month file into the panels we estimate on.

    python3 Code/build/cendeu_reshape.py lender_month
    python3 Code/build/cendeu_reshape.py firm
    python3 Code/build/cendeu_reshape.py sample
    python3 Code/build/cendeu_reshape.py person_month

Block 00 in panel24_wide is 2026m7; block i is i months earlier.

Each borrower-lender pair is kept from the first month it shows any activity
onwards, zeros included: a zero after the relationship started means the debt
was cancelled, which is what we want to see. Zeros before it started are
dropped. `active` marks which is which.

Everything runs one month at a time, reading three columns of the parquet per
pass, so DuckDB never spills a stacked table. Each pass writes its own file and
is skipped on re-runs, so an interrupted job just picks up where it left off.
"""

import os
import sys
import glob
import pathlib
import duckdb

ANCHOR = 2026 * 12 + 7
ROOT = pathlib.Path(__file__).resolve().parents[2]
CENDEU = ROOT / "Data" / "processed" / "cendeu"
IN = str(CENDEU / "panel24_wide.parquet")
OUT = str(CENDEU)
SLICES = 8
SAMPLE_PCT = 5

# largest i with activity = month the relationship starts, computed row-wise
FIRST_LAG = "greatest(" + ", ".join(
    f"case when status_{i:02d} > 0 or amount_{i:02d}_ars > 0 then {i} else -1 end"
    for i in range(24)) + ")"

PERSON = "substr(cuit,1,2) in ('20','23','24','27')"
FIRM = "substr(cuit,1,2) in ('30','33','34')"


def con():
    c = duckdb.connect()
    c.execute("SET memory_limit='3GB'")
    c.execute("SET preserve_insertion_order = false")
    tmp = os.path.expanduser("~/.duckdb_tmp")
    os.makedirs(tmp, exist_ok=True)
    c.execute(f"SET temp_directory='{tmp}'")
    # hard cap: fail fast instead of filling the disk
    c.execute("SET max_temp_directory_size='2GB'")
    return c


def clean_tmp():
    import shutil
    shutil.rmtree(os.path.expanduser("~/.duckdb_tmp"), ignore_errors=True)


def month_cols(i):
    """The per-row expressions for month i, already filtered to the relationship span."""
    ym = ANCHOR - i - 1
    return f"""
        select ent, cuit,
               {ym} as ym, {ym // 12} as year, {ym % 12 + 1} as month,
               status_{i:02d}                as status,
               amount_{i:02d}_ars            as amount_ars,
               legal_{i:02d}                 as legal,
               case when status_{i:02d} > 0 or amount_{i:02d}_ars > 0
                    then 1 else 0 end        as active,
               case when status_{i:02d} in (3,4,5) then 1 else 0 end as npl
        from '{IN}'
        where {i} <= {FIRST_LAG}"""


def run(name, body, where="", slices=1):
    """body is SQL over a `m` CTE holding one month; write one file per pass."""
    outdir = f"{OUT}/{name}"
    os.makedirs(outdir, exist_ok=True)
    for i in range(24):
        for k in range(slices):
            tag = f"{i:02d}" if slices == 1 else f"{i:02d}-{k}"
            part = f"{outdir}/part-{tag}.parquet"
            if os.path.exists(part):
                continue
            w = [where] if where else []
            if slices > 1:
                w.append(f"abs(hash(cuit)) % {slices} = {k}")
            filt = ("\n          and " + "\n          and ".join(w)) if w else ""
            c = con()
            c.execute(f"COPY (with m as ({month_cols(i)}{filt}) {body}) "
                      f"TO '{part}' (FORMAT parquet, COMPRESSION zstd)")
            c.close()
            clean_tmp()
        print(f"  {name} {i+1}/24", flush=True)

    c = con()
    n = c.sql(f"select count(*) from '{outdir}/*.parquet'").fetchone()[0]
    mb = sum(os.path.getsize(f) for f in glob.glob(f"{outdir}/*.parquet")) / 1e6
    print(f"{name:20s} {n:>14,} rows   {mb:>8,.0f} MB")


JOBS = {

"lender_month": lambda: run("lender_month", """
    select ent, ym, year, month,
           case when """ + PERSON + """ then 'person'
                when """ + FIRM + """ then 'firm' else 'other' end as borrower_type,
           sum(active)                                     as borrowers,
           count(*)                                        as relationships,
           sum(npl)                                        as npl_borrowers,
           sum(amount_ars)                                 as credit_ars,
           sum(case when npl=1 then amount_ars else 0 end) as npl_ars,
           sum(legal)                                      as legal_cases
    from m group by ent, ym, year, month, borrower_type"""),

"firm": lambda: run("firm", "select * from m", where=FIRM),

"sample": lambda: run("person_lender_5pct", "select * from m",
                      where=f"{PERSON} and abs(hash(cuit)) % 100 < {SAMPLE_PCT}"),

"person_month": lambda: run("person_month", """
    select cuit, ym, year, month,
           sum(active)                                     as n_lenders,
           count(*)                                        as n_relationships,
           sum(amount_ars)                                 as debt_ars,
           sum(case when npl=1 then amount_ars else 0 end) as npl_ars,
           max(status)                                     as worst_status,
           max(npl)                                        as npl
    from m group by cuit, ym, year, month""", where=PERSON, slices=SLICES),
}

if __name__ == "__main__":
    clean_tmp()
    which = sys.argv[1] if len(sys.argv) > 1 else "lender_month"
    print(f"-- {which}", flush=True)
    JOBS[which]()
