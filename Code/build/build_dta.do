* build_dta.do
* Builds the processed .dta files from the raw BCRA sources.
* Inputs:  Data/raw/bcra_inclusion/   (province-level txt, utf-8)
*          Data/raw/bcra_ief/YYYYMM/              (monthly IEF files, latin-1; see
*                                        descargar_ief_selectivo.py)
*          $Data/raw/ipc/sh_ipc.xls           (INDEC CPI, national and regional)
* Money variables in balances_bancos and prestamos_depositos_prov are
* expressed at January 2026 prices, deflated with the national CPI.
* Output:  Data/processed/
* Run from anywhere inside the repo.
* Some months lack the provincial xlsx or inf_adi/indicad because the BCRA
* did not publish them; those months are skipped where relevant.

version 17
clear all
set more off

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
cap mkdir "$proc"

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
import delimited "$raw/bcra_inclusion/BCRA_deudores_SFA_total_por_provincia.txt", ///
    varnames(1) bindquote(strict) stringcols(_all) clear
fix_prov tx_provincia
gen ym = ym(real(substr(cd_periodo,1,4)), real(substr(cd_periodo,5,2)))
gen pct_adultos_credito = real(subinstr(nu_valor, ",", ".", .))
keep provincia ym pct_adultos_credito
tempfile f1
save `f1'

* share of adults with credit, by lender group
import delimited "$raw/bcra_inclusion/BCRA_deudores_SFA_por_grupo_institucional_y_provincia.txt", ///
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
import delimited "$raw/bcra_inclusion/BCRA_deudores_SFA_por_tipo_asistencia_y_provincia.txt", ///
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
import delimited "$raw/bcra_inclusion/BCRA_puntos_acceso_por_tipo_y_provincia.txt", ///
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
save "$proc/inclusion_prov.dta", replace

* ------------------------------------------------------------------
* 2. account holdings, folded into the same province x month panel
* ------------------------------------------------------------------
* The series is quarterly (only March, June, September and December show
* up in the raw file), so these variables are filled in quarter-end
* months and missing in between.

import delimited "$raw/bcra_inclusion/BCRA_tenencia_cuentas_bancarias_y_de_pago_por_provincia.txt", ///
    varnames(1) bindquote(strict) stringcols(_all) clear
fix_prov tx_provincia
gen ym = ym(real(substr(cd_periodo,1,4)), real(substr(cd_periodo,5,2)))
gen valor = real(subinstr(nu_valor, ",", ".", .))
gen tipo = ""
replace tipo = "ambas_ctas"        if strpos(tx_tipo_cuenta, "Bank and payment")
replace tipo = "solo_cta_bancaria" if strpos(tx_tipo_cuenta, "Only bank")
replace tipo = "solo_cta_pago"     if strpos(tx_tipo_cuenta, "Only payment")
replace tipo = "min1_cta_bancaria" if strpos(tx_tipo_cuenta, "one bank")
replace tipo = "min1_cta_pago"     if strpos(tx_tipo_cuenta, "one payment")
replace tipo = "min1_cta"          if strpos(tx_tipo_cuenta, "one account")
drop if tipo == ""
keep provincia ym tipo valor
reshape wide valor, i(provincia ym) j(tipo) string
rename valor* n_pers_*
chk_prov
tempfile ften
save `ften'

use "$proc/inclusion_prov.dta", clear
merge 1:1 provincia ym using `ften', nogen
chk_prov
label var n_pers_solo_cta_bancaria "Personas con cuenta bancaria (CBU) solamente (trimestral)"
label var n_pers_solo_cta_pago "Personas con cuenta de pago (CVU) solamente (trimestral)"
label var n_pers_ambas_ctas "Personas con cuenta bancaria y de pago (trimestral)"
label var n_pers_min1_cta_bancaria "Personas con al menos una cuenta bancaria (trimestral)"
label var n_pers_min1_cta_pago "Personas con al menos una cuenta de pago (trimestral)"
label var n_pers_min1_cta "Personas con al menos una cuenta (trimestral)"
sort provincia ym
save "$proc/inclusion_prov.dta", replace

* ------------------------------------------------------------------
* 3. ipc.dta: INDEC CPI, national and by region (dec-2016 = 100)
* ------------------------------------------------------------------
* Row positions checked against the July 2026 release of sh_ipc.xls
* (dates in row 6, "Nivel general" in rows 10/40/70/100/130/160/190);
* re-check them if the file is replaced by a newer release.

import excel "$raw/ipc/sh_ipc.xls", sheet("Índices IPC Cobertura Nacional") allstring clear
keep if inlist(_n, 10, 40, 70, 100, 130, 160, 190)
drop A
destring _all, replace force
xpose, clear
drop if missing(v1)
* columns are consecutive months starting December 2016
gen ym = ym(2016,12) + _n - 1
assert inrange(v1[1], 99.9, 100.1)   // base month must equal 100
rename v1 ipc_nacional
rename v2 ipc_gba
rename v3 ipc_pampeana
rename v4 ipc_noroeste
rename v5 ipc_noreste
rename v6 ipc_cuyo
rename v7 ipc_patagonia
order ym
format ym %tm

label var ym "Mes"
label var ipc_nacional "IPC nivel general, total nacional (dic-2016=100)"
label var ipc_gba "IPC nivel general, region GBA (dic-2016=100)"
label var ipc_pampeana "IPC nivel general, region Pampeana (dic-2016=100)"
label var ipc_noroeste "IPC nivel general, region Noroeste (dic-2016=100)"
label var ipc_noreste "IPC nivel general, region Noreste (dic-2016=100)"
label var ipc_cuyo "IPC nivel general, region Cuyo (dic-2016=100)"
label var ipc_patagonia "IPC nivel general, region Patagonia (dic-2016=100)"
label data "IPC INDEC, nacional y regiones"
sort ym
save "$proc/ipc.dta", replace

qui su ipc_nacional if ym == ym(2026,1), meanonly
assert r(N) == 1   // stop here if the January 2026 index is not in the file
global ipc_base = r(mean)

* ------------------------------------------------------------------
* 4. balances_bancos.dta: bank x month, balance sheet items as columns
* ------------------------------------------------------------------
* Selected accounts from baldet (codes are stable over 2018-2025):
*   100000 assets            110000 cash             120000 securities
*   130000 loans             131700 loans priv sector (pesos, principal)
*   300000 liabilities       310000 deposits         311700 deposits priv sector
*   311706 checking accts    311718 savings accts    311726 payroll accts
*   311740 time deposits     400000 equity           500000 profits
* wholesale / remunerated funding, the leg that FCI money market funds and
* payment providers (PSP) use.  There is no partida by depositor type, so
* these are instrument-level proxies:
*   311712 interest-bearing checking accounts
*   311723 special checking acct for legal persons, no interest
*   311724 special checking acct for legal persons, interest bearing
*   311736 term deposits with an early cancellation option, transferable
*   311744 same, non transferable
* 311724 and 311736/311744 are the instruments a money market fund can hold
* under efectivo minimo 1.3.12; PSP client funds sit in some sight account
* (1.3.14) but the plan de cuentas does not separate them.

local dirs : dir "$raw/bcra_ief" dirs "2*"
local dirs : list sort dirs

* institutional classification, from entint (monthly, so ownership or
* charter changes are picked up when they happen):
*   AA100 banks, AA110 public, AA120 private, AA121 private domestic,
*   AA123/AA124 foreign (local subsidiary / branch), AA200 finance
*   companies, AA210 domestic, AA220 foreign, AA910 top 10 private banks
tempfile clasif
local first = 1
foreach m of local dirs {
    cap confirm file "$raw/bcra_ief/`m'/entint.txt"
    if _rc continue
    qui {
        import delimited "$raw/bcra_ief/`m'/entint.txt", delimiters(tab) ///
            varnames(nonames) encoding("latin1") bindquote(strict) stringcols(_all) clear
        gen ent = real(v1)
        drop if missing(ent)
        gen ym = ym(real(substr("`m'",1,4)), real(substr("`m'",5,2)))
        gen byte es_banco            = v4 == "AA100"
        gen byte banco_publico       = v4 == "AA110"
        gen byte banco_privado       = v4 == "AA120"
        gen byte banco_capnacional   = v4 == "AA121"
        gen byte banco_capextranjero = inlist(v4, "AA123", "AA124")
        gen byte cia_financiera      = v4 == "AA200"
        gen byte cia_fin_extranjera  = v4 == "AA220"
        gen byte top10_privados      = v4 == "AA910"
        collapse (max) es_banco banco_publico banco_privado banco_capnacional ///
            banco_capextranjero cia_financiera cia_fin_extranjera top10_privados, ///
            by(ent ym)
        if `first' == 0 append using `clasif'
        local first = 0
        save `clasif', replace
    }
}

tempfile bal
local first = 1
* account codes kept from baldet. Deposits: 31 + currency/residence (1 pesos
* resident, 5 fx resident) + sector (1 public, 4 financial, 7 private) +
* instrument. Results (5xxxxx) are cumulative within the fiscal year.
local codes_tot   "100000 110000 120000 130000 131700 135700 140000 300000 310000 311000 315000 320000 400000 500000 510000 520000 521000 525000 560000"
local codes_sect  "311100 311400 311700 315100 315400 315700 311106 311112 311131 311140 311156 311167"
local codes_ars   "311706 311712 311718 311722 311723 311724 311725 311726 311730 311731 311735 311736 311738 311740 311742 311744 311745 311747 311751 311753 311754 311766 311767 311783 311785 311786 311788 311789 311790 311791 311792 311793"
local codes_usd   "315706 315712 315718 315723 315724 315725 315731 315732 315733 315737 315742 315743 315751 315753 315754 315781 315783 315784 315785 315786 315787 315788 315790 315791 315792 315793 315794"
local codes_egr   "521003 521021 521062 521063 521064 521065 521080 521092 521093 521112 521113 525003 525062 525063 525064 525065"
* asset side: liquidity instruments of the BCRA and the Treasury, plus the
* accounts that hold reserve requirements. Species-level accounts open and
* close with the instrument: LELIQ ends 2024m1, LEFI runs 2024m7-2025m6.
local codes_act   "111015 111017 111021 111025 121000 125000 121003 121016 121040 121058 121091 121092 121093 125003 125016 125042 125058"
local codes_pase  "141104 141124 141134 141143 141144 141433 145120 141153 141169 141170 145153"
local codes_ing   "511047 511048 511049 511050 511051 511052 511053 511054 511107 511111 511113"
local codes_all   "`codes_tot' `codes_sect' `codes_ars' `codes_usd' `codes_egr' `codes_ing' `codes_act' `codes_pase'"
foreach m of local dirs {
    cap confirm file "$raw/bcra_ief/`m'/baldet.txt"
    if _rc continue
    qui {
        import delimited "$raw/bcra_ief/`m'/baldet.txt", delimiters(tab) ///
            varnames(nonames) encoding("latin1") bindquote(strict) stringcols(_all) clear
        gen byte keep_ = 0
        foreach c of local codes_all {
            replace keep_ = 1 if v4 == "`c'"
        }
        keep if keep_
        drop keep_
        gen ent    = real(v1)
        gen nombre = v2
        gen ym     = ym(real(substr(v3,1,4)), real(substr(v3,5,2)))
        * signed balance: assets carry a debit balance, liabilities, equity
        * and results a credit one; this keeps the sign of losses right
        gen double saldo = cond(inlist(substr(v4,1,1), "1", "2"), ///
            real(v6) - real(v7), real(v7) - real(v6))
        gen pub = "`m'"   // publication month of the file
        keep ent nombre ym v4 saldo pub
        reshape wide saldo, i(ent ym) j(v4) string
        if `first' == 0 append using `bal'
        local first = 0
        save `bal', replace
    }
}
use `bal', clear
* files also carry balances of late-reporting banks for earlier months, so
* the same bank-month can show up in more than one file; keep the most
* recent publication
bysort ent ym (pub): keep if _n == _N
drop pub
* the january 2018 files also carry a handful of late 2017m12 balances,
* too few to form a usable month
keep if ym >= ym(2018,1)
* a missing account in a reporting bank is a zero balance, not missing data
foreach v of varlist saldo* {
    replace `v' = 0 if `v' == . & saldo100000 < .
}

* totals and assets
rename saldo100000 activo
rename saldo110000 efectivo
rename saldo120000 titulos
rename saldo130000 prestamos
rename saldo131700 prest_spnf
rename saldo135700 prest_spnf_usd
rename saldo140000 otros_cred_if
rename saldo300000 pasivo
rename saldo310000 depositos
rename saldo311000 dep_ars_res
rename saldo315000 dep_usd_res
rename saldo320000 otras_oblig_if
rename saldo400000 pn
rename saldo500000 resultados
rename saldo510000 ing_fin_acum
rename saldo520000 egr_fin_acum
rename saldo521000 egr_fin_ars_acum
rename saldo525000 egr_fin_usd_acum
rename saldo560000 gastos_adm_acum
* deposits by sector
rename saldo311100 dep_spub
rename saldo311106 dep_spub_ctacte
rename saldo311112 dep_spub_ctacte_int
rename saldo311131 dep_spub_pf_t
rename saldo311140 dep_spub_pf_i
rename saldo311156 dep_spub_precanc
rename saldo311167 dep_spub_pf_cer
rename saldo311400 dep_sfin
rename saldo311700 dep_spnf
rename saldo315100 dep_spub_usd
rename saldo315400 dep_sfin_usd
rename saldo315700 dep_spnf_usd
* SPNF deposits in pesos, by instrument
rename saldo311706 dep_ctacte
rename saldo311712 dep_ctacte_int
rename saldo311718 dep_cajaahorro
rename saldo311722 dep_cgu
rename saldo311723 dep_ctaesp_sint
rename saldo311724 dep_ctaesp_cint
rename saldo311725 dep_judicial_vista
rename saldo311726 dep_ctasueldo
rename saldo311730 dep_fondo_cese
rename saldo311731 dep_pf_transf
rename saldo311735 dep_plazo_const_t
rename saldo311736 dep_precanc_t
rename saldo311738 dep_retrib_var_t
rename saldo311740 dep_pf_intransf
rename saldo311742 dep_inmovil
rename saldo311744 dep_precanc_i
rename saldo311745 dep_ordenes
rename saldo311747 dep_retrib_var
rename saldo311751 dep_garantia
rename saldo311753 dep_judicial_pf
rename saldo311754 dep_otros
rename saldo311766 dep_pf_cer_t
rename saldo311767 dep_pf_cer_i
rename saldo311783 dep_esp_l27260
rename saldo311785 dep_ahorro_uva
rename saldo311786 dep_ahorro_uvi
rename saldo311788 dep_uva_precanc_a
rename saldo311789 dep_uva_precanc_b
rename saldo311790 dep_esp_depcanc
rename saldo311791 dep_esp_titulares
rename saldo311792 dep_esp_export
rename saldo311793 dep_esp_regular
* SPNF deposits in foreign currency, by instrument
rename saldo315706 dep_ctacte_usd
rename saldo315712 dep_ctacte_int_usd
rename saldo315718 dep_cajaahorro_usd
rename saldo315723 dep_ctaesp_sint_usd
rename saldo315724 dep_ctaesp_cint_usd
rename saldo315725 dep_judicial_vista_usd
rename saldo315731 dep_plazo_const_t_usd
rename saldo315732 dep_pf_transf_usd
rename saldo315733 dep_precanc_t_usd
rename saldo315737 dep_pf_intransf_usd
rename saldo315742 dep_inmovil_usd
rename saldo315743 dep_precanc_i_usd
rename saldo315751 dep_garantia_usd
rename saldo315753 dep_judicial_pf_usd
rename saldo315754 dep_otros_usd
rename saldo315781 dep_esp_l27260a_usd
rename saldo315783 dep_esp_l27260c_usd
rename saldo315784 dep_repatr_ca_usd
rename saldo315785 dep_repatr_pf_usd
rename saldo315786 dep_repatr_esp_usd
rename saldo315787 dep_repatr_pfesp_usd
rename saldo315788 dep_repatr_aporte_usd
rename saldo315790 dep_esp_depcanc_usd
rename saldo315791 dep_esp_financ_usd
rename saldo315792 dep_esp_fomento_usd
rename saldo315793 dep_esp_depcanc2_usd
rename saldo315794 dep_esp_regular_usd
* interest expense on deposits, cumulative within the year
rename saldo521003 int_otros_acum
rename saldo521021 aporte_fgd_acum
rename saldo521062 int_ctacte_acum
rename saldo521063 int_cajaahorro_acum
rename saldo521064 int_pf_acum
rename saldo521065 int_otras_imp_acum
rename saldo521080 aj_pf_cer_acum
rename saldo521092 aj_ca_uva_acum
rename saldo521093 aj_ca_uvi_acum
rename saldo521112 aj_dep_uva_acum
rename saldo521113 int_caucion_acum
rename saldo511047 ing_adelantos_acum
rename saldo511048 ing_documentos_acum
rename saldo511049 ing_hipot_viv_acum
rename saldo511050 ing_hipot_otros_acum
rename saldo511051 ing_prend_auto_acum
rename saldo511052 ing_prend_otros_acum
rename saldo511053 ing_otros_prest_acum
rename saldo511054 ing_tarjetas_acum
rename saldo511107 ing_personales_acum
rename saldo511111 ing_hipotecarios2_acum
rename saldo511113 ing_personales2_acum
rename saldo525003 int_otros_usd_acum
rename saldo525062 int_ctacte_usd_acum
rename saldo525063 int_cajaahorro_usd_acum
rename saldo525064 int_pf_usd_acum
rename saldo525065 int_otras_imp_usd_acum
* liquidity instruments of the BCRA and the Treasury, and reserve holdings
rename saldo111015 bcra_ctacte
rename saldo111017 otras_ctas_efvomin
rename saldo111021 otras_ctas_noefvomin
rename saldo111025 bcra_ctaesp
rename saldo121003 titpub_ars_vr
rename saldo121016 titpub_ars_ca
rename saldo121040 titpub_ars_vr2
rename saldo125003 titpub_usd_vr
rename saldo125016 titpub_usd_ca
rename saldo125042 titpub_usd_vr2
rename saldo121000 tit_ars_tot
rename saldo125000 tit_usd_tot
rename saldo121058 leliq
rename saldo125058 ledic_usd
rename saldo121091 lefi_a
rename saldo121092 lefi_b
rename saldo121093 lefi_c
rename saldo141104 pase_nofin_tp
rename saldo141124 pase_cpra_term
rename saldo141134 pase_fin_tp
rename saldo141143 pase_fin_a
rename saldo141144 pase_fin_b
rename saldo141433 pase_reg_monet
rename saldo145120 pase_nofin_tp_usd
rename saldo141153 bcra_ctaesp_gtias
rename saldo141169 bcra_dep_indisp_camb
rename saldo141170 bcra_dep_indisp_otros
rename saldo145153 bcra_ctaesp_gtias_usd
format ym %tm

* result accounts are cumulative within the fiscal year (january restarts
* at zero). Monthly flow = change vs the previous month, or the january
* value itself. Expense accounts carry a debit balance, so their signed
* value is negative: flip them so that a flow is a positive expense
sort ent ym
foreach v of varlist *_acum {
    local base = subinstr("`v'", "_acum", "", .)
    local sgn = cond("`base'" == "ing_fin" | strpos("`base'", "ing_") == 1, 1, -1)
    gen double `base'_flow = .
    by ent: replace `base'_flow = `sgn' * `v' if month(dofm(ym)) == 1
    by ent: replace `base'_flow = `sgn' * (`v' - `v'[_n-1]) ///
        if month(dofm(ym)) != 1 & ym == ym[_n-1] + 1
}
* interest on deposits, total, by currency
gen double int_dep_ars_flow = int_ctacte_flow + int_cajaahorro_flow + int_pf_flow ///
    + int_otras_imp_flow + int_otros_flow
gen double int_dep_usd_flow = int_ctacte_usd_flow + int_cajaahorro_usd_flow ///
    + int_pf_usd_flow + int_otras_imp_usd_flow + int_otros_usd_flow

* aggregates used in the analysis
gen double dep_vista_min = dep_cajaahorro + dep_ctasueldo + dep_cgu + dep_ahorro_uva + dep_ahorro_uvi
gen double dep_pf_total  = dep_pf_transf + dep_pf_intransf + dep_pf_cer_t + dep_pf_cer_i ///
    + dep_precanc_t + dep_precanc_i + dep_retrib_var + dep_retrib_var_t + dep_plazo_const_t + dep_uva_precanc_a + dep_uva_precanc_b
gen double dep_especiales = dep_esp_depcanc + dep_esp_titulares + dep_esp_export + dep_esp_regular + dep_esp_l27260
gen double dep_fci_proxy = dep_ctaesp_cint
gen double dep_precanc = dep_precanc_t + dep_precanc_i
gen double dep_pf_total_usd = dep_pf_transf_usd + dep_pf_intransf_usd + dep_precanc_t_usd + dep_precanc_i_usd + dep_plazo_const_t_usd
gen double dep_especiales_usd = dep_esp_depcanc_usd + dep_esp_financ_usd + dep_esp_fomento_usd ///
    + dep_esp_depcanc2_usd + dep_esp_regular_usd + dep_esp_l27260a_usd + dep_esp_l27260c_usd ///
    + dep_repatr_ca_usd + dep_repatr_pf_usd + dep_repatr_esp_usd + dep_repatr_pfesp_usd + dep_repatr_aporte_usd

* liquidity position vis-a-vis the BCRA and the Treasury.
* Built on the subtotals of the chart of accounts, not on the species lines.
* Banks differ in the line they use for the same instrument: in 2024m7 the
* three LEFI accounts pick up only 5.7 of the 9.6 trillion the BCRA reports
* in series 196, and within the peso block the balance moves between the
* measurement-criterion lines. The subtotals 121000 and 125000 are exactly
* additive over their species, so they absorb that choice. Private
* securities are inside 121000 but stay below 2% of it throughout.
* lefi and leliq are kept for description only, never as an intensity.
* See Data/docs/nota_lefi_leliq.md
gen double lefi       = lefi_a + lefi_b + lefi_c
gen double titpub_ars = titpub_ars_vr + titpub_ars_ca + titpub_ars_vr2
gen double titpub_usd = titpub_usd_vr + titpub_usd_ca + titpub_usd_vr2
gen double pases_bcra = pase_nofin_tp + pase_cpra_term + pase_fin_tp + pase_fin_a ///
    + pase_fin_b + pase_reg_monet + pase_nofin_tp_usd
gen double bcra_dep   = bcra_ctacte + bcra_ctaesp + bcra_ctaesp_gtias ///
    + bcra_dep_indisp_camb + bcra_dep_indisp_otros + bcra_ctaesp_gtias_usd
gen double liq_publica = tit_ars_tot + pases_bcra + bcra_dep
* outside the life of each instrument a zero is an artifact of the fill-in
* rule above, not a holding of zero
replace lefi  = . if ym < ym(2024,7) | ym > ym(2025,6)
replace leliq = . if ym > ym(2024,2)

merge 1:1 ent ym using `clasif', keep(master match) nogen
merge m:1 ym using "$proc/ipc.dta", keepusing(ipc_nacional) keep(master match) nogen

label var ent "Codigo de entidad BCRA"
label var nombre "Nombre de la entidad"
label var ym "Mes"
label var activo "Activo total"
label var efectivo "Efectivo y depositos en bancos"
label var titulos "Titulos publicos y privados"
label var prestamos "Prestamos (total)"
label var prest_spnf "Prestamos al SPNF en pesos, capitales"
label var prest_spnf_usd "Prestamos al SPNF en moneda extranjera, capitales"
label var otros_cred_if "Otros creditos por intermediacion financiera"
label var pasivo "Pasivo total"
label var depositos "Depositos (total)"
label var dep_ars_res "Depositos en pesos de residentes"
label var dep_usd_res "Depositos en moneda extranjera de residentes"
label var otras_oblig_if "Otras obligaciones por intermediacion financiera"
label var pn "Patrimonio neto"
label var resultados "Resultados acumulados del ejercicio (positivo = ganancia)"
label var dep_spub "Depositos del sector publico no financiero, pesos"
label var dep_spub_ctacte "Sector publico cuenta corriente sin interes, pesos"
label var dep_spub_ctacte_int "Sector publico cuenta corriente con interes, pesos"
label var dep_spub_pf_t "Sector publico plazo fijo transferible, pesos"
label var dep_spub_pf_i "Sector publico plazo fijo intransferible, pesos"
label var dep_spub_precanc "Sector publico inversiones precancelables, pesos"
label var dep_spub_pf_cer "Sector publico plazo fijo CER, pesos"
label var dep_sfin "Depositos del sector financiero, pesos"
label var dep_spnf "Depositos del SPNF en pesos, capitales"
label var dep_spub_usd "Depositos del sector publico no financiero, moneda extranjera"
label var dep_sfin_usd "Depositos del sector financiero, moneda extranjera"
label var dep_spnf_usd "Depositos del SPNF en moneda extranjera, capitales"
label var dep_ctacte "SPNF cuenta corriente sin interes"
label var dep_ctacte_int "SPNF cuenta corriente con interes"
label var dep_cajaahorro "SPNF caja de ahorros"
label var dep_cgu "SPNF cuenta gratuita universal"
label var dep_ctaesp_sint "SPNF cta cte especial personas juridicas sin interes"
label var dep_ctaesp_cint "SPNF cta cte especial personas juridicas con interes"
label var dep_judicial_vista "SPNF depositos judiciales a la vista"
label var dep_ctasueldo "SPNF cuenta sueldo y previsional"
label var dep_fondo_cese "SPNF fondo de cese laboral trabajadores de la construccion"
label var dep_pf_transf "SPNF plazo fijo transferible"
label var dep_plazo_const_t "SPNF inversiones a plazo constante, transferibles"
label var dep_precanc_t "SPNF inversiones con cancelacion anticipada, transferibles"
label var dep_retrib_var_t "SPNF inversiones a plazo con retribucion variable, transferibles"
label var dep_pf_intransf "SPNF plazo fijo intransferible"
label var dep_inmovil "SPNF saldos inmovilizados"
label var dep_precanc_i "SPNF inversiones con cancelacion anticipada, intransferibles"
label var dep_ordenes "SPNF ordenes por pagar"
label var dep_retrib_var "SPNF inversiones a plazo con retribucion variable"
label var dep_garantia "SPNF depositos en garantia"
label var dep_judicial_pf "SPNF depositos judiciales a plazo fijo"
label var dep_otros "SPNF otros depositos"
label var dep_pf_cer_t "SPNF plazo fijo transferible con CER"
label var dep_pf_cer_i "SPNF plazo fijo intransferible con CER"
label var dep_esp_l27260 "SPNF cuenta especial Ley 27260, exteriorizacion 2016-17"
label var dep_ahorro_uva "SPNF cuenta de ahorro en UVA"
label var dep_ahorro_uvi "SPNF cuenta de ahorro en UVI"
label var dep_uva_precanc_a "SPNF depositos UVA con opcion de cancelacion (311788)"
label var dep_uva_precanc_b "SPNF depositos UVA con opcion de cancelacion (311789)"
label var dep_esp_depcanc "SPNF cuenta especial de deposito y cancelacion (desde 2021)"
label var dep_esp_titulares "SPNF cuenta especial titulares con activos (desde 2022)"
label var dep_esp_export "SPNF cuenta especial para exportadores (desde 2022)"
label var dep_esp_regular "SPNF cuenta especial regularizacion de activos, blanqueo 2024"
label var dep_ctacte_usd "SPNF ME cuenta corriente sin interes"
label var dep_ctacte_int_usd "SPNF ME cuenta corriente con interes"
label var dep_cajaahorro_usd "SPNF ME caja de ahorros"
label var dep_ctaesp_sint_usd "SPNF ME cta cte especial PJ sin interes"
label var dep_ctaesp_cint_usd "SPNF ME cta cte especial PJ con interes"
label var dep_judicial_vista_usd "SPNF ME depositos judiciales a la vista"
label var dep_plazo_const_t_usd "SPNF ME inversiones a plazo constante, transferibles"
label var dep_pf_transf_usd "SPNF ME plazo fijo transferible"
label var dep_precanc_t_usd "SPNF ME inversiones con cancelacion anticipada, transferibles"
label var dep_pf_intransf_usd "SPNF ME plazo fijo intransferible"
label var dep_inmovil_usd "SPNF ME saldos inmovilizados"
label var dep_precanc_i_usd "SPNF ME inversiones con cancelacion anticipada, intransferibles"
label var dep_garantia_usd "SPNF ME depositos en garantia"
label var dep_judicial_pf_usd "SPNF ME depositos judiciales a plazo fijo"
label var dep_otros_usd "SPNF ME otros depositos"
label var dep_esp_l27260a_usd "SPNF ME cuenta especial Ley 27260 art 38 inc a, exteriorizacion 2016-17"
label var dep_esp_l27260c_usd "SPNF ME cuenta especial Ley 27260 art 38 inc c, exteriorizacion 2016-17"
label var dep_repatr_ca_usd "SPNF ME caja de ahorros repatriacion de fondos (Bienes Personales)"
label var dep_repatr_pf_usd "SPNF ME plazo fijo repatriacion Bienes Personales"
label var dep_repatr_esp_usd "SPNF ME cuenta especial repatriacion de fondos RG AFIP"
label var dep_repatr_pfesp_usd "SPNF ME plazo fijo cuenta especial repatriacion"
label var dep_repatr_aporte_usd "SPNF ME cuenta especial repatriacion, aporte solidario"
label var dep_esp_depcanc_usd "SPNF ME cuenta especial de deposito y cancelacion"
label var dep_esp_financ_usd "SPNF ME cuenta especial para acreditar financiaciones"
label var dep_esp_fomento_usd "SPNF ME cuenta especial regimen de fomento"
label var dep_esp_depcanc2_usd "SPNF ME cuenta especial de deposito y cancelacion (segunda)"
label var dep_esp_regular_usd "SPNF ME cuenta especial regularizacion de activos, blanqueo 2024"
label var dep_vista_min "SPNF vista minorista: caja de ahorro + sueldo + CGU + ahorro UVA/UVI"
label var dep_pf_total "SPNF plazo fijo total: transf + intransf + CER + precancelables + retrib variable + UVA precancelable"
label var dep_especiales "SPNF cuentas especiales (dep y canc, titulares, exportadores, blanqueos 2016 y 2024)"
label var dep_fci_proxy "Proxy fondeo FCI/institucional a la vista: cta esp PJ con interes (311724). Contaminado: incluye toda PJ"
label var dep_precanc "Mayorista a plazo: inversiones precancelables transferibles e intransferibles"
label var dep_pf_total_usd "SPNF ME plazo fijo total"
label var dep_especiales_usd "SPNF ME cuentas especiales (blanqueos 2016 y 2024, repatriacion Bienes Personales)"
label var ing_fin_acum "Ingresos financieros, acumulado del ejercicio"
label var egr_fin_acum "Egresos financieros, acumulado del ejercicio (negativo)"
label var egr_fin_ars_acum "Egresos financieros por operaciones en pesos, acumulado (negativo)"
label var egr_fin_usd_acum "Egresos financieros por operaciones en ME, acumulado (negativo)"
label var gastos_adm_acum "Gastos de administracion, acumulado (negativo)"
label var int_otros_acum "Intereses por otros depositos, pesos, acumulado (negativo)"
label var aporte_fgd_acum "Aporte al fondo de garantia de depositos, acumulado (negativo)"
label var int_ctacte_acum "Intereses por depositos en cuenta corriente, pesos, acumulado (negativo)"
label var int_cajaahorro_acum "Intereses por depositos en caja de ahorros, pesos, acumulado (negativo)"
label var int_pf_acum "Intereses por depositos a plazo fijo, pesos, acumulado (negativo)"
label var int_otras_imp_acum "Intereses por otras imposiciones a plazo, pesos, acumulado (negativo)"
label var aj_pf_cer_acum "Ajustes CER por plazo fijo, acumulado (negativo)"
label var aj_ca_uva_acum "Ajustes por cuenta de ahorro UVA, acumulado (negativo)"
label var aj_ca_uvi_acum "Ajustes por cuenta de ahorro UVI, acumulado (negativo)"
label var aj_dep_uva_acum "Ajustes e intereses por depositos UVA, acumulado (negativo)"
label var int_caucion_acum "Intereses por operaciones de caucion bursatil, acumulado (negativo)"
label var ing_adelantos_acum "Intereses ganados por adelantos, acumulado"
label var ing_documentos_acum "Intereses ganados por documentos, acumulado"
label var ing_hipot_viv_acum "Intereses ganados por hipotecarios sobre vivienda, acumulado"
label var ing_hipot_otros_acum "Intereses ganados por otros hipotecarios, acumulado"
label var ing_prend_auto_acum "Intereses ganados por prendarios automotores, acumulado"
label var ing_prend_otros_acum "Intereses ganados por otros prendarios, acumulado"
label var ing_otros_prest_acum "Intereses ganados por otros prestamos, acumulado"
label var ing_tarjetas_acum "Intereses ganados por tarjetas de credito, acumulado"
label var ing_personales_acum "Intereses ganados por prestamos personales, acumulado"
label var ing_hipotecarios2_acum "Intereses ganados por prestamos hipotecarios (NIIF), acumulado"
label var ing_personales2_acum "Intereses ganados por prestamos personales (NIIF), acumulado"
label var int_otros_usd_acum "Intereses por otros depositos, ME, acumulado (negativo)"
label var int_ctacte_usd_acum "Intereses por depositos en cuenta corriente, ME, acumulado (negativo)"
label var int_cajaahorro_usd_acum "Intereses por depositos en caja de ahorros, ME, acumulado (negativo)"
label var int_pf_usd_acum "Intereses por depositos a plazo fijo, ME, acumulado (negativo)"
label var int_otras_imp_usd_acum "Intereses por otras imposiciones a plazo, ME, acumulado (negativo)"
foreach v of varlist *_flow {
    local base = subinstr("`v'", "_flow", "", .)
    cap confirm variable `base'_acum
    if !_rc {
        local lab : var label `base'_acum
        local lab = subinstr("`lab'", ", acumulado del ejercicio (negativo)", "", .)
        local lab = subinstr("`lab'", ", acumulado (negativo)", "", .)
        local lab = subinstr("`lab'", ", acumulado del ejercicio", "", .)
        label var `v' "`lab', flujo mensual"
    }
}
label var int_dep_ars_flow "Intereses pagados por depositos en pesos, flujo mensual"
label var int_dep_usd_flow "Intereses pagados por depositos en ME, flujo mensual"
* real versions at January 2026 prices, keeping the nominal series
ds ent nombre ym ipc_nacional es_banco banco_publico banco_privado banco_capnacional ///
    banco_capextranjero cia_financiera cia_fin_extranjera top10_privados, not
foreach v of varlist `r(varlist)' {
    gen double `v'_r = `v' * $ipc_base / ipc_nacional
    label var `v'_r "`: var label `v'' (pesos de 2026m1)"
    label var `v' "`: var label `v'' (nominal)"
}
label var es_banco "Banco (AA100)"
label var banco_publico "Banco publico (AA110)"
label var banco_privado "Banco privado (AA120)"
label var banco_capnacional "Banco local de capital nacional (AA121)"
label var banco_capextranjero "Banco de capital extranjero o sucursal del exterior (AA123/AA124)"
label var cia_financiera "Compania financiera (AA200)"
label var cia_fin_extranjera "Compania financiera de capital extranjero (AA220)"
label var top10_privados "Entre los 10 primeros bancos privados (AA910)"
label var ipc_nacional "IPC nacional usado para deflactar (dic-2016=100)"
label var bcra_ctacte "Cuenta corriente en el BCRA, pesos"
label var otras_ctas_efvomin "Otras cuentas corrientes computables para efectivo minimo"
label var otras_ctas_noefvomin "Otras cuentas corrientes no computables para efectivo minimo"
label var bcra_ctaesp "Cuentas corrientes especiales en el BCRA"
label var tit_ars_tot "Titulos en pesos, subtotal 121000"
label var tit_usd_tot "Titulos en moneda extranjera, subtotal 125000"
label var titpub_ars "Titulos publicos en pesos"
label var titpub_usd "Titulos publicos en moneda extranjera"
label var leliq "Letras de Liquidez del BCRA (hasta 2024m1)"
label var ledic_usd "Letras del BCRA LEDIV a tasa cero, moneda extranjera"
label var lefi "Letras Fiscales de Liquidez (2024m7-2025m6, subestimada)"
label var pases_bcra "Pases activos, capitales"
label var bcra_dep "Depositos y cuentas en el BCRA"
label var liq_publica "Posicion liquida en instrumentos del BCRA y del Tesoro"
label data "Balances mensuales por entidad, IEF BCRA (baldet)"
sort ent ym
save "$proc/balances_bancos.dta", replace

* ------------------------------------------------------------------
* 5. prestamos_depositos_prov.dta: bank x province x month
* ------------------------------------------------------------------
* Branches and ATMs come from suc_pcia (all months); loan and deposit
* amounts come from the distribgeo xlsx (quarterly, missing in a few
* months of 2020).

tempfile suc
local first = 1
foreach m of local dirs {
    cap confirm file "$raw/bcra_ief/`m'/suc_pcia.txt"
    if _rc continue
    qui {
        import delimited "$raw/bcra_ief/`m'/suc_pcia.txt", delimiters(tab) ///
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
    cap confirm file "$raw/bcra_ief/`m'/prestamos_depositos_prov.xlsx"
    if _rc continue
    qui {
        import excel "$raw/bcra_ief/`m'/prestamos_depositos_prov.xlsx", cellrange(A5) allstring clear
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

merge m:1 ent ym using `clasif', keep(master match) nogen
merge m:1 ym using "$proc/ipc.dta", keepusing(ipc_nacional) keep(master match) nogen
gen double prestamos_prov_r = prestamos_prov * $ipc_base / ipc_nacional
gen double depositos_prov_r = depositos_prov * $ipc_base / ipc_nacional

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
label var prestamos_prov "Prestamos del banco en la provincia (trimestral, nominal)"
label var depositos_prov "Depositos del banco en la provincia (trimestral, nominal)"
label var prestamos_prov_r "Prestamos del banco en la provincia (trimestral, pesos de 2026m1)"
label var depositos_prov_r "Depositos del banco en la provincia (trimestral, pesos de 2026m1)"
label var es_banco "Banco (AA100)"
label var banco_publico "Banco publico (AA110)"
label var banco_privado "Banco privado (AA120)"
label var banco_capnacional "Banco local de capital nacional (AA121)"
label var banco_capextranjero "Banco de capital extranjero o sucursal del exterior (AA123/AA124)"
label var cia_financiera "Compania financiera (AA200)"
label var cia_fin_extranjera "Compania financiera de capital extranjero (AA220)"
label var top10_privados "Entre los 10 primeros bancos privados (AA910)"
label var ipc_nacional "IPC nacional usado para deflactar (dic-2016=100)"
label data "Presencia y negocio por banco x provincia, IEF BCRA"
sort ent provincia ym
save "$proc/prestamos_depositos_prov.dta", replace

* ------------------------------------------------------------------
* 6. caracteristicas_bancos.dta: bank x month, long format
* ------------------------------------------------------------------
* From inf_adi (accounts, cards, staff), indicad (indicators) and esd
* (debtor status). Columns 6-10 of the raw files hold the last five
* balance dates; we keep column 10, the most recent one.

tempfile car
local first = 1
foreach m of local dirs {
    foreach s in inf_adi indicad esd {
        cap confirm file "$raw/bcra_ief/`m'/`s'.txt"
        if _rc continue
        qui {
            import delimited "$raw/bcra_ief/`m'/`s'.txt", delimiters(tab) ///
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
* 99999 is a sentinel for not-computable indicators, not a value
replace valor = . if valor == 99999 & fuente == "indicad"

label var ent "Codigo de entidad BCRA"
label var nombre "Nombre de la entidad"
label var ym "Mes"
label var fuente "Archivo IEF de origen (inf_adi, indicad o esd)"
label var codigo "Codigo de linea BCRA"
label var descripcion "Descripcion de la linea"
label var valor "Valor a la fecha mas reciente del archivo"
label data "Caracteristicas por banco x mes, IEF BCRA (formato largo)"
sort ent ym fuente codigo
save "$proc/caracteristicas_bancos.dta", replace

di as text "done: 5 files written to $out"
