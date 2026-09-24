-- Cohorte con saldo en la entidad focal y bancos comparadores en la fecha inicial.
-- La entidad focal se excluye del comparador incluso si es banco.
WITH p AS (SELECT * FROM read_parquet(?)),q AS (SELECT * FROM read_parquet(?)),
focal AS (SELECT cuit,amount_ars AS focal_before FROM p WHERE ent=? AND amount_ars>0),
pre AS (
 SELECT f.cuit,f.focal_before,sum(p.amount_ars) AS all_before,
 sum(CASE WHEN p.ent<>? AND p.ent IN (SELECT ent FROM bank_ids) THEN p.amount_ars ELSE 0 END) AS bank_before
 FROM focal f JOIN p USING(cuit) GROUP BY f.cuit,f.focal_before
), post AS (
 SELECT p.cuit,p.focal_before,p.bank_before,p.all_before,
 coalesce(sum(q.amount_ars),0)*? AS all_after,
 coalesce(sum(CASE WHEN q.ent=? THEN q.amount_ars ELSE 0 END),0)*? AS focal_after,
 coalesce(sum(CASE WHEN q.ent<>? AND q.ent IN (SELECT ent FROM bank_ids) THEN q.amount_ars ELSE 0 END),0)*? AS bank_after
 FROM pre p LEFT JOIN q USING(cuit) WHERE p.bank_before>0
 GROUP BY p.cuit,p.focal_before,p.bank_before,p.all_before
), changes AS (
 SELECT *,focal_after-focal_before AS df,bank_after-bank_before AS db,
 focal_before+bank_before AS base_total FROM post
), bins AS (
 SELECT *,CASE WHEN df < -0.01*base_total THEN 'Cae' WHEN df>0.01*base_total THEN 'Sube' ELSE 'Estable' END AS focal_bin,
 CASE WHEN db < -0.01*base_total THEN 'Cae' WHEN db>0.01*base_total THEN 'Sube' ELSE 'Estable' END AS bank_bin
 FROM changes
)
SELECT focal_bin,bank_bin,count(*) AS persons,sum(base_total) AS base_total,
 sum(df) AS focal_change,sum(db) AS bank_change,
 sum(focal_after+bank_after) AS end_total,
 sum(all_before) AS all_before,sum(all_after) AS all_after,
 count(*) FILTER(WHERE focal_after=0) AS focal_no_balance,
 count(*) FILTER(WHERE bank_after=0) AS banks_no_balance
FROM bins GROUP BY 1,2;
