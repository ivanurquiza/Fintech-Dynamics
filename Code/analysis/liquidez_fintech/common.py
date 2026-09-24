"""Configuración, clasificación explícita y estilo compartidos por los notebooks."""
from pathlib import Path
import json
import importlib.metadata
import pandas as pd
import duckdb
import matplotlib as mpl
import matplotlib.dates as mdates

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / 'Data/processed'
CENDEU = DATA / 'cendeu'
HERE = Path(__file__).resolve().parent
OUT = ROOT / 'Code/output/liquidez_fintech'
OUT.mkdir(parents=True, exist_ok=True)
BASELINE = pd.Timestamp('2025-05-01')
GROUPS = ['Bancos tradicionales', 'Bancos digitales', 'Financieras digitales',
          'Fintech PNFC', 'Otros prestamistas', 'Garantías', 'Sin clasificar']
COLORS = {'Bancos': '#24465B', 'Fintech PNFC': '#AD683B',
          'Otros prestamistas': '#777363', 'Total': '#252525'}


def connect():
    con = duckdb.connect()
    con.execute("SET memory_limit='3GB'")
    con.execute('SET threads=4')
    con.execute("SET max_temp_directory_size='2GB'")
    tmp = ROOT / '.duckdb_tmp/liquidez_fintech'
    tmp.mkdir(parents=True, exist_ok=True)
    con.execute(f"SET temp_directory='{tmp.as_posix()}'")
    return con


def lender_taxonomy():
    """Vista analítica; no modifica el crosswalk fuente. Estado regulado a mayo 2025."""
    tax = pd.read_csv(ROOT / 'Data/crosswalks/cendeu_lenders.csv')
    assert tax.ent.is_unique
    balance = pd.read_stata(DATA / 'balances_bancos.dta', convert_categoricals=False)
    pre = balance.loc[balance.ym.eq(BASELINE), ['ent', 'es_banco']].copy()
    pre.ent = pre.ent.astype(int)
    assert pre.ent.is_unique
    tax = tax.merge(pre, on='ent', how='left', validate='one_to_one')
    tax['grupo'] = 'Otros prestamistas'
    tax.loc[tax['group'].isin(['sin_clasificar']), 'grupo'] = 'Sin clasificar'
    tax.loc[tax['group'].isin(['sgr', 'fondo_garantia_publico']), 'grupo'] = 'Garantías'
    tax.loc[tax['group'].eq('pnfc_fintech'), 'grupo'] = 'Fintech PNFC'
    # Códigos bancarios fuera del corte se conservan según taxonomía fuente y se marcan.
    is_bank = tax.es_banco.eq(1) | (tax.es_banco.isna() & tax['group'].str.startswith('banco_'))
    tax.loc[is_bank, 'grupo'] = 'Bancos tradicionales'
    tax.loc[is_bank & tax['group'].eq('banco_digital'), 'grupo'] = 'Bancos digitales'
    tax.loc[tax['group'].eq('cia_financiera_digital'), 'grupo'] = 'Financieras digitales'
    tax['is_bank'] = tax.grupo.isin(['Bancos tradicionales', 'Bancos digitales'])
    tax['is_fintech'] = tax.grupo.eq('Fintech PNFC')
    tax['include_credit'] = ~tax.grupo.isin(['Garantías', 'Sin clasificar'])
    tax['report_group'] = 'Otros prestamistas'
    tax.loc[tax.is_bank, 'report_group'] = 'Bancos'
    tax.loc[tax.is_fintech, 'report_group'] = 'Fintech PNFC'
    tax['revision'] = ''
    suspect = tax.es_banco.eq(0) & tax['group'].isin(['fideicomiso', 'pnfc_otro'])
    tax.loc[suspect, 'revision'] = 'Entidad regulada en IEF; revisar categoría fuente'
    tax.loc[is_bank & tax.es_banco.isna(), 'revision'] = 'Banco fuera del corte IEF de mayo; fechar continuidad'
    return tax


def price_index():
    ipc = pd.read_stata(DATA / 'ipc.dta')[['ym', 'ipc_nacional']].rename(columns={'ym':'fecha'})
    assert ipc.fecha.is_unique and ipc.ipc_nacional.gt(0).all()
    base = ipc.loc[ipc.fecha.eq(BASELINE), 'ipc_nacional'].item()
    ipc['deflactor'] = base / ipc.ipc_nacional
    return ipc


def figure_style():
    mpl.rcParams.update({'font.family':'DejaVu Sans', 'font.size':10,
        'axes.titlesize':11, 'axes.labelsize':10, 'axes.spines.top':False,
        'axes.spines.right':False, 'axes.edgecolor':'#888888', 'axes.linewidth':0.6,
        'axes.facecolor':'white', 'figure.facecolor':'white', 'axes.grid':False,
        'legend.frameon':False, 'lines.linewidth':1.8, 'figure.dpi':120,
        'savefig.dpi':180, 'pdf.fonttype':42, 'svg.fonttype':'none'})


def time_axis(ax, dates):
    dates = pd.DatetimeIndex(dates)
    ticks = sorted(set([dates.min(), dates.max(), BASELINE,
                       pd.Timestamp('2025-01-01'), pd.Timestamp('2026-01-01')]))
    ax.set_xticks([x for x in ticks if dates.min() <= x <= dates.max()])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
    ax.grid(axis='y', color='#dddddd', linewidth=0.5)


def save_figure(fig, name):
    for extension in ['png', 'pdf']:
        fig.savefig(OUT / f'{name}.{extension}', bbox_inches='tight')


def record_inputs(paths, name):
    """Trazabilidad por tamaño/mtime; no es un hash criptográfico de las bases."""
    files = [{'path':str(p.relative_to(ROOT)), 'bytes':p.stat().st_size,
              'mtime_ns':p.stat().st_mtime_ns} for p in sorted(set(paths))]
    packages = {p:importlib.metadata.version(p) for p in
                ['duckdb','pandas','numpy','pyarrow','matplotlib','nbformat','nbclient']}
    (OUT / f'{name}_inputs.json').write_text(json.dumps(
        {'files':files,'packages':packages,'baseline':str(BASELINE.date())}, indent=2)+'\n')
