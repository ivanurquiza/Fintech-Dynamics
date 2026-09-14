#!/usr/bin/env python3
"""Registro de Proveedores de Servicios de Pago del BCRA.

La pagina publica (bcra.gob.ar/SistemasFinancierosYdePagos/registro-de-
proveedores-de-servicios-de-pago-resultados-por-tipo/?tipoPSP=N) no ofrece
descarga: arma la tabla en el navegador llamando a un endpoint interno.
Ese endpoint es publico y devuelve JSON. Los nueve tipos de PSP se piden
por separado; una misma firma puede estar inscripta en varios.

Salida: data/raw/psp/registro_psp.csv  (una fila por firma-tipo)
        data/raw/psp/registro_psp_<AAAAMMDD>.json  (crudo, para versionar)

El registro NO tiene historia: es una foto del dia. Correrlo periodicamente
y guardar el json fechado es la unica forma de reconstruir altas y bajas.
"""

import csv
import json
import os
import sys
import time
from datetime import date

import requests

ENDPOINT = "https://www.bcra.gob.ar/api/endpoints/proveedores-psp.php"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.bcra.gob.ar/SistemasFinancierosYdePagos/"
               "registro-de-proveedores-de-servicios-de-pago-resultados-por-tipo/",
}

# los nueve tipos del registro; el 1 (PSPCP) es el unico que custodia
# fondos de clientes y por lo tanto el unico relevante para el paper
TIPOS = range(1, 10)

CAMPOS = ["tipo_psp", "tipo_psp_nombre", "codigo", "cuit", "denominacion_pj",
          "denominacion", "domicilio", "localidad", "provincia", "codigo_postal",
          "telefono", "habilitadoOperaComoServicio", "id_proveedor"]


def bajar(tipo, intentos=4):
    for i in range(intentos):
        try:
            r = requests.get(ENDPOINT, params={"tipoPSP": tipo},
                             headers=HEADERS, timeout=30)
            r.raise_for_status()
            j = r.json()
            if not j.get("success"):
                raise RuntimeError(f"respuesta sin success: {j}")
            return j
        except Exception as e:
            if i == intentos - 1:
                raise
            print(f"  reintento {i+1} tipo {tipo}: {e}", file=sys.stderr)
            time.sleep(2 * (i + 1))


def main():
    aqui = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    destino = os.path.join(aqui, "raw", "psp")
    os.makedirs(destino, exist_ok=True)

    crudo, filas = {}, []
    for t in TIPOS:
        j = bajar(t)
        crudo[str(t)] = j
        nombre = j.get("tipo_psp_nombre", "")
        print(f"tipo {t}: {j.get('total')} firmas - {nombre}")
        for p in j.get("proveedores", []):
            fila = {c: p.get(c, "") for c in CAMPOS}
            fila["tipo_psp"] = t
            fila["tipo_psp_nombre"] = nombre
            # el domicilio viene con <br>
            fila["domicilio"] = str(fila["domicilio"]).replace("<br>", " ")
            filas.append(fila)

    hoy = date.today().strftime("%Y%m%d")
    with open(os.path.join(destino, f"registro_psp_{hoy}.json"), "w",
              encoding="utf-8") as f:
        json.dump(crudo, f, ensure_ascii=False, indent=1)

    salida = os.path.join(destino, "registro_psp.csv")
    with open(salida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(filas)

    pspcp = sum(1 for x in filas if x["tipo_psp"] == 1)
    print(f"\n{len(filas)} filas firma-tipo, {pspcp} PSPCP -> {salida}")


if __name__ == "__main__":
    main()
