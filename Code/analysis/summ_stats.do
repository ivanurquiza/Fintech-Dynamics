* summ_stats.do
* Tablas descriptivas (latex) y figuras. Correr con el wd en code/.
* Requiere: data/build_dta.do y data/extraer_fci_balhist.py ya corridos.

version 17
clear all
set more off
set scheme s1color

* ------------------------------------------------------------------
* repo root. Run from anywhere inside Fintech-Dynamics.
* ------------------------------------------------------------------
local n = 0
while !fileexists("README.md") & `n' < 6 {
    cd ..
    local n = `n' + 1
}
if !fileexists("README.md") {
    di as error "run this from inside the Fintech-Dynamics repo"
    exit 601
}
global root  "`c(pwd)'"
global raw   "$root/Data/raw"
global proc  "$root/Data/processed"
global cross "$root/Data/crosswalks"
global tab   "$root/Code/output/tablas"
global fig   "$root/Code/output/figuras"
cap mkdir "$root/Code/output"
cap mkdir "$tab"
cap mkdir "$fig"
cap which esttab
if _rc ssc install estout

global s1_m = ym(2021,11)
global s2_m = ym(2022,1)
global s3_m = ym(2024,4)
global s1_q = tq(2021q4)
global s2_q = tq(2022q1)
global s3_q = tq(2024q2)

* ---------------- cuentas FCI y PSP en bancos ----------------

import delimited "$raw/cafci/fci_cuentas.csv", varnames(1) clear
replace saldo = -saldo
gen ym = ym(floor(fecha/100), mod(fecha,100))
format ym %tm
keep if ym >= ym(2018,1)
reshape wide saldo, i(ent ym) j(cuenta)
rename saldo311706 cc_sin_interes
rename saldo311723 ctaesp_sin_int
rename saldo311724 ctaesp_con_int
tempfile fci
save `fci'

collapse (sum) ctaesp_sin_int ctaesp_con_int, by(ym)
merge 1:1 ym using "$proc/ipc.dta", keepusing(ipc_nacional) keep(match) nogen
qui su ipc_nacional if ym == ym(2026,1), meanonly
global ipc0 = r(mean)
gen remun_r = ctaesp_con_int*$ipc0/ipc_nacional
gen noremun_r = ctaesp_sin_int*$ipc0/ipc_nacional
tempfile fcisis
save `fcisis'

* ---------------- figura 1 ----------------

use `fcisis', clear
qui su remun_r if ym == ym(2021,12), meanonly
gen i_remun = 100*remun_r/r(mean)
qui su noremun_r if ym == ym(2021,12), meanonly
gen i_noremun = 100*noremun_r/r(mean)
twoway (line i_remun ym, lcolor(navy) lwidth(medthick)) ///
       (line i_noremun ym, lcolor(maroon) lwidth(medthick)), ///
    xline($s1_m $s2_m $s3_m, lcolor(black) lpattern(solid)) ///
    legend(size(small) order(1 "Remuneradas (FCI)" 2 "No remuneradas (PSP)") position(6) rows(1)) ///
    xlabel(, labsize(small)) ylabel(, labsize(small)) xsize(10) ysize(4.4) ///
    xtitle("") ytitle("Indice real, dic-2021 = 100", size(small)) ///
    note("Cuentas corrientes especiales de personas juridicas en bancos, total del sistema, deflactado por IPC.", size(vsmall))
graph export "$fig/f1_cuentas_pj.png", replace width(2400)

* ---------------- figura 2 ----------------

use "$proc/inclusion_prov.dta", clear
drop if missing(n_pers_min1_cta_pago)
collapse (sum) n_pers_min1_cta_pago n_pers_min1_cta_bancaria n_pers_ambas_ctas ///
    n_pers_solo_cta_pago n_pers_solo_cta_bancaria n_pers_min1_cta, by(ym)
gen yq = qofd(dofm(ym))
format yq %tq
tsset yq
gen pct_min1_pago = 100*n_pers_min1_cta_pago/n_pers_min1_cta
gen pct_min1_banc = 100*n_pers_min1_cta_bancaria/n_pers_min1_cta
gen pct_ambas     = 100*n_pers_ambas_ctas/n_pers_min1_cta
gen pct_solo_pago = 100*n_pers_solo_cta_pago/n_pers_min1_cta
gen pct_solo_banc = 100*n_pers_solo_cta_bancaria/n_pers_min1_cta
twoway (line pct_min1_banc yq, lcolor(navy) lwidth(medthick)) ///
       (line pct_min1_pago yq, lcolor(maroon) lwidth(medthick)) ///
       (line pct_solo_banc yq, lcolor(navy) lpattern(shortdash)) ///
       (line pct_solo_pago yq, lcolor(maroon) lpattern(shortdash)), ///
    xline($s1_q $s2_q $s3_q, lcolor(black) lpattern(solid)) ///
    legend(size(small) order(1 "Al menos una bancaria" 2 "Al menos una de pago" ///
        3 "Solo bancaria" 4 "Solo de pago") position(6) rows(1)) ///
    xlabel(, labsize(small)) ylabel(, labsize(small)) xsize(10) ysize(4.4) ///
    xtitle("") ytitle("% de las personas con alguna cuenta", size(small))
graph export "$fig/f2_adopcion.png", replace width(2400)

* ---------------- figura 3 ----------------

gen mill_pago = n_pers_min1_cta_pago/1e6
gen yoy_pago = 100*(mill_pago/L4.mill_pago - 1)
twoway line yoy_pago yq, lcolor(navy) lwidth(medthick) ///
    xline($s1_q $s2_q $s3_q, lcolor(black) lpattern(solid)) ///
    yline(0, lcolor(gs10)) ///
    xlabel(, labsize(small)) ylabel(, labsize(small)) xsize(10) ysize(4.4) ///
    xtitle("") ytitle("Variacion interanual (%)", size(small)) ///
    note("Personas con al menos una cuenta de pago, total pais.", size(vsmall))
graph export "$fig/f3_adopcion_yoy.png", replace width(2400)

* ---------------- figura 4 ----------------

use "$proc/balances_bancos.dta", clear
collapse (sum) dep_pf_total, by(ym)
merge 1:1 ym using `fcisis', keep(match) nogen
gen pf_r = dep_pf_total*$ipc0/ipc_nacional
qui su pf_r if ym == ym(2021,12), meanonly
gen i_pf = 100*pf_r/r(mean)
qui su remun_r if ym == ym(2021,12), meanonly
gen i_fci = 100*remun_r/r(mean)
twoway (line i_pf ym, lcolor(navy) lwidth(medthick)) ///
       (line i_fci ym, lcolor(maroon) lwidth(medthick)), ///
    xline($s1_m $s2_m $s3_m, lcolor(black) lpattern(solid)) ///
    legend(size(small) order(1 "Plazo fijo del sector privado" 2 "Cuentas remuneradas de FCI") position(6) rows(1)) ///
    xlabel(, labsize(small)) ylabel(, labsize(small)) xsize(10) ysize(4.4) ///
    xtitle("") ytitle("Indice real, dic-2021 = 100", size(small))
graph export "$fig/f4_pf_vs_fci.png", replace width(2400)

* ---------------- figura 6 ----------------

use `fcisis', clear
gen yq = qofd(dofm(ym))
bysort yq (ym): keep if _n == _N
tempfile fciq
save `fciq'

use "$proc/inclusion_prov.dta", clear
drop if missing(n_pers_min1_cta_pago)
collapse (sum) n_pers_min1_cta_pago, by(ym)
gen yq = qofd(dofm(ym))
merge 1:1 yq using `fciq', keep(match) nogen
format yq %tq
qui su remun_r if yq == tq(2021q4), meanonly
gen i_fci = 100*remun_r/r(mean)
qui su n_pers_min1_cta_pago if yq == tq(2021q4), meanonly
gen i_cvu = 100*n_pers_min1_cta_pago/r(mean)
twoway (line i_fci yq, lcolor(navy) lwidth(medthick)) ///
       (line i_cvu yq, lcolor(maroon) lwidth(medthick)), ///
    xline($s1_q $s2_q $s3_q, lcolor(black) lpattern(solid)) ///
    legend(size(small) order(1 "Ctas remuneradas de FCI en bancos (real)" 2 "Personas con al menos una cuenta de pago") ///
        position(6) rows(1)) ///
    xlabel(, labsize(small)) ylabel(, labsize(small)) xsize(10) ysize(4.4) ///
    xtitle("") ytitle("Indice, 2021q4 = 100", size(small))
graph export "$fig/f6_fci_vs_adopcion.png", replace width(2400)

* ---------------- tabla 1, panel A ----------------

use "$proc/prestamos_depositos_prov.dta", clear
collapse (sum) prestamos_prov_r depositos_prov_r, by(provincia ym)
rename (prestamos_prov_r depositos_prov_r) (prestamos_bcos_r depositos_bcos_r)
tempfile provbcos
save `provbcos'

use "$proc/inclusion_prov.dta", clear
merge 1:1 provincia ym using `provbcos', keep(master match) nogen
gen mill_min1_pago = n_pers_min1_cta_pago/1e6
gen pct_pago = 100*n_pers_min1_cta_pago/n_pers_min1_cta
gen mill_solo_cvu = n_pers_solo_cta_pago/1e6
gen bill_dep = depositos_bcos_r/1e9
gen bill_prest = prestamos_bcos_r/1e9
label var mill_min1_pago "Personas con al menos una cuenta de pago (millones)"
label var pct_pago "Con cuenta de pago / con alguna cuenta (\%)"
label var mill_solo_cvu "Personas solo cuenta de pago (millones)"
label var pct_adultos_credito "Adultos con credito, total (\%)"
label var pct_adultos_cred_ent_fin "Adultos con credito de entidades financieras (\%)"
label var pct_adultos_cred_opnfc "Adultos con credito de OPNFC (\%)"
label var n_sucursales "Sucursales"
label var n_atm "Cajeros automaticos"
label var bill_dep "Depositos bancarios (bill. \$ de 2026m1)"
label var bill_prest "Prestamos bancarios (bill. \$ de 2026m1)"

local varsA mill_min1_pago pct_pago mill_solo_cvu pct_adultos_credito ///
    pct_adultos_cred_ent_fin pct_adultos_cred_opnfc n_sucursales n_atm ///
    bill_dep bill_prest

estpost tabstat `varsA' if ym == ym(2019,12), stat(mean sd p10 p90) columns(statistics)
est store pA_2019
estpost tabstat `varsA' if ym == ym(2025,12), stat(mean sd p10 p90) columns(statistics)
est store pA_2025
esttab pA_2019 pA_2025 using "$tab/tabla1_panelA.tex", replace label booktabs ///
    cells("mean(fmt(2)) sd(fmt(2)) p10(fmt(2)) p90(fmt(2))") noobs nonumbers ///
    mtitles("Diciembre 2019" "Diciembre 2025") ///
    title("Panel A. Provincias (24 observaciones)")

* ---------------- tabla 1, panel B ----------------

use "$proc/balances_bancos.dta", clear
merge 1:1 ent ym using `fci', keep(master match) nogen
keep if es_banco == 1
gen bill_activo = activo_r/1e9
gen share_vista = (dep_ctacte + dep_cajaahorro + dep_ctasueldo)/dep_spnf
gen share_pf = dep_pf_total/dep_spnf
gen share_fci = ctaesp_con_int/depositos
label var bill_activo "Activo (bill. \$ de 2026m1)"
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
esttab pB_todos pB_pub pB_privnac pB_ext using "$tab/tabla1_panelB.tex", replace label booktabs ///
    cells("mean(fmt(3)) sd(fmt(3))") noobs nonumbers ///
    mtitles("Todos" "Publicos" "Priv. nacionales" "Extranjeros") ///
    title("Panel B. Bancos, marzo 2024")

* ---------------- tabla 1, panel C ----------------

use "$proc/inclusion_prov.dta", clear
keep if inlist(ym, ym(2021,9), ym(2025,12))
gen share_cvu = 100*n_pers_min1_cta_pago/n_pers_min1_cta
label var share_cvu "Con cuenta de pago / con alguna cuenta (\%)"
estpost tabstat share_cvu if ym == ym(2021,9), stat(mean sd min p50 max) columns(statistics)
est store pC_2021
estpost tabstat share_cvu if ym == ym(2025,12), stat(mean sd min p50 max) columns(statistics)
est store pC_2025
esttab pC_2021 pC_2025 using "$tab/tabla1_panelC.tex", replace label booktabs ///
    cells("mean(fmt(2)) sd(fmt(2)) min(fmt(2)) p50(fmt(2)) max(fmt(2))") noobs nonumbers ///
    mtitles("2021q3" "2025q4") ///
    title("Panel C. Adopcion de billeteras por provincia (\%)")

di as text "listo"
