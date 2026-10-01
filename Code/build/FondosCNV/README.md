# FondosCNV

Bases de fondos comunes de inversión a partir de dos fuentes públicas de la CNV. Detalle de fuentes y variables en el proyecto: `claude/fuentes_fci.md` y `claude/diccionario_fci.md`.

| Notebook | Qué hace | Sale en `Data/processed/FondosCNV/` |
|---|---|---|
| `01_planillas_diarias.ipynb` | Baja las planillas diarias CAFCI/CNV (desde ene-2020) y las apila | `planillas_todas.parquet`, `planillas_mm.parquet` |
| `02_carteras_semanales.ipynb` | Arma el crosswalk de fondos y baja la cartera semanal de cada money market (desde 2019) | `carteras_encabezado.parquet`, `carteras_lineas.parquet` |
| `03_paneles_y_merge.ipynb` | Variables derivadas, paneles clase × día, fondo × día y fondo × semana, merge con cartera | `panel_clase_dia.parquet`, `panel_fondo_dia.parquet`, `panel_fondo_semana.parquet` / `.dta` |

Las funciones están en `fondoscnv.py`. Los notebooks se corren desde esta carpeta y en orden.

**Paso manual entre 02 y 03:** revisar `Data/crosswalks/fondos_cnv_lfc.csv` (código CNV de la planilla ↔ id de la ficha CNV) y marcar `revisado = 1`. El 03 sólo usa filas revisadas.

**Crudos:** `Data/raw/FondosCNV/` guarda los xlsx y html tal como vienen, más un manifest con fecha y hash de cada descarga. No van al repo (ver `.gitignore`), porque son ~1 GB.

**Descargas:** se pueden cortar y retomar. Lo que ya está en disco no se vuelve a pedir. El servicio de archivos de la CNV da 503 a rachas; si pasa, esperar y volver a correr la celda.

Pendiente: crosswalk de las contrapartes de plazo fijo ("Bco Nacion", "Nvo Bco Indus") a código de entidad BCRA.

Requiere: `pandas`, `numpy`, `requests`, `beautifulsoup4`, `openpyxl`, `pyarrow`, `matplotlib`.
