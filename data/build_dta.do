* build_dta.do
* Builds the processed .dta files from the raw BCRA sources.
* Inputs:  Inclusion_financiera_BCRA/   (province-level txt, utf-8)
*          raw/ief/YYYYMM/              (monthly IEF files, latin-1; see
*                                        descargar_ief_selectivo.py)
* Output:  processed/
* Run with the working directory in data/.
* Some months lack the provincial xlsx or inf_adi/indicad because the BCRA
* did not publish them; those months are skipped where relevant.

version 17
clear all
set more off

* paths are relative to data/, where this file lives
global inc "Inclusion_financiera_BCRA"
global ief "raw/ief"
global out "processed"
cap mkdir "$out"

* ------------------------------------------------------------------
* helpers
* ------------------------------------------------------------------

* Standardize province names. The sources disagree on spelling: accents on
* and off, "CABA" vs "CIUDAD DE BUENOS AIRES - CAPITAL FEDERAL" (with three
* different spacings in the xlsx), "TIERRA DE FUEGO" (sic) in the old
* suc_pcia files, and the long official Tierra del Fuego name in the PDA txt.
* The xlsx also splits Buenos Aires into "GRAN BUENOS AIRES" and "RESTO DE
* LA PROVINCIA DE BUENOS AIRES"; both are mapped to BUENOS AIRES and summed
* later, to keep one row per province.
cap program drop fix_prov
program define fix_prov
    args v
    replace `v' = ustrto(ustrnormalize(ustrupper(ustrtrim(`v')), "nfd"), "ascii", 2)
    drop if `v' == "TOTAL" | `v' == ""
    replace `v' = "CABA" if strpos(`v', "CAPITAL") | strpos(`v', "CIUDAD")
    replace `v' = "TIERRA DEL FUEGO" if strpos(`v', "TIERRA D")
    replace `v' = "BUENOS AIRES" if strpos(`v', "GRAN BUENOS") | strpos(`v', "RESTO DE LA PROV")
    rename `v' provincia
end

* Stop if a province name survived outside the canonical list of 24
cap program drop chk_prov
program define chk_prov
    qui levelsof provincia, local(provs)
    assert `: word count `provs'' == 24
end

* ------------------------------------------------------------------
* 1. inclusion_prov.dta: province x month panel
* ------------------------------------------------------------------

* share of adults with credit, all lenders
import delimited "$inc/BCRA_deudores_SFA_total_por_provincia.txt", ///
    varnames(1) bindquote(strict) stringcols(_all) clear
fix_prov tx_provincia
gen ym = ym(real(substr(cd_periodo,1,4)), real(substr(cd_periodo,5,2)))
gen pct_adultos_credito = real(subinstr(nu_valor, ",", ".", .))
keep provincia ym pct_adultos_credito
tempfile f1
save `f1'

* share of adults with credit, by lender group
import delimited "$inc/BCRA_deudores_SFA_por_grupo_institucional_y_provincia.txt", ///
    varnames(1) bindquote(strict) stringcols(_all) clear
fix_prov tx_provincia
gen ym = ym(real(substr(cd_periodo,1,4)), real(substr(cd_periodo,5,2)))
gen valor = real(subinstr(nu_valor, ",", ".", .))
gen grupo = ""
replace grupo = "opnfc"       if strpos(tx_grupo, "OPNFC")
replace grupo = "pnfc"        if strpos(tx_grupo, "PNFC") & grupo == ""
replace grupo = "bcos_priv"   if strpos(tx_grupo, "Privados")
replace grupo = "bcos_pub"    if strpos(tx_grupo, "Public Banks")
replace grupo = "comp_fin"    if strpos(tx_grupo, "Financial Companies")
replace grupo = "ent_fin"     if strpos(tx_grupo, "EEFF")
replace grupo = "tarj_nobanc" if strpos(tx_grupo, "TCNB")
drop if grupo == ""
keep provincia ym grupo valor
reshape wide valor, i(provincia ym) j(grupo) string
rename valor* pct_adultos_cred_*
tempfile f2
save `f2'

* share of adults with credit, by product
import delimited "$inc/BCRA_deudores_SFA_por_tipo_asistencia_y_provincia.txt", ///
    varnames(1) bindquote(strict) stringcols(_all) clear
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
rename valor* pct_adultos_cred_*
tempfile f3
save `f3'

* access points by type
import delimited "$inc/BCRA_puntos_acceso_por_tipo_y_provincia.txt", ///
    varnames(1) bindquote(strict) stringcols(_all) clear
fix_prov tx_provincia
gen ym = ym(real(substr(cd_periodo,1,4)), real(substr(cd_periodo,5,2)))
gen valor = real(subinstr(nu_pda, ",", ".", .))
gen tipo = ""
replace tipo = "acsf"               if strpos(tx_tipopda, "ACSF")
replace tipo = "atm"                if strpos(tx_tipopda, "ATM")
replace tipo = "sucursales_moviles" if strpos(tx_tipopda, "Mobile")
replace tipo = "sucursales"         if strpos(tx_tipopda, "Sucursales")
replace tipo = "tas"                if strpos(tx_tipopda, "TAS")
drop if tipo == ""
keep provincia ym tipo valor
reshape wide valor, i(provincia ym) j(tipo) string
rename valor* n_*

merge 1:1 provincia ym using `f3', nogen
merge 1:1 provincia ym using `f2', nogen
merge 1:1 provincia ym using `f1', nogen
chk_prov
format ym %tm

label var provincia "Provincia"
label var ym "Mes"
label var pct_adultos_credito "% de adultos con financiamiento en el sistema financiero ampliado"
label var pct_adultos_cred_bcos_priv "% de adultos con financiamiento de bancos privados"
label var pct_adultos_cred_bcos_pub "% de adultos con financiamiento de bancos publicos"
label var pct_adultos_cred_comp_fin "% de adultos con financiamiento de companias financieras"
label var pct_adultos_cred_ent_fin "% de adultos con financiamiento de entidades financieras (EEFF)"
label var pct_adultos_cred_opnfc "% de adultos con financ. de otros proveedores no financieros (OPNFC)"
label var pct_adultos_cred_pnfc "% de adultos con financ. de proveedores no financieros de credito (PNFC)"
label var pct_adultos_cred_tarj_nobanc "% de adultos con financiamiento de tarjetas no bancarias (TCNB)"
label var pct_adultos_cred_adelantos "% de adultos con adelantos"
label var pct_adultos_cred_hipotecarios "% de adultos con credito hipotecario"
label var pct_adultos_cred_personales "% de adultos con prestamos personales"
label var pct_adultos_cred_prendarios "% de adultos con credito prendario"
label var pct_adultos_cred_tarjetas "% de adultos con tarjeta de credito"
label var n_sucursales "Sucursales (cantidad)"
label var n_sucursales_moviles "Sucursales moviles (cantidad)"
label var n_atm "Cajeros automaticos ATM (cantidad)"
label var n_tas "Terminales de autoservicio (cantidad)"
label var n_acsf "Agencias complementarias de servicios financieros (cantidad)"
label data "Inclusion financiera BCRA, provincia x mes"
sort provincia ym
save "$out/inclusion_prov.dta", replace

* ------------------------------------------------------------------
* 2. tenencia_cuentas_prov.dta: province x quarter, account holdings
* ------------------------------------------------------------------

import delimited "$inc/BCRA_tenencia_cuentas_bancarias_y_de_pago_por_provincia.txt", ///
    varnames(1) bindquote(strict) stringcols(_all) clear
fix_prov tx_provincia
gen ym = ym(real(substr(cd_periodo,1,4)), real(substr(cd_periodo,5,2)))
gen yq = qofd(dofm(ym))
gen valor = real(subinstr(nu_valor, ",", ".", .))
gen tipo = ""
replace tipo = "ambas_ctas"        if strpos(tx_tipo_cuenta, "Bank and payment")
replace tipo = "solo_cta_bancaria" if strpos(tx_tipo_cuenta, "Only bank")
replace tipo = "solo_cta_pago"     if strpos(tx_tipo_cuenta, "Only payment")
replace tipo = "min1_cta_bancaria" if strpos(tx_tipo_cuenta, "one bank")
replace tipo = "min1_cta_pago"     if strpos(tx_tipo_cuenta, "one payment")
replace tipo = "min1_cta"          if strpos(tx_tipo_cuenta, "one account")
drop if tipo == ""
keep provincia yq tipo valor
reshape wide valor, i(provincia yq) j(tipo) string
rename valor* n_pers_*
chk_prov
format yq %tq

label var provincia "Provincia"
label var yq "Trimestre"
label var n_pers_solo_cta_bancaria "Personas con cuenta bancaria (CBU) solamente"
label var n_pers_solo_cta_pago "Personas con cuenta de pago (CVU) solamente"
label var n_pers_ambas_ctas "Personas con cuenta bancaria y de pago"
label var n_pers_min1_cta_bancaria "Personas con al menos una cuenta bancaria"
label var n_pers_min1_cta_pago "Personas con al menos una cuenta de pago"
label var n_pers_min1_cta "Personas con al menos una cuenta"
label data "Tenencia de cuentas bancarias y de pago BCRA, provincia x trimestre"
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

label var ent "Codigo de entidad BCRA"
label var nombre "Nombre de la entidad"
label var ym "Mes"
label var activo "Activo total"
label var efectivo "Efectivo y depositos en bancos"
label var titulos "Titulos publicos y privados"
label var prestamos "Prestamos (total)"
label var prest_spnf "Prestamos al sector privado no financiero (pesos, capitales)"
label var pasivo "Pasivo total"
label var depositos "Depositos (total)"
label var dep_spnf "Depositos del sector privado no financiero (pesos, capitales)"
label var dep_ctacte "Depositos SPNF en cuenta corriente"
label var dep_cajaahorro "Depositos SPNF en caja de ahorros"
label var dep_ctasueldo "Depositos SPNF en cuenta sueldo y previsional"
label var dep_pfijo "Depositos SPNF a plazo fijo"
label var pn "Patrimonio neto"
label var resultados "Resultados"
label data "Balances mensuales por entidad, IEF BCRA (baldet)"
sort ent ym
save "$out/balances_bancos.dta", replace

* ------------------------------------------------------------------
* 4. prestamos_depositos_prov.dta: bank x province x month
* ------------------------------------------------------------------
* Branches and ATMs come from suc_pcia (all months); loan and deposit
* amounts come from the distribgeo xlsx (quarterly, missing in a few
* months of 2020).

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
        * the xlsx holds the last closed quarter, which is not the folder
        * month: date it with its own Fecha column (yyyymmdd)
        gen ym = ym(real(substr(A,1,4)), real(substr(A,5,2)))
        gen double prestamos_prov = real(E)
        gen double depositos_prov = real(F)
        keep ent provincia ym prestamos_prov depositos_prov
        drop if missing(ent) | missing(ym)
        * add up GBA and the rest of Buenos Aires province
        collapse (sum) prestamos_prov depositos_prov, by(ent provincia ym)
        if `first' == 0 append using `geo'
        local first = 0
        save `geo', replace
    }
}
* consecutive monthly folders repeat the same quarter; keep one copy
use `geo', clear
duplicates drop ent provincia ym, force

tempfile geoq
save `geoq'
use `suc', clear
* Banco Macro appears twice in Tucuman during 2019m11-2021m3 (accent
* artifact in the raw files); add up the duplicated rows
collapse (sum) suc_plenas suc_esp suc_moviles dep_autom atm tas promocion acsf, ///
    by(ent nombre provincia ym)
replace acsf = . if ym < ym(2021,4)   // collapse turns all-missing into zero
isid ent provincia ym
* amounts are quarterly, so they only fill the quarter-end months
merge 1:1 ent provincia ym using `geoq', nogen
chk_prov
format ym %tm

label var ent "Codigo de entidad BCRA"
label var nombre "Nombre de la entidad"
label var provincia "Provincia"
label var ym "Mes"
label var suc_plenas "Sucursales plenas habilitadas"
label var suc_esp "Sucursales de operatoria especifica habilitadas"
label var suc_moviles "Sucursales moviles habilitadas"
label var dep_autom "Dependencias automatizadas habilitadas"
label var atm "Cajeros automaticos habilitados"
label var tas "Terminales de autoservicio habilitadas"
label var promocion "Puestos de promocion habilitados"
label var acsf "Agencias complementarias de serv. financieros (desde 2021m4)"
label var prestamos_prov "Prestamos del banco en la provincia (trimestral, distribgeo IEF)"
label var depositos_prov "Depositos del banco en la provincia (trimestral, distribgeo IEF)"
label data "Presencia y negocio por banco x provincia, IEF BCRA"
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

label var ent "Codigo de entidad BCRA"
label var nombre "Nombre de la entidad"
label var ym "Mes"
label var fuente "Archivo IEF de origen (inf_adi, indicad o esd)"
label var codigo "Codigo de linea BCRA"
label var descripcion "Descripcion de la linea"
label var valor "Valor a la fecha mas reciente del archivo"
label data "Caracteristicas por banco x mes, IEF BCRA (formato largo)"
sort ent ym fuente codigo
save "$out/caracteristicas_bancos.dta", replace

di as text "done: 5 files written to $out"
