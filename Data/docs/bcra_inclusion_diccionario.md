# Datos de Inclusión Financiera — BCRA

**Fuente:** [Indicadores de inclusión financiera, BCRA](https://www.bcra.gob.ar/indicadores-inclusion-financiera/)
**Descarga reproducible:** `python descargar_datos_bcra.py`
**Última descarga:** 2026-07-29 (datos hasta 2025-12)

Formato común: CSV con campos entre comillas dobles, separador coma. **Ojo:** los valores numéricos
usan **coma decimal dentro de comillas** (`"28,575462"`), y la codificación original es Latin-1/Windows-1252.
En Stata: `import delimited, encoding("latin1")` y convertir coma decimal. Los nombres de provincia
cambian de grafía entre períodos (`Córdoba`/`Cordoba`, `Total`/`TOTAL`) → normalizar antes de todo
merge/append. Cada archivo incluye categorías `TOTAL` que hay que excluir de los paneles.

## 1. BCRA_deudores_SFA_total_por_provincia.txt (~100 KB, 2.700 filas)
% de población adulta con financiamiento en el Sistema Financiero Ampliado (SFA = entidades
reguladas + otros proveedores de crédito no financieros). Columnas: cd_periodo (AAAAMM),
tx_provincia (24 jurisdicciones + TOTAL), nu_valor (%). Mensual, 2017m1–2025m12.

## 2. BCRA_deudores_SFA_por_grupo_institucional_y_provincia.txt (~1,4 MB, 18.900 filas)
Ídem 1 pero desagregado por grupo institucional del acreedor: Bancos Privados; Bancos Públicos;
Compañías Financieras; EEFF (total reguladas); OPNFC (Otros Proveedores No Financieros de Crédito —
acá caen los PSP/fintech que dan crédito, p. ej. Mercado Pago); PNFC; TCNB (tarjetas no bancarias).
Mensual, 2017m1–2025m12. Los grupos NO son excluyentes a nivel persona → no sumar % entre grupos.

## 3. BCRA_deudores_SFA_por_tipo_asistencia_y_provincia.txt (~950 KB, 13.500 filas)
% de adultos con cada producto: Adelantos; Hipotecarios; Personales; Prendarios; Tarjetas de crédito.
Mensual, 2017m1–2025m12. Etiquetas con grafía inconsistente entre períodos → normalizar.

## 4. BCRA_puntos_acceso_por_tipo_y_provincia.txt (~510 KB)
Cantidad de puntos de acceso (PDA) físicos: Sucursales; Sucursales móviles; ATM; TAS (terminales de
autoservicio); ACSF (agencias complementarias/agentes); TOTAL. Mensual, 2019m1–2025m12.

## 5. BCRA_puntos_acceso_por_entidad_tipo_y_provincia.txt (~15 MB, 143.339 filas)
PDA por entidad (≈80: ~50 bancos privados, ~14 públicos, ~15 compañías financieras, + ATMs no
bancarios). Columnas: cd_periodo, tx_tipoPDA, tx_grupo, tx_entidad, tx_provincia, nu_PDA.
Mensual, 2019m1–2025m12. Permite construir la huella territorial banco-por-banco
(aperturas/cierres por provincia-mes) → variación para diseños de exposición/shift-share.

## 6. BCRA_tenencia_cuentas_bancarias_y_de_pago_por_provincia.txt (~330 KB, 4.032 filas)
Cantidad de personas humanas titulares de cuentas por tipo: Sólo cuentas bancarias (CBU); Sólo
cuentas de pago (CVU, en PSP); Ambas; Al menos una bancaria; Al menos una de pago; Al menos una.
TRIMESTRAL, 2019q1–2025q4. Es LA variable de adopción PSP vs. banca a nivel provincia:
"sólo CVU" ≈ margen extensivo de inclusión vía fintech; "ambas" ≈ multihoming. Para tasas,
dividir por población adulta proyectada (INDEC) por provincia-año.
