# Notas de revisión de datos

Estado al 12-oct-2026. Lo corregido queda registrado abajo para no volver a revisarlo; lo pendiente son chequeos cortos antes de usar cada base en una tabla del paper.

## Pendiente

**Balances (`balances_bancos.dta`)**

- [ ] Volver a correr `build_dta.do`. La base es del 19-ago y el do del 22-sep: faltan `tit_ars_tot`, `lefi`, `leliq`, `pases_bcra`, `liq_publica` y sus etiquetas (ver `nota_lefi_leliq.md`). Después, `documentar_bases.py`.
- [ ] `dep_pf_total` incluye las inversiones precancelables. Para plazo fijo puro usar los componentes.
- [ ] Unidades: los saldos están en miles de pesos (depósitos del sistema en abr-2026 = 206,7 billones). Dejarlo escrito en las notas de cada tabla.
- [ ] `dep_fci_proxy` es sólo la partida 311724. No es "depósitos de FCI": la vista de los FCI se reparte entre varias partidas (contraste con las series 1030 y 1063 de la API del BCRA, la cuenta corriente de FCI va de 0,87 a 0,40 veces la 311724 entre 2021 y 2023).

**Características (`caracteristicas_bancos.dta`)**

- [ ] Hay valores extremos en `indicad` aun sin el centinela (máximo 1,08e9). Recortar por indicador antes de promediar.
- [ ] Pesa 80 MB, cerca del límite de 100 MB de GitHub. Si crece, pasarla a parquet fuera de git.

**Puntos de acceso (`pda_*`)**

- [ ] `pda_lender_depto` identifica la entidad por nombre, no por código BCRA. Falta el cruce a `ent`. Pesa 77 MB.
- [ ] El paso de código postal del padrón a departamento INDEC sigue sin tabla.

**CENDEU (`Data/processed/cendeu/`)**

- [ ] El umbral de $25.000 para informar deudores identificados es nominal y no se indexa: parte del crecimiento en cantidad de deudores es entrada mecánica.
- [ ] El `24DSF` excluye a los deudores irregulares de entidades dadas de baja, también hacia atrás. Acotar comparando el corte mensual con la columna del mismo mes del panel.
- [ ] `refinanced` y `days_past_due` no son confiables para proveedores no financieros. Los códigos de `covered`, `legal_review`, `forced_reclass` y `legal_status` siguen sin cotejar con el LEAME.
- [ ] Rectificaciones: no sumar `rectifications` a los saldos originales. Fechar cada descarga; dos descargas del mismo mes no son el mismo dato.
- [ ] La muestra del 5% depende de la función de hash de DuckDB. Registrar la versión.

**FondosCNV**

- [ ] 24 pedidos de cartera quedaron cortados por tiempo. Volver a pedirlos (`estado = error` en `manifest_carteras.csv`).
- [ ] 185 carteras con `cartera_valida = 0`. Ver si alguna se puede recuperar a mano o descartarlas.
- [ ] Disponibilidades no se abren por banco. La depositaria no es el banco de la vista.
- [ ] Contrapartes de plazo fijo y caución en texto libre de la gerente. Falta el crosswalk a código de entidad BCRA.
- [ ] `tipo_clase_cuota` (minorista, mayorista, general) sólo está en dos días. Para el resto, reglamentos de gestión.
- [ ] Mercado Fondo antes del 19-feb-2020, Cohen antes de ago-2021 y Adcap IX antes de dic-2023 no son money market. Filtrar por sección y fecha.
- [ ] Los manifests por lote (`manifest_lote_*`, `manifest_carteras_b*`) son redundantes con los consolidados. Pasarlos a una subcarpeta.

**General**

- [ ] La copia `Documents/GitHub/personal/Fintech-Dynamics` está huérfana. Borrarla para que ningún script escriba ahí.
- [ ] Evaluar la inscripción de la base derivada de CENDEU en el Registro Nacional de Bases de Datos (Ley 25.326).

## Corregido

- `dep_mayorista` (missing por sumas con faltantes en Stata) se eliminó; las partidas finas se usan por separado.
- La partida 311724 está separada de las precancelables 311736/311744 (`dep_fci_proxy` y `dep_precanc`).
- Centinela 99999 de `indicad` puesto en missing.
- Resultados desacumulados (`*_flow`).
- Las bases de puntos de acceso y el panel fondo × semana tienen etiquetas de variable.
- FondosCNV: sección money market previa a sep-2021, planillas con formato `agen_10`, TNA fuera de rango y carteras mal cargadas, todos tratados en el código (ver `diccionario_fondoscnv.md`).
- Crosswalk de fondos completo (82/82), con Lombard Ahorro corregido a 63301.
- `panel_ctaesp_raw.csv`, intermedio sin uso en el código, sacado del repo.
