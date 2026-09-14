"""Access points to financial services (BCRA, Informe de Inclusión Financiera)
into panels that merge with the credit register by INDEC department code.

    python3 Code/build/build_puntos_acceso.py

Input, in Data/raw/bcra_inclusion/puntos_acceso/, from
bcra.gob.ar/indicadores-inclusion-financiera/:

    inclusion-financiera-puntos-acceso-entidad-tipo-localidad.txt   (required)
    inclusion-financiera-puntos-acceso-tipo-localidad.txt           (optional)

Output, in Data/processed/:

    pda_localidad     locality x type x month
    pda_depto         department x month, one column per type   (+ .dta)
    pda_lender_depto  lender x department x type x month        (+ .dta)

Three things about the source, all handled here:

  * the header names one column fewer than the rows carry. The unnamed field is
    the 10-digit INDEC locality code and sits right after the lender.
  * `tx_tipoPDA` is "TOTAL" on rows that already sum the types. Those are
    dropped; a check confirms they equal the detail exactly.
  * province names differ across BCRA files ("CABA" vs "Ciudad Autonoma de
    Buenos Aires"), so they are normalised to the same 24 the rest of the
    project uses.

On ACSF: one agency serves several banks at once, so summing over lenders
counts bank-agency links, not physical points. The column is named
`acsf_vinculos` to keep that visible. Sucursales, ATM, TAS and mobile branches
reconcile exactly against the province-level file the BCRA publishes.
"""

import pathlib
import duckdb

ROOT = pathlib.Path(__file__).resolve().parents[2]
RAW = ROOT / "Data" / "raw" / "bcra_inclusion" / "puntos_acceso"
OUT = ROOT / "Data" / "processed"
MAIN = RAW / "inclusion-financiera-puntos-acceso-entidad-tipo-localidad.txt"

COLS = {f"c{i}": "VARCHAR" for i in range(1, 10)}

TIPO = """
    case when tipo like 'Sucursales%'    then 'sucursal'
         when tipo like 'Sucursal%vil%'  then 'suc_movil'
         when tipo like 'ATM%'           then 'atm'
         when tipo like 'TAS%'           then 'tas'
         when tipo like 'ACSF%'          then 'acsf'
         when tipo = 'TOTAL'             then 'total'
         else 'otro' end
"""

# the file spells CABA and Tierra del Fuego differently than the rest of the
# project, and latin-1 mangles the accents
PROV = """
    case when provincia ilike '%capital%' or provincia ilike '%ciudad aut%'
              or provincia = 'CABA'            then 'CABA'
         when provincia ilike 'tierra d%'      then 'TIERRA DEL FUEGO'
         when provincia ilike 'santiago del%'  then 'SANTIAGO DEL ESTERO'
         when provincia ilike 'entre r%'       then 'ENTRE RIOS'
         when provincia ilike 'r%o negro'      then 'RIO NEGRO'
         when provincia ilike 'neuqu%'         then 'NEUQUEN'
         when provincia ilike 'tucum%'         then 'TUCUMAN'
         when provincia ilike 'c%rdoba'        then 'CORDOBA'
         else upper(trim(provincia)) end
"""


def con():
    c = duckdb.connect()
    c.execute("SET memory_limit='4GB'")
    c.execute("SET preserve_insertion_order = false")
    t = pathlib.Path.home() / ".duckdb_tmp"
    t.mkdir(exist_ok=True)
    c.execute(f"SET temp_directory='{t}'")
    return c


def views(c):
    c.execute(f"""
        create or replace view src as
        select try_cast(c1 as integer)                      as period,
               trim(c2) as tipo, trim(c3) as grupo, trim(c4) as entidad,
               trim(c5) as cod_loc, trim(c6) as provincia,
               trim(c7) as departamento, trim(c8) as localidad,
               try_cast(replace(trim(c9), '.', '') as integer) as n_pda
        from read_csv('{MAIN}', columns = {COLS}, header = false, skip = 1,
                      quote = '"', delim = ',', encoding = 'latin-1',
                      strict_mode = false)
        where c9 is not null
    """)
    c.execute(f"""
        create or replace view pda as
        select period,
               period // 100                                    as year,
               period % 100                                     as month,
               (period // 100 - 1960) * 12 + (period % 100) - 1  as ym,
               cod_loc,
               substr(cod_loc, 1, 5)                            as cod_depto,
               substr(cod_loc, 1, 2)                            as cod_prov,
               {PROV}                                           as provincia,
               departamento, localidad, grupo, entidad,
               {TIPO}                                           as tipo_pda,
               n_pda
        from src
    """)


def write(c, name, sql, dta=False):
    p = OUT / f"{name}.parquet"
    c.execute(f"COPY ({sql}) TO '{p}' (FORMAT parquet, COMPRESSION zstd)")
    n = c.sql(f"select count(*) from '{p}'").fetchone()[0]
    print(f"{name:20s} {n:>12,} filas  {p.stat().st_size/1e6:>6,.1f} MB", end="")
    if dta:
        df = c.sql(f"select * from '{p}'").df()
        for col in df.columns:
            if df[col].dtype == "O":
                df[col] = df[col].astype(str)
        df.to_stata(OUT / f"{name}.dta", write_index=False, version=118)
        print(f"  + {name}.dta", end="")
    print()


def check(c):
    """The TOTAL rows must equal the detail, and the four clean types must
    reconcile against the province-level file."""
    d, t = c.sql("""
        select sum(case when tipo_pda <> 'total' then n_pda else 0 end),
               sum(case when tipo_pda =  'total' then n_pda else 0 end)
        from pda""").fetchone()
    print(f"\ndetalle {d:,}  |  filas TOTAL {t:,}  |  "
          f"{'coinciden' if d == t else 'NO COINCIDEN'}")

    prov_file = RAW.parent / "BCRA_puntos_acceso_por_tipo_y_provincia.txt"
    if not prov_file.exists():
        return
    c.execute(f"""
        create or replace view provfile as
        select try_cast(cd_periodo as integer) period, trim("tx_tipoPDA") tipo,
               try_cast("nu_PDA" as integer) n
        from read_csv('{prov_file}', header = true, quote = '"', delim = ',',
                      encoding = 'latin-1', strict_mode = false, all_varchar = true)
        where "tx_tipoPDA" <> 'TOTAL'
    """)
    print("\ncontrol contra el archivo por provincia del BCRA:")
    print(c.sql(f"""
        with a as (select {TIPO} as tipo_pda, sum(n) as provincial from provfile group by 1),
             b as (select tipo_pda, sum(n_pda) as nuestro from pda
                   where tipo_pda <> 'total' group by 1)
        select b.tipo_pda, a.provincial, b.nuestro, b.nuestro - a.provincial as dif
        from b left join a using (tipo_pda) order by b.nuestro desc
    """).df().to_string(index=False))


def main():
    if not MAIN.exists():
        raise SystemExit(f"falta {MAIN}")
    c = con()
    views(c)

    write(c, "pda_localidad", """
        select ym, year, month, cod_loc, cod_depto, cod_prov,
               any_value(provincia) as provincia,
               any_value(departamento) as departamento,
               any_value(localidad) as localidad,
               tipo_pda, sum(n_pda) as n_pda
        from pda where tipo_pda <> 'total'
        group by ym, year, month, cod_loc, cod_depto, cod_prov, tipo_pda
    """)

    write(c, "pda_depto", """
        select ym, year, month, cod_depto, substr(cod_depto,1,2) as cod_prov,
               any_value(provincia) as provincia,
               any_value(departamento) as departamento,
               count(distinct cod_loc) as n_localidades,
               sum(case when tipo_pda='sucursal'  then n_pda else 0 end) as sucursales,
               sum(case when tipo_pda='suc_movil' then n_pda else 0 end) as suc_moviles,
               sum(case when tipo_pda='atm'       then n_pda else 0 end) as atm,
               sum(case when tipo_pda='tas'       then n_pda else 0 end) as tas,
               sum(case when tipo_pda='acsf'      then n_pda else 0 end) as acsf_vinculos,
               sum(case when tipo_pda in ('sucursal','suc_movil','atm','tas')
                        then n_pda else 0 end)                           as pda_sin_acsf,
               sum(n_pda)                                                as pda_total
        from pda where tipo_pda <> 'total'
        group by ym, year, month, cod_depto
    """, dta=True)

    # province level, carrying the ARCA province code so it merges straight
    # against padron.province from the credit register
    cw = ROOT / "Data" / "crosswalks" / "provincias_arca_indec.csv"
    c.execute(f"create or replace view cw as select * from read_csv('{cw}', header=true, all_varchar=true)")
    write(c, "pda_provincia", """
        select p.ym, p.year, p.month, p.cod_prov as cod_prov_indec,
               cw.cod_prov_arca, any_value(p.provincia) as provincia,
               count(distinct p.cod_depto) as n_deptos,
               count(distinct p.cod_loc)   as n_localidades,
               sum(case when tipo_pda='sucursal'  then n_pda else 0 end) as sucursales,
               sum(case when tipo_pda='suc_movil' then n_pda else 0 end) as suc_moviles,
               sum(case when tipo_pda='atm'       then n_pda else 0 end) as atm,
               sum(case when tipo_pda='tas'       then n_pda else 0 end) as tas,
               sum(case when tipo_pda='acsf'      then n_pda else 0 end) as acsf_vinculos,
               sum(case when tipo_pda in ('sucursal','suc_movil','atm','tas')
                        then n_pda else 0 end)                           as pda_sin_acsf,
               sum(n_pda) as pda_total
        from pda p join cw on cw.cod_prov_indec = p.cod_prov
        where tipo_pda <> 'total'
        group by p.ym, p.year, p.month, p.cod_prov, cw.cod_prov_arca
    """, dta=True)

    write(c, "pda_lender_depto", """
        select ym, year, month, cod_depto, grupo, entidad, tipo_pda,
               sum(n_pda) as n_pda
        from pda where tipo_pda <> 'total'
        group by ym, year, month, cod_depto, grupo, entidad, tipo_pda
    """, dta=True)

    check(c)
    print("\nllave con la Central de Deudores: cod_depto, 5 digitos INDEC")


if __name__ == "__main__":
    main()
