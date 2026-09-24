"""Funciones del análisis de orden de repago.

Todo corre en la máquina local. Los intermedios que conservan un identificador
(hash del CUIT) van a un directorio temporal fuera del repositorio y se borran al
final del notebook. Las salidas en Code/output/pecking_order son agregadas.
"""
from pathlib import Path
import os, sys, json, shutil, tempfile, importlib.metadata
import numpy as np
import pandas as pd
import duckdb

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = ROOT / 'Data/processed'
CENDEU = DATA / 'cendeu'
SAMPLE = CENDEU / 'person_lender_5pct'
OUT = ROOT / 'Code/output/pecking_order'
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT / 'Code/analysis/liquidez_fintech'))
from common import figure_style  # noqa: E402  mismo estilo que el resto del proyecto

BLUE, OCHRE, OLIVE, INK, GREY = '#24465B', '#AD683B', '#777363', '#252525', '#9a9a9a'
YM_LAST = 2026 * 12 + 6      # 07/2026: corte incompleto, no se usa como mes t
YM_FIRST = 2024 * 12 + 7     # 08/2024: primer mes del panel, inicio de relación censurado
MIN_PERSONAS = 500           # piso para cualquier corte geográfico

# Bancos provinciales o municipales con provincia de origen inequívoca (código ARCA).
HOME = {14: 1, 20: 3, 29: 0, 45: 10, 65: 12, 83: 17, 86: 23, 93: 21, 94: 4, 97: 20,
        268: 24, 309: 8, 311: 16, 315: 18, 321: 13, 330: 12, 386: 5}
MACRO = 285
MACRO_HOME = {9, 6, 19, 14}  # agente financiero en Salta, Jujuy, Misiones y Tucumán

CATS = ['Banco público', 'Banco digital', 'Compañía financiera', 'Financiera digital',
        'Tarjeta no bancaria', 'MercadoLibre', 'Otras fintech', 'Retail',
        'Financiera de consumo', 'Mutual o cooperativa', 'Otro PNFC']
REF = 'Banco privado'


def ym_label(ym):
    return pd.to_datetime(dict(year=ym // 12, month=ym % 12 + 1, day=1))


def workdir():
    tmp = Path(tempfile.mkdtemp(prefix='orden_repago_'))
    (tmp / 'duckdb').mkdir()
    (tmp / 'ev').mkdir()
    return tmp


def connect(tmp):
    con = duckdb.connect()
    con.execute(f"SET memory_limit='{os.environ.get('PO_MEM', '2GB')}'")
    con.execute('SET threads=4')
    con.execute(f"SET temp_directory='{(tmp / 'duckdb').as_posix()}'")
    return con


def categories():
    """Categorías analíticas por rango de código BCRA y grupo del crosswalk.
    Corrige dos problemas del crosswalk: los códigos 44xxx-45xxx y 65xxx son compañías
    financieras (no fideicomisos) y MercadoLibre va aparte porque es 3/4 de 'fintech'."""
    x = pd.read_csv(ROOT / 'Data/crosswalks/cendeu_lenders.csv')[['ent', 'name', 'group']]
    g, e = x['group'], x.ent
    cat = pd.Series('Otro PNFC', index=x.index)
    cat[g.eq('banco_publico')] = 'Banco público'
    cat[g.isin(['banco_privado_nacional', 'banco_privado_extranjero', 'banco_sucursal_exterior'])] = 'Banco privado'
    cat[g.eq('banco_digital')] = 'Banco digital'
    cat[e.between(44000, 45999) | e.between(65000, 65999) | g.eq('cia_financiera')] = 'Compañía financiera'
    cat[g.eq('cia_financiera_digital')] = 'Financiera digital'
    cat[g.eq('pnfc_tarjeta')] = 'Tarjeta no bancaria'
    cat[g.eq('pnfc_fintech')] = 'Otras fintech'
    cat[e.eq(72634)] = 'MercadoLibre'
    cat[g.eq('pnfc_retail')] = 'Retail'
    cat[g.eq('pnfc_financiera_consumo')] = 'Financiera de consumo'
    cat[g.eq('mutual_coop')] = 'Mutual o cooperativa'
    cat[e.between(10000, 10999) | e.eq(40011)] = 'Fideicomiso financiero'
    cat[g.isin(['sgr', 'fondo_garantia_publico'])] = 'Garantía'
    cat[g.eq('sin_clasificar')] = 'Sin clasificar'
    x['cat'] = cat
    return x


def build_events(con, tmp):
    """Relaciones elegibles para el primer evento de mora, un archivo por mes t.
    Elegible en t-1: persona con 2+ relaciones con saldo, todas en situación 1.
    outcome en t: 0 sigue sana, 1 pasa a situación 2-5, 2 sale (sin fila o saldo cero)."""
    con.execute(f"""COPY (SELECT ent, hash(cuit) AS pid, min(ym) AS start_ym
        FROM read_parquet('{SAMPLE.as_posix()}/part-*.parquet') GROUP BY 1, 2)
        TO '{(tmp / 'start.parquet').as_posix()}' (FORMAT parquet)""")
    for i in range(1, 23):   # part i = mes t; part i+1 = t-1; part-00 (07/2026) queda fuera
        prev, curr = SAMPLE / f'part-{i + 1:02d}.parquet', SAMPLE / f'part-{i:02d}.parquet'
        con.execute(f"""COPY (
        WITH prev AS (SELECT ent, hash(cuit) pid, ym, status, amount_ars
                      FROM read_parquet('{prev.as_posix()}') WHERE amount_ars > 0),
        ppl AS (SELECT pid, count(*) k, bool_and(status = 1) all_good FROM prev GROUP BY pid),
        curr AS (SELECT ent, hash(cuit) pid, status, amount_ars FROM read_parquet('{curr.as_posix()}'))
        SELECT p.ym + 1 AS ym, p.pid, p.ent, p.amount_ars AS amt_prev, ppl.k::TINYINT AS k,
               c.status AS status_t,
               CASE WHEN c.status BETWEEN 2 AND 5 THEN 1
                    WHEN c.pid IS NULL OR c.amount_ars = 0 THEN 2 ELSE 0 END::TINYINT AS outcome
        FROM prev p JOIN ppl USING (pid)
        LEFT JOIN curr c ON c.ent = p.ent AND c.pid = p.pid
        WHERE ppl.all_good AND ppl.k >= 2)
        TO '{(tmp / 'ev' / f'ev-{i:02d}.parquet').as_posix()}' (FORMAT parquet)""")
    return (tmp / 'ev' / '*.parquet').as_posix()


def build_long(con, tmp, pids_sql):
    """Panel completo de las personas con evento, para seguir cada relación en t+h."""
    con.execute(f"""COPY (SELECT ym, hash(cuit) pid, ent, status, amount_ars
        FROM read_parquet('{SAMPLE.as_posix()}/part-*.parquet')
        WHERE hash(cuit) IN ({pids_sql}) AND ym < {YM_LAST})
        TO '{(tmp / 'long.parquet').as_posix()}' (FORMAT parquet)""")
    return (tmp / 'long.parquet').as_posix()


# ---------- estimación ----------

def _groups(df, g):
    df = df.sort_values(g, kind='stable').reset_index(drop=True)
    gid = pd.factorize(df[g])[0]
    starts = np.r_[0, np.flatnonzero(np.diff(gid)) + 1]
    return df, gid, starts


def _chunks(starts, n, size=150_000):
    """Cortes de filas que respetan los límites de grupo, para no multiplicar matrices enteras."""
    cuts = [0]
    for s_ in starts[1:]:
        if s_ - cuts[-1] >= size:
            cuts.append(int(s_))
    return cuts + [n]


def clogit(df, y, X, g='grp', cluster='pid', iters=60, tol=1e-9):
    """Logit condicional con efecto fijo de grupo (persona-mes). Usa los grupos con
    exactamente una relación que cae: el modelo describe cuál de las relaciones cae.
    Errores agrupados por persona. Trabaja por bloques de grupos para acotar memoria."""
    X = list(X)
    mask = df.groupby(g)[y].transform('sum').eq(1) & df.groupby(g)[y].transform('size').ge(2)
    tmp, gid, starts = _groups(df.loc[mask, [g, y, cluster] + X], g)
    Xm, yv = tmp[X].to_numpy(np.float32), tmp[y].to_numpy(bool)
    keep = Xm.std(0) > 0
    Xm, names = Xm[:, keep], [x for x, k in zip(X, keep) if k]
    cuts = _chunks(starts, len(tmp))
    K = Xm.shape[1]

    def pieces(b):
        """Probabilidades dentro de grupo, x promedio por grupo, gradiente y hessiano."""
        xbar_all, grad, A = [], np.zeros(K), np.zeros((K, K))
        for lo, hi in zip(cuts[:-1], cuts[1:]):
            st = starts[(starts >= lo) & (starts < hi)] - lo
            gi = gid[lo:hi] - gid[lo]
            x = Xm[lo:hi].astype(np.float64)
            eta = x @ b
            eta -= np.maximum.reduceat(eta, st)[gi]
            w = np.exp(eta)
            p = w / np.add.reduceat(w, st)[gi]
            xp = x * p[:, None]
            xbar = np.add.reduceat(xp, st)
            grad += x[yv[lo:hi]].sum(0) - xbar.sum(0)
            A += x.T @ xp - xbar.T @ xbar
            xbar_all.append(xbar)
        return np.vstack(xbar_all), grad, -A

    b = np.zeros(K)
    for it in range(iters):
        xbar, grad, H = pieces(b)
        step = np.linalg.solve(H, grad)
        b -= step
        if np.max(np.abs(step)) < tol:
            break
    xbar, grad, H = pieces(b)
    # score por persona: x del elegido menos x promedio del grupo
    chosen = np.flatnonzero(yv)
    sc = Xm[chosen].astype(np.float64) - xbar[gid[chosen]]
    cl = pd.factorize(tmp[cluster].to_numpy()[chosen])[0]
    S = np.zeros((cl.max() + 1, K))
    np.add.at(S, cl, sc)
    Hinv = np.linalg.inv(H)
    G = S.shape[0]
    V = Hinv @ (S.T @ S) @ Hinv * G / (G - 1)
    se = np.sqrt(np.diag(V))
    out = pd.DataFrame({'coef': b, 'se': se, 'or': np.exp(b),
                        'lo': np.exp(b - 1.96 * se), 'hi': np.exp(b + 1.96 * se)}, index=names)
    info = {'grupos': len(starts), 'relaciones': len(tmp), 'personas': G, 'iteraciones': it + 1}
    return out, info


def fe_ols(df, y, X, g='grp', cluster='pid'):
    """MCO con efecto fijo de grupo; errores agrupados por persona."""
    tmp, gid, starts = _groups(df[[g, y, cluster] + list(X)], g)
    Xm, yv = tmp[X].to_numpy(float), tmp[y].to_numpy(float)
    n = np.diff(np.r_[starts, len(tmp)])
    Xd = Xm - (np.add.reduceat(Xm, starts) / n[:, None])[gid]
    yd = yv - (np.add.reduceat(yv, starts) / n)[gid]
    XtX = Xd.T @ Xd
    b = np.linalg.solve(XtX, Xd.T @ yd)
    u = yd - Xd @ b
    cl = pd.factorize(tmp[cluster])[0]
    S = np.zeros((cl.max() + 1, Xm.shape[1]))
    np.add.at(S, cl, Xd * u[:, None])
    Inv = np.linalg.inv(XtX)
    G = S.shape[0]
    V = Inv @ (S.T @ S) @ Inv * G / (G - 1)
    return pd.DataFrame({'coef': b, 'se': np.sqrt(np.diag(V))}, index=X)


# ---------- variables ----------

SIZE = ['sh_lt10', 'sh_10_25', 'sh_50p']        # referencia: 25 a 50% de la deuda de la persona
AGE = ['age_lt3', 'age_3_6', 'age_6_12']        # referencia: 12 meses o más, o inicio censurado


def prep(d):
    d = d.copy()
    d['y'] = (d.outcome == 1).astype(int)
    d['grp'] = d.ym.astype(np.int64) * (2 ** 22) + pd.factorize(d.pid)[0]
    d['sh_lt10'] = (d.share < 0.10).astype('float32')
    d['sh_10_25'] = d.share.between(0.10, 0.25, inclusive='left').astype('float32')
    d['sh_50p'] = (d.share >= 0.50).astype('float32')
    d['age'] = (d.ym - 1) - d.start_ym
    cens = d.start_ym.eq(YM_FIRST)
    d['age_lt3'] = ((d.age < 3) & ~cens).astype('float32')
    d['age_3_6'] = (d.age.between(3, 5) & ~cens).astype('float32')
    d['age_6_12'] = (d.age.between(6, 11) & ~cens).astype('float32')
    return d


def add_borrower(d, pad):
    d = d.merge(pad, on='pid', how='left', validate='many_to_one')
    by = pd.to_numeric(d.birth_date.str[:4], errors='coerce')
    by[by <= 1901] = np.nan
    d['edad'] = d.ym // 12 - by
    act = d.activity.fillna(0).astype(int)
    d['con_actividad'] = act.gt(0)
    d['comercio'] = act.astype(str).str[:2].isin(['46', '47'])
    d['prov_bank'] = d.ent.isin(list(HOME))
    home = d.ent.map(HOME)
    d['pb_home'] = (d.prov_bank & home.eq(d.province)).astype('float32')
    d['pb_away'] = (d.prov_bank & home.ne(d.province)).astype('float32')
    d['macro_home'] = (d.ent.eq(MACRO) & d.province.isin(MACRO_HOME)).astype('float32')
    d['macro_away'] = (d.ent.eq(MACRO) & ~d.province.isin(MACRO_HOME)).astype('float32')
    return d


def cat_dummies(d, split_banks=False):
    """Una dummy por categoría; la referencia es la banca privada. Con split_banks, los
    bancos provinciales y Macro salen de su categoría y entran por separado."""
    cols = []
    for k in CATS:
        m = d.cat.eq(k)
        if split_banks:
            m &= ~d.prov_bank & d.ent.ne(MACRO)
        d['c_' + k] = m.astype('float32')
        cols.append('c_' + k)
    if split_banks:
        cols += ['pb_home', 'pb_away', 'macro_home', 'macro_away']
    return cols


# ---------- salidas ----------

# nombres cortos para tablas y figuras
SHORT = {72634: 'MercadoLibre', 7: 'Galicia', 11: 'Nación', 14: 'Provincia de Buenos Aires', 17: 'BBVA',
         15: 'ICBC', 72: 'Santander', 285: 'Macro', 27: 'Supervielle', 29: 'Ciudad', 20: 'Córdoba',
         321: 'Santiago del Estero', 311: 'Chaco', 94: 'Corrientes', 386: 'Entre Ríos', 330: 'Santa Fe',
         65: 'Municipal de Rosario', 93: 'La Pampa', 97: 'Neuquén', 83: 'Chubut', 45: 'San Juan',
         309: 'La Rioja', 315: 'Formosa', 86: 'Santa Cruz', 268: 'Tierra del Fuego', 143: 'Brubank',
         384: 'Ualá', 45030: 'Naranja Digital', 70408: 'Tarjeta Naranja', 45072: 'Reba',
         55024: 'Credicuotas', 55054: 'Crédito Directo', 55085: 'Moni', 55294: 'Creditech',
         55166: 'Waynicoin', 55412: 'Delivery Hero', 70147: 'Cencosud', 55012: 'CFN', 55030: 'Frávega',
         338: 'BST', 191: 'Credicoop', 44: 'Hipotecario', 34: 'Patagonia', 389: 'Columbia',
         322: 'Industrial', 310: 'Del Sol', 44077: 'Compañía Financiera Argentina',
         330: 'Santa Fe', 16: 'Citibank'}


def short_name(ent, name):
    if ent in SHORT:
        return SHORT[ent]
    n = ' ' + ' '.join(str(name).upper().replace('.', ' ').replace(',', ' ').split()) + ' '
    for suf in [' SOCIEDAD ANONIMA UNIPERSONAL', ' SOCIEDAD ANONIMA', ' SOCIEDAD ANÓNIMA', ' S A U ', ' S A ',
                ' SAU ', ' SA ', ' SRL ', ' S R L ', ' SAS ', ' SACI E I ', ' S A C I E I ']:
        n = n.replace(suf, ' ')
    words = n.split()
    small = {'DE', 'DEL', 'LA', 'LOS', 'Y', 'E'}
    out = [w.capitalize() if (i == 0 or w.upper() not in small) else w.lower() for i, w in enumerate(words)]
    return ' '.join(out)[:34]


def save(fig, name):
    for ext in ['png', 'pdf']:
        fig.savefig(OUT / f'{name}.{ext}', bbox_inches='tight')


def or_plot(ax, tab, labels=None, color=BLUE, offset=0.0, label=None, marker='o'):
    """Razones de chances con intervalo al 95%, escala logarítmica, referencia en 1."""
    y = np.arange(len(tab))[::-1] + offset
    ax.hlines(y, tab.lo, tab.hi, color=color, linewidth=1.2)
    ax.plot(tab['or'], y, marker, color=color, markersize=5, label=label, linestyle='none')
    ax.axvline(1, color=GREY, linewidth=0.7, linestyle=':')
    ax.set_xscale('log')
    ax.set_yticks(np.arange(len(tab))[::-1])
    ax.set_yticklabels(labels if labels is not None else tab.index)
    ticks = [0.2, 0.3, 0.5, 0.7, 1, 1.5, 2]
    ax.set_xticks(ticks)
    ax.set_xticklabels([f'{t:g}'.replace('.', ',') for t in ticks])
    ax.minorticks_off()


def record_inputs(paths, name):
    files = [{'path': str(Path(p).relative_to(ROOT)), 'bytes': Path(p).stat().st_size,
              'mtime_ns': Path(p).stat().st_mtime_ns} for p in sorted(set(map(str, paths)))]
    pk = {p: importlib.metadata.version(p) for p in ['duckdb', 'pandas', 'numpy', 'pyarrow', 'matplotlib']}
    (OUT / f'{name}_inputs.json').write_text(json.dumps({'files': files, 'packages': pk}, indent=2) + '\n')


def cleanup(tmp):
    shutil.rmtree(tmp, ignore_errors=True)
