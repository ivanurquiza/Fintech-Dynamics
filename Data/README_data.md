# Datos del proyecto

Qué hay, de dónde sale y en qué orden se construye. Todos los scripts viven en
`Code/build/` y resuelven la raíz del repositorio por su cuenta, así que se corren
desde cualquier subcarpeta.

```
Data/
├── raw/          descargas crudas, una carpeta por fuente. Fuera de git
├── processed/    bases construidas, listas para estimar
├── crosswalks/   tablas de correspondencia curadas a mano. Sí van a git
└── docs/         documentación de las bases, en PDF
```

`raw/` y `processed/cendeu/` están fuera de control de versiones: pesan unos 11 GB y la
Central de Deudores contiene microdato identificado sujeto a la declaración jurada de la
Ley 25.326.

---

## Fuentes crudas

| Carpeta | Fuente | Contenido | Se baja con |
|---|---|---|---|
| `raw/bcra_ief/` | BCRA, Información de Entidades Financieras | Directorios previstos para ene-2018 a dic-2026; los paneles construidos contienen 100 meses, ene-2018 a abr-2026 | `descargar_ief_selectivo.py` |
| `raw/bcra_inclusion/` | BCRA, Informe de Inclusión Financiera | Series provinciales de deudores, puntos de acceso y tenencia de cuentas | `descargar_datos_bcra.py` |
| `raw/bcra_inclusion/puntos_acceso/` | BCRA, Informe de Inclusión Financiera | Puntos de acceso por entidad, tipo y **localidad**, mensual desde 2019 | descarga manual desde `bcra.gob.ar/indicadores-inclusion-financiera/` |
| `raw/bcra_balhist/` | BCRA, balances históricos | `balhist.txt`, partidas contables por entidad y mes | descarga manual |
| `raw/bcra_cendeu/` | BCRA, Central de Deudores | Archivos `.7z` del mes corriente y del panel de 24 meses | Clave Fiscal de ARCA, servicio *BCRA – Cheques y Deudores* |
| `raw/cafci/` | CAFCI | Resúmenes mensuales de la industria de fondos, maestro de fondos y cuentas | `descargar_cafci.py` |
| `raw/psp/` | BCRA | Registro de proveedores de servicios de pago | `descargar_registro_psp.py` |
| `raw/ipc/` | INDEC | `sh_ipc.xls`, índice de precios nacional y regional | descarga manual |
| `raw/geo/` | — | `ar_provincias.geojson`, contornos provinciales para los mapas | — |

## Bases construidas

| Archivo | Nivel | Filas | Columnas |
|---|---|---|---|
| `processed/balances_bancos.dta` | entidad × mes | 7.681 | 328 |
| `processed/caracteristicas_bancos.dta` | entidad × mes × código, formato largo | 528.714 | 7 |
| `processed/prestamos_depositos_prov.dta` | entidad × provincia × mes; montos solo en cierres trimestrales | 48.115 | 25 |
| `processed/inclusion_prov.dta` | provincia × mes | 2.592 | 26 |
| `processed/ipc.dta` | mes | 115 | 8 |
| `processed/pda_depto.dta` | departamento × mes | 43.851 | 15 |
| `processed/pda_provincia.dta` | provincia × mes | 2.016 | 15 |
| `processed/pda_localidad.parquet` | localidad × tipo × mes | 368.939 | 11 |
| `processed/pda_lender_depto.dta` | entidad × departamento × tipo × mes | 594.214 | 8 |
| `processed/cendeu/` | ver `docs/cendeu_bases.pdf` | — | — |

Los puntos de acceso están documentados en `docs/pda_bases.pdf`, con el control de
consistencia contra el archivo por provincia que publica el BCRA.

Las versiones monetarias con sufijo `_r` de `balances_bancos` y
`prestamos_depositos_prov` están a precios de enero de 2026, deflactadas con el
IPC nacional; las columnas originales conservan los valores nominales.

## Correspondencias

| Archivo | Qué mapea |
|---|---|
| `crosswalks/psp_fci_map.csv` | Billetera → entidad legal, fondo, clase de cuotaparte, gerente, depositaria y su código de entidad BCRA |
| `crosswalks/cendeu_lenders.csv` | 577 acreedores de la Central de Deudores: código, nombre, clase regulatoria derivada del rango del código, taxonomía propia y si tiene balance publicado |
| `crosswalks/provincias_arca_indec.csv` | Código provincial de ARCA ↔ código provincial del INDEC. Une el padrón de deudores con los puntos de acceso |

---

## Orden del pipeline

**1. Descarga.** Cada fuente por separado; son independientes entre sí.

```
python3 Code/build/descargar_ief_selectivo.py
python3 Code/build/descargar_datos_bcra.py
python3 Code/build/descargar_cafci.py
python3 Code/build/descargar_registro_psp.py
python3 Code/build/extraer_cafci_agregados.py
python3 Code/build/extraer_fci_balhist.py
```

**2. Construcción del panel bancario.** Lee `raw/bcra_ief/`, `raw/bcra_inclusion/` y
`raw/ipc/`; escribe los `.dta` de `processed/`.

```
stata -b do Code/build/build_dta.do
```

**2b. Puntos de acceso.** Independiente del resto.

```
python3 Code/build/build_puntos_acceso.py
```

**3. Central de Deudores.** Descomprimir los `.7z` en
`raw/bcra_cendeu/extracted/` y después:

```
python3 Code/build/cendeu_build.py deudores          # corte mensual
python3 Code/build/cendeu_build.py dsf1              # antigüedad en situación normal
python3 Code/build/cendeu_build_text.py rect         # rectificativas
python3 Code/build/cendeu_build_text.py padron       # padrón de ARCA
bsdtar -xOf Data/raw/bcra_cendeu/24DSF*.7Z 24DSF.txt | python3 Code/build/cendeu_build_panel.py
python3 Code/build/cendeu_reshape.py lender_month
python3 Code/build/cendeu_reshape.py firm
python3 Code/build/cendeu_reshape.py sample
python3 Code/build/cendeu_reshape.py person_month
```

Los `.txt` intermedios pesan hasta 22 GB y se borran después de convertir. Los `.7z`
originales conviene guardarlos: el BCRA publica sólo el mes corriente, así que un mes
que no se baja se pierde.

## Llaves

`ent` es el código de entidad del BCRA y une la Central de Deudores con los balances y
con el mapa de billeteras. `cuit` une entre sí a los archivos de la Central y con el
padrón de ARCA. En los `.dta`, `ym` es el índice mensual de Stata, meses desde
enero de 1960 (pandas lo convierte a fecha cuando tiene formato Stata `%tm`).
En los parquet derivados de CENDEU, `ym = year * 12 + month - 1`:
para pasarlo a índice Stata se resta `1960 * 12 = 23520`. No unir por el entero
`ym` sin armonizar estas convenciones.

Los puntos de acceso se unen a la Central de Deudores **por provincia**: el padrón trae el
código provincial de ARCA y `provincias_arca_indec.csv` lo lleva al código del INDEC que usa
`pda_provincia`. Las 24 verificadas. Bajar a departamento requiere una tabla que lleve el
código postal del padrón al código de departamento del INDEC, que no existe publicada de
forma abierta y limpia. Es la pieza pendiente para el diseño geográfico fino.
