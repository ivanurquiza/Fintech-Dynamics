# Diccionario de variables de CENDEU

Versión de trabajo: 13 de septiembre de 2026. Describe las **nueve bases locales** de `Data/processed/cendeu/`, contrastando todos sus nombres y tipos con los esquemas parquet y sus transformaciones con el código. No reproduce datos personales.

Las definiciones económicas provienen de la documentación del proyecto y de los constructores; **no reemplazan el diccionario oficial del BCRA**. Las categorías que requieren cotejo con los LEAME originales se señalan expresamente. Las llaves indicadas son candidatas por diseño, no una auditoría exhaustiva de unicidad.

## Convenciones comunes

- Montos `_ars`: pesos nominales. El origen informa miles con un decimal; el parser elimina la coma y multiplica por 100. Ejemplo ficticio: `238,0` → 238.000 pesos. No son miles ni valores deflactados.
- Bloque `00`: julio de 2026; `23`: agosto de 2024. Un número de bloque mayor corresponde a un mes anterior.
- `ym` de estos parquet usa `año*12+mes-1`, distinto del índice Stata. Julio de 2026: 24318 en CENDEU, 798 en Stata.
- Situación: se conserva el código original. `npl` es una definición analítica del proyecto ({3,4,5}), no atraso positivo ni toda situación distinta de 1. El código 11 no debe ordenarse como más riesgoso que 5.
- En derivados se mantienen ceros desde la primera actividad observada de cada relación. No prueban cancelación económica: pueden intervenir umbrales, omisiones y rezagos.
- Los parsers del panel, padrón y rectificativas convierten algunos campos vacíos/no numéricos a cero; el corte construido con DuckDB puede conservar nulos por conversión fallida. Cero y faltante no son equivalentes.
- La muestra de personas usa `abs(hash(cuit)) % 100 < 5` en DuckDB; documentar la versión de DuckDB si se requiere reproducir exactamente la selección.
- El padrón es un corte, no un historial de domicilio o actividad. En el parser usado se descarta el nombre de la persona.

## Inventario

| Base | Unidad | Filas según metadatos | Variables |
|---|---|---:|---:|
| `deudores.parquet` | Deudor × entidad × período informado | 41,055,396 | 24 |
| `panel24_wide.parquet` | Deudor × entidad; 24 bloques mensuales | 59,292,141 | 75 |
| `normal_since.parquet` | Deudor | 14,675,514 | 3 |
| `padron.parquet` | Registro del padrón | 65,386,335 | 9 |
| `rectifications.parquet` | Rectificación de deudor × entidad × período | 1,727,160 | 6 |
| `firm` | Empresa × entidad × mes | 14,335,169 | 10 |
| `person_lender_5pct` | Persona × entidad × mes; muestra por hash de CUIT | 54,958,697 | 10 |
| `person_month` | Persona × mes, agregado entre acreedores | 521,598,419 | 10 |
| `lender_month` | Entidad × mes × tipo de deudor | 18,804 | 11 |

## deudores.parquet

**Unidad:** Deudor × entidad × período informado. **Cobertura:** Corte descargado en julio de 2026; incluye períodos rezagados.

**Llave candidata:** `ent, id_type, cuit, period`.

| Variable | Tipo físico | Definición / regla / advertencia |
|---|---|---|
| `ent` | `int32` | Código de entidad acreedora del BCRA; enlace con balances y cendeu_lenders.csv. |
| `period` | `int32` | Período informado, entero AAAAMM; puede diferir del mes de descarga por rezagos. |
| `id_type` | `int32` | Código original de tipo de identificación. Catálogo de valores pendiente de cotejo con LEAME del BCRA. |
| `cuit` | `string` | Identificador del deudor conservado como texto; llave de enlace, no variable económica. |
| `activity` | `int32` | Actividad informada por el acreedor, campo original de 3 posiciones; no equiparar al código ARCA del padrón. |
| `status` | `int32` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. |
| `loans_ars` | `int64` | Financiaciones informadas en el corte mensual; pesos nominales. Es saldo, no originación. |
| `unused_ars` | `int64` | Concepto original de asistencia no utilizada, en pesos nominales; cotejar alcance del campo antes de interpretarlo como límite disponible. |
| `guarantees_given_ars` | `int64` | Garantías otorgadas, importe en pesos nominales. |
| `other_items_ars` | `int64` | Otros conceptos informados, importe en pesos nominales; alcance detallado pendiente del catálogo original. |
| `pref_guar_a_ars` | `int64` | Importe con garantías preferidas A, pesos nominales. |
| `pref_guar_b_ars` | `int64` | Importe con garantías preferidas B, pesos nominales. |
| `no_pref_guar_ars` | `int64` | Importe sin garantías preferidas, pesos nominales. |
| `counter_guar_a_ars` | `int64` | Concepto de contragarantías A, pesos nominales; alcance regulatorio pendiente de cotejo. |
| `counter_guar_b_ars` | `int64` | Concepto de contragarantías B, pesos nominales; alcance regulatorio pendiente de cotejo. |
| `no_counter_guar_ars` | `int64` | Concepto sin contragarantías, pesos nominales; alcance regulatorio pendiente de cotejo. |
| `provisions_ars` | `int64` | Previsiones, pesos nominales. El notebook reporta ceros en todo el corte; no interpretar como ausencia real de previsiones sin validar fuente y parser. |
| `covered` | `int32` | Código original de deuda cubierta. Esquema de codificación pendiente; no asumir que todo valor no nulo significa sí. |
| `legal_review` | `int32` | Código original de proceso judicial o información en revisión; categorías pendientes de cotejo. |
| `refinanced` | `int32` | Código original de refinanciación; categorías pendientes de cotejo. |
| `forced_reclass` | `int32` | Código original de recategorización obligatoria; categorías pendientes de cotejo. |
| `legal_status` | `int32` | Código original de situación jurídica; categorías pendientes de cotejo. |
| `uncollectible` | `int32` | Código original de irrecuperabilidad por disposición técnica; categorías pendientes de cotejo. |
| `days_past_due` | `int32` | Días de atraso informados en el corte; no disponible como serie de 24 meses. |

## panel24_wide.parquet

**Unidad:** Deudor × entidad; 24 bloques mensuales. **Cobertura:** Agosto de 2024 a julio de 2026.

**Llave candidata:** `ent, id_type, cuit`.

| Variable | Tipo físico | Definición / regla / advertencia |
|---|---|---|
| `ent` | `int32` | Código de entidad acreedora del BCRA; enlace con balances y cendeu_lenders.csv. |
| `id_type` | `int8` | Código original de tipo de identificación. Catálogo de valores pendiente de cotejo con LEAME del BCRA. |
| `cuit` | `string` | Identificador del deudor conservado como texto; llave de enlace, no variable económica. |
| `status_00` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. Mes: 2026-07 (rezago 0). |
| `amount_00_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. Mes: 2026-07 (rezago 0). |
| `legal_00` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. Mes: 2026-07 (rezago 0). |
| `status_01` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. Mes: 2026-06 (rezago 1). |
| `amount_01_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. Mes: 2026-06 (rezago 1). |
| `legal_01` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. Mes: 2026-06 (rezago 1). |
| `status_02` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. Mes: 2026-05 (rezago 2). |
| `amount_02_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. Mes: 2026-05 (rezago 2). |
| `legal_02` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. Mes: 2026-05 (rezago 2). |
| `status_03` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. Mes: 2026-04 (rezago 3). |
| `amount_03_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. Mes: 2026-04 (rezago 3). |
| `legal_03` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. Mes: 2026-04 (rezago 3). |
| `status_04` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. Mes: 2026-03 (rezago 4). |
| `amount_04_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. Mes: 2026-03 (rezago 4). |
| `legal_04` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. Mes: 2026-03 (rezago 4). |
| `status_05` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. Mes: 2026-02 (rezago 5). |
| `amount_05_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. Mes: 2026-02 (rezago 5). |
| `legal_05` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. Mes: 2026-02 (rezago 5). |
| `status_06` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. Mes: 2026-01 (rezago 6). |
| `amount_06_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. Mes: 2026-01 (rezago 6). |
| `legal_06` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. Mes: 2026-01 (rezago 6). |
| `status_07` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. Mes: 2025-12 (rezago 7). |
| `amount_07_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. Mes: 2025-12 (rezago 7). |
| `legal_07` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. Mes: 2025-12 (rezago 7). |
| `status_08` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. Mes: 2025-11 (rezago 8). |
| `amount_08_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. Mes: 2025-11 (rezago 8). |
| `legal_08` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. Mes: 2025-11 (rezago 8). |
| `status_09` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. Mes: 2025-10 (rezago 9). |
| `amount_09_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. Mes: 2025-10 (rezago 9). |
| `legal_09` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. Mes: 2025-10 (rezago 9). |
| `status_10` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. Mes: 2025-09 (rezago 10). |
| `amount_10_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. Mes: 2025-09 (rezago 10). |
| `legal_10` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. Mes: 2025-09 (rezago 10). |
| `status_11` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. Mes: 2025-08 (rezago 11). |
| `amount_11_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. Mes: 2025-08 (rezago 11). |
| `legal_11` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. Mes: 2025-08 (rezago 11). |
| `status_12` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. Mes: 2025-07 (rezago 12). |
| `amount_12_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. Mes: 2025-07 (rezago 12). |
| `legal_12` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. Mes: 2025-07 (rezago 12). |
| `status_13` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. Mes: 2025-06 (rezago 13). |
| `amount_13_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. Mes: 2025-06 (rezago 13). |
| `legal_13` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. Mes: 2025-06 (rezago 13). |
| `status_14` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. Mes: 2025-05 (rezago 14). |
| `amount_14_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. Mes: 2025-05 (rezago 14). |
| `legal_14` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. Mes: 2025-05 (rezago 14). |
| `status_15` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. Mes: 2025-04 (rezago 15). |
| `amount_15_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. Mes: 2025-04 (rezago 15). |
| `legal_15` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. Mes: 2025-04 (rezago 15). |
| `status_16` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. Mes: 2025-03 (rezago 16). |
| `amount_16_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. Mes: 2025-03 (rezago 16). |
| `legal_16` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. Mes: 2025-03 (rezago 16). |
| `status_17` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. Mes: 2025-02 (rezago 17). |
| `amount_17_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. Mes: 2025-02 (rezago 17). |
| `legal_17` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. Mes: 2025-02 (rezago 17). |
| `status_18` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. Mes: 2025-01 (rezago 18). |
| `amount_18_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. Mes: 2025-01 (rezago 18). |
| `legal_18` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. Mes: 2025-01 (rezago 18). |
| `status_19` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. Mes: 2024-12 (rezago 19). |
| `amount_19_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. Mes: 2024-12 (rezago 19). |
| `legal_19` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. Mes: 2024-12 (rezago 19). |
| `status_20` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. Mes: 2024-11 (rezago 20). |
| `amount_20_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. Mes: 2024-11 (rezago 20). |
| `legal_20` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. Mes: 2024-11 (rezago 20). |
| `status_21` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. Mes: 2024-10 (rezago 21). |
| `amount_21_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. Mes: 2024-10 (rezago 21). |
| `legal_21` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. Mes: 2024-10 (rezago 21). |
| `status_22` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. Mes: 2024-09 (rezago 22). |
| `amount_22_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. Mes: 2024-09 (rezago 22). |
| `legal_22` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. Mes: 2024-09 (rezago 22). |
| `status_23` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. Mes: 2024-08 (rezago 23). |
| `amount_23_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. Mes: 2024-08 (rezago 23). |
| `legal_23` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. Mes: 2024-08 (rezago 23). |

## normal_since.parquet

**Unidad:** Deudor. **Cobertura:** Corte julio de 2026; antigüedad histórica en normalidad.

**Llave candidata:** `id_type, cuit`.

| Variable | Tipo físico | Definición / regla / advertencia |
|---|---|---|
| `id_type` | `int32` | Código original de tipo de identificación. Catálogo de valores pendiente de cotejo con LEAME del BCRA. |
| `cuit` | `string` | Identificador del deudor conservado como texto; llave de enlace, no variable económica. |
| `normal_since` | `int32` | Mes AAAAMM desde el cual el deudor permanece en situación normal en todas sus entidades, según archivo 1DSF; no es fecha del primer crédito. |

## padron.parquet

**Unidad:** Registro del padrón. **Cobertura:** Corte 31 de julio de 2026.

**Llave candidata:** `cuit`.

| Variable | Tipo físico | Definición / regla / advertencia |
|---|---|---|
| `cuit` | `string` | Identificador del deudor conservado como texto; llave de enlace, no variable económica. |
| `activity` | `int32` | Código de actividad ARCA del padrón, campo de 6 posiciones; no equiparar al campo activity del corte de deudores. |
| `dropped` | `string` | Código de baja del padrón, conservado como texto; catálogo pendiente. |
| `cuit_replacement` | `string` | Identificador de reemplazo informado por el padrón; conservar como texto. |
| `birth_date` | `string` | Fecha de nacimiento almacenada como texto, esperada AAAA-MM-DD. 1901-01-01 está documentado como centinela; excluirlo de cálculos de edad. |
| `sex` | `string` | Código de sexo en el padrón; no inferir ni completar categorías no documentadas. |
| `zip` | `string` | Código postal del padrón, texto. No equivale a departamento INDEC ni necesariamente a ubicación económica actual. |
| `province` | `int32` | Código provincial ARCA. Enlace con provincias_arca_indec.csv; no unir directamente a códigos INDEC. |
| `death_date` | `string` | Fecha de fallecimiento almacenada como texto, esperada AAAAMMDD; vacío y 19010101 son centinelas documentados. |

## rectifications.parquet

**Unidad:** Rectificación de deudor × entidad × período. **Cobertura:** Períodos históricos; ver period.

**Llave candidata:** `ent, cuit, period (puede requerir depuración de rectificaciones repetidas)`.

| Variable | Tipo físico | Definición / regla / advertencia |
|---|---|---|
| `ent` | `int32` | Código de entidad acreedora del BCRA; enlace con balances y cendeu_lenders.csv. |
| `period` | `int32` | Período informado, entero AAAAMM; puede diferir del mes de descarga por rezagos. |
| `id_type` | `int32` | Código original de tipo de identificación. Catálogo de valores pendiente de cotejo con LEAME del BCRA. |
| `cuit` | `string` | Identificador del deudor conservado como texto; llave de enlace, no variable económica. |
| `status` | `int32` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. |
| `amount_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. |

## firm

**Unidad:** Empresa × entidad × mes. **Cobertura:** Agosto de 2024 a julio de 2026.

**Llave candidata:** `ent, cuit, ym`.

| Variable | Tipo físico | Definición / regla / advertencia |
|---|---|---|
| `ent` | `int32` | Código de entidad acreedora del BCRA; enlace con balances y cendeu_lenders.csv. |
| `cuit` | `string` | Identificador del deudor conservado como texto; llave de enlace, no variable económica. |
| `ym` | `int32` | Índice mensual del constructor: year*12 + month - 1. Restar 23520 para convertir a índice mensual Stata. |
| `year` | `int32` | Año calendario derivado del bloque del panel. |
| `month` | `int32` | Mes calendario, de 1 a 12, derivado del bloque del panel. |
| `status` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. |
| `amount_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. |
| `legal` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. |
| `active` | `int32` | Variable derivada: 1 si status > 0 o amount_ars > 0; 0 en caso contrario. Actividad registral, no necesariamente saldo positivo. |
| `npl` | `int32` | Variable derivada: 1 si status pertenece a {3,4,5}; 0 en otro caso. En person_month es el máximo entre acreedores. |

## person_lender_5pct

**Unidad:** Persona × entidad × mes; muestra por hash de CUIT. **Cobertura:** Agosto de 2024 a julio de 2026.

**Llave candidata:** `ent, cuit, ym`.

| Variable | Tipo físico | Definición / regla / advertencia |
|---|---|---|
| `ent` | `int32` | Código de entidad acreedora del BCRA; enlace con balances y cendeu_lenders.csv. |
| `cuit` | `string` | Identificador del deudor conservado como texto; llave de enlace, no variable económica. |
| `ym` | `int32` | Índice mensual del constructor: year*12 + month - 1. Restar 23520 para convertir a índice mensual Stata. |
| `year` | `int32` | Año calendario derivado del bloque del panel. |
| `month` | `int32` | Mes calendario, de 1 a 12, derivado del bloque del panel. |
| `status` | `int8` | Situación crediticia original. El proyecto clasifica como irregular los códigos 3, 4 y 5; conservar otros códigos por separado. |
| `amount_ars` | `int64` | Saldo de la relación en pesos nominales. En rectificaciones es el monto rectificado; no sumar las rectificaciones al saldo original. |
| `legal` | `int8` | Código original legal del bloque mensual; no está recodificado a indicador binario por el constructor. |
| `active` | `int32` | Variable derivada: 1 si status > 0 o amount_ars > 0; 0 en caso contrario. Actividad registral, no necesariamente saldo positivo. |
| `npl` | `int32` | Variable derivada: 1 si status pertenece a {3,4,5}; 0 en otro caso. En person_month es el máximo entre acreedores. |

## person_month

**Unidad:** Persona × mes, agregado entre acreedores. **Cobertura:** Agosto de 2024 a julio de 2026.

**Llave candidata:** `cuit, ym`.

| Variable | Tipo físico | Definición / regla / advertencia |
|---|---|---|
| `cuit` | `string` | Identificador del deudor conservado como texto; llave de enlace, no variable económica. |
| `ym` | `int32` | Índice mensual del constructor: year*12 + month - 1. Restar 23520 para convertir a índice mensual Stata. |
| `year` | `int32` | Año calendario derivado del bloque del panel. |
| `month` | `int32` | Mes calendario, de 1 a 12, derivado del bloque del panel. |
| `n_lenders` | `double` | Suma de active entre acreedores de una persona y mes; tipo físico double aunque representa un conteo. |
| `n_relationships` | `int64` | Cantidad de relaciones conservadas para persona–mes, incluyendo canceladas después de su primera actividad. |
| `debt_ars` | `double` | Suma de los saldos entre acreedores de una persona y mes, pesos nominales. |
| `npl_ars` | `double` | Suma de amount_ars solo en relaciones con npl=1, pesos nominales. |
| `worst_status` | `int8` | Máximo NUMÉRICO de status entre acreedores. No equivale siempre a peor riesgo: códigos especiales como 11 requieren tratamiento explícito. |
| `npl` | `int32` | Variable derivada: 1 si status pertenece a {3,4,5}; 0 en otro caso. En person_month es el máximo entre acreedores. |

## lender_month

**Unidad:** Entidad × mes × tipo de deudor. **Cobertura:** Agosto de 2024 a julio de 2026.

**Llave candidata:** `ent, ym, borrower_type`.

| Variable | Tipo físico | Definición / regla / advertencia |
|---|---|---|
| `ent` | `int32` | Código de entidad acreedora del BCRA; enlace con balances y cendeu_lenders.csv. |
| `ym` | `int32` | Índice mensual del constructor: year*12 + month - 1. Restar 23520 para convertir a índice mensual Stata. |
| `year` | `int32` | Año calendario derivado del bloque del panel. |
| `month` | `int32` | Mes calendario, de 1 a 12, derivado del bloque del panel. |
| `borrower_type` | `string` | Tipo derivado del prefijo de CUIT: person (20,23,24,27), firm (30,33,34), other (resto). |
| `borrowers` | `double` | Suma de active por entidad, mes y tipo. Cuenta relaciones activas; coincide con deudores únicos solo si deudor–entidad no tiene duplicados. |
| `relationships` | `int64` | Cantidad de filas de relaciones conservadas, activas o canceladas después de su primera actividad. |
| `npl_borrowers` | `double` | Suma del indicador npl por entidad, mes y tipo; conteo de relaciones irregulares, sujeto a unicidad de la llave. |
| `credit_ars` | `double` | Suma de amount_ars por entidad, mes y tipo, en pesos nominales. |
| `npl_ars` | `double` | Suma de amount_ars solo en relaciones con npl=1, pesos nominales. |
| `legal_cases` | `double` | Suma del código legal original. No interpretar automáticamente como cantidad de casos hasta verificar que sus valores sean binarios. |

## Variables que esta fuente no permite seguir

El panel de 24 meses no contiene tasa contractual, plazo, monto originado, destino, solicitudes rechazadas ni límite disponible histórico. Días de atraso, refinanciación y garantías se observan en el corte detallado, no como serie equivalente. Primera aparición en la ventana no significa primer crédito de la vida.

## Fuentes de la documentación

- [Documentación de bases](cendeu_bases.pdf).
- [Parser del corte mensual](../../Code/build/cendeu_build.py).
- [Parser del panel de 24 meses](../../Code/build/cendeu_build_panel.py).
- [Parser del padrón y rectificativas](../../Code/build/cendeu_build_text.py).
- [Construcción de derivados](../../Code/build/cendeu_reshape.py).
- [Correspondencia de acreedores](../crosswalks/cendeu_lenders.csv).
- [Correspondencia provincial](../crosswalks/provincias_arca_indec.csv).

