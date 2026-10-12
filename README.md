# Fintech-Dynamics

Proyecto de investigación sobre la interacción entre medios de pago digitales, fondos comunes de inversión money market, crédito no bancario y fondeo de los bancos en Argentina. Universidad de San Andrés.

## Horizonte del estudio

Desde 2020 el ahorro transaccional de los hogares argentinos se desplazó en buena medida hacia billeteras digitales cuyos saldos se invierten en fondos money market, y esos fondos colocan a su vez en cuentas a la vista, plazos fijos y cauciones. En paralelo, el BCRA cambió varias veces el tratamiento de esos pasivos (encajes sobre la vista de los fondos y sobre las cuentas de los proveedores de pago, interoperabilidad, salida de la LEFI) y los proveedores no financieros pasaron a ser una parte relevante del crédito a personas. El proyecto estudia cómo esos cambios se transmiten a la composición y al costo del fondeo bancario, a la asignación de cartera de los fondos y a la oferta y el repago del crédito, con datos administrativos a nivel de banco, fondo y deudor.

Hoy hay tres líneas de trabajo, con notas propias en `Methodological_Notes/`:

| Línea | Tema | Datos principales | Estado |
|---|---|---|---|
| A | Fondos money market, encajes y fondeo bancario | FondosCNV, balances, normativa | Base completa; descriptivos |
| B | Liquidez bancaria de 2025 y sustitución por crédito fintech | CENDEU, balances | Descriptivos; diseño abierto |
| C | Orden de repago entre acreedores del mismo deudor | CENDEU (muestra 5%), padrón | Primera estimación y diagnósticos |

## Estructura

| Carpeta | Contenido |
|---|---|
| `Data/` | Datos crudos (fuera de git), bases construidas, crosswalks y documentación. Ver `Data/README_data.md` |
| `Code/build/` | Descarga y construcción de las bases. `FondosCNV/` arma las de fondos |
| `Code/analysis/` | Análisis por línea. Ver `Code/analysis/README.md` |
| `Code/output/` | Figuras y tablas |
| `Methodological_Notes/` | Notas de discusión y diseño, por línea, más `comun/` y `archivo/` |
| `Regulation/` | Corpus normativo del BCRA, cronología y alícuotas de efectivo mínimo |
| `Literature/` | 19 PDF y una guía de lectura comentada |
| `Presentations/` | Presentaciones de avance y documento de datos para el BCRA |

## Fuentes de datos

| Fuente | Organismo | Qué se usa | Frecuencia y cobertura | Acceso |
|---|---|---|---|---|
| Información de Entidades Financieras (IEF): balances (`baldet`/`balhist`), indicadores, información adicional, estado de situación de deudores y red de atención por provincia | BCRA | Balance de saldos por cuenta, resultados, indicadores, cartera por situación, sucursales y cajeros, préstamos y depósitos por provincia | Mensual, ene-2018 a abr-2026, ~77 entidades por mes | Público, `Code/build/descargar_ief_selectivo.py` |
| Informe de Inclusión Financiera | BCRA | Puntos de acceso por localidad y entidad; personas con cuenta y con crédito por provincia | Mensual (personas con cuenta, trimestral), 2017 a 2025 | Público, `descargar_datos_bcra.py` y descarga manual |
| Central de Deudores (CENDEU) y padrón de ARCA | BCRA | Deudor × entidad × mes: situación, saldo, proceso judicial, refinanciación, días de atraso; panel de 24 meses | Mensual, ago-2024 a jul-2026 | Clave Fiscal y declaración jurada (Ley 25.326); microdato identificado |
| Planilla diaria de valores de cuotaparte | CNV (provista por CAFCI) | Clase × día: cuotapartes, VCP, patrimonio, honorarios, gerente, depositaria | Diaria, ene-2020 a sep-2026 | Público, AIF de la CNV |
| Composición de cartera de cada fondo | CNV | Fondo × semana: vista, plazo fijo por banco, caución, títulos | Semanal, nov-2019 a sep-2026 | Público, ficha del fondo en la CNV |
| Resúmenes y maestro de fondos | CAFCI | Agregados de la industria y padrón de fondos y clases | Mensual | Público |
| Registro de proveedores de servicios de pago | BCRA | PSP con cuenta de pago | Corte | Público |
| Normativa (Comunicaciones "A", textos ordenados) | BCRA | Encajes, interoperabilidad, PSP | 2016 a 2026 | Público, `Regulation/descargar_normativa.py` |
| IPC | INDEC | Nivel general nacional y regional | Mensual, dic-2016 a jun-2026 | Público |

## Bases construidas

Todas en `Data/processed/`. Diccionarios variable por variable en `Data/docs/`.

| Base | Unidad | Cobertura | Contenido |
|---|---|---|---|
| `balances_bancos.dta` | entidad × mes | 2018m1 a 2026m4 | 328 variables: activo, préstamos, depósitos por sector, instrumento y moneda (incluidas las partidas 311723, 311724 y precancelables), resultados mensuales, tipo de entidad, versiones reales en pesos de ene-2026 |
| `caracteristicas_bancos.dta` | entidad × mes × código | 2018m1 a 2026m4 | 110 códigos del IEF en formato largo: indicadores (capital, calidad de cartera, rentabilidad, tasas implícitas), cantidad de cuentas y operaciones, cartera por situación de deudores |
| `prestamos_depositos_prov.dta` | entidad × provincia × mes | 2018m1 a 2026m4 | Sucursales, cajeros, terminales y agencias; préstamos y depósitos por provincia (trimestrales) |
| `inclusion_prov.dta` | provincia × mes | 2017m1 a 2025m12 | Puntos de acceso, % de adultos con crédito por tipo y proveedor, personas con cuenta bancaria y de pago |
| `pda_provincia.dta`, `pda_depto.dta`, `pda_localidad.parquet`, `pda_lender_depto.dta` | provincia, departamento, localidad o entidad × departamento, por mes | 2019m1 a 2025m12 | Puntos de acceso por tipo |
| `ipc.dta` | mes | dic-2016 a jun-2026 | IPC nacional y regional |
| `cendeu/` (9 bases parquet) | deudor × entidad × mes y agregados | ago-2024 a jul-2026 | Corte mensual, panel de 24 meses, padrón, rectificaciones, agregados por entidad, empresa, persona y una muestra del 5% de personas |
| `FondosCNV/panel_fondo_semana.dta` | fondo money market × semana | ene-2020 a sep-2026 | 82 fondos: patrimonio, flujo neto, TNA bruta, honorarios y composición de cartera |
| `FondosCNV/*.parquet` | clase × día, fondo × día, cartera | ene-2020 a sep-2026 | Planilla diaria, variables derivadas, líneas de cartera por banco y mercado |

Las llaves de cruce son `ent` (código de entidad BCRA) entre balances, CENDEU y crosswalks; `cuit` dentro de CENDEU; `cod_cnv` y `cod_cafci` en fondos. Las convenciones de meses difieren entre bases y están explicadas en `Data/README_data.md`. Los chequeos pendientes sobre cada base están en `Data/docs/notas_revision_datos.md`.

## Cómo correr

Los scripts resuelven la raíz del repo por su cuenta y se pueden ejecutar desde cualquier subcarpeta. Los `.do` suben directorios hasta encontrar este archivo y definen `$root`, `$raw`, `$proc`, `$cross`, `$tab` y `$fig`.

```
python3 Code/build/descargar_ief_selectivo.py     # IEF del BCRA
stata -b do Code/build/build_dta.do               # .dta de bancos, provincias e IPC
python3 Code/build/build_puntos_acceso.py         # puntos de acceso
python3 Code/build/cendeu_build.py deudores       # Central de Deudores (ver la secuencia completa)
# Code/build/FondosCNV/01, 02 y 03                # fondos money market
python3 Code/build/documentar_bases.py            # diccionario de las bases
```

El orden completo está en `Data/README_data.md`. Requiere Python 3.10 o posterior con `pandas`, `numpy`, `pyarrow`, `duckdb`, `requests`, `beautifulsoup4`, `openpyxl` y `matplotlib`, y Stata 17 o posterior.

## Qué no está en el repositorio

`Data/raw/`, `Data/processed/cendeu/` y todos los `.parquet` están fuera de git (unos 14 GB). La Central de Deudores contiene microdato identificado sujeto a la declaración jurada de la Ley 25.326: se procesa sólo en máquinas del equipo, y las salidas del repo son agregados. Los archivos de la Central se publican sólo para el mes corriente, así que los `.7z` originales se guardan con su hash; el resto se reconstruye con los scripts de `Code/build/`.

## Por dónde empezar

1. `Methodological_Notes/comun/revision_integral_2026-09-28.md`: estado del proyecto y evaluación de cada línea.
2. `Data/README_data.md` y `Data/docs/`: datos.
3. El `README.md` de la línea que interese en `Methodological_Notes/` y su carpeta en `Code/analysis/`.
