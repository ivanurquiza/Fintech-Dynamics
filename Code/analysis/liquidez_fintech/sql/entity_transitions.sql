-- Comparación de meses consecutivos. Cero y ausencia se conservan por separado.
WITH pairs AS (
 SELECT coalesce(p.ent,q.ent) AS ent,p.cuit AS prev_id,q.cuit AS curr_id,
 coalesce(p.amount_ars,0) AS prev_amount,coalesce(q.amount_ars,0) AS curr_amount,
 p.status AS prev_status,q.status AS curr_status,p.active AS prev_active,q.active AS curr_active,
 p.legal AS prev_legal,q.legal AS curr_legal
 FROM read_parquet(?) p FULL OUTER JOIN read_parquet(?) q USING(ent,cuit)
)
SELECT ent,
 count(*) FILTER(WHERE prev_amount>0) AS prev_positive,
 count(*) FILTER(WHERE curr_amount>0) AS curr_positive,
 count(*) FILTER(WHERE prev_amount>0 AND curr_amount>0) AS continuing,
 count(*) FILTER(WHERE prev_amount=0 AND curr_amount>0 AND prev_id IS NULL) AS first_observed,
 count(*) FILTER(WHERE prev_amount=0 AND curr_amount>0 AND prev_id IS NOT NULL) AS reappearing,
 count(*) FILTER(WHERE prev_amount>0 AND curr_amount=0 AND curr_id IS NOT NULL) AS to_zero,
 count(*) FILTER(WHERE prev_amount>0 AND curr_id IS NULL) AS missing_row,
 count(*) FILTER(WHERE prev_amount>0 AND curr_amount=0 AND prev_status BETWEEN 3 AND 6) AS exit_after_bad,
 count(*) FILTER(WHERE prev_amount>0 AND prev_status IN (1,2)) AS prev_good,
 count(*) FILTER(WHERE prev_amount>0 AND prev_status IN (1,2) AND curr_amount>0 AND curr_status BETWEEN 3 AND 6) AS to_bad,
 count(*) FILTER(WHERE prev_amount>0 AND prev_status BETWEEN 3 AND 6) AS prev_bad,
 count(*) FILTER(WHERE prev_amount>0 AND prev_status BETWEEN 3 AND 6 AND curr_amount>0 AND curr_status IN (1,2)) AS to_good,
 count(*) FILTER(WHERE prev_amount>0 AND curr_amount>0 AND prev_legal=0 AND curr_legal=1) AS legal_entry,
 sum(prev_amount) AS prev_amount,sum(curr_amount) AS curr_amount,
 sum(CASE WHEN prev_amount=0 THEN curr_amount ELSE 0 END) AS entry_amount,
 sum(CASE WHEN curr_amount=0 THEN prev_amount ELSE 0 END) AS exit_amount,
 sum(CASE WHEN curr_amount>0 AND prev_amount>0 THEN curr_amount ELSE 0 END) AS continuing_current,
 sum(CASE WHEN curr_amount>0 AND prev_amount>0 THEN prev_amount ELSE 0 END) AS continuing_previous
FROM pairs GROUP BY ent;
