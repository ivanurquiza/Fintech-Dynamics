# Orden de repago dentro del deudor

Exploración de la idea de `Methodological_Notes/C_orden_repago/pecking_order.md` con la muestra de
personas de CENDEU. Un notebook, un módulo de funciones y una nota de resultados.

- `01_orden_de_repago.ipynb`: el análisis completo, ejecutado. Diez secciones, de la
  definición del evento a la validación con la recategorización obligatoria.
- `po.py`: rutas, categorías de acreedores, construcción de eventos, logit condicional
  con efecto fijo de persona-mes y errores agrupados por persona, y utilidades de figura.
- `resultados.md`: lo que se encontró, lo que no quedó resuelto y lo que abre.

Salidas agregadas en `Code/output/pecking_order`, con prefijo por sección.

## Ejecutar

```sh
cd Code/analysis/pecking_order
PO_MEM=2GB python -m jupyter nbconvert --execute --to notebook --inplace \
  --ExecutePreprocessor.timeout=1800 01_orden_de_repago.ipynb
```

Tarda unos dos minutos. Usa duckdb, pandas, numpy, pyarrow y matplotlib; statsmodels
es opcional y solo se usa para contrastar el estimador propio (sección 3).
`PO_MEM` fija el límite de memoria de DuckDB.

## Privacidad

Todo corre en la máquina local. Los intermedios que conservan un identificador (hash del
CUIT) van a un directorio temporal del sistema, fuera del repositorio, y la última celda
los borra. Las salidas son agregados por acreedor o por categoría. Las celdas geográficas
con menos de 500 personas se suprimen (sección 6).

## Decisiones que conviene conocer

- Evento: relación que pasa de situación 1 a 2 o peor, en personas con dos o más
  relaciones con saldo y todas en situación 1 el mes anterior. Julio de 2026 no se usa
  como mes del evento porque el corte está incompleto.
- Categorías: por rango de código BCRA y grupo del crosswalk, con dos correcciones. Los
  códigos 44xxx, 45xxx y 65xxx son compañías financieras, no fideicomisos, y MercadoLibre
  va separado del resto de las fintech.
- Se excluyen garantías, fideicomisos financieros y el código 150 (absorbido por Galicia
  en junio de 2025).
- El estimador está escrito a mano para trabajar por bloques de grupos y agrupar errores
  por persona. Coincide con `ConditionalLogit` de statsmodels hasta el tercer decimal en
  una submuestra de 25.000 eventos.
