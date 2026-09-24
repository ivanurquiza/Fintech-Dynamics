-- Cambios reales individuales, manteniendo a TODA la cohorte inicial.
WITH before AS (
    SELECT p.cuit,
           sum(p.amount_ars) FILTER (WHERE t.is_bank) AS bank_before,
           sum(p.amount_ars) FILTER (WHERE t.is_fintech) AS fintech_before
    FROM read_parquet(?) p JOIN tax t USING(ent) JOIN cohort c USING(cuit)
    WHERE t.include_credit AND p.amount_ars>0 GROUP BY p.cuit
), after AS (
    SELECT p.cuit,
           sum(p.amount_ars) FILTER (WHERE t.is_bank) AS bank_after,
           sum(p.amount_ars) FILTER (WHERE t.is_fintech) AS fintech_after
    FROM read_parquet(?) p JOIN tax t USING(ent) JOIN cohort c USING(cuit)
    WHERE t.include_credit AND p.amount_ars>0 GROUP BY p.cuit
), changes AS (
    SELECT c.cohort,
        (? * coalesce(a.bank_after,0)-coalesce(b.bank_before,0))/c.baseline_amount AS bank_change,
        (? * coalesce(a.fintech_after,0)-coalesce(b.fintech_before,0))/c.baseline_amount AS fintech_change
    FROM cohort c LEFT JOIN before b USING(cuit) LEFT JOIN after a USING(cuit)
), bins AS (
    SELECT cohort,
        CASE WHEN bank_change < -? THEN 'Cae' WHEN bank_change > ? THEN 'Sube' ELSE 'Estable' END AS bank_bin,
        CASE WHEN fintech_change < -? THEN 'Cae' WHEN fintech_change > ? THEN 'Sube' ELSE 'Estable' END AS fintech_bin
    FROM changes
)
SELECT cohort, bank_bin, fintech_bin, count(*) AS personas
FROM bins GROUP BY 1,2,3;
