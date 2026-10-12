# Análisis

Cada archivo resuelve la raíz del repo por su cuenta y escribe en `Code/output/`. Ninguno guarda microdato identificado.

## Por línea

| Línea | Archivo | Qué hace | Insumos |
|---|---|---|---|
| A. Pasivo bancario y fondos | `summ_stats.do` | Tablas y figuras descriptivas de depósitos por instrumento, partidas 311723 y 311724 | `balances_bancos.dta`, `ipc.dta` |
| A | `motivacion_provincial.do` | Adopción provincial de billeteras y su dispersión; panel banco × provincia | `inclusion_prov.dta`, `prestamos_depositos_prov.dta` |
| A | `mapa_adopcion.py` | Mapa provincial de adopción (personas sólo con CVU sobre personas con cuenta) | `inclusion_prov.dta`, `Data/raw/geo/` |
| A | `shock_depositos.ipynb` | Exposición de bancos a la adopción, terciles, regresiones simples alrededor del QR interoperable (nov-2021) y pull (sep-2022) | balances, `prestamos_depositos_prov.dta` |
| A | `presentacion_avances.ipynb` | Figuras de la presentación de avances (serie 311724 con la escalera de encajes, mapa) | balances, inclusión |
| B. Liquidez y sustitución | `liquidez_fintech/` | Notebooks 01, 03, 05 y 06 sobre CENDEU, con README propio | CENDEU, balances |
| B | `audit_identificacion_2026-09-20.ipynb` | Cobertura y superposición de acreedores para el cruce con CENDEU | CENDEU |
| C. Orden de repago | `pecking_order/` | Notebook 01, `po.py` y el diagnóstico de edad jubilatoria, con README propio | muestra 5% de CENDEU, padrón |
| CENDEU, general | `cendeu_explore.ipynb` | Primera mirada a las bases de la Central | CENDEU |
| CENDEU, general | `cendeu_summ_stats.ipynb` | Estadísticas descriptivas del universo, personas y empresas | `panel24_wide.parquet` |

Los fondos (línea A) todavía no tienen carpeta de análisis: la primera tabla descriptiva está al final de `Code/build/FondosCNV/03_paneles_y_merge.ipynb`.

## Salidas

`Code/output/figuras` y `Code/output/tablas` para los archivos sueltos; `Code/output/liquidez_fintech` y `Code/output/pecking_order` para las carpetas. `Code/output/tmp/` está fuera de git.
