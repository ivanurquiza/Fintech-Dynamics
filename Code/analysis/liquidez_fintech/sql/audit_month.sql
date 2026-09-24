-- Integridad del archivo mensual de la muestra; no exporta identificadores.
SELECT min(year) AS year, min(month) AS month,
       count(DISTINCT (year, month)) AS n_months,
       count(*) AS rows,
       count(*) - count(DISTINCT (cuit, ent)) AS duplicates,
       count(*) FILTER (WHERE cuit IS NULL OR ent IS NULL OR amount_ars IS NULL OR status IS NULL) AS missing,
       count(*) FILTER (WHERE amount_ars < 0) AS negative,
       count(*) FILTER (WHERE amount_ars > 0 AND status = 0) AS positive_status_zero,
       count(*) FILTER (WHERE amount_ars = 0 AND status > 0) AS zero_with_status,
       count(*) FILTER (WHERE status NOT BETWEEN 0 AND 5) AS unusual_status,
       count(DISTINCT cuit) FILTER (WHERE amount_ars > 0) AS borrowers_positive,
       count(DISTINCT ent) FILTER (WHERE amount_ars > 0) AS lenders_positive,
       count(*) FILTER (WHERE amount_ars > 0 AND abs(hash(cuit)) % 100 >= 5) AS outside_current_hash,
       sum(amount_ars) AS amount_ars
FROM read_parquet(?);
