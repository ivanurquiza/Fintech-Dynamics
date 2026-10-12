# Diccionario de las bases en `Data/processed`

Generado por `Code/build/documentar_bases.py` a partir de los archivos. No editar a mano: si cambia una base, se vuelve a correr el script. Las bases de la Central de Deudores están en `diccionario_cendeu.md` y las de fondos, con su construcción, en `diccionario_fondoscnv.md`.

Convención de meses: en los `.dta` `ym` es el índice `%tm` de Stata (en las bases de puntos de acceso, guardado como entero sin formato). En los parquet de CENDEU es `anio*12 + mes - 1`; para pasar a `%tm` se resta 23520.

## `balances_bancos.dta`

_Balances mensuales por entidad, IEF BCRA (baldet)_

Unidad: entidad × mes. Llave: `ent, ym`. Filas: 7.681. Variables: 328. Cobertura: 2018-01 a 2026-04.

Balance de saldos (balhist/baldet del IEF), resultados, tipo de entidad e IPC. Saldos en miles de pesos nominales; sufijo `_r`: pesos de enero de 2026. `*_acum`: resultado acumulado en el ejercicio; `*_flow`: resultado del mes (desacumulado).

| Variable | Tipo | % no faltante | Descripción |
|---|---|---:|---|
| `ent` | num | 100 | Codigo de entidad BCRA |
| `ym` | fecha | 100 | Mes |
| `activo` | num | 100 | Activo total (nominal) |
| `efectivo` | num | 100 | Efectivo y depositos en bancos (nominal) |
| `titulos` | num | 100 | Titulos publicos y privados (nominal) |
| `prestamos` | num | 100 | Prestamos (total) (nominal) |
| `prest_spnf` | num | 100 | Prestamos al SPNF en pesos, capitales (nominal) |
| `prest_spnf_usd` | num | 100 | Prestamos al SPNF en moneda extranjera, capitales (nominal) |
| `otros_cred_if` | num | 100 | Otros creditos por intermediacion financiera (nominal) |
| `pasivo` | num | 100 | Pasivo total (nominal) |
| `depositos` | num | 100 | Depositos (total) (nominal) |
| `dep_ars_res` | num | 100 | Depositos en pesos de residentes (nominal) |
| `dep_spub` | num | 100 | Depositos del sector publico no financiero, pesos (nominal) |
| `dep_spub_ctacte` | num | 100 | Sector publico cuenta corriente sin interes, pesos (nominal) |
| `dep_spub_ctacte_int` | num | 100 | Sector publico cuenta corriente con interes, pesos (nominal) |
| `dep_spub_pf_t` | num | 100 | Sector publico plazo fijo transferible, pesos (nominal) |
| `dep_spub_pf_i` | num | 100 | Sector publico plazo fijo intransferible, pesos (nominal) |
| `dep_spub_precanc` | num | 100 | Sector publico inversiones precancelables, pesos (nominal) |
| `dep_spub_pf_cer` | num | 100 | Sector publico plazo fijo CER, pesos (nominal) |
| `dep_sfin` | num | 100 | Depositos del sector financiero, pesos (nominal) |
| `dep_spnf` | num | 100 | Depositos del SPNF en pesos, capitales (nominal) |
| `dep_ctacte` | num | 100 | SPNF cuenta corriente sin interes (nominal) |
| `dep_ctacte_int` | num | 100 | SPNF cuenta corriente con interes (nominal) |
| `dep_cajaahorro` | num | 100 | SPNF caja de ahorros (nominal) |
| `dep_cgu` | num | 100 | SPNF cuenta gratuita universal (nominal) |
| `dep_ctaesp_sint` | num | 100 | SPNF cta cte especial personas juridicas sin interes (nominal) |
| `dep_ctaesp_cint` | num | 100 | SPNF cta cte especial personas juridicas con interes (nominal) |
| `dep_judicial_vista` | num | 100 | SPNF depositos judiciales a la vista (nominal) |
| `dep_ctasueldo` | num | 100 | SPNF cuenta sueldo y previsional (nominal) |
| `dep_fondo_cese` | num | 100 | SPNF fondo de cese laboral trabajadores de la construccion (nominal) |
| `dep_pf_transf` | num | 100 | SPNF plazo fijo transferible (nominal) |
| `dep_precanc_t` | num | 100 | SPNF inversiones con cancelacion anticipada, transferibles (nominal) |
| `dep_pf_intransf` | num | 100 | SPNF plazo fijo intransferible (nominal) |
| `dep_inmovil` | num | 100 | SPNF saldos inmovilizados (nominal) |
| `dep_precanc_i` | num | 100 | SPNF inversiones con cancelacion anticipada, intransferibles (nominal) |
| `dep_ordenes` | num | 100 | SPNF ordenes por pagar (nominal) |
| `dep_retrib_var` | num | 100 | SPNF inversiones a plazo con retribucion variable (nominal) |
| `dep_garantia` | num | 100 | SPNF depositos en garantia (nominal) |
| `dep_judicial_pf` | num | 100 | SPNF depositos judiciales a plazo fijo (nominal) |
| `dep_otros` | num | 100 | SPNF otros depositos (nominal) |
| `dep_pf_cer_t` | num | 100 | SPNF plazo fijo transferible con CER (nominal) |
| `dep_pf_cer_i` | num | 100 | SPNF plazo fijo intransferible con CER (nominal) |
| `dep_esp_l27260` | num | 100 | SPNF cuenta especial Ley 27260, exteriorizacion 2016-17 (nominal) |
| `dep_ahorro_uva` | num | 100 | SPNF cuenta de ahorro en UVA (nominal) |
| `dep_ahorro_uvi` | num | 100 | SPNF cuenta de ahorro en UVI (nominal) |
| `dep_uva_precanc_a` | num | 100 | SPNF depositos UVA con opcion de cancelacion (311788) (nominal) |
| `dep_uva_precanc_b` | num | 100 | SPNF depositos UVA con opcion de cancelacion (311789) (nominal) |
| `dep_esp_depcanc` | num | 100 | SPNF cuenta especial de deposito y cancelacion (desde 2021) (nominal) |
| `dep_esp_titulares` | num | 100 | SPNF cuenta especial titulares con activos (desde 2022) (nominal) |
| `dep_esp_export` | num | 100 | SPNF cuenta especial para exportadores (desde 2022) (nominal) |
| `dep_esp_regular` | num | 100 | SPNF cuenta especial regularizacion de activos, blanqueo 2024 (nominal) |
| `dep_usd_res` | num | 100 | Depositos en moneda extranjera de residentes (nominal) |
| `dep_spub_usd` | num | 100 | Depositos del sector publico no financiero, moneda extranjera (nominal) |
| `dep_sfin_usd` | num | 100 | Depositos del sector financiero, moneda extranjera (nominal) |
| `dep_spnf_usd` | num | 100 | Depositos del SPNF en moneda extranjera, capitales (nominal) |
| `dep_ctacte_usd` | num | 100 | SPNF ME cuenta corriente sin interes (nominal) |
| `dep_ctacte_int_usd` | num | 100 | SPNF ME cuenta corriente con interes (nominal) |
| `dep_cajaahorro_usd` | num | 100 | SPNF ME caja de ahorros (nominal) |
| `dep_ctaesp_sint_usd` | num | 100 | SPNF ME cta cte especial PJ sin interes (nominal) |
| `dep_ctaesp_cint_usd` | num | 100 | SPNF ME cta cte especial PJ con interes (nominal) |
| `dep_judicial_vista_usd` | num | 100 | SPNF ME depositos judiciales a la vista (nominal) |
| `dep_pf_transf_usd` | num | 100 | SPNF ME plazo fijo transferible (nominal) |
| `dep_precanc_t_usd` | num | 100 | SPNF ME inversiones con cancelacion anticipada, transferibles (nominal) |
| `dep_pf_intransf_usd` | num | 100 | SPNF ME plazo fijo intransferible (nominal) |
| `dep_inmovil_usd` | num | 100 | SPNF ME saldos inmovilizados (nominal) |
| `dep_precanc_i_usd` | num | 100 | SPNF ME inversiones con cancelacion anticipada, intransferibles (nominal) |
| `dep_garantia_usd` | num | 100 | SPNF ME depositos en garantia (nominal) |
| `dep_judicial_pf_usd` | num | 100 | SPNF ME depositos judiciales a plazo fijo (nominal) |
| `dep_otros_usd` | num | 100 | SPNF ME otros depositos (nominal) |
| `dep_esp_l27260a_usd` | num | 100 | SPNF ME cuenta especial Ley 27260 art 38 inc a, exteriorizacion 2016-17 (nominal |
| `dep_esp_l27260c_usd` | num | 100 | SPNF ME cuenta especial Ley 27260 art 38 inc c, exteriorizacion 2016-17 (nominal |
| `dep_repatr_ca_usd` | num | 100 | SPNF ME caja de ahorros repatriacion de fondos (Bienes Personales) (nominal) |
| `dep_repatr_pf_usd` | num | 100 | SPNF ME plazo fijo repatriacion Bienes Personales (nominal) |
| `dep_repatr_esp_usd` | num | 100 | SPNF ME cuenta especial repatriacion de fondos RG AFIP (nominal) |
| `dep_repatr_pfesp_usd` | num | 100 | SPNF ME plazo fijo cuenta especial repatriacion (nominal) |
| `dep_repatr_aporte_usd` | num | 100 | SPNF ME cuenta especial repatriacion, aporte solidario (nominal) |
| `dep_esp_depcanc_usd` | num | 100 | SPNF ME cuenta especial de deposito y cancelacion (nominal) |
| `dep_esp_financ_usd` | num | 100 | SPNF ME cuenta especial para acreditar financiaciones (nominal) |
| `dep_esp_fomento_usd` | num | 100 | SPNF ME cuenta especial regimen de fomento (nominal) |
| `dep_esp_depcanc2_usd` | num | 100 | SPNF ME cuenta especial de deposito y cancelacion (segunda) (nominal) |
| `dep_esp_regular_usd` | num | 100 | SPNF ME cuenta especial regularizacion de activos, blanqueo 2024 (nominal) |
| `otras_oblig_if` | num | 100 | Otras obligaciones por intermediacion financiera (nominal) |
| `pn` | num | 100 | Patrimonio neto (nominal) |
| `resultados` | num | 100 | Resultados acumulados del ejercicio (positivo = ganancia) (nominal) |
| `ing_fin_acum` | num | 100 | Ingresos financieros, acumulado del ejercicio (nominal) |
| `ing_adelantos_acum` | num | 100 | Intereses ganados por adelantos, acumulado (nominal) |
| `ing_documentos_acum` | num | 100 | Intereses ganados por documentos, acumulado (nominal) |
| `ing_hipot_viv_acum` | num | 100 | Intereses ganados por hipotecarios sobre vivienda, acumulado (nominal) |
| `ing_hipot_otros_acum` | num | 100 | Intereses ganados por otros hipotecarios, acumulado (nominal) |
| `ing_prend_auto_acum` | num | 100 | Intereses ganados por prendarios automotores, acumulado (nominal) |
| `ing_prend_otros_acum` | num | 100 | Intereses ganados por otros prendarios, acumulado (nominal) |
| `ing_otros_prest_acum` | num | 100 | Intereses ganados por otros prestamos, acumulado (nominal) |
| `ing_tarjetas_acum` | num | 100 | Intereses ganados por tarjetas de credito, acumulado (nominal) |
| `ing_personales_acum` | num | 100 | Intereses ganados por prestamos personales, acumulado (nominal) |
| `ing_hipotecarios2_acum` | num | 100 | Intereses ganados por prestamos hipotecarios (NIIF), acumulado (nominal) |
| `ing_personales2_acum` | num | 100 | Intereses ganados por prestamos personales (NIIF), acumulado (nominal) |
| `egr_fin_acum` | num | 100 | Egresos financieros, acumulado del ejercicio (negativo) (nominal) |
| `egr_fin_ars_acum` | num | 100 | Egresos financieros por operaciones en pesos, acumulado (negativo) (nominal) |
| `int_otros_acum` | num | 100 | Intereses por otros depositos, pesos, acumulado (negativo) (nominal) |
| `aporte_fgd_acum` | num | 100 | Aporte al fondo de garantia de depositos, acumulado (negativo) (nominal) |
| `int_ctacte_acum` | num | 100 | Intereses por depositos en cuenta corriente, pesos, acumulado (negativo) (nomina |
| `int_cajaahorro_acum` | num | 100 | Intereses por depositos en caja de ahorros, pesos, acumulado (negativo) (nominal |
| `int_pf_acum` | num | 100 | Intereses por depositos a plazo fijo, pesos, acumulado (negativo) (nominal) |
| `int_otras_imp_acum` | num | 100 | Intereses por otras imposiciones a plazo, pesos, acumulado (negativo) (nominal) |
| `aj_pf_cer_acum` | num | 100 | Ajustes CER por plazo fijo, acumulado (negativo) (nominal) |
| `aj_ca_uva_acum` | num | 100 | Ajustes por cuenta de ahorro UVA, acumulado (negativo) (nominal) |
| `aj_ca_uvi_acum` | num | 100 | Ajustes por cuenta de ahorro UVI, acumulado (negativo) (nominal) |
| `aj_dep_uva_acum` | num | 100 | Ajustes e intereses por depositos UVA, acumulado (negativo) (nominal) |
| `int_caucion_acum` | num | 100 | Intereses por operaciones de caucion bursatil, acumulado (negativo) (nominal) |
| `egr_fin_usd_acum` | num | 100 | Egresos financieros por operaciones en ME, acumulado (negativo) (nominal) |
| `int_otros_usd_acum` | num | 100 | Intereses por otros depositos, ME, acumulado (negativo) (nominal) |
| `int_ctacte_usd_acum` | num | 100 | Intereses por depositos en cuenta corriente, ME, acumulado (negativo) (nominal) |
| `int_cajaahorro_usd_acum` | num | 100 | Intereses por depositos en caja de ahorros, ME, acumulado (negativo) (nominal) |
| `int_pf_usd_acum` | num | 100 | Intereses por depositos a plazo fijo, ME, acumulado (negativo) (nominal) |
| `int_otras_imp_usd_acum` | num | 100 | Intereses por otras imposiciones a plazo, ME, acumulado (negativo) (nominal) |
| `gastos_adm_acum` | num | 100 | Gastos de administracion, acumulado (negativo) (nominal) |
| `nombre` | texto | 100 | Nombre de la entidad |
| `dep_retrib_var_t` | num | 100 | SPNF inversiones a plazo con retribucion variable, transferibles (nominal) |
| `dep_plazo_const_t` | num | 100 | SPNF inversiones a plazo constante, transferibles (nominal) |
| `dep_plazo_const_t_usd` | num | 100 | SPNF ME inversiones a plazo constante, transferibles (nominal) |
| `ing_fin_flow` | num | 100 | Ingresos financieros, flujo mensual (nominal) |
| `ing_adelantos_flow` | num | 100 | Intereses ganados por adelantos, acumulado, flujo mensual (nominal) |
| `ing_documentos_flow` | num | 100 | Intereses ganados por documentos, acumulado, flujo mensual (nominal) |
| `ing_hipot_viv_flow` | num | 100 | Intereses ganados por hipotecarios sobre vivienda, acumulado, flujo mensual (nom |
| `ing_hipot_otros_flow` | num | 100 | Intereses ganados por otros hipotecarios, acumulado, flujo mensual (nominal) |
| `ing_prend_auto_flow` | num | 100 | Intereses ganados por prendarios automotores, acumulado, flujo mensual (nominal) |
| `ing_prend_otros_flow` | num | 100 | Intereses ganados por otros prendarios, acumulado, flujo mensual (nominal) |
| `ing_otros_prest_flow` | num | 100 | Intereses ganados por otros prestamos, acumulado, flujo mensual (nominal) |
| `ing_tarjetas_flow` | num | 100 | Intereses ganados por tarjetas de credito, acumulado, flujo mensual (nominal) |
| `ing_personales_flow` | num | 100 | Intereses ganados por prestamos personales, acumulado, flujo mensual (nominal) |
| `ing_hipotecarios2_flow` | num | 100 | Intereses ganados por prestamos hipotecarios (NIIF), acumulado, flujo mensual (n |
| `ing_personales2_flow` | num | 100 | Intereses ganados por prestamos personales (NIIF), acumulado, flujo mensual (nom |
| `egr_fin_flow` | num | 100 | Egresos financieros, flujo mensual (nominal) |
| `egr_fin_ars_flow` | num | 100 | Egresos financieros por operaciones en pesos, flujo mensual (nominal) |
| `int_otros_flow` | num | 100 | Intereses por otros depositos, pesos, flujo mensual (nominal) |
| `aporte_fgd_flow` | num | 100 | Aporte al fondo de garantia de depositos, flujo mensual (nominal) |
| `int_ctacte_flow` | num | 100 | Intereses por depositos en cuenta corriente, pesos, flujo mensual (nominal) |
| `int_cajaahorro_flow` | num | 100 | Intereses por depositos en caja de ahorros, pesos, flujo mensual (nominal) |
| `int_pf_flow` | num | 100 | Intereses por depositos a plazo fijo, pesos, flujo mensual (nominal) |
| `int_otras_imp_flow` | num | 100 | Intereses por otras imposiciones a plazo, pesos, flujo mensual (nominal) |
| `aj_pf_cer_flow` | num | 100 | Ajustes CER por plazo fijo, flujo mensual (nominal) |
| `aj_ca_uva_flow` | num | 100 | Ajustes por cuenta de ahorro UVA, flujo mensual (nominal) |
| `aj_ca_uvi_flow` | num | 100 | Ajustes por cuenta de ahorro UVI, flujo mensual (nominal) |
| `aj_dep_uva_flow` | num | 100 | Ajustes e intereses por depositos UVA, flujo mensual (nominal) |
| `int_caucion_flow` | num | 100 | Intereses por operaciones de caucion bursatil, flujo mensual (nominal) |
| `egr_fin_usd_flow` | num | 100 | Egresos financieros por operaciones en ME, flujo mensual (nominal) |
| `int_otros_usd_flow` | num | 100 | Intereses por otros depositos, ME, flujo mensual (nominal) |
| `int_ctacte_usd_flow` | num | 100 | Intereses por depositos en cuenta corriente, ME, flujo mensual (nominal) |
| `int_cajaahorro_usd_flow` | num | 100 | Intereses por depositos en caja de ahorros, ME, flujo mensual (nominal) |
| `int_pf_usd_flow` | num | 100 | Intereses por depositos a plazo fijo, ME, flujo mensual (nominal) |
| `int_otras_imp_usd_flow` | num | 100 | Intereses por otras imposiciones a plazo, ME, flujo mensual (nominal) |
| `gastos_adm_flow` | num | 100 | Gastos de administracion, flujo mensual (nominal) |
| `int_dep_ars_flow` | num | 100 | Intereses pagados por depositos en pesos, flujo mensual (nominal) |
| `int_dep_usd_flow` | num | 100 | Intereses pagados por depositos en ME, flujo mensual (nominal) |
| `dep_vista_min` | num | 100 | SPNF vista minorista: caja de ahorro + sueldo + CGU + ahorro UVA/UVI (nominal) |
| `dep_pf_total` | num | 100 | SPNF plazo fijo total: transf + intransf + CER + precancelables + retrib variabl |
| `dep_especiales` | num | 100 | SPNF cuentas especiales (dep y canc, titulares, exportadores, blanqueos 2016 y 2 |
| `dep_fci_proxy` | num | 100 | Proxy fondeo FCI/institucional a la vista: cta esp PJ con interes (311724). Cont |
| `dep_precanc` | num | 100 | Mayorista a plazo: inversiones precancelables transferibles e intransferibles (n |
| `dep_pf_total_usd` | num | 100 | SPNF ME plazo fijo total (nominal) |
| `dep_especiales_usd` | num | 100 | SPNF ME cuentas especiales (blanqueos 2016 y 2024, repatriacion Bienes Personale |
| `es_banco` | num | 100 | Banco (AA100) |
| `banco_publico` | num | 100 | Banco publico (AA110) |
| `banco_privado` | num | 100 | Banco privado (AA120) |
| `banco_capnacional` | num | 100 | Banco local de capital nacional (AA121) |
| `banco_capextranjero` | num | 100 | Banco de capital extranjero o sucursal del exterior (AA123/AA124) |
| `cia_financiera` | num | 100 | Compania financiera (AA200) |
| `cia_fin_extranjera` | num | 100 | Compania financiera de capital extranjero (AA220) |
| `top10_privados` | num | 100 | Entre los 10 primeros bancos privados (AA910) |
| `ipc_nacional` | num | 100 | IPC nacional usado para deflactar (dic-2016=100) |
| `activo_r` | num | 100 | Activo total (pesos de 2026m1) |
| `efectivo_r` | num | 100 | Efectivo y depositos en bancos (pesos de 2026m1) |
| `titulos_r` | num | 100 | Titulos publicos y privados (pesos de 2026m1) |
| `prestamos_r` | num | 100 | Prestamos (total) (pesos de 2026m1) |
| `prest_spnf_r` | num | 100 | Prestamos al SPNF en pesos, capitales (pesos de 2026m1) |
| `prest_spnf_usd_r` | num | 100 | Prestamos al SPNF en moneda extranjera, capitales (pesos de 2026m1) |
| `otros_cred_if_r` | num | 100 | Otros creditos por intermediacion financiera (pesos de 2026m1) |
| `pasivo_r` | num | 100 | Pasivo total (pesos de 2026m1) |
| `depositos_r` | num | 100 | Depositos (total) (pesos de 2026m1) |
| `dep_ars_res_r` | num | 100 | Depositos en pesos de residentes (pesos de 2026m1) |
| `dep_spub_r` | num | 100 | Depositos del sector publico no financiero, pesos (pesos de 2026m1) |
| `dep_spub_ctacte_r` | num | 100 | Sector publico cuenta corriente sin interes, pesos (pesos de 2026m1) |
| `dep_spub_ctacte_int_r` | num | 100 | Sector publico cuenta corriente con interes, pesos (pesos de 2026m1) |
| `dep_spub_pf_t_r` | num | 100 | Sector publico plazo fijo transferible, pesos (pesos de 2026m1) |
| `dep_spub_pf_i_r` | num | 100 | Sector publico plazo fijo intransferible, pesos (pesos de 2026m1) |
| `dep_spub_precanc_r` | num | 100 | Sector publico inversiones precancelables, pesos (pesos de 2026m1) |
| `dep_spub_pf_cer_r` | num | 100 | Sector publico plazo fijo CER, pesos (pesos de 2026m1) |
| `dep_sfin_r` | num | 100 | Depositos del sector financiero, pesos (pesos de 2026m1) |
| `dep_spnf_r` | num | 100 | Depositos del SPNF en pesos, capitales (pesos de 2026m1) |
| `dep_ctacte_r` | num | 100 | SPNF cuenta corriente sin interes (pesos de 2026m1) |
| `dep_ctacte_int_r` | num | 100 | SPNF cuenta corriente con interes (pesos de 2026m1) |
| `dep_cajaahorro_r` | num | 100 | SPNF caja de ahorros (pesos de 2026m1) |
| `dep_cgu_r` | num | 100 | SPNF cuenta gratuita universal (pesos de 2026m1) |
| `dep_ctaesp_sint_r` | num | 100 | SPNF cta cte especial personas juridicas sin interes (pesos de 2026m1) |
| `dep_ctaesp_cint_r` | num | 100 | SPNF cta cte especial personas juridicas con interes (pesos de 2026m1) |
| `dep_judicial_vista_r` | num | 100 | SPNF depositos judiciales a la vista (pesos de 2026m1) |
| `dep_ctasueldo_r` | num | 100 | SPNF cuenta sueldo y previsional (pesos de 2026m1) |
| `dep_fondo_cese_r` | num | 100 | SPNF fondo de cese laboral trabajadores de la construccion (pesos de 2026m1) |
| `dep_pf_transf_r` | num | 100 | SPNF plazo fijo transferible (pesos de 2026m1) |
| `dep_precanc_t_r` | num | 100 | SPNF inversiones con cancelacion anticipada, transferibles (pesos de 2026m1) |
| `dep_pf_intransf_r` | num | 100 | SPNF plazo fijo intransferible (pesos de 2026m1) |
| `dep_inmovil_r` | num | 100 | SPNF saldos inmovilizados (pesos de 2026m1) |
| `dep_precanc_i_r` | num | 100 | SPNF inversiones con cancelacion anticipada, intransferibles (pesos de 2026m1) |
| `dep_ordenes_r` | num | 100 | SPNF ordenes por pagar (pesos de 2026m1) |
| `dep_retrib_var_r` | num | 100 | SPNF inversiones a plazo con retribucion variable (pesos de 2026m1) |
| `dep_garantia_r` | num | 100 | SPNF depositos en garantia (pesos de 2026m1) |
| `dep_judicial_pf_r` | num | 100 | SPNF depositos judiciales a plazo fijo (pesos de 2026m1) |
| `dep_otros_r` | num | 100 | SPNF otros depositos (pesos de 2026m1) |
| `dep_pf_cer_t_r` | num | 100 | SPNF plazo fijo transferible con CER (pesos de 2026m1) |
| `dep_pf_cer_i_r` | num | 100 | SPNF plazo fijo intransferible con CER (pesos de 2026m1) |
| `dep_esp_l27260_r` | num | 100 | SPNF cuenta especial Ley 27260, exteriorizacion 2016-17 (pesos de 2026m1) |
| `dep_ahorro_uva_r` | num | 100 | SPNF cuenta de ahorro en UVA (pesos de 2026m1) |
| `dep_ahorro_uvi_r` | num | 100 | SPNF cuenta de ahorro en UVI (pesos de 2026m1) |
| `dep_uva_precanc_a_r` | num | 100 | SPNF depositos UVA con opcion de cancelacion (311788) (pesos de 2026m1) |
| `dep_uva_precanc_b_r` | num | 100 | SPNF depositos UVA con opcion de cancelacion (311789) (pesos de 2026m1) |
| `dep_esp_depcanc_r` | num | 100 | SPNF cuenta especial de deposito y cancelacion (desde 2021) (pesos de 2026m1) |
| `dep_esp_titulares_r` | num | 100 | SPNF cuenta especial titulares con activos (desde 2022) (pesos de 2026m1) |
| `dep_esp_export_r` | num | 100 | SPNF cuenta especial para exportadores (desde 2022) (pesos de 2026m1) |
| `dep_esp_regular_r` | num | 100 | SPNF cuenta especial regularizacion de activos, blanqueo 2024 (pesos de 2026m1) |
| `dep_usd_res_r` | num | 100 | Depositos en moneda extranjera de residentes (pesos de 2026m1) |
| `dep_spub_usd_r` | num | 100 | Depositos del sector publico no financiero, moneda extranjera (pesos de 2026m1) |
| `dep_sfin_usd_r` | num | 100 | Depositos del sector financiero, moneda extranjera (pesos de 2026m1) |
| `dep_spnf_usd_r` | num | 100 | Depositos del SPNF en moneda extranjera, capitales (pesos de 2026m1) |
| `dep_ctacte_usd_r` | num | 100 | SPNF ME cuenta corriente sin interes (pesos de 2026m1) |
| `dep_ctacte_int_usd_r` | num | 100 | SPNF ME cuenta corriente con interes (pesos de 2026m1) |
| `dep_cajaahorro_usd_r` | num | 100 | SPNF ME caja de ahorros (pesos de 2026m1) |
| `dep_ctaesp_sint_usd_r` | num | 100 | SPNF ME cta cte especial PJ sin interes (pesos de 2026m1) |
| `dep_ctaesp_cint_usd_r` | num | 100 | SPNF ME cta cte especial PJ con interes (pesos de 2026m1) |
| `dep_judicial_vista_usd_r` | num | 100 | SPNF ME depositos judiciales a la vista (pesos de 2026m1) |
| `dep_pf_transf_usd_r` | num | 100 | SPNF ME plazo fijo transferible (pesos de 2026m1) |
| `dep_precanc_t_usd_r` | num | 100 | SPNF ME inversiones con cancelacion anticipada, transferibles (pesos de 2026m1) |
| `dep_pf_intransf_usd_r` | num | 100 | SPNF ME plazo fijo intransferible (pesos de 2026m1) |
| `dep_inmovil_usd_r` | num | 100 | SPNF ME saldos inmovilizados (pesos de 2026m1) |
| `dep_precanc_i_usd_r` | num | 100 | SPNF ME inversiones con cancelacion anticipada, intransferibles (pesos de 2026m1 |
| `dep_garantia_usd_r` | num | 100 | SPNF ME depositos en garantia (pesos de 2026m1) |
| `dep_judicial_pf_usd_r` | num | 100 | SPNF ME depositos judiciales a plazo fijo (pesos de 2026m1) |
| `dep_otros_usd_r` | num | 100 | SPNF ME otros depositos (pesos de 2026m1) |
| `dep_esp_l27260a_usd_r` | num | 100 | SPNF ME cuenta especial Ley 27260 art 38 inc a, exteriorizacion 2016-17 (pesos d |
| `dep_esp_l27260c_usd_r` | num | 100 | SPNF ME cuenta especial Ley 27260 art 38 inc c, exteriorizacion 2016-17 (pesos d |
| `dep_repatr_ca_usd_r` | num | 100 | SPNF ME caja de ahorros repatriacion de fondos (Bienes Personales) (pesos de 202 |
| `dep_repatr_pf_usd_r` | num | 100 | SPNF ME plazo fijo repatriacion Bienes Personales (pesos de 2026m1) |
| `dep_repatr_esp_usd_r` | num | 100 | SPNF ME cuenta especial repatriacion de fondos RG AFIP (pesos de 2026m1) |
| `dep_repatr_pfesp_usd_r` | num | 100 | SPNF ME plazo fijo cuenta especial repatriacion (pesos de 2026m1) |
| `dep_repatr_aporte_usd_r` | num | 100 | SPNF ME cuenta especial repatriacion, aporte solidario (pesos de 2026m1) |
| `dep_esp_depcanc_usd_r` | num | 100 | SPNF ME cuenta especial de deposito y cancelacion (pesos de 2026m1) |
| `dep_esp_financ_usd_r` | num | 100 | SPNF ME cuenta especial para acreditar financiaciones (pesos de 2026m1) |
| `dep_esp_fomento_usd_r` | num | 100 | SPNF ME cuenta especial regimen de fomento (pesos de 2026m1) |
| `dep_esp_depcanc2_usd_r` | num | 100 | SPNF ME cuenta especial de deposito y cancelacion (segunda) (pesos de 2026m1) |
| `dep_esp_regular_usd_r` | num | 100 | SPNF ME cuenta especial regularizacion de activos, blanqueo 2024 (pesos de 2026m |
| `otras_oblig_if_r` | num | 100 | Otras obligaciones por intermediacion financiera (pesos de 2026m1) |
| `pn_r` | num | 100 | Patrimonio neto (pesos de 2026m1) |
| `resultados_r` | num | 100 | Resultados acumulados del ejercicio (positivo = ganancia) (pesos de 2026m1) |
| `ing_fin_acum_r` | num | 100 | Ingresos financieros, acumulado del ejercicio (pesos de 2026m1) |
| `ing_adelantos_acum_r` | num | 100 | Intereses ganados por adelantos, acumulado (pesos de 2026m1) |
| `ing_documentos_acum_r` | num | 100 | Intereses ganados por documentos, acumulado (pesos de 2026m1) |
| `ing_hipot_viv_acum_r` | num | 100 | Intereses ganados por hipotecarios sobre vivienda, acumulado (pesos de 2026m1) |
| `ing_hipot_otros_acum_r` | num | 100 | Intereses ganados por otros hipotecarios, acumulado (pesos de 2026m1) |
| `ing_prend_auto_acum_r` | num | 100 | Intereses ganados por prendarios automotores, acumulado (pesos de 2026m1) |
| `ing_prend_otros_acum_r` | num | 100 | Intereses ganados por otros prendarios, acumulado (pesos de 2026m1) |
| `ing_otros_prest_acum_r` | num | 100 | Intereses ganados por otros prestamos, acumulado (pesos de 2026m1) |
| `ing_tarjetas_acum_r` | num | 100 | Intereses ganados por tarjetas de credito, acumulado (pesos de 2026m1) |
| `ing_personales_acum_r` | num | 100 | Intereses ganados por prestamos personales, acumulado (pesos de 2026m1) |
| `ing_hipotecarios2_acum_r` | num | 100 | Intereses ganados por prestamos hipotecarios (NIIF), acumulado (pesos de 2026m1) |
| `ing_personales2_acum_r` | num | 100 | Intereses ganados por prestamos personales (NIIF), acumulado (pesos de 2026m1) |
| `egr_fin_acum_r` | num | 100 | Egresos financieros, acumulado del ejercicio (negativo) (pesos de 2026m1) |
| `egr_fin_ars_acum_r` | num | 100 | Egresos financieros por operaciones en pesos, acumulado (negativo) (pesos de 202 |
| `int_otros_acum_r` | num | 100 | Intereses por otros depositos, pesos, acumulado (negativo) (pesos de 2026m1) |
| `aporte_fgd_acum_r` | num | 100 | Aporte al fondo de garantia de depositos, acumulado (negativo) (pesos de 2026m1) |
| `int_ctacte_acum_r` | num | 100 | Intereses por depositos en cuenta corriente, pesos, acumulado (negativo) (pesos  |
| `int_cajaahorro_acum_r` | num | 100 | Intereses por depositos en caja de ahorros, pesos, acumulado (negativo) (pesos d |
| `int_pf_acum_r` | num | 100 | Intereses por depositos a plazo fijo, pesos, acumulado (negativo) (pesos de 2026 |
| `int_otras_imp_acum_r` | num | 100 | Intereses por otras imposiciones a plazo, pesos, acumulado (negativo) (pesos de  |
| `aj_pf_cer_acum_r` | num | 100 | Ajustes CER por plazo fijo, acumulado (negativo) (pesos de 2026m1) |
| `aj_ca_uva_acum_r` | num | 100 | Ajustes por cuenta de ahorro UVA, acumulado (negativo) (pesos de 2026m1) |
| `aj_ca_uvi_acum_r` | num | 100 | Ajustes por cuenta de ahorro UVI, acumulado (negativo) (pesos de 2026m1) |
| `aj_dep_uva_acum_r` | num | 100 | Ajustes e intereses por depositos UVA, acumulado (negativo) (pesos de 2026m1) |
| `int_caucion_acum_r` | num | 100 | Intereses por operaciones de caucion bursatil, acumulado (negativo) (pesos de 20 |
| `egr_fin_usd_acum_r` | num | 100 | Egresos financieros por operaciones en ME, acumulado (negativo) (pesos de 2026m1 |
| `int_otros_usd_acum_r` | num | 100 | Intereses por otros depositos, ME, acumulado (negativo) (pesos de 2026m1) |
| `int_ctacte_usd_acum_r` | num | 100 | Intereses por depositos en cuenta corriente, ME, acumulado (negativo) (pesos de  |
| `int_cajaahorro_usd_acum_r` | num | 100 | Intereses por depositos en caja de ahorros, ME, acumulado (negativo) (pesos de 2 |
| `int_pf_usd_acum_r` | num | 100 | Intereses por depositos a plazo fijo, ME, acumulado (negativo) (pesos de 2026m1) |
| `int_otras_imp_usd_acum_r` | num | 100 | Intereses por otras imposiciones a plazo, ME, acumulado (negativo) (pesos de 202 |
| `gastos_adm_acum_r` | num | 100 | Gastos de administracion, acumulado (negativo) (pesos de 2026m1) |
| `dep_retrib_var_t_r` | num | 100 | SPNF inversiones a plazo con retribucion variable, transferibles (pesos de 2026m |
| `dep_plazo_const_t_r` | num | 100 | SPNF inversiones a plazo constante, transferibles (pesos de 2026m1) |
| `dep_plazo_const_t_usd_r` | num | 100 | SPNF ME inversiones a plazo constante, transferibles (pesos de 2026m1) |
| `ing_fin_flow_r` | num | 100 | Ingresos financieros, flujo mensual (pesos de 2026m1) |
| `ing_adelantos_flow_r` | num | 100 | Intereses ganados por adelantos, acumulado, flujo mensual (pesos de 2026m1) |
| `ing_documentos_flow_r` | num | 100 | Intereses ganados por documentos, acumulado, flujo mensual (pesos de 2026m1) |
| `ing_hipot_viv_flow_r` | num | 100 | Intereses ganados por hipotecarios sobre vivienda, acumulado, flujo mensual (pes |
| `ing_hipot_otros_flow_r` | num | 100 | Intereses ganados por otros hipotecarios, acumulado, flujo mensual (pesos de 202 |
| `ing_prend_auto_flow_r` | num | 100 | Intereses ganados por prendarios automotores, acumulado, flujo mensual (pesos de |
| `ing_prend_otros_flow_r` | num | 100 | Intereses ganados por otros prendarios, acumulado, flujo mensual (pesos de 2026m |
| `ing_otros_prest_flow_r` | num | 100 | Intereses ganados por otros prestamos, acumulado, flujo mensual (pesos de 2026m1 |
| `ing_tarjetas_flow_r` | num | 100 | Intereses ganados por tarjetas de credito, acumulado, flujo mensual (pesos de 20 |
| `ing_personales_flow_r` | num | 100 | Intereses ganados por prestamos personales, acumulado, flujo mensual (pesos de 2 |
| `ing_hipotecarios2_flow_r` | num | 100 | Intereses ganados por prestamos hipotecarios (NIIF), acumulado, flujo mensual (p |
| `ing_personales2_flow_r` | num | 100 | Intereses ganados por prestamos personales (NIIF), acumulado, flujo mensual (pes |
| `egr_fin_flow_r` | num | 100 | Egresos financieros, flujo mensual (pesos de 2026m1) |
| `egr_fin_ars_flow_r` | num | 100 | Egresos financieros por operaciones en pesos, flujo mensual (pesos de 2026m1) |
| `int_otros_flow_r` | num | 100 | Intereses por otros depositos, pesos, flujo mensual (pesos de 2026m1) |
| `aporte_fgd_flow_r` | num | 100 | Aporte al fondo de garantia de depositos, flujo mensual (pesos de 2026m1) |
| `int_ctacte_flow_r` | num | 100 | Intereses por depositos en cuenta corriente, pesos, flujo mensual (pesos de 2026 |
| `int_cajaahorro_flow_r` | num | 100 | Intereses por depositos en caja de ahorros, pesos, flujo mensual (pesos de 2026m |
| `int_pf_flow_r` | num | 100 | Intereses por depositos a plazo fijo, pesos, flujo mensual (pesos de 2026m1) |
| `int_otras_imp_flow_r` | num | 100 | Intereses por otras imposiciones a plazo, pesos, flujo mensual (pesos de 2026m1) |
| `aj_pf_cer_flow_r` | num | 100 | Ajustes CER por plazo fijo, flujo mensual (pesos de 2026m1) |
| `aj_ca_uva_flow_r` | num | 100 | Ajustes por cuenta de ahorro UVA, flujo mensual (pesos de 2026m1) |
| `aj_ca_uvi_flow_r` | num | 100 | Ajustes por cuenta de ahorro UVI, flujo mensual (pesos de 2026m1) |
| `aj_dep_uva_flow_r` | num | 100 | Ajustes e intereses por depositos UVA, flujo mensual (pesos de 2026m1) |
| `int_caucion_flow_r` | num | 100 | Intereses por operaciones de caucion bursatil, flujo mensual (pesos de 2026m1) |
| `egr_fin_usd_flow_r` | num | 100 | Egresos financieros por operaciones en ME, flujo mensual (pesos de 2026m1) |
| `int_otros_usd_flow_r` | num | 100 | Intereses por otros depositos, ME, flujo mensual (pesos de 2026m1) |
| `int_ctacte_usd_flow_r` | num | 100 | Intereses por depositos en cuenta corriente, ME, flujo mensual (pesos de 2026m1) |
| `int_cajaahorro_usd_flow_r` | num | 100 | Intereses por depositos en caja de ahorros, ME, flujo mensual (pesos de 2026m1) |
| `int_pf_usd_flow_r` | num | 100 | Intereses por depositos a plazo fijo, ME, flujo mensual (pesos de 2026m1) |
| `int_otras_imp_usd_flow_r` | num | 100 | Intereses por otras imposiciones a plazo, ME, flujo mensual (pesos de 2026m1) |
| `gastos_adm_flow_r` | num | 100 | Gastos de administracion, flujo mensual (pesos de 2026m1) |
| `int_dep_ars_flow_r` | num | 100 | Intereses pagados por depositos en pesos, flujo mensual (pesos de 2026m1) |
| `int_dep_usd_flow_r` | num | 100 | Intereses pagados por depositos en ME, flujo mensual (pesos de 2026m1) |
| `dep_vista_min_r` | num | 100 | SPNF vista minorista: caja de ahorro + sueldo + CGU + ahorro UVA/UVI (pesos de 2 |
| `dep_pf_total_r` | num | 100 | SPNF plazo fijo total: transf + intransf + CER + precancelables + retrib variabl |
| `dep_especiales_r` | num | 100 | SPNF cuentas especiales (dep y canc, titulares, exportadores, blanqueos 2016 y 2 |
| `dep_fci_proxy_r` | num | 100 | Proxy fondeo FCI/institucional a la vista: cta esp PJ con interes (311724). Cont |
| `dep_precanc_r` | num | 100 | Mayorista a plazo: inversiones precancelables transferibles e intransferibles (p |
| `dep_pf_total_usd_r` | num | 100 | SPNF ME plazo fijo total (pesos de 2026m1) |
| `dep_especiales_usd_r` | num | 100 | SPNF ME cuentas especiales (blanqueos 2016 y 2024, repatriacion Bienes Personale |

## `caracteristicas_bancos.dta`

_Caracteristicas por banco x mes, IEF BCRA (formato largo)_

Unidad: entidad × mes × código (formato largo). Llave: `ent, ym, fuente, codigo`. Filas: 528.714. Variables: 7. Cobertura: 2018-01 a 2026-04.

Indicadores (`indicad`), información adicional (`inf_adi`) y estado de situación de deudores (`esd`) del IEF. El catálogo de códigos está en `catalogo_caracteristicas.csv`. El centinela 99999 de `indicad` ya está en missing.

| Variable | Tipo | % no faltante | Descripción |
|---|---|---:|---|
| `ent` | num | 100 | Codigo de entidad BCRA |
| `nombre` | texto | 100 | Nombre de la entidad |
| `ym` | fecha | 100 | Mes |
| `fuente` | texto | 100 | Archivo IEF de origen (inf_adi, indicad o esd) |
| `codigo` | texto | 100 | Codigo de linea BCRA |
| `descripcion` | texto | 100 | Descripcion de la linea |
| `valor` | num | 99 | Valor a la fecha mas reciente del archivo |

Códigos por fuente: `esd` 64, `indicad` 31, `inf_adi` 15.

## `prestamos_depositos_prov.dta`

_Presencia y negocio por banco x provincia, IEF BCRA_

Unidad: entidad × provincia × mes. Llave: `ent, provincia, ym`. Filas: 48.115. Variables: 25. Cobertura: 2018-01 a 2026-04.

Red de atención por provincia (mensual) y préstamos y depósitos por provincia (sólo cierres trimestrales).

| Variable | Tipo | % no faltante | Descripción |
|---|---|---:|---|
| `provincia` | texto | 100 | Provincia |
| `ent` | num | 100 | Codigo de entidad BCRA |
| `nombre` | texto | 100 | Nombre de la entidad |
| `ym` | fecha | 100 | Mes |
| `suc_plenas` | num | 100 | Sucursales plenas habilitadas |
| `suc_esp` | num | 100 | Sucursales de operatoria especifica habilitadas |
| `suc_moviles` | num | 100 | Sucursales moviles habilitadas |
| `dep_autom` | num | 100 | Dependencias automatizadas habilitadas |
| `atm` | num | 100 | Cajeros automaticos habilitados |
| `tas` | num | 100 | Terminales de autoservicio habilitadas |
| `promocion` | num | 100 | Puestos de promocion habilitados |
| `acsf` | num | 61 | Agencias complementarias de serv. financieros (desde 2021m4) |
| `prestamos_prov` | num | 28 | Prestamos del banco en la provincia (trimestral, nominal) |
| `depositos_prov` | num | 28 | Depositos del banco en la provincia (trimestral, nominal) |
| `es_banco` | num | 100 | Banco (AA100) |
| `banco_publico` | num | 100 | Banco publico (AA110) |
| `banco_privado` | num | 100 | Banco privado (AA120) |
| `banco_capnacional` | num | 100 | Banco local de capital nacional (AA121) |
| `banco_capextranjero` | num | 100 | Banco de capital extranjero o sucursal del exterior (AA123/AA124) |
| `cia_financiera` | num | 100 | Compania financiera (AA200) |
| `cia_fin_extranjera` | num | 100 | Compania financiera de capital extranjero (AA220) |
| `top10_privados` | num | 100 | Entre los 10 primeros bancos privados (AA910) |
| `ipc_nacional` | num | 100 | IPC nacional usado para deflactar (dic-2016=100) |
| `prestamos_prov_r` | num | 28 | Prestamos del banco en la provincia (trimestral, pesos de 2026m1) |
| `depositos_prov_r` | num | 28 | Depositos del banco en la provincia (trimestral, pesos de 2026m1) |

## `inclusion_prov.dta`

_Inclusion financiera BCRA, provincia x mes_

Unidad: provincia × mes. Llave: `provincia, ym`. Filas: 2.592. Variables: 26. Cobertura: 2017-01 a 2025-12.

Informe de Inclusión Financiera del BCRA. Las variables de personas con cuenta son trimestrales.

| Variable | Tipo | % no faltante | Descripción |
|---|---|---:|---|
| `provincia` | texto | 100 | Provincia |
| `ym` | fecha | 100 | Mes |
| `n_acsf` | num | 63 | Agencias complementarias de servicios financieros (cantidad) |
| `n_atm` | num | 78 | Cajeros automaticos ATM (cantidad) |
| `n_sucursales` | num | 78 | Sucursales (cantidad) |
| `n_sucursales_moviles` | num | 31 | Sucursales moviles (cantidad) |
| `n_tas` | num | 78 | Terminales de autoservicio (cantidad) |
| `pct_adultos_cred_adelantos` | num | 100 | % de adultos con adelantos |
| `pct_adultos_cred_hipotecarios` | num | 100 | % de adultos con credito hipotecario |
| `pct_adultos_cred_personales` | num | 100 | % de adultos con prestamos personales |
| `pct_adultos_cred_prendarios` | num | 100 | % de adultos con credito prendario |
| `pct_adultos_cred_tarjetas` | num | 100 | % de adultos con tarjeta de credito |
| `pct_adultos_cred_bcos_priv` | num | 100 | % de adultos con financiamiento de bancos privados |
| `pct_adultos_cred_bcos_pub` | num | 100 | % de adultos con financiamiento de bancos publicos |
| `pct_adultos_cred_comp_fin` | num | 100 | % de adultos con financiamiento de companias financieras |
| `pct_adultos_cred_ent_fin` | num | 100 | % de adultos con financiamiento de entidades financieras (EEFF) |
| `pct_adultos_cred_opnfc` | num | 100 | % de adultos con financ. de otros proveedores no financieros (OPNFC) |
| `pct_adultos_cred_pnfc` | num | 100 | % de adultos con financ. de proveedores no financieros de credito (PNFC) |
| `pct_adultos_cred_tarj_nobanc` | num | 100 | % de adultos con financiamiento de tarjetas no bancarias (TCNB) |
| `pct_adultos_credito` | num | 100 | % de adultos con financiamiento en el sistema financiero ampliado |
| `n_pers_ambas_ctas` | num | 26 | Personas con cuenta bancaria y de pago (trimestral) |
| `n_pers_min1_cta` | num | 26 | Personas con al menos una cuenta (trimestral) |
| `n_pers_min1_cta_bancaria` | num | 26 | Personas con al menos una cuenta bancaria (trimestral) |
| `n_pers_min1_cta_pago` | num | 26 | Personas con al menos una cuenta de pago (trimestral) |
| `n_pers_solo_cta_bancaria` | num | 26 | Personas con cuenta bancaria (CBU) solamente (trimestral) |
| `n_pers_solo_cta_pago` | num | 26 | Personas con cuenta de pago (CVU) solamente (trimestral) |

## `ipc.dta`

_IPC INDEC, nacional y regiones_

Unidad: mes. Llave: `ym`. Filas: 115. Variables: 8. Cobertura: 2016-12 a 2026-06.

IPC del INDEC, nivel general, dic-2016 = 100.

| Variable | Tipo | % no faltante | Descripción |
|---|---|---:|---|
| `ym` | fecha | 100 | Mes |
| `ipc_nacional` | num | 100 | IPC nivel general, total nacional (dic-2016=100) |
| `ipc_gba` | num | 100 | IPC nivel general, region GBA (dic-2016=100) |
| `ipc_pampeana` | num | 100 | IPC nivel general, region Pampeana (dic-2016=100) |
| `ipc_noroeste` | num | 100 | IPC nivel general, region Noroeste (dic-2016=100) |
| `ipc_noreste` | num | 100 | IPC nivel general, region Noreste (dic-2016=100) |
| `ipc_cuyo` | num | 100 | IPC nivel general, region Cuyo (dic-2016=100) |
| `ipc_patagonia` | num | 100 | IPC nivel general, region Patagonia (dic-2016=100) |

## `pda_provincia.dta`

Unidad: provincia × mes. Llave: `cod_prov_indec, ym`. Filas: 2.016. Variables: 15. Cobertura: 2019-01 a 2025-12.

Puntos de acceso del BCRA agregados a provincia. `ym` es el índice `%tm` guardado como entero, sin formato.

| Variable | Tipo | % no faltante | Descripción |
|---|---|---:|---|
| `ym` | num | 100 | Mes, indice %tm de Stata (meses desde 1960m1) guardado como entero |
| `year` | num | 100 | Anio |
| `month` | num | 100 | Mes (1-12) |
| `cod_prov_indec` | texto | 100 | Codigo de provincia INDEC |
| `cod_prov_arca` | texto | 100 | Codigo de provincia ARCA (padron de CENDEU) |
| `provincia` | texto | 100 | Provincia |
| `n_deptos` | num | 100 | Departamentos con al menos un punto de acceso |
| `n_localidades` | num | 100 | Localidades con al menos un punto de acceso |
| `sucursales` | num | 100 | Sucursales |
| `suc_moviles` | num | 100 | Sucursales moviles |
| `atm` | num | 100 | Cajeros automaticos (ATM) |
| `tas` | num | 100 | Terminales de autoservicio (TAS) |
| `acsf_vinculos` | num | 100 | Vinculos con agencias complementarias (ACSF); una agencia puede contar varias ve |
| `pda_sin_acsf` | num | 100 | Puntos de acceso sin ACSF: sucursales + moviles + ATM + TAS |
| `pda_total` | num | 100 | Puntos de acceso totales, incluye vinculos ACSF |

## `pda_depto.dta`

Unidad: departamento × mes. Llave: `cod_depto, ym`. Filas: 43.851. Variables: 15. Cobertura: 2019-01 a 2025-12.

Puntos de acceso agregados a departamento INDEC. `ym` es el índice `%tm` guardado como entero.

| Variable | Tipo | % no faltante | Descripción |
|---|---|---:|---|
| `ym` | num | 100 | Mes, indice %tm de Stata (meses desde 1960m1) guardado como entero |
| `year` | num | 100 | Anio |
| `month` | num | 100 | Mes (1-12) |
| `cod_depto` | texto | 100 | Codigo de departamento INDEC (5 digitos) |
| `cod_prov` | texto | 100 | Codigo de provincia INDEC |
| `provincia` | texto | 100 | Provincia |
| `departamento` | texto | 100 | Departamento |
| `n_localidades` | num | 100 | Localidades con al menos un punto de acceso |
| `sucursales` | num | 100 | Sucursales |
| `suc_moviles` | num | 100 | Sucursales moviles |
| `atm` | num | 100 | Cajeros automaticos (ATM) |
| `tas` | num | 100 | Terminales de autoservicio (TAS) |
| `acsf_vinculos` | num | 100 | Vinculos con agencias complementarias (ACSF); una agencia puede contar varias ve |
| `pda_sin_acsf` | num | 100 | Puntos de acceso sin ACSF: sucursales + moviles + ATM + TAS |
| `pda_total` | num | 100 | Puntos de acceso totales, incluye vinculos ACSF |

## `pda_lender_depto.dta`

Unidad: entidad × departamento × tipo × mes. Llave: `entidad, cod_depto, tipo_pda, ym`. Filas: 594.214. Variables: 8. Cobertura: 2019-01 a 2025-12.

Puntos de acceso por entidad. La entidad viene por nombre, no por código BCRA.

| Variable | Tipo | % no faltante | Descripción |
|---|---|---:|---|
| `ym` | num | 100 | Mes, indice %tm de Stata (meses desde 1960m1) guardado como entero |
| `year` | num | 100 | Anio |
| `month` | num | 100 | Mes (1-12) |
| `cod_depto` | texto | 100 | Codigo de departamento INDEC (5 digitos) |
| `grupo` | texto | 100 | Grupo de entidad segun el BCRA |
| `entidad` | texto | 100 | Entidad financiera (nombre) |
| `tipo_pda` | texto | 100 | Tipo de punto de acceso |
| `n_pda` | num | 100 | Cantidad de puntos de acceso |

## `FondosCNV/panel_fondo_semana.dta`

_FCI money market, fondo x semana (CNV)_

Unidad: fondo money market × semana. Llave: `cod_cnv, semana`. Filas: 17.893. Variables: 38. Cobertura: 2020-01-03 a 2026-09-25.

Planillas diarias CNV/CAFCI llevadas a semana y cruzadas con la cartera semanal de la ficha CNV. Detalle de construcción en `diccionario_fondoscnv.md`.

| Variable | Tipo | % no faltante | Descripción |
|---|---|---:|---|
| `cod_cnv` | num | 100 | Codigo CNV del fondo (planilla diaria); llave del fondo |
| `semana` | fecha | 100 | Viernes de cierre de la semana (W-FRI) |
| `fondo` | texto | 100 | Nombre del fondo segun la planilla diaria |
| `gerente` | texto | 100 | Sociedad gerente (planilla) |
| `depositaria` | texto | 100 | Sociedad depositaria (planilla); no es donde esta la vista |
| `tipo_dinero` | texto | 29 | Tipo de money market: Clasico o Dinamico (planilla) |
| `pn` | num | 100 | Patrimonio neto del fondo, ultimo dia habil de la semana, pesos nominales |
| `flujo` | num | 100 | Flujo neto de la semana: suma de dCCP x VCP/1000 de las clases, pesos |
| `n_dias` | num | 100 | Dias con planilla en la semana |
| `ultima_fecha` | fecha | 100 | Ultimo dia con planilla en la semana |
| `fee_medio` | num | 100 | Honorarios SG+SD+gastos, promedio por PN de las clases, % anual |
| `tna_bruta` | num | 99 | TNA bruta del fondo (neta + honorarios), prom. por dias, % |
| `fondo_cnv` | texto | 96 | Nombre del fondo segun la ficha CNV (cartera) |
| `cartera_al` | fecha | 96 | Fecha efectiva de la cartera informada |
| `gerente_cnv` | texto | 96 | Sociedad gerente segun la ficha CNV |
| `depositaria_cnv` | texto | 96 | Sociedad depositaria segun la ficha CNV |
| `clasificacion_cnv` | texto | 96 | Clasificacion del fondo segun la ficha CNV |
| `moneda_cnv` | texto | 96 | Moneda del fondo segun la ficha CNV |
| `region_cnv` | texto | 96 | Region segun la ficha CNV |
| `horizonte_cnv` | texto | 96 | Horizonte segun la ficha CNV |
| `pn_cartera` | num | 96 | Patrimonio neto informado en la cartera, pesos nominales |
| `total_pct` | num | 96 | Suma de porcentajes informada en la cartera (deberia ser 100) |
| `moneda_pn` | texto | 96 | Moneda en que se expresa pn_cartera |
| `lfc` | texto | 96 | Id del fondo en la ficha CNV (DetallesFCI/{lfc}) |
| `fecha_pedida` | fecha | 96 | Viernes pedido a la ficha CNV |
| `pct_disponibilidades` | num | 96 | Disponibilidades (cuentas a la vista, sin banco), % del PN |
| `pct_operaciones_plazo` | num | 92 | Operaciones a plazo (plazo fijo + caucion), % del PN |
| `pct_titulos` | num | 10 | Titulos de deuda, % del PN |
| `pct_cuotapartes_fci` | num | 1 | Cuotapartes de otros FCI, % del PN |
| `pct_otros_activos` | num | 0 | Otros activos, % del PN |
| `pct_pasivos` | num | 90 | Pasivos, % del PN |
| `pct_plazo_fijo` | num | 90 | Plazo fijo tradicional en pesos (suma de bancos), % del PN |
| `pct_plazo_fijo_uva` | num | 3 | Plazo fijo UVA (suma de bancos), % del PN |
| `pct_caucion` | num | 64 | Caucion colocadora (suma de mercados), % del PN |
| `n_bancos_pf` | num | 90 | Cantidad de bancos con plazo fijo del fondo |
| `cartera_valida` | num | 96 | 1 si la cartera pasa los controles de carga (pct en [-1,100.5], PN>1e6) |
| `tiene_cartera` | num | 100 | 1 si hay cartera para esa semana |
| `pn_ratio` | num | 96 | PN planilla / PN cartera (control de crosswalk) |
