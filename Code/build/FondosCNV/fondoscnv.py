"""
fondoscnv.py

Funciones para bajar y ordenar dos fuentes públicas de la CNV sobre fondos
comunes de inversión:

  1. Planillas diarias de valores de cuotaparte (provistas por CAFCI).
     Una fila por clase de fondo y por día, desde ene-2020.
     Índice: https://www.cnv.gov.ar/SitioWeb/FondosComunesInversion/CuotaPartes

  2. Composición de cartera de cada fondo, semanal.
     Ficha: https://www.cnv.gov.ar/SitioWeb/FondosComunesInversion/DetallesFCI/{id}
     con los parámetros compo=true y fecha=AAAA-MM-DD.

Lo usan los notebooks 01, 02 y 03 de esta carpeta. Las descargas son
idempotentes: si un archivo ya está en disco no se vuelve a pedir, así que
se puede cortar y retomar sin perder nada.

Diccionario de variables y fuentes: claude/diccionario_fci.md y
claude/fuentes_fci.md en el proyecto.
"""

from __future__ import annotations

import gzip
import hashlib
import html as htmllib
import re
import time
import unicodedata
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------

def raiz_repo(inicio: Path | None = None) -> Path:
    """Sube desde la carpeta actual hasta encontrar Code/ y Data/."""
    p = (inicio or Path.cwd()).resolve()
    for q in [p, *p.parents]:
        if (q / "Code").is_dir() and (q / "Data").is_dir():
            return q
    raise FileNotFoundError("No encontré la raíz del repo (carpetas Code/ y Data/).")


def rutas(root: Path | None = None) -> dict:
    root = root or raiz_repo()
    r = {
        "root": root,
        "raw": root / "Data" / "raw" / "FondosCNV",
        "proc": root / "Data" / "processed" / "FondosCNV",
        "xwalk": root / "Data" / "crosswalks",
    }
    r["raw_planillas"] = r["raw"] / "planillas"
    r["raw_carteras"] = r["raw"] / "carteras"
    for k in ["raw", "proc", "xwalk", "raw_planillas", "raw_carteras"]:
        r[k].mkdir(parents=True, exist_ok=True)
    return r


# ---------------------------------------------------------------------------
# Sesión HTTP
# ---------------------------------------------------------------------------

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

BASE_CNV = "https://www.cnv.gov.ar/SitioWeb/FondosComunesInversion"
BASE_AIF = "https://aif2.cnv.gov.ar"
BASE_BLOB = "https://blob.cnv.gov.ar/BlobWebService.svc/DownloadBlob"


def sesion() -> requests.Session:
    """Sesión con reintentos. El servicio de archivos de la CNV da 503 a
    rachas, así que conviene reintentar con espera creciente."""
    s = requests.Session()
    s.headers.update({"User-Agent": UA})
    retry = Retry(total=6, backoff_factor=2.0,
                  status_forcelist=[429, 500, 502, 503, 504],
                  allowed_methods=["GET", "POST"])
    s.mount("https://", HTTPAdapter(max_retries=retry))
    return s


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def ahora() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def agregar_manifest(ruta: Path, fila: dict) -> None:
    """Agrega una fila al manifest (csv). Queda un registro de cada intento."""
    df = pd.DataFrame([fila])
    df.to_csv(ruta, mode="a", header=not ruta.exists(), index=False)


# ---------------------------------------------------------------------------
# Fechas en castellano
# ---------------------------------------------------------------------------

MESES = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6,
         "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12}


def fecha_es(txt: str):
    """'18 sep. 2026' o '18 sep. 2026 20:19' -> Timestamp."""
    if txt is None:
        return pd.NaT
    m = re.search(r"(\d{1,2})\s+([a-zA-Z]{3})\.?\s+(\d{4})(?:\s+(\d{1,2}):(\d{2}))?", str(txt))
    if not m:
        return pd.NaT
    d, mes, a, hh, mm = m.groups()
    mes = MESES.get(mes.lower())
    if mes is None:
        return pd.NaT
    return pd.Timestamp(int(a), mes, int(d), int(hh or 0), int(mm or 0))


# Secciones de la planilla que corresponden a money market en pesos. Hasta el
# 6-sep-2021 CAFCI los clasificaba como "Plazo Fijo Peso Argentina"; desde el
# 13-sep-2021 la misma sección se llama "Mercado de Dinero Peso Argentina"
# (mismos 42 fondos, mismo patrimonio). Un fondo puede entrar a la sección
# después de haber sido de otro tipo (Mercado Fondo era Renta Fija en 2020).
SECCIONES_MM = ["Plazo Fijo Peso Argentina", "Mercado de Dinero Peso Argentina"]


# ===========================================================================
# 1. PLANILLAS DIARIAS
# ===========================================================================

def indice_planillas(s: requests.Session) -> pd.DataFrame:
    """Lee la página índice de la CNV. Devuelve una fila por presentación.

    La fecha del documento (primera columna) no siempre coincide con la fecha
    de los datos: la fecha efectiva sale de la descripción ('... al 23 sep. 2026').
    """
    r = s.get(f"{BASE_CNV}/CuotaPartes", timeout=60)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    filas = []
    for tr in soup.find_all("tr"):
        td = tr.find_all("td")
        if len(td) != 4:
            continue
        a = td[0].find("a", href=True)
        if a is None:
            continue
        url = a["href"]
        m = re.search(r"publicview/([0-9A-Fa-f-]{36})", url)
        desc = td[2].get_text(" ", strip=True)
        filas.append({
            "fecha_documento": fecha_es(td[0].get_text(" ", strip=True)),
            "fecha_recepcion": fecha_es(td[1].get_text(" ", strip=True)),
            "descripcion": desc,
            "id_presentacion": td[3].get_text(" ", strip=True),
            "uuid_presentacion": m.group(1) if m else None,
            "url_presentacion": url,
            "fecha_info": fecha_es(desc.split(" al ")[-1]) if " al " in desc else pd.NaT,
        })
    df = pd.DataFrame(filas)
    df["fecha_info"] = pd.to_datetime(df["fecha_info"]).dt.normalize()
    return df


def ultima_version(idx: pd.DataFrame) -> pd.DataFrame:
    """Casi todos los días hay dos presentaciones: la de la noche y una
    corregida al día siguiente. Nos quedamos con la de recepción más tardía."""
    idx = idx.dropna(subset=["fecha_info", "uuid_presentacion"]).copy()
    idx["n_versiones"] = idx.groupby("fecha_info")["uuid_presentacion"].transform("count")
    idx = idx.sort_values(["fecha_info", "fecha_recepcion"])
    return idx.groupby("fecha_info", as_index=False).tail(1).reset_index(drop=True)


def adjunto_de_presentacion(s: requests.Session, uuid_presentacion: str) -> dict:
    """Busca en la página pública de la presentación el id del archivo
    adjunto (guid del blob) y su nombre. El dato viene en un input oculto
    con un json escapado: nombreArchivo, guid, hash."""
    url = f"{BASE_AIF}/Presentations/publicview/{uuid_presentacion}"
    r = s.get(url, timeout=60)
    r.raise_for_status()
    h = htmllib.unescape(r.text)
    nombres = re.findall(r'"nombreArchivo"\s*:\s*"([^"]+)"', h)
    guids = re.findall(r'"guid"\s*:\s*"([0-9A-Fa-f-]{36})"', h)
    if not guids:
        # respaldo: el primer uuid de la página que no sea el de la presentación
        todos = re.findall(r"[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}", h)
        guids = [g for g in dict.fromkeys(todos) if g.lower() != uuid_presentacion.lower()][:1]
    return {"file_guid": guids[0] if guids else None,
            "nombre_archivo": nombres[0] if nombres else None,
            "n_adjuntos": len(guids), "url_presentacion": url}


def bajar_blob(s: requests.Session, file_guid: str, referer: str) -> bytes:
    """Dos pasos, como hace el botón de la página:
    (1) pedir una clave temporal (valet key) para ese archivo;
    (2) mandarla por POST, como formulario, al servicio de archivos."""
    r1 = s.get(f"{BASE_AIF}/api/ValetKeyProvider/GetPublicValetKey/{file_guid}",
               params={"operation": "DownloadBlob"}, timeout=60)
    r1.raise_for_status()
    clave = r1.json()["valetKeyData"]
    r2 = s.post(f"{BASE_BLOB}/{file_guid}", data={"ValetKey": clave},
                headers={"Referer": referer, "Origin": BASE_AIF}, timeout=120)
    r2.raise_for_status()
    return r2.content


def descargar_planillas(sel: pd.DataFrame, destino: Path, manifest: Path,
                        pausa: float = 0.5, max_n: int | None = None,
                        s: requests.Session | None = None) -> pd.DataFrame:
    """Baja las planillas de `sel` (salida de ultima_version). Guarda cada una
    como AAAAMMDD_<id_presentacion>.xlsx y anota todo en el manifest."""
    s = s or sesion()
    hechos = 0
    log = []
    for _, f in sel.iterrows():
        if max_n is not None and hechos >= max_n:
            break
        nombre = f"{f.fecha_info:%Y%m%d}_{f.id_presentacion}.xlsx"
        ruta = destino / nombre
        if ruta.exists():
            continue
        fila = {"fecha_info": f.fecha_info.date(), "id_presentacion": f.id_presentacion,
                "uuid_presentacion": f.uuid_presentacion, "fecha_recepcion": f.fecha_recepcion,
                "archivo_local": nombre, "descargado": ahora()}
        try:
            adj = adjunto_de_presentacion(s, f.uuid_presentacion)
            fila.update(adj)
            if adj["file_guid"] is None:
                raise ValueError("sin adjunto en la presentación")
            b = bajar_blob(s, adj["file_guid"], adj["url_presentacion"])
            if b[:2] != b"PK":
                raise ValueError(f"respuesta no es xlsx ({len(b)} bytes)")
            ruta.write_bytes(b)
            fila.update({"estado": "ok", "bytes": len(b), "sha256": sha256(b)})
            hechos += 1
        except Exception as e:  # se anota y se sigue; se reintenta en la próxima corrida
            fila.update({"estado": "error", "error": f"{type(e).__name__}: {e}"})
        agregar_manifest(manifest, fila)
        log.append(fila)
        time.sleep(pausa)
    return pd.DataFrame(log)


# --- lectura de una planilla ----------------------------------------------

# Nombres de columna por encabezado. Las columnas de la planilla tienen dos
# filas de encabezado; en la segunda aparecen fechas que cambian cada día
# (día anterior, fin de mes, fin de año, hace 12 meses), así que no se puede
# leer por nombre literal. Se mapea por grupo y posición.
COLS_SIMPLES = {
    "Fondo": "fondo_clase", "Fecha": "fecha", "Market Share": "market_share",
    "Sociedad Depositaria": "depositaria", "Codigo CNV": "cod_cnv",
    "Calificación": "calificacion", "Código CAFCI": "cod_cafci",
    "Código de Soc.Gte.": "cod_gerente", "Código de Soc.Dep.": "cod_depositaria",
    "Sociedad Gerente": "gerente", "Código de Clasificación": "cod_clasificacion",
    "Código de Moneda": "cod_moneda", "Código de Región": "cod_region",
    "Código de Horizonte": "cod_horizonte", "Indice de MM": "indice_mm",
    "Comision Ingreso": "com_ingreso", "Honorarios Adm. SG": "hon_sg",
    "Honorarios Adm. SD": "hon_sd", "Gastos Ord Gestion": "gastos",
    "Comision Rescate": "com_rescate", "Comision Transferencia": "com_transferencia",
    "Honorarios Éxito": "hon_exito", "Moneda Fondo": "moneda_fondo",
    "Plazo Liq.": "plazo_liq", "Decreto 596": "decreto_596",
    "Id Fondo CAFCI padre": "id_cafci_padre", "Id Fondo CNV padre": "id_cnv_padre",
    "Tipo de escisión": "tipo_escision", "Repatriacion": "repatriacion",
    "Mínimo de Inversión": "minimo_inversion",
    "Regularización Ley 27.743": "ley_27743", "Tipo de Dinero": "tipo_dinero",
    "Calificado": "calificado",
}

NUMERICAS = ["vcp", "vcp_ant", "var_diaria", "vcp_reexp_pesos", "var_desde_fin_mes",
             "var_desde_fin_anio", "var_12m", "ccp", "ccp_ant", "pn", "pn_ant",
             "market_share", "cod_cnv", "cod_cafci", "cod_gerente", "cod_depositaria",
             "cod_clasificacion", "cod_moneda", "cod_region", "cod_horizonte",
             "com_ingreso", "hon_sg", "hon_sd", "gastos", "com_rescate",
             "com_transferencia", "plazo_liq", "minimo_inversion"]


def _mapear_encabezado(h1: list, h2: list) -> tuple[list, dict]:
    nombres, extra = [], {}
    grupo = None
    k_var = 0
    def _limpio(v):
        if v is None or (isinstance(v, float) and np.isnan(v)):
            return None
        v = str(v).strip()
        return None if v == "" or v.lower() == "nan" else v

    for a, b in zip(h1, h2):
        a, b = _limpio(a), _limpio(b)
        if a is not None:
            grupo = a
            k_var = 0
        elif b is None:
            grupo = None
        g = a if a is not None else grupo
        nom = None
        if g is None:
            nom = None
        elif g == "Clasificación":
            nom = {"Moneda": "moneda", "Región": "region", "Horizonte": "horizonte"}.get(b)
        elif g.startswith("Valor"):
            if b == "Actual":
                nom = "vcp"
            elif b and b.startswith("Variac"):
                nom = "var_diaria"
            elif b and b.startswith("Reexp"):
                nom = "vcp_reexp_pesos"
            else:
                nom = "vcp_ant"
                extra["fecha_ant"] = b
        elif g.startswith("Variacion cuotaparte"):
            nom = ["var_desde_fin_mes", "var_desde_fin_anio", "var_12m"][min(k_var, 2)]
            k_var += 1
        elif g.startswith("Cantidad de cuotapartes"):
            nom = "ccp" if b == "Actual" else "ccp_ant"
        elif g == "Patrimonio":
            nom = "pn" if b == "Actual" else "pn_ant"
        else:
            nom = COLS_SIMPLES.get(g, re.sub(r"\W+", "_", g.lower()).strip("_"))
        nombres.append(nom)
    return nombres, extra


def _leer_planilla_agen10(crudo: pd.DataFrame, ruta: Path) -> pd.DataFrame:
    """Formato alternativo que aparece en pocos días (hoja 'agen_10', p. ej.
    20241017 y 20250306). La clasificación viene en jerarquía en las columnas
    0 a 6 (tipo de fondo, tipo de renta o tipo de money market, región, ...,
    moneda) y hay una columna extra 'Clase de Cuota' (Minorista / Mayorista /
    General) que las planillas estándar no tienen."""
    col0 = crudo.iloc[:, 0].astype(str).str.strip()
    fila_h = crudo.index[col0.eq("CLASIFICACIÓN")][0]
    h1 = crudo.iloc[fila_h].tolist()
    h2 = crudo.iloc[fila_h + 1].tolist()
    h1 = ["Fondo" if str(a).strip() == "Fondos" else a for a in h1]
    h1 = ["Valor (mil cuotapartes)" if str(a).startswith("Valor (mil") else a for a in h1]
    ren = {"Clase de Cuota": "tipo_clase_cuota", "Calificacion": "Calificación",
           "Código Clase CAFCI": "Código CAFCI", "Otros Gastos": "Gastos Ord Gestion",
           "Comisión Ingreso": "Comision Ingreso", "Comisión Rescate": "Comision Rescate",
           "Comisión Transferencia": "Comision Transferencia", "Plazo Liq (Dias)": "Plazo Liq.",
           "Código CNV": "Codigo CNV"}
    h1 = [ren.get(str(a).strip(), a) if isinstance(a, str) else a for a in h1]
    h1[:7] = [None] * 7
    h2[:7] = [None] * 7
    # en este formato las variaciones (fin de mes, año, 12 meses) cuelgan del
    # grupo del VCP; se las separa para que el mapeo sea el mismo
    j = next(i for i, b in enumerate(h2) if str(b).startswith("Reexp"))
    h1[j + 1] = "Variacion cuotaparte %"
    nombres, extra = _mapear_encabezado(h1, h2)
    nombres = ["tipo_clase_cuota" if n == "tipo_clase_cuota" else n for n in nombres]
    datos = crudo.iloc[fila_h + 2:].reset_index(drop=True)
    renta, moneda, tipo_mm, regs = None, None, None, []
    for _, f in datos.iterrows():
        nom = f.iloc[7]
        if pd.isna(nom) or str(nom).strip() == "":
            v1, v6 = f.iloc[1], f.iloc[6]
            if pd.notna(v1):
                v1 = str(v1).strip()
                if v1 in ("Clásico", "Dinámico"):
                    tipo_mm = v1
                else:
                    renta, tipo_mm = v1, None
            if pd.notna(v6):
                moneda = str(v6).strip()
            continue
        rec = {n: f.iloc[j] for j, n in enumerate(nombres) if n is not None}
        rec["seccion"] = f"{renta} {moneda}" if renta and moneda else renta
        rec["subseccion"] = None
        if tipo_mm:
            rec["tipo_dinero"] = tipo_mm
        regs.append(rec)
    return pd.DataFrame(regs), extra


def leer_planilla(ruta: Path) -> pd.DataFrame:
    """Lee una planilla diaria y la devuelve en formato largo: una fila por
    clase, con la sección (tipo de fondo) y la subsección cuando existe
    (por ejemplo, fondos en liquidación)."""
    crudo = pd.read_excel(ruta, sheet_name=0, header=None, dtype=object)
    es_fondo = crudo.iloc[:, 0].astype(str).str.strip().eq("Fondo")
    if not es_fondo.any():
        df, extra = _leer_planilla_agen10(crudo, ruta)
        return _terminar_planilla(df, extra, ruta)
    fila_h = crudo.index[es_fondo][0]
    h1 = crudo.iloc[fila_h].tolist()
    h2 = crudo.iloc[fila_h + 1].tolist()
    nombres, extra = _mapear_encabezado(h1, h2)
    datos = crudo.iloc[fila_h + 2:].reset_index(drop=True)

    seccion, subseccion, registros = None, None, []
    j_fecha = nombres.index("fecha") if "fecha" in nombres else 4
    for _, fila in datos.iterrows():
        v0 = fila.iloc[0]
        if v0 is None or (isinstance(v0, float) and np.isnan(v0)) or str(v0).strip() == "":
            continue
        resto = fila.iloc[1:j_fecha + 1]
        if resto.isna().all():
            # fila de título: sección o subsección (las subsecciones vienen con sangría)
            txt = str(v0)
            if txt.startswith(" "):
                subseccion = txt.strip()
            else:
                seccion, subseccion = txt.strip(), None
            continue
        rec = {n: fila.iloc[j] for j, n in enumerate(nombres) if n is not None}
        rec["seccion"] = seccion
        rec["subseccion"] = subseccion
        registros.append(rec)

    df = pd.DataFrame(registros)
    return _terminar_planilla(df, extra, ruta)


def _terminar_planilla(df: pd.DataFrame, extra: dict, ruta: Path) -> pd.DataFrame:
    for c in NUMERICAS:
        if c in df:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df["fecha"] = pd.to_datetime(df["fecha"], format="%d/%m/%y", errors="coerce")
    df["fecha_ant"] = pd.to_datetime(extra.get("fecha_ant"), format="%d/%m/%y", errors="coerce")
    df["archivo"] = Path(ruta).name
    # La columna 'Fecha' es la del último valor informado por cada clase. Un
    # fondo que no reportó ese día aparece con una fecha vieja: se marca.
    m = re.match(r"(\d{8})", Path(ruta).name)
    df["fecha_planilla"] = pd.to_datetime(m.group(1), format="%Y%m%d") if m else df["fecha"].max()
    df["desactualizado"] = (df["fecha"] < df["fecha_planilla"]).astype(int)
    # nombre del fondo sin la clase, y la clase
    df["fondo"] = df["fondo_clase"].astype(str).str.replace(r"\s*-\s*Clase\b.*$", "", regex=True).str.strip()
    df["clase"] = df["fondo_clase"].astype(str).str.extract(r"Clase\s+(.+)$", expand=False).str.strip()
    return df


def apilar_planillas(carpeta: Path, salida: Path, solo_seccion: str | None = None) -> pd.DataFrame:
    """Lee todas las planillas bajadas y las guarda en un parquet.
    Si `solo_seccion` está dado, filtra (por ej. 'Mercado de Dinero Peso Argentina')."""
    partes, errores = [], []
    for p in sorted(carpeta.glob("*.xlsx")):
        try:
            d = leer_planilla(p)
            if solo_seccion:
                d = d[d["seccion"] == solo_seccion]
            partes.append(d)
        except Exception as e:
            errores.append({"archivo": p.name, "error": f"{type(e).__name__}: {e}"})
    df = pd.concat(partes, ignore_index=True) if partes else pd.DataFrame()
    for c in df.columns:  # columnas de texto mixtas: a string para que parquet no se queje
        if df[c].dtype == object and c not in ("fecha", "fecha_ant"):
            df[c] = df[c].astype("string")
    df.to_parquet(salida, index=False)
    if errores:
        pd.DataFrame(errores).to_csv(salida.with_suffix(".errores.csv"), index=False)
    return df


# ===========================================================================
# 2. CARTERAS (composición semanal por fondo)
# ===========================================================================

def lista_fondos_cnv(s: requests.Session) -> pd.DataFrame:
    """Lista de fondos del buscador de la CNV: id interno (Lfc) y nombre.
    Ojo: puede no incluir fondos ya liquidados."""
    r = s.get(BASE_CNV, timeout=60)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    sel = soup.find("select", {"id": "Lfc"}) or soup.find("select", {"name": "Lfc"})
    filas = [{"lfc": o.get("value").strip(), "nombre_cnv": o.get_text(" ", strip=True)}
             for o in sel.find_all("option") if o.get("value", "").strip()]
    return pd.DataFrame(filas)


def url_cartera(lfc: str | int, fecha: str) -> str:
    return (f"{BASE_CNV}/DetallesFCI/{lfc}?denominacion=x&estado=Aprobado%20Lanzado"
            f"&idEstado=5&compo=true&fecha={fecha}")


def viernes(desde: str, hasta: str | None = None) -> list[str]:
    hasta = hasta or pd.Timestamp.today().strftime("%Y-%m-%d")
    return [d.strftime("%Y-%m-%d") for d in pd.date_range(desde, hasta, freq="W-FRI")]


def descargar_carteras(lfcs: list, fechas: list, destino: Path, manifest: Path,
                       pausa: float = 0.4, s: requests.Session | None = None,
                       max_n: int | None = None) -> int:
    """Para cada fondo y cada fecha pide la ficha con la cartera vigente a esa
    fecha y guarda el HTML comprimido en destino/<lfc>/<fecha>.html.gz."""
    s = s or sesion()
    n = 0
    for lfc in lfcs:
        (destino / str(lfc)).mkdir(parents=True, exist_ok=True)
        for f in fechas:
            if max_n is not None and n >= max_n:
                return n
            ruta = destino / str(lfc) / f"{f}.html.gz"
            if ruta.exists():
                continue
            fila = {"lfc": lfc, "fecha_pedida": f, "descargado": ahora()}
            try:
                r = s.get(url_cartera(lfc, f), timeout=60)
                r.raise_for_status()
                b = r.content
                ruta.write_bytes(gzip.compress(b))
                fila.update({"estado": "ok", "bytes": len(b), "sha256": sha256(b)})
                n += 1
            except Exception as e:
                fila.update({"estado": "error", "error": f"{type(e).__name__}: {e}"})
            agregar_manifest(manifest, fila)
            time.sleep(pausa)
    return n


def _num_ar(txt: str):
    """'7.211.901.281.160,48' -> 7211901281160.48 ; '' -> NaN"""
    t = (txt or "").strip()
    if t == "":
        return np.nan
    try:
        return float(t.replace(".", "").replace(",", "."))
    except ValueError:
        return np.nan


def _tipo_linea(rubro: str, linea: str) -> tuple[str, str]:
    """Clasifica una línea de detalle y extrae la contraparte (banco o mercado)."""
    l = linea.strip()
    m = re.match(r"Pzo Fi\s+(UVA\s+)?\$\s+(.*)$", l)
    if m:
        return ("plazo_fijo_uva" if m.group(1) else "plazo_fijo"), m.group(2).strip()
    m = re.match(r"Caucion\s+Colocadora\s+\$\s*(.*)$", l, flags=re.I)
    if m:
        return "caucion", (m.group(1).strip() or "sin_mercado")
    r = (rubro or "").lower()
    if "titulos" in r or "títulos" in r:
        return "titulo", l
    if "certificados de participacion" in r or l.startswith("FCI "):
        return "cuotaparte_fci", l
    if "operaciones a plazo" in r:
        return "plazo_otro", l
    return "otro", l


def parsear_cartera(html: str) -> tuple[dict, pd.DataFrame]:
    """Devuelve (encabezado, líneas).

    Estructura de la tabla 'Detalle (1)':
      - filas de rubro (texto en negrita, valor en la tercera columna):
        Disponibilidades, Operaciones a Plazo, Títulos de Deuda, Certificados de
        Participación, Otros Activos, Pasivos; una fila sin texto con el 100,00;
      - filas de detalle (texto dentro de <span>, valor en la segunda columna),
        que cuelgan del último rubro;
      - una fila '(Peso Argentina)' con el patrimonio en pesos.
    """
    soup = BeautifulSoup(html, "html.parser")
    enc = {}
    t_enc = next((t for t in soup.find_all("table") if "Cartera al" in t.get_text()), None)
    if t_enc is not None:
        for tr in t_enc.find_all("tr"):
            td = tr.find_all("td")
            if len(td) >= 2:
                enc[td[0].get_text(" ", strip=True)] = td[1].get_text(" ", strip=True)
    encab = {
        "fondo_cnv": enc.get("Fondo"),
        "cartera_al": pd.to_datetime(enc.get("Cartera al (*)"), format="%d/%m/%y", errors="coerce"),
        "gerente_cnv": enc.get("Gerente"), "depositaria_cnv": enc.get("Depositaria"),
        "clasificacion_cnv": enc.get("Clasificación"), "moneda_cnv": enc.get("Moneda"),
        "region_cnv": enc.get("Región"), "horizonte_cnv": enc.get("Horizonte"),
        "pn_cartera": np.nan, "total_pct": np.nan,
    }
    t_det = next((t for t in soup.find_all("table") if "Detalle" in t.get_text()), None)
    lineas = []
    if t_det is not None:
        rubro = None
        filas = t_det.find("tbody").find_all("tr") if t_det.find("tbody") else t_det.find_all("tr")[1:]
        for orden, tr in enumerate(filas):
            td = tr.find_all("td")
            if len(td) < 3:
                continue
            texto = td[0].get_text(" ", strip=True)
            v1, v2 = _num_ar(td[1].get_text()), _num_ar(td[2].get_text())
            if texto.startswith("(") and texto.endswith(")"):
                encab["pn_cartera"] = v1
                encab["moneda_pn"] = texto.strip("()")
                continue
            if texto == "":
                encab["total_pct"] = v2
                continue
            if td[0].find("span") is None:
                rubro = texto
                lineas.append({"orden": orden, "nivel": "rubro", "rubro": rubro, "linea": texto,
                               "tipo": "rubro", "contraparte": None, "pct": v2})
            else:
                tipo, contra = _tipo_linea(rubro, texto)
                lineas.append({"orden": orden, "nivel": "detalle", "rubro": rubro, "linea": texto,
                               "tipo": tipo, "contraparte": contra, "pct": v1})
    return encab, pd.DataFrame(lineas)


def apilar_carteras(carpeta: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Lee todos los HTML bajados. Devuelve (encabezados, líneas), una fila por
    (lfc, fecha pedida). Como la ficha devuelve la cartera vigente a la fecha
    pedida, varias fechas pueden traer la misma cartera; se deduplica después
    por (lfc, cartera_al)."""
    encs, lins = [], []
    for p in sorted(list(carpeta.glob("*/*.html.gz")) + list(carpeta.glob("*/*.html"))):
        lfc, fecha = p.parent.name, p.name.replace(".html.gz", "").replace(".html", "")
        try:
            b = p.read_bytes()
            b = gzip.decompress(b) if p.suffix == ".gz" else b
            e, l = parsear_cartera(b.decode("utf-8", errors="replace"))
        except Exception as ex:
            e, l = {"error": f"{type(ex).__name__}: {ex}"}, pd.DataFrame()
        e.update({"lfc": lfc, "fecha_pedida": pd.Timestamp(fecha)})
        encs.append(e)
        if len(l):
            l.insert(0, "fecha_pedida", pd.Timestamp(fecha))
            l.insert(0, "lfc", lfc)
            l["cartera_al"] = e.get("cartera_al")
            lins.append(l)
    E = pd.DataFrame(encs)
    L = pd.concat(lins, ignore_index=True) if lins else pd.DataFrame()
    return E, L


# ===========================================================================
# 3. CROSSWALK DE FONDOS (código CNV de la planilla <-> id de la ficha)
# ===========================================================================

_QUITAR = [r"\bF\.?\s?C\.?\s?I\.?\b", r"FONDO COMUN DE INVERSION", r"\bFONDO\b",
           r"\bS\.?A\.?\b", r"\bCLASE\s+\w+\b"]


def normalizar_nombre(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().upper()
    s = s.replace("$", " PESOS ")
    for pat in _QUITAR:
        s = re.sub(pat, " ", s)
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def proponer_crosswalk(fondos_planilla: pd.DataFrame, lista_cnv: pd.DataFrame,
                       top: int = 3) -> pd.DataFrame:
    """Para cada fondo de la planilla (cod_cnv, fondo) propone el id de la
    ficha CNV por similitud de nombre. Hay que revisarlo a mano: la columna
    'revisado' se completa con 1 cuando el match está confirmado."""
    L = lista_cnv.copy()
    L["n"] = L["nombre_cnv"].map(normalizar_nombre)
    out = []
    for _, f in fondos_planilla.iterrows():
        n = normalizar_nombre(f["fondo"])
        sc = L["n"].map(lambda x: SequenceMatcher(None, n, x).ratio())
        # bonus si el nombre de la planilla está contenido en el de la CNV (casos 'ex ...')
        sc = sc + L["n"].map(lambda x: 0.15 if n and (n in x) else 0.0)
        best = sc.sort_values(ascending=False).head(top)
        cand = [f"{L.loc[i,'lfc']}:{L.loc[i,'nombre_cnv']} ({sc[i]:.2f})" for i in best.index]
        i0 = best.index[0]
        out.append({"cod_cnv": f["cod_cnv"], "fondo_planilla": f["fondo"],
                    "gerente_planilla": f.get("gerente"),
                    "lfc": L.loc[i0, "lfc"], "nombre_cnv": L.loc[i0, "nombre_cnv"],
                    "score": round(float(best.iloc[0]), 3),
                    "exacto": int(n == L.loc[i0, "n"]),
                    "candidatos": " | ".join(cand), "revisado": 0, "nota": ""})
    return pd.DataFrame(out)


# ===========================================================================
# 4. VARIABLES DERIVADAS Y PANELES
# ===========================================================================

def semana(fechas: pd.Series) -> pd.Series:
    """Viernes de la semana (semanas que cierran el viernes)."""
    return pd.to_datetime(fechas).dt.to_period("W-FRI").dt.end_time.dt.normalize()


def derivar_clase_dia(pl: pd.DataFrame) -> pd.DataFrame:
    """Variables por clase y día. Convenciones (ver diccionario_fci.md):
      vcp es el precio de 1.000 cuotapartes, así que el precio unitario es vcp/1000;
      rendimiento neto = vcp / vcp_ant - 1, en los días corridos entre fecha_ant y fecha;
      tna_neta = rendimiento / días * 365 (en %);
      fee = hon_sg + hon_sd + gastos (% anual);
      tna_bruta = tna_neta + fee: lo que rinde la cartera antes de honorarios;
      flujo = (ccp - ccp_ant) * vcp / 1000, en pesos.
    """
    d = pl.sort_values(["cod_cafci", "fecha"]).copy()
    # cuando la planilla no trae el dato del día anterior, se usa la planilla previa
    g = d.groupby("cod_cafci")
    d["vcp_ant_lag"] = g["vcp"].shift()
    d["ccp_ant_lag"] = g["ccp"].shift()
    d["fecha_lag"] = g["fecha"].shift()
    d["vcp_ant_u"] = d["vcp_ant"].where(d["vcp_ant"].notna(), d["vcp_ant_lag"])
    d["ccp_ant_u"] = d["ccp_ant"].where(d["ccp_ant"].notna(), d["ccp_ant_lag"])
    f_ant = d["fecha_ant"].where(d["vcp_ant"].notna(), d["fecha_lag"])
    d["dias"] = (d["fecha"] - f_ant).dt.days
    d["r_neto"] = d["vcp"] / d["vcp_ant_u"] - 1
    d["tna_neta"] = 100 * d["r_neto"] / d["dias"] * 365
    d["fee"] = d[["hon_sg", "hon_sd", "gastos"]].fillna(0).sum(axis=1)
    d["tna_bruta"] = d["tna_neta"] + d["fee"]
    d["flujo"] = (d["ccp"] - d["ccp_ant_u"]) * d["vcp"] / 1000
    d["flujo_rel"] = d["flujo"] / (d["ccp_ant_u"] * d["vcp_ant_u"] / 1000)
    # clases sin patrimonio, VCP en 1000 (nunca activadas) o días raros: fuera del rendimiento
    malo = (d["pn"] <= 0) | (d["dias"] <= 0) | (d["dias"] > 10) | (d["vcp_ant_u"] <= 0)
    # saltos de VCP que no son rendimiento (relanzamiento de una clase, errores de
    # carga): en un money market una TNA fuera de [-50, 500] no es plausible
    malo = malo | ~d["tna_neta"].between(-50, 500)
    if "desactualizado" in d:
        malo = malo | d["desactualizado"].eq(1)
        d.loc[d["desactualizado"].eq(1), ["flujo", "flujo_rel"]] = np.nan
    d.loc[malo, ["r_neto", "tna_neta", "tna_bruta"]] = np.nan
    return d.drop(columns=["vcp_ant_lag", "ccp_ant_lag", "fecha_lag"])


def fondo_dia(cd: pd.DataFrame) -> pd.DataFrame:
    """Agrega clases a fondo (cod_cnv) y día. Se descartan las filas
    desactualizadas (clases que ese día repitieron un valor viejo)."""
    x = cd[cd["desactualizado"].eq(0)].copy() if "desactualizado" in cd else cd.copy()
    x["w"] = x["pn"].clip(lower=0)
    x["tb_w"] = x["tna_bruta"] * x["w"]
    x["fee_w"] = x["fee"] * x["w"]
    x["w_tb"] = x["w"].where(x["tna_bruta"].notna(), 0)
    g = x.groupby(["cod_cnv", "fecha"])
    out = g.agg(fondo=("fondo", "first"), gerente=("gerente", "first"),
                depositaria=("depositaria", "first"), tipo_dinero=("tipo_dinero", "first"),
                pn=("pn", "sum"), flujo=("flujo", lambda v: v.sum(min_count=1)), dias=("dias", "max"),
                n_clases=("cod_cafci", "nunique"),
                n_clases_activas=("pn", lambda s: int((s > 0).sum())),
                tb_w=("tb_w", "sum"), w_tb=("w_tb", "sum"), fee_w=("fee_w", "sum"), w=("w", "sum"))
    out["tna_bruta"] = out["tb_w"] / out["w_tb"].replace(0, np.nan)
    out["fee_medio"] = out["fee_w"] / out["w"].replace(0, np.nan)
    return out.drop(columns=["tb_w", "w_tb", "fee_w", "w"]).reset_index()


def fondo_semana(fd: pd.DataFrame) -> pd.DataFrame:
    """Lleva fondo x día a fondo x semana (cierre viernes).
    Flujo: suma. PN: último día. TNA bruta: promedio ponderado por días."""
    x = fd.sort_values(["cod_cnv", "fecha"]).copy()
    x["semana"] = semana(x["fecha"])
    x["tb_d"] = x["tna_bruta"] * x["dias"]
    x["d_ok"] = x["dias"].where(x["tna_bruta"].notna(), 0)
    g = x.groupby(["cod_cnv", "semana"])
    out = g.agg(fondo=("fondo", "last"), gerente=("gerente", "last"),
                depositaria=("depositaria", "last"), tipo_dinero=("tipo_dinero", "last"),
                pn=("pn", "last"), flujo=("flujo", lambda v: v.sum(min_count=1)), n_dias=("fecha", "count"),
                ultima_fecha=("fecha", "max"), tb_d=("tb_d", "sum"), d_ok=("d_ok", "sum"),
                fee_medio=("fee_medio", "last"))
    out["tna_bruta"] = out["tb_d"] / out["d_ok"].replace(0, np.nan)
    return out.drop(columns=["tb_d", "d_ok"]).reset_index()


def cartera_ancha(E: pd.DataFrame, L: pd.DataFrame) -> pd.DataFrame:
    """Una fila por (lfc, cartera_al) con los rubros principales en % del PN."""
    e = (E.dropna(subset=["cartera_al"]).sort_values("fecha_pedida")
           .drop_duplicates(["lfc", "cartera_al"], keep="last"))
    l = L.dropna(subset=["cartera_al"]).drop_duplicates(["lfc", "cartera_al", "orden"])
    rub = l[l["nivel"] == "rubro"].copy()
    rub["r"] = rub["rubro"].str.lower()
    def suma(mask):
        return rub[mask].groupby(["lfc", "cartera_al"])["pct"].sum(min_count=1)
    w = pd.DataFrame({
        "pct_disponibilidades": suma(rub["r"].str.startswith("disponibilidades")),
        "pct_operaciones_plazo": suma(rub["r"].str.startswith("operaciones a plazo")),
        "pct_titulos": suma(rub["r"].str.contains("titulos|títulos")),
        "pct_cuotapartes_fci": suma(rub["r"].str.contains("certificados de participacion")),
        "pct_otros_activos": suma(rub["r"].str.startswith("otros activos")),
        "pct_pasivos": suma(rub["r"].str.startswith("pasivos")),
    })
    det = l[l["nivel"] == "detalle"]
    for t in ["plazo_fijo", "plazo_fijo_uva", "caucion"]:
        w[f"pct_{t}"] = det[det["tipo"] == t].groupby(["lfc", "cartera_al"])["pct"].sum(min_count=1)
    w["n_bancos_pf"] = det[det["tipo"].isin(["plazo_fijo", "plazo_fijo_uva"])].groupby(
        ["lfc", "cartera_al"])["contraparte"].nunique()
    w = w.reset_index()
    # carteras mal cargadas por la gerente: porcentajes > 100 (a veces montos en
    # pesos en la columna de %) o patrimonio absurdo. Se marcan, no se corrigen.
    pcts = [c for c in w.columns if c.startswith("pct_")]
    w["cartera_valida"] = (w[pcts].fillna(0).le(100.5).all(axis=1)
                           & w[pcts].fillna(0).ge(-1).all(axis=1)).astype(int)
    out = e.merge(w, on=["lfc", "cartera_al"], how="left")
    out.loc[out["pn_cartera"].fillna(0) < 1e6, "cartera_valida"] = 0
    out["semana"] = semana(out["cartera_al"])
    return out
