* summ_stats.do
* Summary statistics and descriptive figures.
* Inputs:  ../data/processed/*.dta (run data/build_dta.do first)
*          ../data/raw/fci_cuentas.csv (run data/extraer_fci_balhist.py first)
* Output:  ../output/tablas/  and  ../output/figuras/
* Run with the working directory in code/.

version 17
clear all
set more off
set scheme s1color

cap cd "~/Documents/GitHub/Fintech-Dynamics/code"
cap cd "code"
cap confirm file "../data/processed/inclusion_prov.dta"
if _rc {
    di as error "run this file with the working directory in code/"
    exit 601
}

global dat "../data/processed"
global tab "../output/tablas"
global fig "../output/figuras"
cap mkdir "../output"
cap mkdir "$tab"
cap mkdir "$fig"
cap which esttab
if _rc ssc install estout

* reference dates: full QR interoperability, first FCI reserve hike, big 2025 hikes
global t_interop = ym(2021,11)
global t_encaje1 = ym(2024,4)
global t_encaje2 = ym(2025,8)

* ------------------------------------------------------------------
* 0. FCI remunerated accounts at banks, from balhist (codes 3117xx)
* ------------------------------------------------------------------

import delimited "../data/raw/fci_cuentas.csv", varnames(1) clear
* liability accounts come with debit-credit sign, flip them
replace saldo = -saldo
gen ym = ym(floor(fecha/100), mod(fecha,100))
format ym %tm
keep if ym >= ym(2018,1)
reshape wide saldo, i(ent ym) j(cuenta)
rename saldo311706 cc_sin_interes
rename saldo311723 ctaesp_sin_int
rename saldo311724 ctaesp_con_int
label var cc_sin_interes "Ctas ctes SPNF sin interes"
label var ctaesp_sin_int "Ctas ctes especiales de pers. juridicas sin interes"
label var ctaesp_con_int "Ctas ctes especiales de pers. juridicas con interes (FCI)"
tempfile fci
save `fci'

* ------------------------------------------------------------------
* 1. Tabla 1, Panel A: provincias, 2019 vs 2025
* ------------------------------------------------------------------

use "$dat/prestamos_depositos_prov.dta", clear
collapse (sum) prestamos_prov_r depositos_prov_r suc_plenas atm, by(provincia ym)
rename (prestamos_prov_r depositos_prov_r) (prestamos_bcos_r depositos_bcos_r)
tempfile provbcos
save `provbcos'

use "$dat/inclusion_prov.dta", clear
merge 1:1 provincia ym using `provbcos', keep(master match) nogen
gen mill_solo_cvu = n_pers_solo_cta_pago/1e6
gen mill_solo_cbu = n_pers_solo_cta_bancaria/1e6
gen bill_dep = depositos_bcos_r/1e9
gen bill_prest = prestamos_bcos_r/1e9
label var mill_solo_cvu "Personas solo cuenta de pago (millones)"
label var mill_solo_cbu "Personas solo cuenta bancaria (millones)"
label var pct_adultos_credito "Adultos con credito, total (%)"
label var pct_adultos_cred_ent_fin "Adultos con credito de entidades financieras (%)"
label var pct_adultos_cred_opnfc "Adultos con credito de OPNFC (%)"
label var n_sucursales "Sucursales"
label var n_atm "Cajeros automaticos"
label var bill_dep "Depositos bancarios (bill. $ de 2026m1)"
label var bill_prest "Prestamos bancarios (bill. $ de 2026m1)"

local varsA mill_solo_cvu mill_solo_cbu pct_adultos_credito ///
    pct_adultos_cred_ent_fin pct_adultos_cred_opnfc n_sucursales n_atm ///
    bill_dep bill_prest

estpost tabstat `varsA' if ym == ym(2019,12), stat(mean sd p10 p90) columns(statistics)
est store pA_2019
estpost tabstat `varsA' if ym == ym(2025,12), stat(mean sd p10 p90) columns(statistics)
est store pA_2025
esttab pA_2019 pA_2025 using "$tab/tabla1_panelA.rtf", replace label ///
    cells("mean(fmt(2)) sd(fmt(2)) p10(fmt(2)) p90(fmt(2))") noobs nonumbers ///
    mtitles("Diciembre 2019" "Diciembre 2025") ///
    title("Panel A. Provincias (24 observaciones)")
esttab pA_2019 pA_2025 using "$tab/tabla1_panelA.csv", replace label ///
    cells("mean sd p10 p90") noobs nonumbers mtitles("dic2019" "dic2025")

* ------------------------------------------------------------------
* 2. Tabla 1, Panel B: bancos, corte pre tratamiento (2024m3)
* ------------------------------------------------------------------

use "$dat/balances_bancos.dta", clear
merge 1:1 ent ym using `fci', keep(master match) nogen
keep if es_banco == 1
gen bill_activo = activo_r/1e9
gen share_vista = (dep_ctacte + dep_cajaahorro + dep_ctasueldo)/dep_spnf
gen share_pf = dep_pfijo/dep_spnf
gen share_fci = ctaesp_con_int/depositos
label var bill_activo "Activo (bill. $ de 2026m1)"
label var share_vista "Depositos a la vista / dep. SPNF"
label var share_pf "Plazo fijo / dep. SPNF"
label var share_fci "Ctas remuneradas de FCI / depositos"

gen grupo = "Privado nacional"
replace grupo = "Publico" if banco_publico == 1
replace grupo = "Extranjero" if banco_capextranjero == 1

local varsB bill_activo share_vista share_pf share_fci
estpost tabstat `varsB' if ym == ym(2024,3), stat(mean sd p10 p90) columns(statistics)
est store pB_todos
estpost tabstat `varsB' if ym == ym(2024,3) & grupo == "Publico", stat(mean sd) columns(statistics)
est store pB_pub
estpost tabstat `varsB' if ym == ym(2024,3) & grupo == "Privado nacional", stat(mean sd) columns(statistics)
est store pB_privnac
estpost tabstat `varsB' if ym == ym(2024,3) & grupo == "Extranjero", stat(mean sd) columns(statistics)
est store pB_ext
esttab pB_todos pB_pub pB_privnac pB_ext using "$tab/tabla1_panelB.rtf", replace label ///
    cells("mean(fmt(3)) sd(fmt(3))") noobs nonumbers ///
    mtitles("Todos" "Publicos" "Priv. nacionales" "Extranjeros") ///
    title("Panel B. Bancos, marzo 2024")
esttab pB_todos pB_pub pB_privnac pB_ext using "$tab/tabla1_panelB.csv", replace label ///
    cells("mean sd") noobs nonumbers mtitles("todos" "publicos" "privnac" "extranjeros")

* ------------------------------------------------------------------
* 3. Tabla 1, Panel C: exposiciones
* ------------------------------------------------------------------

* provincial exposure: wallet-only share among people with some account, 2021q3
use "$dat/inclusion_prov.dta", clear
keep if ym == ym(2021,9)
gen expo_prov = n_pers_solo_cta_pago/n_pers_min1_cta
label var expo_prov "Cuentas de pago solamente / con alguna cuenta, 2021q3"
estpost tabstat expo_prov, stat(mean sd min p25 p50 p75 max) columns(statistics)
est store pC_prov
tempfile expoq
keep provincia expo_prov
save `expoq'

* bank exposure: FCI remunerated accounts over deposits, average 2023m6 to 2024m3
use "$dat/balances_bancos.dta", clear
merge 1:1 ent ym using `fci', keep(master match) nogen
keep if es_banco == 1 & inrange(ym, ym(2023,6), ym(2024,3))
gen share_fci = ctaesp_con_int/depositos
collapse (mean) share_fci, by(ent nombre)
label var share_fci "Ctas remuneradas de FCI / depositos, prom. 2023m6-2024m3"
estpost tabstat share_fci, stat(mean sd min p25 p50 p75 max) columns(statistics)
est store pC_bco
esttab pC_prov pC_bco using "$tab/tabla1_panelC.rtf", replace label ///
    cells("mean(fmt(3)) sd(fmt(3)) min(fmt(3)) p25(fmt(3)) p50(fmt(3)) p75(fmt(3)) max(fmt(3))") ///
    noobs nonumbers mtitles("Provincias" "Bancos") ///
    title("Panel C. Variables de exposicion")

histogram share_fci, bin(20) fcolor(navy%60) lcolor(navy) ///
    xtitle("Ctas remuneradas de FCI / depositos, promedio 2023m6-2024m3") ///
    ytitle("Bancos") 
graph export "$fig/f6_hist_exposicion_fci.png", replace width(2400)

* ------------------------------------------------------------------
* 4. Figura 1: la tijera (solo CVU vs solo CBU, nacional)
* ------------------------------------------------------------------

use "$dat/inclusion_prov.dta", clear
collapse (sum) n_pers_solo_cta_pago n_pers_solo_cta_bancaria, by(ym)
drop if missing(n_pers_solo_cta_pago)
gen mill_cvu = n_pers_solo_cta_pago/1e6
gen mill_cbu = n_pers_solo_cta_bancaria/1e6
twoway (line mill_cbu ym, lcolor(navy) lwidth(medthick)) ///
       (line mill_cvu ym, lcolor(maroon) lwidth(medthick)), ///
    xline($t_interop, lpattern(dash) lcolor(gs8)) ///
    xline($t_encaje1, lpattern(dash) lcolor(gs8)) ///
    xline($t_encaje2, lpattern(dash) lcolor(gs8)) ///
    legend(order(1 "Solo cuenta bancaria (CBU)" 2 "Solo cuenta de pago (CVU)") ///
        position(6) rows(1)) ///
    xtitle("") ytitle("Millones de personas") ///
    note("Lineas verticales: QR interoperable pleno (2021m11), primer encaje a FCI (2024m4), suba de encajes (2025m8)")
graph export "$fig/f1_tijera_cuentas.png", replace width(2400)

* ------------------------------------------------------------------
* 5. Figura 2: cuentas remuneradas de FCI en bancos, en terminos reales
* ------------------------------------------------------------------

use `fci', clear
collapse (sum) ctaesp_con_int, by(ym)
merge 1:1 ym using "$dat/ipc.dta", keepusing(ipc_nacional) keep(match) nogen
qui su ipc_nacional if ym == ym(2026,1), meanonly
gen fci_real = ctaesp_con_int*r(mean)/ipc_nacional
qui su fci_real if ym == ym(2021,12), meanonly
gen fci_indice = 100*fci_real/r(mean)
twoway line fci_indice ym, lcolor(navy) lwidth(medthick) ///
    xline(`=ym(2022,1)', lpattern(dash) lcolor(gs8)) ///
    xline($t_encaje1, lpattern(dash) lcolor(gs8)) ///
    xline($t_encaje2, lpattern(dash) lcolor(gs8)) ///
    xtitle("") ytitle("Indice real, dic-2021 = 100") ///
    note("Cuentas corrientes especiales de personas juridicas con interes, total del sistema, deflactado por IPC." ///
         "Lineas verticales: encaje 100% a custodia de PSP (2022m1), encajes a FCI (2024m4 y 2025m8)")
graph export "$fig/f2_fci_en_bancos.png", replace width(2400)

* ------------------------------------------------------------------
* 6. Figura 3: adopcion por terciles de exposicion (el antes y despues crudo)
* ------------------------------------------------------------------

use "$dat/inclusion_prov.dta", clear
merge m:1 provincia using `expoq', nogen
drop if missing(n_pers_solo_cta_pago)
xtile terc = expo_prov, nq(3)
keep if inlist(terc, 1, 3)
collapse (sum) n_pers_solo_cta_pago, by(terc ym)
bysort terc (ym): gen base = n_pers_solo_cta_pago if ym == ym(2021,9)
bysort terc: egen b = max(base)
gen indice = 100*n_pers_solo_cta_pago/b
twoway (line indice ym if terc == 3, lcolor(maroon) lwidth(medthick)) ///
       (line indice ym if terc == 1, lcolor(navy) lwidth(medthick) lpattern(longdash)), ///
    xline($t_interop, lpattern(dash) lcolor(gs8)) ///
    xline($t_encaje1, lpattern(dash) lcolor(gs8)) ///
    legend(order(1 "Provincias de alta exposicion (tercil 3)" 2 "Baja exposicion (tercil 1)") ///
        position(6) rows(1)) ///
    xtitle("") ytitle("Personas con solo cuenta de pago, 2021q3 = 100") ///
    note("Exposicion: participacion de cuentas de pago en 2021q3. Terciles de provincias.")
graph export "$fig/f3_adopcion_terciles.png", replace width(2400)

* ------------------------------------------------------------------
* 7. Figura 4: plazo fijo vs cuentas FCI (sustitucion)
* ------------------------------------------------------------------

use "$dat/balances_bancos.dta", clear
merge 1:1 ent ym using `fci', keep(master match) nogen
collapse (sum) dep_pfijo ctaesp_con_int, by(ym)
merge 1:1 ym using "$dat/ipc.dta", keepusing(ipc_nacional) keep(match) nogen
qui su ipc_nacional if ym == ym(2026,1), meanonly
local base = r(mean)
gen pf_real = dep_pfijo*`base'/ipc_nacional
gen fci_real = ctaesp_con_int*`base'/ipc_nacional
qui su pf_real if ym == ym(2021,12), meanonly
gen pf_i = 100*pf_real/r(mean)
qui su fci_real if ym == ym(2021,12), meanonly
gen fci_i = 100*fci_real/r(mean)
twoway (line pf_i ym, lcolor(navy) lwidth(medthick)) ///
       (line fci_i ym, lcolor(maroon) lwidth(medthick)), ///
    xline(`=ym(2022,1)', lpattern(dash) lcolor(gs8)) ///
    xline($t_encaje1, lpattern(dash) lcolor(gs8)) ///
    xline($t_encaje2, lpattern(dash) lcolor(gs8)) ///
    legend(order(1 "Plazo fijo del sector privado" 2 "Cuentas remuneradas de FCI") ///
        position(6) rows(1)) ///
    xtitle("") ytitle("Indice real, dic-2021 = 100")
graph export "$fig/f4_pf_vs_fci.png", replace width(2400)

* ------------------------------------------------------------------
* 8. Figura 5: sucursales vs adopcion de billeteras
* ------------------------------------------------------------------

use "$dat/inclusion_prov.dta", clear
collapse (sum) n_sucursales n_pers_solo_cta_pago, by(ym)
gen mill_cvu = n_pers_solo_cta_pago/1e6
twoway (line n_sucursales ym if !missing(n_sucursales), lcolor(navy) lwidth(medthick)) ///
       (line mill_cvu ym if !missing(mill_cvu), lcolor(maroon) lwidth(medthick) yaxis(2)), ///
    xline($t_interop, lpattern(dash) lcolor(gs8)) ///
    legend(order(1 "Sucursales bancarias (eje izq.)" 2 "Personas solo cuenta de pago, millones (eje der.)") ///
        position(6) rows(1)) ///
    xtitle("") ytitle("Sucursales") ytitle("Millones", axis(2))
graph export "$fig/f5_sucursales_vs_adopcion.png", replace width(2400)

di as text "listo: tablas en $tab, figuras en $fig"
