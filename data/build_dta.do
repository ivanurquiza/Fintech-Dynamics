* build_dta.do
* Builds the processed .dta files from the raw BCRA sources.
* Inputs:  data/Inclusion_financiera_BCRA/   (province-level series)
*          data/raw/ief/YYYYMM/              (monthly IEF files, one folder per month;
*                                             see descargar_ief_selectivo.py)
* Output:  data/processed/
* Run from the repo root: do data/build_dta.do
* Some months lack the provincial xlsx or inf_adi/indicad because the BCRA
* did not publish them; those months are skipped where relevant.

version 17
clear all
set more off

* repo root; adjust the path if your copy lives somewhere else
cap cd "~/Documents/GitHub/Fintech-Dynamics"

global inc "data/Inclusion_financiera_BCRA"
global ief "data/raw/ief"
global out "data/processed"
cap mkdir "$out"

* standardize province names across sources (case, accents, CABA synonyms)
cap program drop fix_prov
program define fix_prov
    args v
    replace `v' = ustrto(ustrnormalize(ustrupper(ustrtrim(`v')), "nfd"), "ascii", 2)
    replace `v' = "CABA" if inlist(`v', "CAPITAL FEDERAL", ///
        "CIUDAD AUTONOMA DE BUENOS AIRES", "CIUDAD DE BUENOS AIRES")
    drop if `v' == "TOTAL" | `v' == ""
    rename `v' provincia
end

* ------------------------------------------------------------------
* 1. inclusion_prov.dta: province x month panel
* ------------------------------------------------------------------

* share of adults with credit, all lenders
import delimited "$inc/BCRA_deudores_SFA_total_por_provincia.txt", ///
    varnames(1) encoding("latin1") bindquote(strict) stringcols(_all) clear
fix_prov tx_provincia
gen ym = ym(real(substr(cd_periodo,1,4)), real(substr(cd_periodo,5,2)))
gen pct_deud = real(subinstr(nu_valor, ",", ".", .))
keep provincia ym pct_deud
tempfile f1
save `f1'

* share of adults with credit, by lender group
import delimited "$inc/BCRA_deudores_SFA_por_grupo_institucional_y_provincia.txt", ///
    varnames(1) encoding("latin1") bindquote(strict) stringcols(_all) clear
fix_prov tx_provincia
gen ym = ym(real(substr(cd_periodo,1,4)), real(substr(cd_periodo,5,2)))
gen valor = real(subinstr(nu_valor, ",", ".", .))
gen grupo = ""
replace grupo = "opnfc" if strpos(tx_grupo, "OPNFC")
replace grupo = "pnfc"  if strpos(tx_grupo, "PNFC") & grupo == ""
replace grupo = "bpriv" if strpos(tx_grupo, "Privados")
replace grupo = "bpub"  if strpos(tx_grupo, "Public Banks")
replace grupo = "cf"    if strpos(tx_grupo, "Financial Companies")
replace grupo = "eeff"  if strpos(tx_grupo, "EEFF")
replace grupo = "tcnb"  if strpos(tx_grupo, "TCNB")
drop if grupo == ""
keep provincia ym grupo valor
reshape wide valor, i(provincia ym) j(grupo) string
rename valor* pct_deud_*
tempfile f2
save `f2'

* share of adults with credit, by product
import delimited "$inc/BCRA_deudores_SFA_por_tipo_asistencia_y_provincia.txt", ///
    varnames(1) encoding("latin1") bindquote(strict) stringcols(_all) clear
fix_prov tx_provincia
gen ym = ym(real(substr(cd_periodo,1,4)), real(substr(cd_periodo,5,2)))
gen valor = real(subinstr(nu_valor, ",", ".", .))
gen prod = ""
replace prod = "adelantos"    if strpos(tx_asistencia, "Adelantos")
replace prod = "hipotecarios" if strpos(tx_asistencia, "Hipotecarios")
replace prod = "personales"   if strpos(tx_asistencia, "Personales")
replace prod = "prendarios"   if strpos(tx_asistencia, "Prendarios")
replace prod = "tarjetas"     if strpos(tx_asistencia, "Credit")
drop if prod == ""
keep provincia ym prod valor
reshape wide valor, i(provincia ym) j(prod) string
rename valor* pct_deud_*
tempfile f3
save `f3'

* access points by type
import delimited "$inc/BCRA_puntos_acceso_por_tipo_y_provincia.txt", ///
    varnames(1) encoding("latin1") bindquote(strict) stringcols(_all) clear
fix_prov tx_provincia
gen ym = ym(real(substr(cd_periodo,1,4)), real(substr(cd_periodo,5,2)))
gen valor = real(subinstr(nu_pda, ",", ".", .))
gen tipo = ""
replace tipo = "acsf"      if strpos(tx_tipopda, "ACSF")
replace tipo = "atm"       if strpos(tx_tipopda, "ATM")
replace tipo = "suc_movil" if strpos(tx_tipopda, "Mobile")
replace tipo = "suc"       if strpos(tx_tipopda, "Sucursales")
replace tipo = "tas"       if strpos(tx_tipopda, "TAS")
drop if tipo == ""
keep provincia ym tipo valor
reshape wide valor, i(provincia ym) j(tipo) string
rename valor* pda_*

merge 1:1 provincia ym using `f3', nogen
merge 1:1 provincia ym using `f2', nogen
merge 1:1 provincia ym using `f1', nogen
format ym %tm
sort provincia ym
save "$out/inclusion_prov.dta", replace

* ------------------------------------------------------------------
* 2. tenencia_cuentas_prov.dta: province x quarter, account holdings
* ------------------------------------------------------------------

import delimited "$inc/BCRA_tenencia_cuentas_bancarias_y_de_pago_por_provincia.txt", ///
    varnames(1) encoding("latin1") bindquote(strict) stringcols(_all) clear
fix_prov tx_provincia
gen ym = ym(real(substr(cd_periodo,1,4)), real(substr(cd_periodo,5,2)))
gen yq = qofd(dofm(ym))
gen valor = real(subinstr(nu_valor, ",", ".", .))
gen tipo = ""
replace tipo = "ambas"           if strpos(tx_tipo_cuenta, "Bank and payment")
replace tipo = "solo_bancaria"   if strpos(tx_tipo_cuenta, "Only bank")
replace tipo = "solo_pago"       if strpos(tx_tipo_cuenta, "Only payment")
replace tipo = "almenos_bancaria" if strpos(tx_tipo_cuenta, "one bank")
replace tipo = "almenos_pago"    if strpos(tx_tipo_cuenta, "one payment")
replace tipo = "almenos_una"     if strpos(tx_tipo_cuenta, "one account")
drop if tipo == ""
keep provincia yq tipo valor
reshape wide valor, i(provincia yq) j(tipo) string
rename valor* n_cuentas_*
format yq %tq
sort provincia yq
save "$out/tenencia_cuentas_prov.dta", replace

* ------------------------------------------------------------------
* 3. balances_bancos.dta: bank x month, balance sheet items as columns
* ------------------------------------------------------------------
* Selected accounts from baldet (codes are stable over 2018-2025):
*   100000 assets            110000 cash             120000 securities
*   130000 loans             131700 loans priv sector (pesos, principal)
*   300000 liabilities       310000 deposits         311700 deposits priv sector
*   311706 checking accts    311718 savings accts    311726 payroll accts
*   311740 time deposits     400000 equity           500000 profits

local dirs : dir "$ief" dirs "2*"
local dirs : list sort dirs
tempfile bal
local first = 1
foreach m of local dirs {
    cap confirm file "$ief/`m'/baldet.txt"
    if _rc continue
    qui {
        import delimited "$ief/`m'/baldet.txt", delimiters(tab) ///
            varnames(nonames) encoding("latin1") bindquote(strict) stringcols(_all) clear
        keep if inlist(v4, "100000", "110000", "120000", "130000", "131700", "300000", "310000") | ///
            inlist(v4, "311700", "311706", "311718", "311726", "311740", "400000", "500000")
        gen ent    = real(v1)
        gen nombre = v2
        gen ym     = ym(real(substr(v3,1,4)), real(substr(v3,5,2)))
        gen double saldo = real(v6) + real(v7)   // one of the two sides is always zero
        keep ent nombre ym v4 saldo
        reshape wide saldo, i(ent ym) j(v4) string
        if `first' == 0 append using `bal'
        local first = 0
        save `bal', replace
    }
}
use `bal', clear
rename saldo100000 activo
rename saldo110000 efectivo
rename saldo120000 titulos
rename saldo130000 prestamos
rename saldo131700 prest_spnf
rename saldo300000 pasivo
rename saldo310000 depositos
rename saldo311700 dep_spnf
rename saldo311706 dep_ctacte
rename saldo311718 dep_cajaahorro
rename saldo311726 dep_ctasueldo
rename saldo311740 dep_pfijo
rename saldo400000 pn
rename saldo500000 resultados
format ym %tm
sort ent ym
save "$out/balances_bancos.dta", replace

* ------------------------------------------------------------------
* 4. prestamos_depositos_prov.dta: bank x province x month
* ------------------------------------------------------------------
* Branches and ATMs come from suc_pcia (all months); loan and deposit
* amounts come from the distribgeo xlsx (missing in a few months of 2020).

tempfile suc
local first = 1
foreach m of local dirs {
    cap confirm file "$ief/`m'/suc_pcia.txt"
    if _rc continue
    qui {
        import delimited "$ief/`m'/suc_pcia.txt", delimiters(tab) ///
            varnames(nonames) encoding("latin1") bindquote(strict) stringcols(_all) clear
        fix_prov v5
        gen ent = real(v1)
        gen nombre = v2
        gen ym = ym(real(substr("`m'",1,4)), real(substr("`m'",5,2)))
        * the column layout changed in 2021m4; the old files carry extra
        * columns (pending and total branches) and a different ordering
        cap confirm variable v15
        if _rc == 0 {
            gen suc_plenas  = real(v6)
            gen suc_esp     = real(v14)
            gen suc_moviles = real(v9)
            gen dep_autom   = real(v10)
            gen atm         = real(v11)
            gen tas         = real(v12)
            gen promocion   = real(v13)
            gen acsf        = .   // not reported before 2021m4
        }
        else {
            gen suc_plenas  = real(v6)
            gen suc_esp     = real(v7)
            gen suc_moviles = real(v8)
            gen dep_autom   = real(v9)
            gen atm         = real(v10)
            gen tas         = real(v11)
            gen promocion   = real(v12)
            gen acsf        = real(v13)
        }
        drop if missing(ent)   // system and group aggregates (AA rows)
        keep ent nombre provincia ym suc_* dep_autom atm tas promocion acsf
        if `first' == 0 append using `suc'
        local first = 0
        save `suc', replace
    }
}

tempfile geo
local first = 1
foreach m of local dirs {
    cap confirm file "$ief/`m'/prestamos_depositos_prov.xlsx"
    if _rc continue
    qui {
        import excel "$ief/`m'/prestamos_depositos_prov.xlsx", cellrange(A5) allstring clear
        drop if missing(B) | missing(D)
        fix_prov D
        gen ent = real(B)
        * the xlsx holds the last closed quarter, which is not the folder month:
        * date it with its own Fecha column (yyyymmdd)
        gen ym = ym(real(substr(A,1,4)), real(substr(A,5,2)))
        gen double prestamos_prov = real(E)
        gen double depositos_prov = real(F)
        keep ent provincia ym prestamos_prov depositos_prov
        drop if missing(ent) | missing(ym)
        if `first' == 0 append using `geo'
        local first = 0
        save `geo', replace
    }
}
* consecutive monthly folders repeat the same quarter; keep one copy
use `geo', clear
duplicates drop ent provincia ym, force
save `geo', replace

use `suc', clear
* Banco Macro appears twice in Tucuman during 2019m11-2021m3 (accent
* artifact in the raw files); add up the duplicated rows
collapse (sum) suc_plenas suc_esp suc_moviles dep_autom atm tas promocion acsf, ///
    by(ent nombre provincia ym)
replace acsf = . if ym < ym(2021,4)   // collapse turns all-missing into zero
isid ent provincia ym
* amounts are quarterly, so they only fill the quarter-end months
merge 1:1 ent provincia ym using `geo', nogen
format ym %tm
sort ent provincia ym
save "$out/prestamos_depositos_prov.dta", replace

* ------------------------------------------------------------------
* 5. caracteristicas_bancos.dta: bank x month, long format
* ------------------------------------------------------------------
* From inf_adi (accounts, cards, staff), indicad (indicators) and esd
* (debtor status). Columns 6-10 of the raw files hold the last five
* balance dates; we keep column 10, the most recent one.

tempfile car
local first = 1
foreach m of local dirs {
    foreach s in inf_adi indicad esd {
        cap confirm file "$ief/`m'/`s'.txt"
        if _rc continue
        qui {
            import delimited "$ief/`m'/`s'.txt", delimiters(tab) ///
                varnames(nonames) encoding("latin1") bindquote(strict) stringcols(_all) clear
            cap confirm variable v10
            if _rc continue
            gen ent    = real(v1)
            gen nombre = v2
            gen ym     = ym(real(substr("`m'",1,4)), real(substr("`m'",5,2)))
            gen fuente = "`s'"
            gen codigo = v4
            gen descripcion = v5
            gen double valor = real(v10)
            drop if missing(ent)   // system and group aggregates (AA rows)
            keep ent nombre ym fuente codigo descripcion valor
            if `first' == 0 append using `car'
            local first = 0
            save `car', replace
        }
    }
}
use `car', clear
format ym %tm
sort ent ym fuente codigo
save "$out/caracteristicas_bancos.dta", replace

di as text "done: 5 files written to $out"
