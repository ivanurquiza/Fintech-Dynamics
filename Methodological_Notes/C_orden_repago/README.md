# Línea C. Orden de repago entre acreedores

## Pregunta

Cuando un deudor empieza a dejar de pagar, en qué orden deja de pagarle a cada acreedor, y cuánto de ese orden lo explica el acceso del acreedor al flujo de ingresos del deudor (débito sobre la cuenta sueldo o la billetera) y no el contrato.

## Datos

CENDEU, muestra del 5% de personas (`person_lender_5pct`), agosto de 2024 a junio de 2026, con el padrón para sexo, edad y provincia. Crosswalk de acreedores `Data/crosswalks/cendeu_lenders.csv`.

## Código

`Code/analysis/pecking_order/`: `01_orden_de_repago.ipynb`, `po.py`, `diag_edad_jubilatoria.py`. Resultados en `resultados.md`.

## Estado

Es la línea más avanzada. El 96,9% de los primeros eventos de mora son parciales y la selección persiste a seis meses. Con logit condicional y efecto fijo persona-mes, la razón de chances de ser la relación que cae, contra banca privada, es 0,33 para MercadoLibre y 1,73 para retail. Macro se protege en sus provincias (0,21) y no fuera (0,62). El diagnóstico por edad jubilatoria (mujeres a los 60, varones a los 65) muestra el patrón esperado en MercadoLibre.

## Discusión

De `comun/revision_integral_2026-09-28.md` §2. Lo que se identifica es un diferencial de hazard entre acreedores del mismo deudor, no una elección del hogar: con débito automático, el acreedor cobra antes de que la plata esté disponible. La situación es única por deudor-entidad, así que un banco con varios productos cae más por construcción; hace falta el tipo de asistencia o una prueba con deudores de una sola línea. La frecuencia de cobro y la refinanciación pueden imitar prioridad. La validación con la recategorización obligatoria no es independiente del panel.

## Pendiente

Correr sobre el universo (`panel24_wide`); diferencia en discontinuidades por edad jubilatoria con logit condicional; test de deudores monoproducto; dilución de las otras relaciones al entrar MercadoLibre; pedir tipo de asistencia y tasas de PNFC al BCRA. Nota de idea: `pecking_order.md`.
