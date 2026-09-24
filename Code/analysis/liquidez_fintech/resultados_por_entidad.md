# Trayectorias por entidad: primera lectura

Corrida del 21 de septiembre de 2026. Notebook `05_trayectorias_por_entidad.ipynb`.
Fuentes: `lender_month`, muestra `person_lender_5pct`, IPC y balances bancarios.
Todas las tablas citadas están en `Code/output/liquidez_fintech/`. Son resultados
descriptivos. La antigua clasificación fintech no interviene en las agregaciones.

## Lo que cambia respecto del primer análisis

El universo incluye 547 códigos con personas y 306 con firmas. Se exportan todos;
las láminas principales seleccionan por saldo o clientes previos y el atlas por
un mínimo de 1.000 clientes en mayo de 2025. No se afirma que todos los códigos
sean préstamos comparables: garantías, transferencias y códigos dudosos se conservan
para revisión. La muestra de personas permite transiciones; las firmas se analizan
aquí en el agregado por acreedor, no todavía en su panel individual.

Entre mayo de 2025 y junio de 2026, saldos reales del universo de personas:

| Entidad | Saldo total | Saldo fuera de situaciones 3–5 | Deudores activos |
|---|---:|---:|---:|
| MercadoLibre | +48,2% | +32,5% | +33,9% |
| Ualá Bank | −13,5% | −39,5% | −9,6% |
| Brubank | −0,9% | −15,5% | +16,2% |
| Reba | +75,4% | +28,2% | +93,9% |
| Naranja Digital | +15,1% | −6,1% | +11,1% |
| Tarjeta Naranja | −8,3% | −24,4% | −3,1% |
| Credicuotas | +8,5% | −22,3% | +24,2% |

Fuente: `05_cambios_entidad.csv`. Activo significa saldo o situación positiva en
el reshape, no uso de una billetera. Saldo fuera de 3–5 no equivale a originación,
ni elimina variación cambiaria, intereses o problemas de reporte.

No hay una trayectoria digital uniforme. Brubank aumenta deudores con saldo total
aproximadamente plano; Reba expande mucho más clientes que saldo; MercadoLibre
expande ambos; Ualá cae en ambos. La oposición fintech/bancos pierde estos márgenes.
Las entidades tampoco cambian en el mismo momento: conservar la trayectoria mensual
es necesario antes de elegir una ventana o episodio.

## Personas y firmas no cuentan la misma historia

Dentro de Supervielle, el saldo fuera de 3–5 cae 23,2% en personas y aumenta 46,3%
en firmas. En Provincia, cae 14,1% en personas y aumenta 19,2% en firmas; en BBVA,
−4,4% y +23,2%. Nación aumenta en ambos: +33,6% y +7,0%, respectivamente.
Esto abre hipótesis de demanda, producto, riesgo y reasignación de cartera. No prueba
que el banco haya retirado crédito de hogares para prestarlo a firmas; la moneda y
la composición de empresas pueden explicar parte de las diferencias.

## La descomposición de relaciones aporta algo distinto del agregado

En la muestra de MercadoLibre, durante mayo 2025–junio 2026, las apariciones de saldo
aportan +110,6 puntos del saldo inicial; las desapariciones −61,3; las relaciones
positivas en ambos meses consecutivos −1,4. El cambio neto es +47,8%. Hay mucha
rotación detrás del crecimiento. Los retornos se separan de las primeras apariciones
en `05_transiciones_entidad.csv`; ni uno ni otro identifica créditos nuevos.
La suma de componentes se reconcilia con la diferencia directa entre extremos.

La muestra no replica perfectamente cada entidad: Reba crece +121,2% en la muestra
frente a +75,4% en el universo. Su peso muestral en saldo pasa de 4,04% a 5,09%.
Por eso las conclusiones sobre tamaño y expansión usan el universo; las transiciones
usan la muestra y conservan su soporte. No expandir automáticamente por veinte.

## Una discontinuidad concreta: códigos 150 y 7

El código 150 queda en cero en junio de 2025 mientras sube Galicia (7). De las 18.234
personas con saldo positivo en 150 en mayo dentro de la muestra, 17.870 tienen saldo
positivo en 7 en junio; representan 99,67% del saldo previo de 150. Es evidencia
fuerte de continuidad de clientela; todavía no documenta el contrato transferido.

La sensibilidad sumando exclusivamente SALDOS de 7 y 150 reduce el crecimiento real
mayo–junio del año siguiente de +21,0% (7 solo) a +5,5% (7+150). El saldo fuera de
3–5 cambia −15,4% en el conjunto. No se suman deudores como personas únicas.
No interpretar el salto individual como expansión de oferta sin resolver identidad.
Fuentes: `05_continuidad_150_7.csv`, `05_sensibilidad_saldos_7_150.csv`.

## Repago: dispersión por acreedor, sin mecanismo identificado

Entre personas con varias relaciones positivas, la brecha de situación 3–6 respecto
de la media del mismo deudor-mes es −3,11 puntos en MercadoLibre, +1,20 en Ualá,
−5,06 en Reba y +3,45 en Naranja Digital en junio de 2026. Son clientelas compartidas
diferentes; estas medias descentradas no constituyen coeficientes causales ni un
ranking sobre una población común. Falta comparar pares con soporte común y controlar
trayectoria previa, tamaño y cambios de composición. Producto y reporte siguen vivos.

Las salidas posteriores a mora tienen picos por entidad. Una mora de stock baja
puede coexistir con salidas rápidas, sin mejor repago. El CSV conserva por separado
salida, deterioro e ingreso a situaciones 1–2 desde 3–6.

`legal` toma 0/1 en la muestra, pero solo hay 25 observaciones entidad-persona-mes
con código 1 en toda la ventana; no son 25 personas ni juicios únicos. La suma de
códigos del agregado completo es apenas 374 en todos los meses y poblaciones. No
hay base para llamarlo una medida útil de enforcement sin revisar fuente y parser.
Agregar situación 6 a 3–5 no cambia saldos en esta muestra; no corresponde afirmar
que produce una corrección sustantiva aquí. Sí se publica la sensibilidad 2–6.

## Cómo seguir sin cerrar la pregunta

1. Documentar identidades y cambios de perímetro, empezando por 150/7, códigos de
   Naranja y fideicomisos. Crear atributos separados y fechados de licencia, fondeo,
   producto y cobro. La clasificación no debe definirse por el resultado observado.
2. Sobre pares concretos de acreedores con clientela común, seguir saldo, primera
   aparición, retorno, deterioro y salida, con composición inicial y riesgo previo.
   Distinguir expansión hacia clientes distintos de cambios dentro de la persona.
3. Extender las transiciones al panel de firmas y contrastar con personas dentro del
   mismo banco. Verificar moneda y concentración en grandes deudores donde sea posible.
4. Volver al canal de tasas con dos hipótesis abiertas: fondeo/oferta de prestamistas
   y servicio de deuda/deterioro de clientes. El cruce descriptivo con depósitos llega
   a abril de 2026. Los ratios previos de efectivo, títulos y depósitos quedan exportados;
   no se seleccionó un instrumento por correlación. Los stocks de tarjetas/personales
   no están en el archivo de balances leído: sus ingresos no sustituyen esos stocks.

El resultado de esta etapa es un mapa de diferencias y problemas de medición que
permite elegir contrastes. No constituye evidencia causal del cierre de LEFI ni
obliga a convertir la mora en el único objeto del paper.

## Ampliación del 22 de septiembre: saltos y clientela compartida

Se agregaron tres figuras al notebook 05 y dos SQL reproducibles. El salto no se
elimina ni se corrige mecánicamente: se identifica qué margen lo explica.

- Creditech, abril de 2026, muestra de personas: 1.151 relaciones pasan a saldo
  positivo; 893 ya habían aparecido anteriormente y 258 aparecen por primera vez
  en la ventana disponible. Los diez mayores cambios explican solo 2,23% de la
  variación absoluta. Es una expansión distribuida entre relaciones que reaparecen,
  no evidencia directa de nuevos clientes ni de un salto por un gran deudor.
- ICBC, julio de 2025, universo de firmas: diez deudores explican 56,50% del cambio
  absoluto mensual, uno solo 16,26%. En Patagonia, noviembre de 2025, diez explican
  39,36%. No se interpreta el cambio agregado como reacción uniforme de clientes.
- El diagnóstico Galicia sigue siendo continuidad entre códigos, a verificar
  documentalmente. Estas fechas fueron elegidas por anomalías observadas, por lo
  que no constituyen shocks independientes de los resultados.

Fuentes: `05_saltos_margenes.csv` y `05_saltos_concentracion.csv`. Las contribuciones
se reconcilian con el cambio neto y, para firmas, con el agregado `lender_month`.

También se fija una cohorte por entidad con saldo positivo en ella y en otros
bancos en mayo de 2025, conservando todas esas personas hasta junio de 2026. La
entidad focal queda fuera del comparador si es banco. No se selecciona por caída
posterior. Las cohortes se superponen y difieren en riesgo, producto y composición.

| Entidad focal | Aporte focal (p.p.) | Otros bancos (p.p.) | Cambio conjunto | Todos los códigos reportantes |
|---|---:|---:|---:|---:|
| MercadoLibre | −1,38 | +2,86 | +1,48% | +2,21% |
| Ualá Bank | −8,14 | +2,12 | −6,02% | −5,84% |
| Naranja Digital | −4,37 | +0,65 | −3,73% | −2,88% |
| Tarjeta Naranja | −3,16 | +2,37 | −0,78% | +1,00% |
| Brubank | −5,61 | +5,78 | +0,17% | +1,84% |
| Credicuotas | −10,44 | −6,41 | −16,85% | −14,57% |

Los aportes usan saldo focal+otros bancos inicial; la última columna utiliza como
base el saldo con todos los códigos, e incluye posibles garantías. Por eso esa
columna no es una estimación depurada de deuda neta. Los saldos incluyen mora;
ninguna compensación significa acceso nuevo, sustitución causal o mayor bienestar.
Fuentes: `05_focal_resumen.csv` y `05_focal_otros_bancos.csv`.

La lectura para el paper queda abierta: hay compensaciones contables casi completas,
parciales y caídas conjuntas. La siguiente comparación debe separar transiciones de
situación crediticia y cambios de composición en estas mismas cohortes; después,
contrastar con exposiciones previas de fondeo y tasas. No seleccionar una entidad
porque confirma una dirección esperada ni construir instrumentos con estos saltos.
