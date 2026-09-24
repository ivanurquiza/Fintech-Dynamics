-- Primer saldo positivo observado con la entidad; historia previa y seguimiento fijo.
CREATE OR REPLACE TEMP TABLE entrant_profiles AS
WITH e AS (SELECT ent,cuit FROM first_focal WHERE first_date=?),
history AS (
 SELECT p.cuit,count(DISTINCT p.ent) AS prior_lenders,
 count(DISTINCT CASE WHEN b.ent IS NOT NULL THEN p.ent END) AS prior_banks
 FROM read_parquet(?) p JOIN (SELECT DISTINCT cuit FROM e) x USING(cuit)
 LEFT JOIN bank_ids b ON p.ent=b.ent WHERE p.amount_ars>0 GROUP BY p.cuit
), snapshots AS (
 SELECT 0 AS horizon,* FROM read_parquet(?)
 UNION ALL SELECT 3 AS horizon,* FROM read_parquet(?)
 UNION ALL SELECT 6 AS horizon,* FROM read_parquet(?)
), states AS (
 SELECT e.ent,e.cuit,p.horizon,
 sum(p.amount_ars) AS all_amount,
 sum(CASE WHEN p.ent=e.ent THEN p.amount_ars ELSE 0 END) AS focal_amount,
 count(DISTINCT CASE WHEN b.ent IS NOT NULL AND p.ent<>e.ent AND p.amount_ars>0 THEN p.ent END) AS banks
 FROM e LEFT JOIN snapshots p USING(cuit)
 LEFT JOIN bank_ids b ON p.ent=b.ent GROUP BY e.ent,e.cuit,p.horizon
), pivoted AS (
 SELECT ent,cuit,
 coalesce(max(all_amount) FILTER(WHERE horizon=0),0) AS all0,
 coalesce(max(all_amount) FILTER(WHERE horizon=6),0) AS all6,
 coalesce(max(focal_amount) FILTER(WHERE horizon=0),0) AS focal0,
 coalesce(max(focal_amount) FILTER(WHERE horizon=3),0) AS focal3,
 coalesce(max(focal_amount) FILTER(WHERE horizon=6),0) AS focal6,
 coalesce(max(banks) FILTER(WHERE horizon=6),0) AS banks6
 FROM states GROUP BY ent,cuit
)
SELECT e.*,coalesce(h.prior_lenders,0) AS prior_lenders,coalesce(h.prior_banks,0) AS prior_banks,
 a.first_date AS first_any_date,v.* EXCLUDE(ent,cuit),
 CASE WHEN coalesce(h.prior_banks,0)>0 THEN 'Con banco previo'
 WHEN coalesce(h.prior_lenders,0)>0 THEN 'Solo otros acreedores previos'
 ELSE 'Sin saldo en seis meses previos' END AS prior_profile
FROM e LEFT JOIN history h USING(cuit) JOIN first_any a USING(cuit)
JOIN pivoted v USING(ent,cuit);
