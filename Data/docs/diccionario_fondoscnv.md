# Bases de fondos comunes de inversión money market (FondosCNV)

Documentación de las bases que arma `Code/build/FondosCNV/`. Cubre las dos fuentes, cómo se descargan, cada archivo resultante y la construcción de las variables derivadas. Versión del 12-oct-2026, con datos hasta el 25-sep-2026.

## 1. Fuentes

**Planilla diaria de valores de cuotaparte (CNV, provista por CAFCI).** Un xlsx por día hábil con una fila por clase de cuotaparte de todos los FCI del país. Se publica en `cnv.gov.ar > Fondos Comunes de Inversión > Últimos valores diarios de cuotaparte`; el índice está en `https://www.cnv.gov.ar/SitioWeb/FondosComunesInversion/CuotaPartes` y cada día es una presentación de la AIF (`https://aif2.cnv.gov.ar/Presentations/publicview/{GUID}`). El archivo se baja con la clave pública del servicio de blobs de la CNV (ver `fondoscnv.bajar_blob`). Cobertura: 2-ene-2020 a la fecha. Si un día tiene más de una versión se usa la última.

**Composición de cartera semanal (ficha CNV de cada fondo).** `https://www.cnv.gov.ar/SitioWeb/FondosComunesInversion/DetallesFCI/{lfc}?...&compo=true&fecha=AAAA-MM-DD` devuelve la última cartera informada a esa fecha. Es una sola por fondo, común a todas sus clases. El historial empieza el 8-nov-2019. `lfc` es el id interno de la ficha y no coincide con el código CNV de la planilla; el puente es `Data/crosswalks/fondos_cnv_lfc.csv`.

Las dos fuentes se descargan desde un navegador con sesión en la CNV (el sitio no responde a clientes fuera de Argentina). Los crudos quedan en `Data/raw/FondosCNV/` con un manifest por descarga (fecha, guid o url, sha256).

## 2. Universo

Fondos de la sección money market en pesos. Hasta el 6-sep-2021 la planilla la llama "Plazo Fijo Peso Argentina" y desde el 13-sep-2021 "Mercado de Dinero Peso Argentina"; `fondoscnv.SECCIONES_MM` toma las dos. Quedan 82 fondos (código CNV) y 287 clases (código CAFCI). Fondos por año en el panel semanal: 39 (2020), 46, 50, 55, 63, 72, 66 (2026).

Tres fondos entran a la sección después de haber sido de otro tipo, con el mismo código: Mercado Fondo (cod. 956) era renta fija hasta el 19-feb-2020, Cohen Renta Fija pasa a Cohen Pesos en ago-2021 y Adcap Balanceado IX pasa a Adcap Ahorro Dinámico en dic-2023. Sus carteras previas no son de money market.

## 3. Archivos

Todo en `Data/processed/FondosCNV/`. Sólo `panel_fondo_semana.dta` está en git; los parquet se regeneran con los notebooks.

| Archivo | Unidad | Filas | Notebook |
|---|---|---:|---|
| `planillas_por_dia/AAAAMMDD_*.parquet` | clase × día, todos los tipos de fondo | 1.634 archivos | 01 |
| `planillas_mm.parquet` | clase × día, money market | 256.475 | 01 |
| `carteras_por_fondo/{lfc}_*.parquet` | encabezado y líneas por fondo | 83 fondos | 02 |
| `carteras_encabezado.parquet` | fondo × fecha pedida | 19.209 | 02 |
| `carteras_lineas.parquet` | línea de cartera | 237.569 | 02 |
| `carteras_ancha.parquet` | fondo × fecha de cartera | 17.642 | 03 |
| `panel_clase_dia.parquet` | clase × día, con derivadas | 256.475 | 03 |
| `panel_fondo_dia.parquet` | fondo × día | 82.248 | 03 |
| `panel_fondo_semana_planilla.parquet` | fondo × semana, sólo planilla | 17.893 | 03 |
| `panel_fondo_semana.parquet` / `.dta` | fondo × semana, planilla + cartera | 17.893 | 03 |

### 3.1 `planillas_mm.parquet` (variables de la planilla)

Nombres normalizados por `fondoscnv.leer_planilla`. Montos en pesos nominales; porcentajes en puntos.

| Variable | Contenido |
|---|---|
| `fecha` | Fecha del valor informado por la clase. Puede ser anterior a la planilla si la clase no reportó |
| `fecha_planilla`, `archivo` | Fecha y nombre del xlsx de origen |
| `fecha_ant` | Fecha del valor anterior |
| `desactualizado` | 1 si `fecha` < `fecha_planilla`: la clase repitió un valor viejo (4,6% de las filas) |
| `fondo_clase`, `fondo`, `clase` | Nombre completo y sus dos partes |
| `cod_cnv` | Código CNV del fondo. Igual para todas sus clases |
| `cod_cafci` | Código CAFCI de la clase. Llave de clase |
| `gerente`, `cod_gerente`, `depositaria`, `cod_depositaria` | Sociedad gerente y sociedad depositaria |
| `seccion`, `subseccion`, `cod_clasificacion`, `moneda`, `cod_moneda`, `region`, `cod_region`, `horizonte`, `cod_horizonte`, `moneda_fondo` | Clasificación CAFCI |
| `tipo_dinero` | Clásico o Dinámico (sólo money market, planillas recientes) |
| `vcp`, `vcp_ant` | Valor de 1.000 cuotapartes, hoy y día anterior |
| `var_diaria`, `var_desde_fin_mes`, `var_desde_fin_anio`, `var_12m` | Variación del VCP, % |
| `vcp_reexp_pesos` | VCP reexpresado en pesos |
| `ccp`, `ccp_ant` | Cuotapartes en circulación, hoy y día anterior |
| `pn`, `pn_ant` | Patrimonio neto de la clase. Cumple `pn = ccp × vcp / 1000` |
| `market_share` | Participación informada por CAFCI. No se usa |
| `hon_sg`, `hon_sd`, `gastos` | Honorarios de gerente y depositaria y gastos ordinarios, % anual |
| `com_ingreso`, `com_rescate`, `com_transferencia`, `hon_exito` | Comisiones. En money market son cero |
| `plazo_liq` | Días hábiles de liquidación del rescate |
| `minimo_inversion` | Monto mínimo de suscripción |
| `calificacion`, `calificado` | Calificación de riesgo |
| `indice_mm` | Índice de referencia informado |
| `decreto_596`, `repatriacion`, `ley_27743` | Marcas de regímenes especiales (la última, clases del régimen de regularización de 2024) |
| `id_cafci_padre`, `id_cnv_padre`, `tipo_escision` | Fondos escindidos |
| `tipo_clase_cuota` | Minorista, Mayorista, General o No registrada. Sólo viene en las dos planillas con formato `agen_10` (17-oct-2024 y 6-mar-2025) |
| `código_*`, `de_dinero_puro_impuro` | Códigos de clasificación adicionales del formato `agen_10` |

### 3.2 `panel_clase_dia.parquet` (planilla + derivadas)

Agrega a lo anterior, en `fondoscnv.derivar_clase_dia`:

| Variable | Construcción |
|---|---|
| `vcp_ant_u`, `ccp_ant_u` | `vcp_ant` y `ccp_ant`; si faltan, el valor de la planilla previa de la misma clase |
| `dias` | Días corridos entre el valor anterior y el actual (el lunes vale 3) |
| `r_neto` | `vcp / vcp_ant_u − 1` |
| `tna_neta` | `100 × r_neto / dias × 365`, % anual |
| `fee` | `hon_sg + hon_sd + gastos`, % anual |
| `tna_bruta` | `tna_neta + fee`. Rendimiento de la cartera antes de costos. Es igual entre clases del mismo fondo (desvío mediano 0,004 pp) |
| `flujo` | `(ccp − ccp_ant_u) × vcp / 1000`, pesos. Suscripciones netas de rescates, sin componente de rendimiento |
| `flujo_rel` | `flujo` sobre el PN del día anterior |

`r_neto`, `tna_neta` y `tna_bruta` quedan en missing si la clase está desactualizada, si `pn ≤ 0`, si `dias` no está entre 1 y 10, o si la TNA neta cae fuera de [−50, 500] (saltos de VCP por relanzamientos o errores de carga). `flujo` queda en missing en filas desactualizadas. El 82% de las filas tiene TNA válida.

### 3.3 `panel_fondo_dia.parquet`

Suma de clases por `cod_cnv` y `fecha`, sólo con filas no desactualizadas. `pn` y `flujo` son sumas (`flujo` es missing si ninguna clase lo tiene); `tna_bruta` y `fee_medio` son promedios ponderados por PN; `n_clases` y `n_clases_activas` (PN > 0) cuentan clases.

### 3.4 Carteras

`carteras_encabezado`: `lfc`, `fecha_pedida` (viernes pedido), `cartera_al` (fecha efectiva; mediana de rezago 0 días, p90 1 día), `fondo_cnv`, `gerente_cnv`, `depositaria_cnv`, `clasificacion_cnv`, `moneda_cnv`, `region_cnv`, `horizonte_cnv`, `pn_cartera` (PN en pesos informado con la cartera), `total_pct`, `moneda_pn`.

`carteras_lineas`: una fila por renglón de la tabla de la ficha. `nivel` es `rubro` (Disponibilidades, Operaciones a Plazo, Títulos de Deuda, Certificados de Participación, Otros Activos, Pasivos) o `detalle`. `tipo` clasifica el detalle: `plazo_fijo`, `plazo_fijo_uva`, `caucion`, `titulo`, `cuotaparte_fci`, `plazo_otro`. `contraparte` es el banco del plazo fijo ("Bco Nacion", "Nvo Bco Indus") o el mercado de la caución, tal como lo escribe la gerente. `pct` es % del PN.

`carteras_ancha`: una fila por `lfc` y `cartera_al`, con los rubros en columnas (`pct_disponibilidades`, `pct_operaciones_plazo`, `pct_titulos`, `pct_cuotapartes_fci`, `pct_otros_activos`, `pct_pasivos`), los detalles sumados (`pct_plazo_fijo`, `pct_plazo_fijo_uva`, `pct_caucion`), `n_bancos_pf` y `cartera_valida`. Una cartera es inválida si algún porcentaje cae fuera de [−1; 100,5] o si `pn_cartera` < $1 millón: son errores de carga de la gerente (montos en la columna de porcentaje, PN absurdo). Hay 185 inválidas sobre 17.642; se marcan, no se corrigen.

Disponibilidades son saldos a la vista, en un único número sin apertura por banco. La sociedad depositaria es el custodio, no necesariamente el banco donde está la vista.

### 3.5 `panel_fondo_semana` (base de análisis)

Semana con cierre el viernes (`W-FRI`). De la planilla: `pn` del último día con dato, `flujo` sumado, `tna_bruta` promediada por días, `fee_medio` del último día, `n_dias`, `ultima_fecha`. Se le pega la cartera de esa semana por `cod_cnv` vía el crosswalk (sólo filas con `revisado = 1`). Controles: `tiene_cartera` (95,8% de las filas) y `pn_ratio` = PN planilla / PN cartera, con mediana 1,000 y p1 a p99 de 0,97 a 1,02. La versión `.dta` tiene las 38 variables etiquetadas.

## 4. Crosswalks

`Data/crosswalks/fondos_cnv_lista.csv`: los 1.702 fondos del selector de la CNV con su `lfc`.

`Data/crosswalks/fondos_cnv_lfc.csv`: `cod_cnv` ↔ `lfc` para los 82 fondos money market, propuesto por similitud de nombre (`fondoscnv.proponer_crosswalk`) y revisado a mano (`revisado = 1` en las 82). Casos resueltos a mano: Lombard Ahorro es 63301 (63300 es un fondo cerrado en 2005); Mercado Fondo es 63968. Los cambios de nombre de un mismo `lfc` son renombres (Goal Pesos a Pionero Pesos Plus II, Quinquela a MEGAQM, IEB Ahorro a Ciclo Nova Ahorro, MAF Liquidez a Transatlántica) salvo las conversiones de la sección 2.

## 5. Datos que no son públicos

Apertura de las disponibilidades por banco, convenios de colocación con agentes (art. 28, Título V, Cap. I de las Normas CNV), informe mensual del colocador por fondo (RG 1089/2025), suscripciones y rescates brutos y cuotapartistas por tipo de inversor. Ver `Methodological_Notes/A_fondos_encajes/pedido_cnv_fci.md`.
