"""
Descarga las fuentes CAFCI que no dependen de la API de series:
  1. Snapshot del registro maestro de fondos y clases (JSON), con fecha en el
     nombre, a raw/cafci/maestro_AAAAMMDD.json
  2. Resumenes mensuales de la industria (PDF), 2019-01 a 2026-07, a
     raw/cafci/resumenes/
Cada descarga queda registrada en raw/cafci/manifest.csv con url, fecha de
descarga y hash sha256 del archivo tal como llego (crudos inmutables).
Fuentes y como se llega a cada una: ver Methodological_Notes/archivo/fuentes_fci_cafci_2026-08.md (API de CAFCI, fuera de servicio desde ago-2026)
Uso:      python descargar_cafci.py
Requiere: pip install requests
"""
import csv
import datetime
import hashlib
import os
import pathlib
import requests

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = pathlib.Path(__file__).resolve().parents[2]
RAW = str(ROOT / "Data" / "raw" / "cafci")
HEADERS = {"User-Agent": "Mozilla/5.0 (research; Fintech-Dynamics repo)"}
MANIFEST = os.path.join(RAW, "manifest.csv")

def registrar(path, url):
    h = hashlib.sha256(open(path, "rb").read()).hexdigest()
    nuevo = not os.path.exists(MANIFEST)
    with open(MANIFEST, "a", newline="") as f:
        w = csv.writer(f)
        if nuevo:
            w.writerow(["archivo", "url", "descargado", "sha256"])
        w.writerow([os.path.relpath(path, RAW), url,
                    datetime.date.today().isoformat(), h])

def bajar(url, path, minimo=1000):
    if os.path.exists(path):
        return "ya estaba"
    r = requests.get(url, headers=HEADERS, timeout=180)
    if r.status_code != 200 or len(r.content) < minimo:
        return f"no disponible ({r.status_code})"
    with open(path, "wb") as f:
        f.write(r.content)
    registrar(path, url)
    return f"OK ({len(r.content)/1e6:.1f} MB)"

os.makedirs(os.path.join(RAW, "resumenes"), exist_ok=True)

# 1. registro maestro (fondos, clases, gerentes, depositarias, estado)
hoy = datetime.date.today().strftime("%Y%m%d")
url = "https://estadisticas.cafci.org.ar/consulta-de-fondos.json"
print("maestro:", bajar(url, os.path.join(RAW, f"maestro_{hoy}.json")))

# 2. resumenes mensuales de la industria
base = "https://www.cafci.org.ar/Publica/Estadistica/Resumenes/Mensual/"
for anio in range(2019, 2027):
    for mes in range(1, 13):
        if (anio, mes) > (2026, 7):
            break
        nombre = f"{anio}{mes:02d}01_Resumen_Industria.pdf"
        r = bajar(base + nombre, os.path.join(RAW, "resumenes", nombre))
        print(f"{anio}-{mes:02d}: {r}")

print("listo; crudos y manifest en data/raw/cafci/")
