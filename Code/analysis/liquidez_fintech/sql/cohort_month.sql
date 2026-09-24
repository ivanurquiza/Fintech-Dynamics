-- Componentes de saldo para una cohorte fija. Ausencia = sin saldo observado, no cancelación verificada.
WITH amounts AS (
    SELECT p.cuit,
        sum(p.amount_ars) FILTER (WHERE t.is_bank) AS bank_amount,
        sum(p.amount_ars) FILTER (WHERE t.is_fintech) AS fintech_amount,
        sum(p.amount_ars) FILTER (WHERE NOT t.is_bank AND NOT t.is_fintech) AS other_amount,
        sum(p.amount_ars) AS total_amount,
        sum(p.amount_ars) FILTER (WHERE p.status IN (3,4,5)) AS npl_amount
    FROM read_parquet(?) p JOIN tax t USING (ent) JOIN cohort c USING (cuit)
    WHERE t.include_credit AND p.amount_ars > 0
    GROUP BY p.cuit
)
SELECT c.cohort, count(*) AS cohort_n,
    sum(coalesce(a.bank_amount,0)) AS bank_amount,
    sum(coalesce(a.fintech_amount,0)) AS fintech_amount,
    sum(coalesce(a.other_amount,0)) AS other_amount,
    sum(coalesce(a.total_amount,0)) AS total_amount,
    sum(coalesce(a.npl_amount,0)) AS npl_amount,
    count(*) FILTER (WHERE a.bank_amount > 0) AS with_bank,
    count(*) FILTER (WHERE a.fintech_amount > 0) AS with_fintech,
    count(*) FILTER (WHERE a.total_amount > 0) AS with_credit,
    count(*) FILTER (WHERE a.cuit IS NULL) AS no_reported_balance
FROM cohort c LEFT JOIN amounts a USING (cuit)
GROUP BY c.cohort;
