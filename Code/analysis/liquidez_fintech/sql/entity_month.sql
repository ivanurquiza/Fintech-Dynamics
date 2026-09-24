-- Todas las entidades, sin asignar tratamiento ni grupos fintech.
WITH p AS (SELECT *, status BETWEEN 3 AND 6 AS bad FROM read_parquet(?)),
peers AS (
 SELECT *, count(*) OVER (PARTITION BY cuit) AS k,
 avg(CAST(bad AS DOUBLE)) OVER (PARTITION BY cuit) AS peer_mean
 FROM p WHERE amount_ars>0
), within_person AS (
 SELECT ent, count(*) FILTER(WHERE k>1) AS shared_n,
 sum(CASE WHEN k>1 THEN CAST(bad AS DOUBLE)-peer_mean END) AS demeaned_sum
 FROM peers GROUP BY ent
)
SELECT p.ent,count(*) AS rows_n,sum(active) AS active_n,
 count(*) FILTER(WHERE amount_ars>0) AS positive_n,
 sum(amount_ars) AS amount,
 sum(CASE WHEN status BETWEEN 3 AND 5 THEN amount_ars ELSE 0 END) AS bad35,
 sum(CASE WHEN status BETWEEN 3 AND 6 THEN amount_ars ELSE 0 END) AS bad36,
 sum(CASE WHEN status BETWEEN 2 AND 6 THEN amount_ars ELSE 0 END) AS bad26,
 count(*) FILTER(WHERE amount_ars>0 AND status BETWEEN 3 AND 6) AS bad_n,
 count(*) FILTER(WHERE amount_ars>0 AND legal=1) AS legal_n,
 count(*) FILTER(WHERE amount_ars>0 AND legal IS NULL) AS legal_missing_n,
 max(w.shared_n) AS shared_n,max(w.demeaned_sum) AS demeaned_sum
FROM p LEFT JOIN within_person w USING(ent) GROUP BY p.ent;
