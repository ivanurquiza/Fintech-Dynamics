-- Un salto de entidad: todos los deudores con saldo positivo en al menos un extremo.
WITH p AS (SELECT * FROM read_parquet(?) WHERE ent=?),
q AS (SELECT * FROM read_parquet(?) WHERE ent=?),
j AS (
 SELECT coalesce(p.cuit,q.cuit) AS cuit,
 coalesce(p.amount_ars,0)*? AS before_real,coalesce(q.amount_ars,0)*? AS after_real,
 p.cuit IS NULL AS first_row,
 p.status AS before_status,q.status AS after_status
 FROM p FULL OUTER JOIN q USING(cuit)
), changes AS (
 SELECT *,after_real-before_real AS delta,
 CASE WHEN before_real=0 THEN 'Apariciones'
      WHEN after_real=0 THEN 'Desapariciones' ELSE 'Continuas' END AS margin
 FROM j WHERE before_real>0 OR after_real>0
), ranked AS (
 SELECT *,row_number() OVER (ORDER BY abs(delta) DESC,cuit) AS change_rank,
 row_number() OVER (ORDER BY after_real DESC,cuit) AS stock_rank FROM changes
)
SELECT margin,count(*) AS borrowers,sum(before_real) AS before_real,sum(after_real) AS after_real,
 sum(delta) AS delta_real,sum(abs(delta)) AS absolute_change,
 sum(CASE WHEN change_rank<=1 THEN abs(delta) ELSE 0 END) AS top1_abs_change,
 sum(CASE WHEN change_rank<=10 THEN abs(delta) ELSE 0 END) AS top10_abs_change,
 sum(CASE WHEN stock_rank<=10 THEN after_real ELSE 0 END) AS top10_stock,
 count(*) FILTER(WHERE before_real=0 AND first_row) AS first_rows,
 count(*) FILTER(WHERE before_real=0 AND NOT first_row) AS returns,
 sum(CASE WHEN after_status BETWEEN 3 AND 6 THEN after_real ELSE 0 END) AS bad_after,
 sum(CASE WHEN before_status BETWEEN 3 AND 6 THEN before_real ELSE 0 END) AS bad_before
FROM ranked GROUP BY margin;
