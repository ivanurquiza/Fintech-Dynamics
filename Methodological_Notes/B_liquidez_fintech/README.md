# Línea B. Liquidez bancaria y sustitución por crédito fintech

## Pregunta

Cuando los bancos enfrentan una restricción de liquidez, qué parte del crédito que dejan de dar la cubren proveedores no bancarios, y si esos proveedores comparten la restricción a través de su propio fondeo. El episodio candidato es julio y agosto de 2025: fin de la LEFI (anunciado el 9 de junio, efectivo el 10 de julio), rescisión de los puts, integración diaria de encajes y suba de alícuotas.

## Datos

CENDEU (`lender_month`, `firm`, `person_lender_5pct`, `panel24_wide`), balances bancarios y la cronología normativa. Diccionario en `Data/docs/diccionario_cendeu.md`.

## Código

`Code/analysis/liquidez_fintech/` (notebooks 01, 03, 05 y 06, SQL en `sql/`), `Code/analysis/audit_identificacion_2026-09-20.ipynb` y `cendeu_summ_stats.ipynb`.

## Estado

Hechos descriptivos sólidos. El saldo real de personas crece 12,4% en bancos y 39,9% en proveedores no financieros fintech entre mayo de 2025 y junio de 2026, pero dentro de la cohorte que ya tenía ambos el componente fintech cae. La banca privada reduce el crédito regular a hogares y aumenta el de firmas; la pública aumenta los dos. MercadoLibre, Reba o Credicuotas reconstruyen su stock en pocos meses; los bancos grandes no.

## Discusión

La revisión del 28-sep (`comun/revision_integral_2026-09-28.md` §3) concluye que hoy no hay evento limpio: el deterioro sube en mayo de 2025, antes del anuncio, y entre junio y agosto se superponen cuatro tratamientos. El stock de LEFI no mide uso como colchón y su registro contable no reconcilia con la serie del BCRA (`Data/docs/nota_lefi_leliq.md`). El shock banco-mes estimado con firmas multibanco no tiene todavía una validación fuera de muestra. Mientras eso no se corra, la línea funciona como contexto institucional de la línea C.

## Notas

- `idea_lefi.md`: qué era la LEFI y el episodio de 2025.
- `tasas_argentina_2026-09-20.md`: tasas de política y de mercado, episodios candidatos.
- `paper_liquidez_fintech_2026-09-21.md`: propuesta de paper.
- `Code/analysis/liquidez_fintech/resultados_por_entidad.md` y `viabilidad_paper.md`: resultados.

## Pendiente

Validar fuera de muestra el shock banco-mes; netear moneda extranjera y separar hipotecario en la reasignación hogares-firmas; correr `build_dta.do` para tener `liq_publica` en la base.
