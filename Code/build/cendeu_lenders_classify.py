"""Fill the classification layers of Data/crosswalks/cendeu_lenders.csv.

Three layers, from hard to soft:
  regulator_class  BCRA code range, untouched here.
  grupo_bcra       official homogeneous group, from the IEF entidad.txt files.
  group            our grouping. Sources, in order: IEF group, legal name
                   (mutuales y cooperativas), explicit list for the largest
                   non financial lenders, name patterns for the tail.
  group3           coarse cut for the paper: banco / fintech / no_banco.

Every row keeps a `fuente` tag saying which rule assigned it.
Run from anywhere: python cendeu_lenders_classify.py
"""

import csv
import glob
import pathlib
import re
import unicodedata

import duckdb

ROOT = pathlib.Path(__file__).resolve().parents[2]
CSV = ROOT / "Data" / "crosswalks" / "cendeu_lenders.csv"
CENDEU = ROOT / "Data" / "processed" / "cendeu"


def norm(s):
    s = unicodedata.normalize("NFD", s.upper())
    return "".join(c for c in s if not unicodedata.combining(c))


# official homogeneous group per entity, latest IEF vintage wins
grupo_bcra = {}
for f in sorted(glob.glob(str(ROOT / "Data/raw/bcra_ief/*/entidad.txt"))):
    for line in open(f, encoding="latin-1"):
        parts = [p.strip().strip('"') for p in line.split("\t")]
        if len(parts) < 5:
            continue
        try:
            ent = int(parts[0])
        except ValueError:
            continue
        g = [p for p in parts if p.startswith(("Bancos", "Compa", "Cajas"))]
        if g:
            grupo_bcra[ent] = g[0]

GRUPO_TO_GROUP = {
    "Bancos Públicos": "banco_publico",
    "Bancos Locales de Capital Nacional": "banco_privado_nacional",
    "Bancos Locales de Capital Extranjero": "banco_privado_extranjero",
    "Bancos Sucursales de Entidades Financieras del Ext": "banco_sucursal_exterior",
    "Compañías Financieras de Capital Nacional": "cia_financiera",
    "Compañías Financieras de Capital Extranjero": "cia_financiera",
}

# licencias digitales: bancos y companias financieras sin sucursales,
# autorizados como entidades 100% digitales
DIGITAL = {
    143: "Brubank, banco digital autorizado en 2017",
    384: "Uala Bank (ex Wilobank), primer banco digital autorizado",
    45030: "Naranja Digital CF, brazo financiero de Naranja X",
    45072: "Reba CF, compania financiera digital de Grupo Transatlantica",
}

# the largest non financial lenders, one by one; together with the
# mutuales they cover about 95 percent of PNFC credit in jul-26
EDITORIAL = {
    70408: ("pnfc_tarjeta", "Tarjeta Naranja, emisora no financiera de tarjetas, Grupo Galicia"),
    72634: ("pnfc_fintech", "Mercado Credito, originacion 100% digital via Mercado Pago"),
    55012: ("pnfc_financiera_consumo", "CFN, prestamos personales con red de sucursales"),
    70147: ("pnfc_retail", "Cencosud, tarjeta de cadena minorista"),
    55024: ("pnfc_fintech", "Credicuotas (Grupo IEB), originacion digital"),
    70101: ("pnfc_tarjeta", "American Express Argentina"),
    55027: ("pnfc_retail", "Megatone, cadena de electrodomesticos"),
    55041: ("pnfc_retail", "Naldo Lombardi, cadena de electrodomesticos"),
    55408: ("pnfc_captiva", "Scania Credit, financiera de marca de camiones"),
    55296: ("pnfc_financiera_consumo", "Santander Consumer, financiera de consumo del grupo bancario"),
    70141: ("pnfc_captiva", "YPF, credito ligado a venta propia de combustible (flotas)"),
    55370: ("pnfc_financiera_consumo", "Credil, prestamos personales con sucursales"),
    70224: ("pnfc_tarjeta", "Tarjetas del Mar, tarjeta regional"),
    72306: ("pnfc_financiera_consumo", "Valle Fertil, prestamos personales"),
    55054: ("pnfc_fintech", "Credito Directo, prestamos online"),
    55294: ("pnfc_fintech", "Creditech (Adelantos), prestamos online"),
    55011: ("pnfc_retail", "Cetrogar, cadena de electrodomesticos"),
    55514: ("pnfc_financiera_consumo", "Cartasur, prestamos personales GBA sur, pese al nombre no es tarjeta"),
    55319: ("pnfc_captiva", "AGCO Capital, financiera de maquinaria agricola"),
    55449: ("pnfc_otro", "fideicomiso privado de administracion CENFIDE"),
    55030: ("pnfc_retail", "Fravega, cadena de electrodomesticos"),
    55043: ("pnfc_otro", "Provincia Leasing, Grupo BAPRO"),
    55100: ("pnfc_retail", "Bazar Avenida, cadena minorista"),
    55166: ("pnfc_fintech", "Waynimovil, prestamos por celular"),
    70248: ("pnfc_tarjeta", "Favacard, tarjeta regional de Mar del Plata"),
    70234: ("pnfc_tarjeta", "Nueva Card, tarjeta regional"),
    55340: ("pnfc_financiera_consumo", "Finanpro, prestamos personales"),
    55085: ("pnfc_fintech", "Moni, prestamos online"),
    55105: ("pnfc_financiera_consumo", "Ceibo Creditos, prestamos personales"),
    55091: ("pnfc_financiera_consumo", "Crediar, prestamos personales"),
    55107: ("pnfc_financiera_consumo", "Argencred, prestamos personales"),
    55028: ("pnfc_financiera_consumo", "Favanet, prestamos personales, grupo Favacard"),
    55412: ("pnfc_fintech", "Delivery Hero FS, credito a repartidores y comercios de PedidosYa"),
    55009: ("pnfc_retail", "Carsa, operador de Musimundo"),
    55015: ("pnfc_retail", "Coppel, cadena minorista"),
    70140: ("pnfc_retail", "Coto, tarjeta de cadena minorista"),
}

MUT = re.compile(r"\b(MUTU\w*|COOPERATIVA\w*|COOP|SOCORROS)\b")
CARD = re.compile(r"\b(CARD|TARJETA[S]?)\b")

REG_DEFAULT = {
    "credit_guarantee_soc": "sgr",
    "public_guarantee_fund": "fondo_garantia_publico",
    "financial_trust": "fideicomiso",
}


def classify(ent, name, reg):
    if ent in DIGITAL:
        base = "banco_digital" if reg == "financial_institution" else "cia_financiera_digital"
        return base, "editorial: " + DIGITAL[ent]
    if reg in ("financial_institution", "finance_company"):
        g = grupo_bcra.get(ent)
        if g in GRUPO_TO_GROUP:
            return GRUPO_TO_GROUP[g], "ief_entidad: " + g
        return "sin_clasificar", "sin grupo en IEF"
    if reg in REG_DEFAULT:
        return REG_DEFAULT[reg], "codigo_bcra"
    # non financial lenders
    if MUT.search(norm(name)):
        return "mutual_coop", "razon_social"
    if ent in EDITORIAL:
        g, why = EDITORIAL[ent]
        return g, "editorial: " + why
    if CARD.search(norm(name)):
        return "pnfc_tarjeta", "razon_social (marca de tarjeta)"
    return "pnfc_otro", "cola no clasificada"


def coarse(group):
    if group.startswith("banco") and group != "banco_digital":
        return "banco"
    if group in ("banco_digital", "cia_financiera_digital", "pnfc_fintech"):
        return "fintech"
    return "no_banco"


rows = {int(r["ent"]): r for r in csv.DictReader(open(CSV, encoding="utf-8"))}

# entities in the bases that the csv does not know yet
con = duckdb.connect()
ents = con.sql(f"""
    select distinct ent from '{CENDEU}/panel24_wide.parquet'
    union select distinct ent from '{CENDEU}/deudores.parquet'
""").df().ent.astype(int)
for e in ents:
    if e not in rows:
        rows[e] = {"ent": str(e), "name": "", "regulator_class": "unknown",
                   "economic_group": "", "has_balance": "0"}

out = []
for e in sorted(rows):
    r = rows[e]
    if r["regulator_class"] == "unknown":
        g, src = "sin_clasificar", "no esta en maeent, rango nuevo"
    else:
        g, src = classify(e, r["name"], r["regulator_class"])
    out.append({
        "ent": e, "name": r["name"], "regulator_class": r["regulator_class"],
        "grupo_bcra": grupo_bcra.get(e, ""), "group": g, "group3": coarse(g),
        "fuente": src, "economic_group": r.get("economic_group", ""),
        "has_balance": r.get("has_balance", "0"),
    })

with open(CSV, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
    w.writeheader()
    w.writerows(out)

from collections import Counter
print(len(out), "rows")
for k, v in Counter(r["group"] for r in out).most_common():
    print(f"  {k:26s} {v}")
print("group3:", Counter(r["group3"] for r in out))
