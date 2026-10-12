# Línea A. Fondos money market, encajes y fondeo bancario

## Pregunta

Qué pasa con el fondeo de los bancos cuando el regulador cambia el encaje sobre la vista remunerada de los fondos money market. El encaje sobre ese pasivo, creado en 0% en abril de 2020 (A 6992), pasó a 10% (A 7988, 15-abr-2024), 15% (A 8000, may-2024), 20% (A 8119, nov-2024) y 40% (A 8281 y A 8289, 1-ago-2025). Entre septiembre y noviembre de 2025 rigió además el adicional general de 3,5 pp (A 8306); A 8355 lo dejó sin efecto el 1-dic-2025 y la alícuota volvió a 40%, donde sigue. La pregunta es cómo reasignan su cartera los fondos (vista, plazo fijo, caución, títulos), a qué costo para el banco y qué rendimiento llega al cuotapartista.

## Datos

- `Data/processed/FondosCNV/panel_fondo_semana.dta`: fondo × semana, 82 fondos, ene-2020 a sep-2026. Flujos, PN, TNA bruta, honorarios y composición de cartera. Diccionario en `Data/docs/diccionario_fondoscnv.md`.
- `Data/processed/balances_bancos.dta`: lado del banco (partida 311724, plazo fijo, tasa implícita en `caracteristicas_bancos`).
- `Regulation/cronologia_normativa.csv`: fechas y alícuotas.

## Código

`Code/build/FondosCNV/` (notebooks 01 a 03). Del lado bancario: `Code/analysis/shock_depositos.ipynb`, `summ_stats.do`, `presentacion_avances.ipynb`.

## Estado

Base completa y validada al 30-sep-2026. Primera mirada (participación en el PN del total money market, ponderada):

| | Vista | Plazo fijo | Caución |
|---|---:|---:|---:|
| 2023Q4 | 69,3 | 22,3 | 5,0 |
| 2024Q2 (encaje 10 a 15%) | 41,7 | 39,8 | 16,0 |
| 2024Q4 (20%) | 32,3 | 49,8 | 12,0 |
| 2025Q3 (30 a 40%) | 32,4 | 39,6 | 19,2 |
| 2025Q4 (40%, sin el adicional) | 30,8 | 41,1 | 22,2 |
| 2026Q2 | 23,8 | 59,0 | 11,9 |

La vista cae unos 27 puntos en el semestre del primer encaje y sigue cayendo con el encaje en 40%. Una versión anterior de las notas leía la caída de 2026 como persistencia tras la eliminación del encaje; es un error: A 8355 sólo eliminó el adicional de 3,5 pp. Es descriptivo: en el mismo período cambian la LEFI, las tasas y la curva.

## Discusión de diseño

Dos cosas a tener presentes, de `comun/revision_integral_2026-09-28.md` §4. Un panel banco × instrumento × mes con efecto fijo banco × mes identifica la alícuota sólo por variación instrumento-tiempo, igual para todos los bancos: el número efectivo de experimentos es el de cambios normativos. La variación útil es la incidencia diferencial entre bancos (composición previa fija por alícuota). En el panel fondo × banco, el efecto fijo fondo × tiempo absorbe la oferta de fondeo y lo que queda es la demanda del banco; el regresor tiene que desplazar al banco (encaje, liquidez), no la tasa que paga. Amenazas: afiliación gerente-banco, topes de concentración por entidad y fondos que persiguen tasa.

## Pendiente

Crosswalk de contrapartes de plazo fijo a código BCRA (habilita el panel fondo × banco); reglamentos de gestión para tipificar clases; 24 carteras cortadas. Notas: `integracion_psp_money_market.md` (propuesta: billeteras, integración vertical y costo de fondeo de los money market), `fuentes_fci.md`, `pedido_cnv_fci.md`.
