#!/usr/bin/env python3
"""Baja las comunicaciones y textos ordenados del BCRA que usa el paper.

Correr desde la raiz del repo o desde Regulation/. Guarda en subcarpetas
tematicas y escribe un manifiesto con tamano y hash para que el corpus sea
reproducible.

El BCRA usa dos patrones de URL para las comunicaciones y no es consistente
entre anios, asi que el script prueba los dos. Los textos ordenados cambian
sin aviso: el manifiesto fechado es la unica forma de saber que version se
uso al escribir.

    python descargar_normativa.py
"""

import csv
import hashlib
import os
import sys
import time
from datetime import date

import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36",
    "Accept": "application/pdf,*/*",
}

BASES = ["https://www.bcra.gob.ar/Pdfs/comytexord/",
         "https://www.bcra.gob.ar/archivos/Pdfs/comytexord/"]

# ---------------------------------------------------------------------------
# Bloque 1: fondos de clientes de PSP y efectivo minimo.
# Es la secuencia de la hipotesis regulatoria (ver README).
# ---------------------------------------------------------------------------
ENCAJES_PSP_FCI = {
    "A6859": "09/01/2020 - crea el regimen PSPCP; 100% de fondos de clientes en bancos",
    "A6885": "30/01/2020 - pto 3.1.2: ya contiene la clausula de fondos comunes de dinero",
    "A6992": "23/04/2020 - crea en efectivo minimo la categoria FCI money market al 0%",
    "A7429": "30/12/2021 - encaje 100% sobre cuentas de PSPOCP con fondos de clientes",
    "A7495": "27/04/2022 - texto ordenado PSP; renumera 3.1.2 a 4.1.2 (NO habilita nada nuevo)",
    "A7611": "22/09/2022 - permite integrar hasta 45 pp del 1.3.14 con Bonos del Tesoro",
    "A7825": "24/08/2023 - obliga a trasladar integramente al cliente la retribucion",
    "A7988": "11/04/2024 - encaje FCI money market 0% a 10%",
    "A8000": "02/05/2024 - 10% a 15%",
    "A8038": "06/06/2024 - PSP: adecuaciones, mantiene 4.1.2",
    "A8102": "10/09/2024 - regimen informativo PSPCP",
    "A8119": "17/10/2024 - 15% a 20%",
    "A8189": "30/01/2025 - extiende a plazos fijos precancelables (cierre de arbitraje)",
    "A8281": "17/07/2025 - 20% a 30%",
    "A8284": "2025 - regimen informativo PSP (codigos 20000dd por banco, 40000dd por fondo)",
    "A8286": "24/07/2025 - pases pasivos al encaje de cauciones (cierre de arbitraje)",
    "A8289": "31/07/2025 - 30% a 40%",
    "A8302": "14/08/2025 - integracion diaria, cargo 3xTAMAR, +5 pp transitorios",
    "A8305": "21/08/2025 - pases y cauciones por posicion neta",
    "A8306": "25/08/2025 - +3,5 pp a todas las obligaciones en pesos",
    "A8350": "30/10/2025 - vuelve a promedio mensual con minimo diario 95%",
    "A8355": "20/11/2025 - elimina los +3,5 pp",
    "A8432": "30/04/2026 - PSP as a service, constitucion regular en el pais",
    "A8454": "14/07/2026 - actualizacion t.o. PSP",
}

# ---------------------------------------------------------------------------
# Bloque 2: interoperabilidad. Es la otra hipotesis.
# ---------------------------------------------------------------------------
INTEROPERABILIDAD = {
    "A5982": "03/06/2016 - transferencias inmediatas, nuevos canales (PPM/PEI)",
    "A6043": "12/08/2016 - ordena transferencias inmediatas por canal PPM",
    "A6099": "14/11/2016 - crea el DEBIN",
    "A6212": "31/03/2017 - cronograma decreciente de tasas de intercambio de tarjetas",
    "A6510": "15/05/2018 - crea el CVU e impone interoperabilidad CVU-CBU",
    "A6698": "10/05/2019 - rediseno del DEBIN, DEBIN recurrente",
    "A7153": "30/10/2020 - crea Transferencias 3.0",
    "A7175": "05/12/2020 - emite los textos ordenados de T3.0",
    "A7361": "08/09/2021 - 15 segundos, 24x7, limites en UVA",
    "A7367": "17/09/2021 - prohibe conductas anticompetitivas de administradores de esquema",
    "A7400": "16/11/2021 - QR interoperable pleno; vigencia plena 29/11/2021",
    "A7409": "25/11/2021 - tolerancia transitoria de 25 segundos entre esquemas",
    "A7462": "24/02/2022 - crea el Registro de billeteras digitales interoperables",
    "A7463": "24/02/2022 - medidas antifraude",
    "A7485": "01/04/2022 - esquema de precios: arancel PCT 0,6-0,8%",
    "A7514": "19/05/2022 - transferencias pull; la billetera debita cuenta de otra entidad",
    "A7533": "29/06/2022 - CBU a toda cuenta a la vista, alias 24x7, QR estandar BCRA",
    "A7688": "02/02/2023 - credenciales de iniciacion de PCT",
    "A7712": "07/03/2023 - PSP: certificacion de integracion para prestar billetera",
    "A7769": "18/05/2023 - QR de tarjeta de credito interoperable",
    "A7811": "20/07/2023 - actualiza umbrales en UVA",
    "A7841": "14/09/2023 - discontinua el DEBIN recurrente como herramienta de fondeo",
    "A7905": "30/11/2023 - PRIMERA PRORROGA de QR-credito y DEBIN recurrente",
    "A7919": "13/12/2023 - actualiza t.o. SNP servicios de pago",
    "A7936": "29/12/2023 - actualiza t.o. transferencias y complementarias",
    "A7942": "11/01/2024 - SEGUNDA PRORROGA: ambas al 30/04/2024",
    "A7996": "30/04/2024 - pull mismo titular, consentimiento OAuth2",
    "A8030": "30/05/2024 - elimina el arancel del pull",
    "A8032": "30/05/2024 - reciprocidad: la billetera debe leer QR de todo adquirente",
    "A8091": "16/08/2024 - los precios de transferencias no pueden ser % del monto",
    "A8103": "12/09/2024 - control CUIT-CBU/CVU-alias, nuevo formato de alias",
    "A8114": "08/10/2024 - consolida reciprocidad y tope 0,07%",
    "A8162": "19/12/2024 - acreditacion en 2 dias; elimina arancel uniforme por rubro",
    "A8176": "14/01/2025 - inscripcion en registros via ARCA",
    "A8180": "16/01/2025 - debito y DEBIN programado",
    "A8206": "27/02/2025 - Viaje con QR (VQR), integracion obligatoria mutua",
    "A8287": "25/07/2025 - nuevas funciones registrables: Administrador QR, Iniciacion",
    "A8303": "19/08/2025 - t.o. SNP servicios de pago",
    "A8399": "12/02/2026 - t.o. transferencias complementarias",
    "A8406": "02/03/2026 - cobro con transferencia, reemplaza debito recurrente",
    "A8436": "14/05/2026 - actualizacion t.o. transferencias complementarias",
}

TEXTOS_ORDENADOS = {
    "t-efemin.pdf": ("https://www.bcra.gob.ar/archivos/Pdfs/texord/t-efemin.pdf",
                     "Efectivo minimo. Ptos 1.3.12 (FCI MM) y 1.3.14 (PSPOCP)"),
    "t-snp-psp.pdf": ("https://www.bcra.gob.ar/archivos/Pdfs/Texord/t-snp-psp.pdf",
                      "Proveedores de servicios de pago. Pto 4.1 custodia de fondos"),
    "t-snp-tr.pdf": ("https://www.bcra.gob.ar/archivos/Pdfs/texord/t-snp-tr.pdf",
                     "SNP transferencias"),
    "t-snp-tr-nc.pdf": ("https://www.bcra.gob.ar/archivos/Pdfs/Texord/t-snp-tr-nc.pdf",
                        "SNP transferencias, normas complementarias: IEP, QR, aranceles"),
    "t-snp-spd.pdf": ("https://www.bcra.gob.ar/archivos/Pdfs/Texord/t-snp-spd.pdf",
                      "SNP servicios de pago: registro de billeteras, QR de tarjetas"),
    "t-RI-PSP.pdf": ("https://www.bcra.gob.ar/archivos/Pdfs/Texord/t-RI-PSP.pdf",
                     "Regimen informativo PSP. Codigos 20000dd por banco y 40000dd por fondo"),
    "t-ri-rml.pdf": ("https://www.bcra.gob.ar/archivos/Pdfs/texord/t-ri-rml.pdf",
                     "Manual RI. Partidas 102190 (FCI MM) y 102200 (PSPOCP)"),
    "plandecuentas.pdf": ("https://bcra.gob.ar/Pdfs/Texord/plandecuentas.pdf",
                          "Plan de cuentas: codigos del balance de saldos"),
}

PUBLICACIONES = {
    "IEF_2026-01.pdf": (
        "https://www.bcra.gob.ar/archivos/Pdfs/PublicacionesEstadisticas/ief0225.pdf",
        "Informe de Estabilidad Financiera. Apartado 1 (pag 48): FCI money market "
        "y sus depositos en entidades financieras. LEER: es el documento clave"),
    "IIF_2025-04.pdf": (
        "https://www.bcra.gob.ar/archivos/Pdfs/PublicacionesEstadisticas/"
        "Informe-inclusion-financiera-abril-25.pdf",
        "Inclusion financiera. Cuentas de pago con saldo en FCD: 13,8M dic-2023 "
        "a 22,4M dic-2024; 53,7% de PH con cuenta de pago"),
    "IIF_2026-04.pdf": (
        "https://www.bcra.gob.ar/archivos/Pdfs/publicacionesestadisticas/informes/"
        "informe-inclusion-financiera-2026-04.pdf",
        "Inclusion financiera 2S-2025. 26,5M de cuentas de pago con saldo en FCD"),
    "IMM_2025-07.pdf": (
        "https://www.bcra.gob.ar/archivos/Pdfs/PublicacionesEstadisticas/"
        "informe-monetario-mensual-jul-25.pdf",
        "Informe monetario. Justificacion de los encajes de agosto 2025"),
    "Pagos_Minoristas_2025.pdf": (
        "https://www.bcra.gob.ar/archivos/Pdfs/PublicacionesEstadisticas/informes/"
        "informe_anual_pagos_minoristas_2025.pdf",
        "Informe anual de pagos minoristas 2025"),
    "Pagos_Minoristas_2025_series.xlsx": (
        "https://www.bcra.gob.ar/archivos/Pdfs/PublicacionesEstadisticas/informes/"
        "series_informe_anual_pagos_minoristas_2025.xlsx",
        "Series del informe anual de pagos minoristas"),
}


def bajar(url, destino, intentos=3):
    for i in range(intentos):
        try:
            r = requests.get(url, headers=HEADERS, timeout=60, allow_redirects=True)
            if r.status_code == 200 and len(r.content) > 1000:
                with open(destino, "wb") as f:
                    f.write(r.content)
                return len(r.content), hashlib.sha256(r.content).hexdigest()[:16]
            return None
        except Exception:
            if i == intentos - 1:
                return None
            time.sleep(2 * (i + 1))


def bajar_comunicacion(cod, carpeta):
    for base in BASES:
        for variante in (cod, cod.lower()):
            res = bajar(base + variante + ".pdf",
                        os.path.join(carpeta, cod + ".pdf"))
            if res:
                return res
    return None


def main():
    aqui = os.path.dirname(os.path.abspath(__file__))
    manifiesto, fallos = [], []

    grupos = [
        ("encajes_psp_fci", ENCAJES_PSP_FCI, "com"),
        ("interoperabilidad", INTEROPERABILIDAD, "com"),
        ("textos_ordenados", TEXTOS_ORDENADOS, "url"),
        ("publicaciones_bcra", PUBLICACIONES, "url"),
    ]

    for nombre, items, modo in grupos:
        carpeta = os.path.join(aqui, nombre)
        os.makedirs(carpeta, exist_ok=True)
        print(f"\n=== {nombre} ({len(items)}) ===")
        for clave, val in items.items():
            if modo == "com":
                desc, res = val, bajar_comunicacion(clave, carpeta)
                archivo = clave + ".pdf"
            else:
                url, desc = val
                archivo = clave
                res = bajar(url, os.path.join(carpeta, archivo))
            if res:
                size, h = res
                print(f"  ok  {archivo:34s} {size/1024:7.0f} KB")
                manifiesto.append({"grupo": nombre, "archivo": archivo,
                                   "descripcion": desc, "bytes": size,
                                   "sha256_16": h, "bajado": date.today().isoformat()})
            else:
                print(f"  FALLA {archivo}", file=sys.stderr)
                fallos.append(archivo)

    with open(os.path.join(aqui, "manifiesto.csv"), "w", newline="",
              encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["grupo", "archivo", "descripcion",
                                          "bytes", "sha256_16", "bajado"])
        w.writeheader()
        w.writerows(manifiesto)

    print(f"\n{len(manifiesto)} archivos bajados, {len(fallos)} fallas")
    if fallos:
        print("Fallaron:", ", ".join(fallos))
        print("Los textos ordenados cambian de URL cuando el BCRA reorganiza el")
        print("sitio. Si falla uno, buscalo en bcra.gob.ar y actualiza el dict.")


if __name__ == "__main__":
    main()
