"""
Extrae de los resumenes mensuales de CAFCI (raw/cafci/resumenes/*.pdf) las
series agregadas del lado del fondeo:
  - patrimonio de personas humanas y de personas juridicas (mensual)
  - cuentas de cuotapartistas via ACDI citadas de CNV (con su fecha de referencia)
Salida: raw/cafci/agregados_cafci.csv (una fila por PDF) y un reporte por
pantalla de que se encontro y que no en cada archivo, para auditar el parseo.
Uso:      python extraer_cafci_agregados.py
Requiere: pip install pdfplumber
"""
import glob
import os
import pathlib
import re
import csv
import pdfplumber

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = pathlib.Path(__file__).resolve().parents[2]
RAW = str(ROOT / "Data" / "raw" / "cafci")

MESES = {"enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5,
         "junio": 6, "julio": 7, "agosto": 8, "septiembre": 9,
         "setiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12}

def num(s):
    return float(s.replace(".", "").replace(",", "."))

def monto(m):
    """Convierte una captura (numero, unidad) a millones de pesos."""
    v = num(m.group(1))
    unidad = (m.group(2) or "").lower()
    if "billon" in unidad:
        v = v * 1e6
    return v

filas = []
for path in sorted(glob.glob(os.path.join(RAW, "resumenes", "*.pdf"))):
    per = os.path.basename(path)[:6]
    texto = ""
    with pdfplumber.open(path) as pdf:
        for p in pdf.pages:
            texto += (p.extract_text() or "") + "\n"
    texto_plano = re.sub(r"\s+", " ", texto)

    fila = {"periodo": per, "pat_humanas": None, "pat_juridicas": None,
            "cuentas_humanas": None, "cuentas_acdi": None, "acdi_ref": None}

    # formato reciente y, como fallback, la redaccion de los reportes 2019
    # ("en manos de Personas Humanas fue de $ X millones"); los montos se
    # normalizan a millones de pesos
    for pat in [r"[Pp]ersonas\s+[Hh]umanas[^0-9$]{0,40}\$?\s*(\d[\d.]*,?\d*)\s*(millones|billones)?",
                r"[Pp]ersonas\s+[Hh]umanas\s+fue\s+de\s+\$?\s*(\d[\d.]*,?\d*)\s*(millones|billones)?"]:
        m = re.search(pat, texto_plano)
        if m:
            fila["pat_humanas"] = monto(m)
            break
    for pat in [r"[Pp]ersonas\s+[Jj]ur.dicas[^0-9$]{0,40}\$?\s*(\d[\d.]*,?\d*)\s*(millones|billones)?",
                r"[Pp]ersonas\s+[Jj]ur.dicas[^$]{0,90}\$\s*(\d[\d.]*,?\d*)\s*(millones|billones)?"]:
        m = re.search(pat, texto_plano)
        if m:
            fila["pat_juridicas"] = monto(m)
            break
    m = re.search(r"cuentas\s+de\s+[Pp]ersonas\s+[Hh]umanas[^0-9]{0,80}(\d[\d.]*)", texto_plano)
    if m:
        fila["cuentas_humanas"] = int(m.group(1).replace(".", ""))

    m = re.search(r"ACDIs?\)?\s*fue\s*de\s*(\d[\d.]*)", texto_plano)
    if m:
        fila["cuentas_acdi"] = int(m.group(1).replace(".", ""))
        ref = re.search(r"[Aa]\s+(" + "|".join(MESES) + r")\s+de\s+(20\d\d)[^.]{0,120}ACDIs?", texto_plano)
        if ref:
            fila["acdi_ref"] = f"{ref.group(2)}{MESES[ref.group(1).lower()]:02d}"

    filas.append(fila)
    falto = [k for k, v in fila.items() if v is None and k not in ("acdi_ref", "cuentas_acdi", "cuentas_humanas")]
    if int(per) < 202000 and fila["cuentas_acdi"] is None:
        pass  # los reportes de 2019 no citan el dato ACDI; faltante legitimo
    print(f"{per}: " + ("completo" if not falto else f"falto {falto}"))

out = os.path.join(RAW, "agregados_cafci.csv")
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["periodo", "pat_humanas", "pat_juridicas",
                                      "cuentas_humanas", "cuentas_acdi", "acdi_ref"])
    w.writeheader()
    w.writerows(filas)
print(f"\n{len(filas)} PDFs -> {out}")
print("Revisar los 'falto': el formato de los reportes cambia entre anios y")
print("el regex puede requerir ajustes; eso es esperable y se corrige iterando.")
