-- Cohorte fijada en mayo 2025: saldo bancario positivo. Sin selección por resultados posteriores.
CREATE OR REPLACE TEMP TABLE cohort AS
SELECT p.cuit,
       CASE WHEN bool_or(t.is_fintech) THEN 'Con fintech PNFC previa'
            ELSE 'Sin fintech PNFC previa' END AS cohort,
       sum(p.amount_ars) AS baseline_amount,
       count(DISTINCT p.ent) FILTER (WHERE t.is_bank) AS baseline_banks
FROM read_parquet(?) p JOIN tax t USING (ent)
WHERE p.amount_ars > 0 AND t.include_credit
GROUP BY p.cuit
HAVING bool_or(t.is_bank);
