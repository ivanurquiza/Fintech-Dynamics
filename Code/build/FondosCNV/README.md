# FondosCNV

Bases de fondos comunes de inversión money market a partir de dos fuentes públicas de la CNV: la planilla diaria por clase (desde ene-2020) y la cartera semanal de cada fondo (desde nov-2019). Variables y construcción: `Data/docs/diccionario_fondoscnv.md`. Fuentes y rutas: `Methodological_Notes/A_fondos_encajes/fuentes_fci.md`.

| Notebook | Qué hace | Sale en `Data/processed/FondosCNV/` |
|---|---|---|
| `01_planillas_diarias.ipynb` | Baja las planillas diarias CAFCI/CNV (desde ene-2020) y las apila | `planillas_por_dia/*.parquet`, `planillas_mm.parquet` |
| `02_carteras_semanales.ipynb` | Arma el crosswalk de fondos y baja la cartera semanal de cada money market (desde 2019) | `carteras_por_fondo/`, `carteras_encabezado.parquet`, `carteras_lineas.parquet` |
| `03_paneles_y_merge.ipynb` | Variables derivadas, paneles clase × día, fondo × día y fondo × semana, merge con cartera | `carteras_ancha.parquet`, `panel_clase_dia.parquet`, `panel_fondo_dia.parquet`, `panel_fondo_semana_planilla.parquet`, `panel_fondo_semana.parquet` / `.dta` |

Las funciones están en `fondoscnv.py`. Los notebooks se corren desde esta carpeta y en orden.

**Paso manual entre 02 y 03:** revisar `Data/crosswalks/fondos_cnv_lfc.csv` (código CNV de la planilla ↔ id de la ficha CNV) y marcar `revisado = 1`. El 03 sólo usa filas revisadas.

**Crudos:** `Data/raw/FondosCNV/` guarda los xlsx y html tal como vienen, más un manifest con fecha y hash de cada descarga. No van al repo (ver `.gitignore`), porque son ~1 GB.

**Descargas:** se pueden cortar y retomar. Lo que ya está en disco no se vuelve a pedir. El servicio de archivos de la CNV da 503 a rachas; si pasa, esperar y volver a correr la celda.

**Desde dónde se corre.** El sitio de la CNV no responde a pedidos desde servidores en la nube; la descarga se hace desde una máquina local. Si `requests` queda bloqueado, las mismas funciones de URL (`url_cartera`, `adjunto_de_presentacion`) sirven para bajar desde el navegador; así se bajó la versión actual (sep-2026) y los archivos se dejaron en las mismas carpetas de `Data/raw/FondosCNV/`. Los notebooks 01 y 02 detectan lo que ya está en disco y sólo apilan.

**Estado (12-oct-2026).** Completo: 1.634 planillas (2-ene-2020 a 25-sep-2026), 19.209 carteras, crosswalk 82/82. Pendiente: 24 carteras cortadas por tiempo y el crosswalk de las contrapartes de plazo fijo ("Bco Nacion", "Nvo Bco Indus") a código de entidad BCRA. Ver `Data/docs/notas_revision_datos.md`.

Requiere: `pandas`, `numpy`, `requests`, `beautifulsoup4`, `openpyxl`, `pyarrow`, `matplotlib`.
