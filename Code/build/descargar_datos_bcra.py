"""
Descarga los datasets de inclusion financiera del BCRA (txt/CSV)
con nombres descriptivos en Data/raw/bcra_inclusion/.
Fuente: https://www.bcra.gob.ar/indicadores-inclusion-financiera/
Uso:    python Code/build/descargar_datos_bcra.py   (requiere: pip install requests)
"""
import os
from pathlib import Path
import requests

BASE = "https://www.bcra.gob.ar/archivos/Pdfs/PublicacionesEstadisticas/inclusion-financiera/"

FILES = {
    "inclusion-financiera-deudores-sistema-financiero-ampliado-provincia.txt":
        "BCRA_deudores_SFA_total_por_provincia.txt",
    "inclusion-financiera-deudores-sistema-financiero-ampliado-grupo-institucional-provincia.txt":
        "BCRA_deudores_SFA_por_grupo_institucional_y_provincia.txt",
    "inclusion-financiera-deudores-sistema-financiero-ampliado-asistencia-provincia.txt":
        "BCRA_deudores_SFA_por_tipo_asistencia_y_provincia.txt",
    "inclusion-financiera-puntos-acceso-tipo-provincia.txt":
        "BCRA_puntos_acceso_por_tipo_y_provincia.txt",
    "inclusion-financiera-puntos-acceso-entidad-tipo-provincia.txt":
        "BCRA_puntos_acceso_por_entidad_tipo_y_provincia.txt",
    "inclusion-financiera-tenencia-cuentas-bancarias-pago-provincia.txt":
        "BCRA_tenencia_cuentas_bancarias_y_de_pago_por_provincia.txt",
}

HEADERS = {"User-Agent": "Mozilla/5.0 (research; Fintech_Dynamics repo)"}

outdir = Path(__file__).resolve().parents[2] / "Data" / "raw" / "bcra_inclusion"
outdir.mkdir(parents=True, exist_ok=True)
for src, dst in FILES.items():
    r = requests.get(BASE + src, headers=HEADERS, timeout=120)
    r.raise_for_status()
    with open(os.path.join(outdir, dst), "wb") as f:
        f.write(r.content)
    print(f"{dst}: {len(r.content):,} bytes")
print("Listo.")
