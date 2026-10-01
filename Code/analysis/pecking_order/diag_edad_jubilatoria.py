"""Orden de repago alrededor de la edad jubilatoria.

Si la prioridad la fija quien controla la cuenta donde entra el ingreso, jubilarse
tendría que mover la prioridad hacia el banco que paga el haber. La edad legal es
60 para mujeres y 65 para varones, así que el corrimiento debería aparecer a edades
distintas según sexo. Es un chequeo descriptivo del mecanismo, no una estimación.

Misma definición de evento que 01_orden_de_repago.ipynb: persona con dos o más
relaciones con saldo, todas en situación 1 en t-1; alguna (no todas) pasa a 2-5 en t.
Medida: caídas observadas sobre esperadas bajo elección al azar (m/k por relación).
Salidas agregadas por sexo, edad y categoría. No se guarda ningún identificador.
"""
from pathlib import Path
import os, tempfile
import numpy as np
import pandas as pd
import duckdb
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SAMPLE = ROOT / 'Data/processed/cendeu/person_lender_5pct'
PADRON = ROOT / 'Data/processed/cendeu/padron.parquet'
OUT = ROOT / 'Code/output/pecking_order'
BLUE, OCHRE, GREY = '#24465B', '#AD683B', '#9a9a9a'

# categorías: mismas reglas que po.categories(), agrupadas un poco más
x = pd.read_csv(ROOT / 'Data/crosswalks/cendeu_lenders.csv')[['ent', 'group']]
g, e = x['group'], x['ent']
cat = pd.Series('Otro', index=x.index)
cat[g.eq('banco_publico')] = 'Banco público'
cat[g.isin(['banco_privado_nacional', 'banco_privado_extranjero', 'banco_sucursal_exterior'])] = 'Banco privado'
cat[g.eq('banco_digital')] = 'Banco digital'
cat[g.isin(['pnfc_retail', 'pnfc_financiera_consumo'])] = 'Retail y consumo'
cat[g.eq('pnfc_tarjeta')] = 'Tarjeta no bancaria'
cat[g.eq('mutual_coop')] = 'Mutual o cooperativa'
cat[e.eq(72634)] = 'MercadoLibre'
cat[e.between(10000, 10999) | e.eq(40011) | g.isin(['sgr', 'fondo_garantia_publico', 'sin_clasificar'])] = 'fuera'
x['cat'] = cat

tmp = Path(tempfile.mkdtemp(prefix='edad_jub_'))
con = duckdb.connect()
con.execute(f"SET memory_limit='{os.environ.get('PO_MEM', '1500MB')}'")
con.execute(f"SET temp_directory='{tmp.as_posix()}'")
con.register('cw', x[['ent', 'cat']])

parts = []
for i in range(1, 23):   # part i = mes t, part i+1 = t-1; 07/2026 queda fuera
    prev, curr = SAMPLE / f'part-{i + 1:02d}.parquet', SAMPLE / f'part-{i:02d}.parquet'
    parts.append(con.execute(f"""
    WITH prev AS (SELECT p.ent, hash(p.cuit) pid, p.cuit, p.ym, p.status
                  FROM read_parquet('{prev.as_posix()}') p JOIN cw USING (ent)
                  WHERE p.amount_ars > 0 AND cw.cat <> 'fuera' AND p.ent <> 150),
    ppl AS (SELECT pid, count(*) k, bool_and(status = 1) ok FROM prev GROUP BY pid),
    curr AS (SELECT ent, hash(cuit) pid, status FROM read_parquet('{curr.as_posix()}')),
    ev AS (SELECT p.ym + 1 ym, p.pid, p.cuit, p.ent, (c.status BETWEEN 2 AND 5)::INT y
           FROM prev p JOIN ppl USING (pid)
           LEFT JOIN curr c ON c.ent = p.ent AND c.pid = p.pid
           WHERE ppl.ok AND ppl.k >= 2),
    grp AS (SELECT ym, pid, sum(y) nb, count(*) k FROM ev GROUP BY 1, 2
            HAVING sum(y) > 0 AND sum(y) < count(*))
    SELECT ev.ym, ev.cuit, cw.cat, ev.y, grp.nb::DOUBLE / grp.k AS esperado
    FROM ev JOIN grp USING (ym, pid) JOIN cw USING (ent)""").fetchdf())
d = pd.concat(parts, ignore_index=True)

con.register('cu', d[['cuit']].drop_duplicates())
pad = con.execute(f"""SELECT p.cuit, p.birth_date, p.sex FROM read_parquet('{PADRON.as_posix()}') p
                      SEMI JOIN cu USING (cuit)""").fetchdf().drop_duplicates('cuit')
d = d.merge(pad, on='cuit', how='left', validate='many_to_one')
bd = d.birth_date.astype(str)
by, bm = pd.to_numeric(bd.str[:4], errors='coerce'), pd.to_numeric(bd.str[5:7], errors='coerce')
d['edad'] = (d.ym - (by * 12 + bm - 1)) // 12
d = d.drop(columns=['cuit', 'birth_date'])
con.close()

tab = (d[d.sex.isin(['F', 'M']) & d.edad.between(50, 75)]
       .groupby(['sex', 'edad', 'cat'])
       .agg(relaciones=('y', 'size'), observadas=('y', 'sum'), esperadas=('esperado', 'sum'))
       .reset_index())
tab['obs_sobre_esp'] = tab.observadas / tab.esperadas
tab.to_csv(OUT / '10_edad_jubilatoria.csv', index=False)

# figura: dos categorías, mujeres y varones, líneas en las edades legales
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.spines.top': False,
                     'axes.spines.right': False, 'axes.edgecolor': '#888888', 'axes.linewidth': 0.6,
                     'legend.frameon': False, 'savefig.dpi': 180, 'pdf.fonttype': 42})
fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), sharey=False, layout='constrained')
for ax, c in zip(axes, ['Banco público', 'MercadoLibre']):
    for sx, col, mk, lab in [('F', OCHRE, 'o', 'Mujeres (edad legal 60)'), ('M', BLUE, 's', 'Varones (edad legal 65)')]:
        s = tab[(tab.cat == c) & (tab.sex == sx) & tab.edad.between(52, 72)].sort_values('edad')
        ax.plot(s.edad, s.obs_sobre_esp, color=col, marker=mk, markersize=3.5, linewidth=1.2, label=lab)
    ax.axvline(60, color=OCHRE, linewidth=0.7, linestyle=':')
    ax.axvline(65, color=BLUE, linewidth=0.7, linestyle=':')
    ax.axhline(1, color=GREY, linewidth=0.6)
    ax.set(title=c, xlabel='Edad en el mes del evento', xticks=range(52, 73, 4))
    ax.grid(axis='y', color='#dddddd', linewidth=0.5)
axes[0].set_ylabel('Caídas observadas / esperadas')
axes[1].legend(loc='upper left')
for ext in ['png', 'pdf']:
    fig.savefig(OUT / f'10_edad_jubilatoria.{ext}', bbox_inches='tight')
print(tab[tab.cat.isin(['Banco público', 'MercadoLibre'])].pivot_table(
    index='edad', columns=['cat', 'sex'], values='obs_sobre_esp').loc[56:68].round(2).to_string())
