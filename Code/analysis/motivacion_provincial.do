* motivacion_provincial.do
* Motivation for the bank x province design: provincial wallet adoption
* over time, its dispersion, and the panel that carries the variation.
* Correr con el wd en code/. Requiere data/build_dta.do ya corrido.

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
cap which listtab
if _rc ssc install listtab

global qr_q   = tq(2021q4)
global pull_q = tq(2022q3)

* ------------------------------------------------------------------
* 1. provincial adoption panel, quarterly
* ------------------------------------------------------------------
use "$proc/inclusion_prov.dta", clear
keep if n_pers_min1_cta < .
gen yq = qofd(dofm(ym))
format yq %tq
gen adop = 100 * n_pers_min1_cta_pago / n_pers_min1_cta
keep provincia yq adop
sort provincia yq

* spaghetti: 24 provinces plus the median
preserve
bysort yq: egen adop_med = median(adop)
separate adop, by(provincia) veryshortlabel
local greys
foreach v of varlist adop? adop?? {
    local greys `greys' (line `v' yq, lcolor(gs12) lwidth(thin))
}
twoway `greys' (line adop_med yq, lcolor(black) lwidth(thick)), ///
    xline($qr_q $pull_q, lcolor(black) lpattern(solid)) ///
    legend(off) xtitle("") ///
    ytitle("% de personas con cuenta que tienen cuenta de pago", size(small)) ///
    xlabel(, labsize(small)) ylabel(, labsize(small)) xsize(10) ysize(4.4)
graph export "$fig/mot_adopcion_spaghetti.pdf", replace
restore

* percentiles of adoption over time
preserve
collapse (p10) p10 = adop (p25) p25 = adop (p50) p50 = adop (p75) p75 = adop (p90) p90 = adop, by(yq)
twoway (line p10 yq, lcolor(gs11) lwidth(medthin)) ///
       (line p25 yq, lcolor(gs7) lwidth(medthin)) ///
       (line p50 yq, lcolor(black) lwidth(thick)) ///
       (line p75 yq, lcolor(gs7) lwidth(medthin)) ///
       (line p90 yq, lcolor(gs11) lwidth(medthin)), ///
    xline($qr_q $pull_q, lcolor(black) lpattern(solid)) ///
    legend(order(5 "p90" 4 "p75" 3 "p50" 2 "p25" 1 "p10") rows(1) size(small)) ///
    xtitle("") ytitle("% de personas con cuenta que tienen cuenta de pago", size(small)) ///
    xlabel(, labsize(small)) ylabel(, labsize(small)) xsize(10) ysize(4.4)
graph export "$fig/mot_adopcion_percentiles.pdf", replace
restore

* identifying variation, two views, each with and without Santa Fe
* (a) sd of the residual from province and quarter fixed effects
preserve
egen iprov = group(provincia)
reg adop i.iprov i.yq
predict res, resid
bysort yq: egen res_sd = sd(res)
keep yq res_sd
duplicates drop
tempfile rcon
save `rcon'
restore
preserve
drop if provincia == "SANTA FE"
egen iprov = group(provincia)
reg adop i.iprov i.yq
predict res, resid
collapse (sd) res_sd_sinsf = res, by(yq)
merge 1:1 yq using `rcon', nogen
twoway (line res_sd yq, lcolor(navy) lwidth(medthick)) ///
       (line res_sd_sinsf yq, lcolor(maroon) lwidth(medthick)), ///
    xline($qr_q $pull_q, lcolor(black) lpattern(solid)) ///
    legend(order(1 "Todas" 2 "Sin Santa Fe") size(small)) ///
    xtitle("") ytitle("Sd del residuo (FE provincia y trimestre), pp", size(small)) ///
    xlabel(, labsize(small)) ylabel(, labsize(small)) xsize(10) ysize(4.4)
graph export "$fig/mot_adopcion_sd_residuo.pdf", replace
restore

* (b) dispersion of quarterly adoption growth net of the national change
preserve
sort provincia yq
by provincia: gen d_adop = adop - adop[_n-1]
drop if d_adop == .
bysort yq: egen d_nac = mean(d_adop)
gen d_dif = d_adop - d_nac
bysort yq: egen d_sd = sd(d_dif)
keep yq d_sd
duplicates drop
tempfile dcon
save `dcon'
restore
preserve
drop if provincia == "SANTA FE"
sort provincia yq
by provincia: gen d_adop = adop - adop[_n-1]
drop if d_adop == .
bysort yq: egen d_nac = mean(d_adop)
gen d_dif = d_adop - d_nac
collapse (sd) d_sd_sinsf = d_dif, by(yq)
merge 1:1 yq using `dcon', nogen
twoway (line d_sd yq, lcolor(navy) lwidth(medthick)) ///
       (line d_sd_sinsf yq, lcolor(maroon) lwidth(medthick)), ///
    xline($qr_q $pull_q, lcolor(black) lpattern(solid)) ///
    legend(order(1 "Todas" 2 "Sin Santa Fe") size(small)) ///
    xtitle("") ytitle("Sd entre provincias del crecimiento trimestral diferencial, pp", size(small)) ///
    xlabel(, labsize(small)) ylabel(, labsize(small)) xsize(10) ysize(4.4)
graph export "$fig/mot_adopcion_sd_crecimiento.pdf", replace
restore

* growth by province around the reforms
preserve
keep if inlist(yq, tq(2021q3), tq(2022q4))
reshape wide adop, i(provincia) j(yq)
gen d_adop = adop`=tq(2022q4)' - adop`=tq(2021q3)'
gsort -d_adop
graph hbar (asis) d_adop, over(provincia, sort(d_adop) descending label(labsize(vsmall))) ///
    ytitle("Cambio en adopcion 2021q3 a 2022q4, pp", size(small)) ///
    ylabel(, labsize(small)) xsize(7) ysize(8)
graph export "$fig/mot_adopcion_cambio.pdf", replace
restore

* table: adoption by province at key dates, ordered by initial level
preserve
keep if inlist(yq, tq(2019q4), tq(2021q3), tq(2022q4), tq(2024q4))
reshape wide adop, i(provincia) j(yq)
rename adop`=tq(2019q4)' adop_2019q4
rename adop`=tq(2021q3)' adop_2021q3
rename adop`=tq(2022q4)' adop_2022q4
rename adop`=tq(2024q4)' adop_2024q4
gen d_post = adop_2022q4 - adop_2021q3
format adop_* d_post %9.1f
gsort -adop_2021q3
listtab provincia adop_2019q4 adop_2021q3 adop_2022q4 adop_2024q4 d_post ///
    using "$tab/mot_adopcion_prov.tex", replace rstyle(tabular) ///
    head("\begin{tabular}{lrrrrr}" "\toprule" ///
    "Provincia & 2019q4 & 2021q3 & 2022q4 & 2024q4 & $\Delta$ 21q3-22q4 \\" "\midrule") ///
    foot("\bottomrule" "\end{tabular}")
restore

* ------------------------------------------------------------------
* 2. the bank x province panel that carries the variation
* ------------------------------------------------------------------
use "$proc/prestamos_depositos_prov.dta", clear
gen yq = qofd(dofm(ym))
format yq %tq
keep if depositos_prov < . & depositos_prov > 0

* coverage: banks per province and provinces per bank, pre period
preserve
keep if ym == ym(2021,9)
bysort provincia: gen n_bancos = _N
bysort ent: gen n_prov = _N
sum n_bancos
di as result "bancos por provincia en 2021m9: min " r(min) " max " r(max)
sum n_prov
di as result "provincias por banco en 2021m9: min " r(min) " max " r(max)
restore

* summary table of the panel, pre period 2021
preserve
keep if inlist(ym, ym(2021,3), ym(2021,6), ym(2021,9))
gen dep_bn = depositos_prov_r / 1e9
gen pre_bn = prestamos_prov_r / 1e9
estpost tabstat dep_bn pre_bn suc_plenas atm, ///
    statistics(mean sd p10 p50 p90 count) columns(statistics)
esttab using "$tab/mot_panel_bp.tex", replace ///
    cells("mean(fmt(2)) sd(fmt(2)) p10(fmt(2)) p50(fmt(2)) p90(fmt(2)) count(fmt(0))") ///
    noobs nonumber nomtitle booktabs ///
    title("Panel banco x provincia, promedios trimestrales 2021 pre reforma")
restore

* ------------------------------------------------------------------
* 3. outcome side, raw: within bank share of business in high adoption
*    provinces (CABA excluded from the shares; terciles of A_p at 2021q3)
* ------------------------------------------------------------------
use "$proc/inclusion_prov.dta", clear
keep if ym == ym(2021,9)
gen adop = 100 * n_pers_min1_cta_pago / n_pers_min1_cta
xtile terc_adop = adop, nq(3)
keep provincia terc_adop
tempfile terc
save `terc'

use "$proc/prestamos_depositos_prov.dta", clear
gen yq = qofd(dofm(ym))
format yq %tq
keep if inlist(mod(ym,12), 2, 5, 8, 11)
keep if depositos_prov < . | prestamos_prov < .
drop if provincia == "CABA"
merge m:1 provincia using `terc', keep(match) nogen

* weight stability: w_bp with 2019 vs 2021 deposits
preserve
keep if inlist(yq, tq(2019q1), tq(2019q2), tq(2019q3), tq(2019q4)) | ///
        inlist(yq, tq(2021q1), tq(2021q2), tq(2021q3))
gen anio = cond(yq <= tq(2019q4), 2019, 2021)
collapse (mean) dep = depositos_prov, by(ent provincia anio)
reshape wide dep, i(ent provincia) j(anio)
bysort ent: egen t19 = total(dep2019)
bysort ent: egen t21 = total(dep2021)
drop if t19 <= 0 | t21 <= 0
gen w19 = dep2019 / t19
gen w21 = dep2021 / t21
corr w19 w21
local r : di %5.3f r(rho)
twoway (scatter w21 w19, mcolor(navy%50) msize(small)) ///
       (function y = x, range(0 1) lcolor(black)), ///
    legend(off) note("corr = `r'", size(small)) ///
    xtitle("Share de la provincia en los depositos del banco, 2019", size(small)) ///
    ytitle("Mismo share, 2021 pre reforma", size(small)) ///
    xlabel(, labsize(small)) ylabel(, labsize(small)) xsize(6) ysize(6)
graph export "$fig/out_pesos_estabilidad.pdf", replace
restore

* share of each bank in tercile 3 provinces, deposits and loans
foreach v in depositos prestamos {
    preserve
    keep if `v'_prov < .
    gen en_alta = `v'_prov * (terc_adop == 3)
    collapse (sum) en_alta tot = `v'_prov, by(ent yq)
    drop if tot <= 0
    gen sh_alta = 100 * en_alta / tot
    * simple mean across banks and aggregate (deposit weighted) share
    bysort yq: egen sh_simple = mean(sh_alta)
    bysort yq: egen num = total(en_alta)
    bysort yq: egen den = total(tot)
    gen sh_pond = 100 * num / den
    keep yq sh_simple sh_pond
    duplicates drop
    twoway (line sh_simple yq, lcolor(navy) lwidth(medthick)) ///
           (line sh_pond yq, lcolor(maroon) lwidth(medthick)), ///
        xline($qr_q $pull_q, lcolor(black) lpattern(solid)) ///
        legend(order(1 "Promedio simple entre bancos" 2 "Ponderado (sistema)") size(small)) ///
        xtitle("") ytitle("`v' del banco en provincias de adopcion alta, %", size(small)) ///
        xlabel(, labsize(small)) ylabel(, labsize(small)) xsize(10) ysize(4.4)
    graph export "$fig/out_share_alta_`v'.pdf", replace
    restore
}

* same deposit share, only banks present in high and low tercile pre
preserve
keep if depositos_prov < .
gen pre = inlist(yq, tq(2021q1), tq(2021q2), tq(2021q3))
bysort ent: egen dep_alta_pre = total(depositos_prov * (terc_adop == 3) * pre)
bysort ent: egen dep_baja_pre = total(depositos_prov * (terc_adop == 1) * pre)
keep if dep_alta_pre > 0 & dep_baja_pre > 0
gen en_alta = depositos_prov * (terc_adop == 3)
collapse (sum) en_alta tot = depositos_prov, by(ent yq)
drop if tot <= 0
gen sh_alta = 100 * en_alta / tot
bysort yq: gen n_bancos = _N
collapse (mean) sh_simple = sh_alta (max) n_bancos, by(yq)
sum n_bancos
di as result "bancos con presencia en terciles alto y bajo: " r(mean)
twoway line sh_simple yq, lcolor(navy) lwidth(medthick) ///
    xline($qr_q $pull_q, lcolor(black) lpattern(solid)) ///
    xtitle("") ytitle("Depositos en prov. adopcion alta, % (bancos en ambos terciles)", size(small)) ///
    xlabel(, labsize(small)) ylabel(, labsize(small)) xsize(10) ysize(4.4)
graph export "$fig/out_share_alta_within.pdf", replace
restore

* ------------------------------------------------------------------
* 4. provinces themselves: real deposits and loans by province,
*    high vs low adoption groups, CABA on its own line
* ------------------------------------------------------------------
use "$proc/prestamos_depositos_prov.dta", clear
gen yq = qofd(dofm(ym))
format yq %tq
keep if inlist(mod(ym,12), 2, 5, 8, 11)
collapse (sum) dep = depositos_prov_r pre = prestamos_prov_r, by(provincia yq)
drop if dep <= 0 | pre <= 0
merge m:1 provincia using `terc', nogen
replace terc_adop = . if provincia == "CABA"

foreach v in dep pre {
    local etiq = cond("`v'" == "dep", "Depositos", "Prestamos")
    preserve
    keep provincia yq `v' terc_adop
    bysort provincia (yq): gen b = `v' if yq == tq(2021q3)
    bysort provincia: egen base = max(b)
    gen i_`v' = 100 * `v' / base
    keep if i_`v' < .

    * spaghetti: every province, colored by adoption group
    separate i_`v', by(provincia) veryshortlabel
    local lo
    local hi
    foreach x of varlist i_`v'?* {
        qui sum terc_adop if `x' < ., meanonly
        if r(N) == 0 continue
        if r(mean) == 3 local hi `hi' (line `x' yq, lcolor(maroon%50) lwidth(thin))
        if r(mean) == 1 local lo `lo' (line `x' yq, lcolor(navy%50) lwidth(thin))
    }
    qui gen i_caba = i_`v' if provincia == "CABA"
    twoway `lo' `hi' (line i_caba yq, lcolor(black) lwidth(thick)), ///
        xline($qr_q $pull_q, lcolor(black) lpattern(solid)) ///
        legend(off) xtitle("") ///
        ytitle("`etiq' reales por provincia, 2021q3 = 100", size(small)) ///
        note("Bordo: adopcion alta. Azul: adopcion baja. Negro: CABA.", size(vsmall)) ///
        xlabel(, labsize(small)) ylabel(, labsize(small)) xsize(10) ysize(4.4)
    graph export "$fig/out_prov_spaghetti_`v'.pdf", replace
    restore

    * medians of each group
    preserve
    keep provincia yq `v' terc_adop
    bysort provincia (yq): gen b = `v' if yq == tq(2021q3)
    bysort provincia: egen base = max(b)
    gen i_`v' = 100 * `v' / base
    gen grupo = terc_adop
    replace grupo = 4 if provincia == "CABA"
    keep if inlist(grupo, 1, 3, 4)
    collapse (median) i_`v', by(grupo yq)
    reshape wide i_`v', i(yq) j(grupo)
    twoway (line i_`v'1 yq, lcolor(navy) lwidth(medthick)) ///
           (line i_`v'3 yq, lcolor(maroon) lwidth(medthick)) ///
           (line i_`v'4 yq, lcolor(black) lwidth(medthick)), ///
        xline($qr_q $pull_q, lcolor(black) lpattern(solid)) ///
        legend(order(2 "Adopcion alta (mediana)" 1 "Adopcion baja (mediana)" 3 "CABA") size(small)) ///
        xtitle("") ytitle("`etiq' reales por provincia, 2021q3 = 100", size(small)) ///
        xlabel(, labsize(small)) ylabel(, labsize(small)) xsize(10) ysize(4.4)
    graph export "$fig/out_prov_grupos_`v'.pdf", replace
    restore
}

di as result "listo: figuras mot_* y out_* en output/figuras, tablas mot_* en output/tablas"
