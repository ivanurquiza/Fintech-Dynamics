# Pecking order de repago entre acreedores

Actualizado: 20 de septiembre de 2026. Nota de idea. Registra una hipótesis de
paper y su diseño candidato, con un resultado crudo preliminar ya corrido. No es
una identificación validada ni un resultado causal. Las afirmaciones normativas
marcadas como "verificar" no están comprobadas contra el texto ordenado.

---

## 0. La idea en un párrafo

Cuando el cobro judicial de una acreencia no garantizada de cien o doscientos mil
pesos cuesta más que la acreencia, el orden en que un hogar deja de pagar no lo
fija el contrato: lo fija la tecnología privada de cobro de cada acreedor, o sea
qué tan directamente cada uno puede alcanzar el flujo de caja del deudor. El riel
de pagos es una de esas tecnologías. Le da al prestamista prelación de hecho sin
prelación contractual. De ahí salen tres afirmaciones encadenadas: dentro de un
mismo deudor y un mismo mes el default está asignado y no es aleatorio entre
acreedores; el crecimiento del crédito con riel reasigna default hacia los bancos,
de modo que la mora bancaria de hogares puede subir sin que el hogar esté peor; y
las políticas que vuelven el riel disputable, interoperabilidad y multi-homing,
erosionan esa prelación.

La frase de política, que es lo que hace al paper citable fuera del gremio: la
regulación de pagos es, sin decirlo, regulación de prelación de acreedores en el
crédito no garantizado a hogares.

---

## 1. El hecho, tal como quedó en la corrida del 2 de septiembre

Muestra `person_lender_5pct`, personas con acreedores de dos o más grupos el mismo
mes. Clasificación por tecnología de cobro, no por regulación:

- **mutual**: cobra por código de descuento sobre el haber, antes de que la plata
  llegue al deudor;
- **billetera**: opera el riel de pagos del deudor (MercadoLibre 72634, Naranja
  Digital 45030, Ualá Bank 384, Brubank 143, Reba 45072, Pago Virtual del Sur 72638);
- **banco**: débito en cuenta, pero el deudor puede retirar antes;
- **no bancario sin riel**: retail, financieras de consumo, cooperativas; sólo
  gestión de cobranza.

| Grupo | Relaciones | Mora cruda | Mora multi-acreedor | Dentro del deudor-mes (p.p.) | Saldo medio |
|---|---:|---:|---:|---:|---:|
| Mutual | 258 K | 19,5% | 17,9% | **−3,48** | $1,14 M |
| Billetera | 6,27 M | 17,0% | 14,6% | **−1,77** | $0,50 M |
| Banco | 9,83 M | 10,6% | 14,2% | **−0,83** | $3,28 M |
| No bancario sin riel | 8,23 M | 25,7% | 23,6% | **+2,45** | $0,92 M |

Tres lecturas. El ordenamiento es monótono en la fuerza de la tecnología de cobro:
cuanto más directo el acceso del acreedor al flujo, mejor le pagan, a igual persona
y mes. La comparación cruda banco contra billetera se da vuelta al fijar la persona,
o sea que la brecha cruda es composición de clientela y el signo se invierte una vez
absorbido el deudor. Y bajo estrés los extremos se separan: entre agosto de 2024 y
julio de 2026 la brecha del mutual pasa de −2,1 a −5,3 p.p. y la del no bancario sin
riel de +1,8 a +3,1, mientras que la de la billetera no se mueve, oscila alrededor de
−1,7 todo el período. Ese último hecho hay que explicarlo, no decorarlo.

Salida intermedia: `output/tmp/agg_out.csv`, agregado, sin CUIT.

---

## 2. Por qué el hueco es real

La literatura de pecking order de defaults de hogares ordena **clases de producto**:
hipoteca contra tarjeta contra prendario contra estudiantil. Andersson, Chomsisengphet,
Glennon y Li (JMCB 2013) documentan el cambio de ese orden alrededor de la crisis;
Cohen-Cole y Morse plantean la misma pregunta para hipoteca contra tarjeta; la nota
de Liberty Street de 2017 la actualiza; y Ganong y Noel (AER 2020) separan default
por iliquidez de default estratégico.

Lo que nadie hace es ordenar **acreedores que tienen el mismo tipo de acreencia no
garantizada sobre la misma persona**, porque casi ningún país tiene un registro que
junte bancos, fintech, mutuales, retail y cooperativas bajo un mismo identificador de
deudor. Argentina sí: CENDEU tiene 587 entidades, de las cuales 60 son bancos y 516
no bancos, y el mismo deudor aparece con varias en el mismo mes. El activo de la base
no es el tamaño, es esa superposición.

---

## 3. El problema central del diseño

La especificación de base es

$$\text{Mora}_{ibt} = \alpha_{it} + \sum_{g} \beta_g \mathbb{1}\{g(b)=g\} + \Gamma X_{ibt} + \varepsilon_{ibt}$$

con $i$ deudor, $b$ acreedor, $t$ mes, $g(b)$ el grupo de tecnología de cobro del
acreedor, y $\alpha_{it}$ efectos fijos deudor×mes.

**Corrección respecto de la primera versión de esta nota (21-09-2026).** La
versión anterior escribía $\gamma_b + \beta\,\text{Riel}_b$, lo cual es
inconsistente: $\text{Riel}_b$ es función de $b$ y queda absorbido por el efecto
fijo de acreedor. La observación es correcta y viene de la actualización de
`debate_paper_2026-09-20.md`. Lo que la tabla preliminar de §1 computa en los
hechos es la media desmeanada dentro de deudor×mes por **grupo** de acreedor, sin
efectos fijos de entidad, que es lo que la ecuación de arriba representa. Si se
quisieran incluir efectos fijos de entidad habría que interactuar el riel con algo
que varíe en el tiempo.

Lo que compra ese efecto fijo: absorbe el shock de ingreso, el desempleo, la
inflación, la capacidad de pago, todo lo que es del hogar. Resuelve el problema de
selección obvio, que es que la clientela de cada tipo de acreedor difiere.

**Lo que no compra, y es el punto que hay que tener presente antes de escribir nada:**
los mecanismos que compiten por explicar el ordenamiento son todos a nivel acreedor y
sobreviven intactos al efecto fijo. Son cuatro:

1. **Enforcement por apropiación en origen.** El mutual descuenta del haber antes de
   que el deudor cobre. No hay elección del deudor. Es prelación efectiva en la
   cascada de caja.
2. **Enforcement por exclusión.** La billetera puede cortar el acceso al riel que el
   deudor usa todos los días. El deudor paga para preservar la opción. Sí hay elección,
   bajo un costo sombra.
3. **Información y matching.** El prestamista con los datos de pago dimensiona y
   precia mejor, así que su exposición está mejor calzada con la capacidad del deudor
   y falla menos aun a igual deudor. Es Parlour, Rajan y Zhu, y antes Mester, Nakamura
   y Renault sobre la cuenta transaccional como tecnología de monitoreo.
4. **Saliencia.** La app te muestra la deuda cada vez que la abrís para pagar el
   colectivo. Pagás la que ves.

Los cuatro predicen el mismo ordenamiento. Entonces el hecho, solo, no identifica un
mecanismo. **El pecking order es la primera sección del paper, no el paper.**

---

## 4. Los tests que separan los mecanismos

**Enforcement contra información.** La información predice que la ventaja existe desde
la originación y es estable a lo largo de la vida del crédito, porque viene del
tamizado. El enforcement predice que la ventaja aparece en el margen de asignación,
o sea exactamente cuando el hogar tiene que elegir a quién no pagarle. El test es
condicionar a que el deudor esté al día con al menos un acreedor y en mora con al
menos otro. Es la lógica de Ganong y Noel de liquidez contra estratégico, trasladada
del corte transversal de productos al corte transversal de acreedores.

La versión dinámica es mejor que la de niveles. Con efectos fijos deudor×mes y
deudor×acreedor, y los 24 bloques del panel, se estima quién se deteriora primero
dentro de la misma persona: un hazard de transición a situación 3 o peor. Una historia
de política contable predice desplazamiento paralelo; una de conducta predice orden
distinto en la secuencia de deterioro y tasas de cura distintas.

**Enforcement contra saliencia.** Se separan con multi-homing. Si la amenaza es cortar
el riel, la bite cae con la cantidad de rieles alternativos que el deudor ya tiene. La
saliencia no depende de eso: la app te sigue notificando. La variación existe y crece
rápido: personas con banco y billetera a la vez pasan de 12,4% en agosto de 2024 a
22,2% en julio de 2026; con billetera, de 23,9% a 39,7%; con dos o más tipos de
acreedor, de 29,9% a 39,3%.

Advertencia: el multi-homing es endógeno, quien multi-homea difiere. Dentro del
deudor×mes el nivel está bien; la interacción necesita que el estatus sea
predeterminado y, en el mejor de los casos, instrumentado. Como está, es evidencia
consistente, no identificación.

**Falsaciones que salen gratis.** Si el mecanismo es enforcement privado, la ventaja
del riel debería desaparecer donde existe un remedio legal real, o sea en las
relaciones con garantía preferida, observables en las seis columnas de garantías del
corte mensual. Y debería ser decreciente en el monto, porque para tickets grandes la
vía judicial vuelve a ser rentable y domina. Las dos predicciones son direccionales y
contrastables.

---

## 5. Amenazas, en orden de peligro

**5.1 Composición de producto y monto. Esta es la que puede matar la idea.** Los
saldos medios difieren mucho, $3,28 M en bancos contra $0,50 M en billeteras, y
CENDEU no trae tipo de producto ni plazo. Un plazo corto produce mecánicamente menos
atraso observado a un horizonte dado. Si el ordenamiento no sobrevive dentro de bandas
de monto y excluyendo lo garantizado, no hay paper. Es el primer cálculo que hay que
hacer.

**5.2 Contabilidad contra conducta.** La situación 1 a 5 la asigna el acreedor. Si los
no bancarios previsionan o castigan más tarde, el diferencial es política contable y no
jerarquía de repago.

El test que se proponía originalmente no sirve: `days_past_due` no está completo. Entre
las relaciones en situación 3 a 5, sólo el 11% de las bancarias y el 0,5% de las no
bancarias tienen un valor positivo, y la mediana es cero en los cuatro grupos. Por
entidad: Santander 21,4%, Provincia 19,3%, Galicia 17,5%, Naranja Digital 10,7%,
Nación 8,5%, MercadoLibre 1,9%, y Tarjeta Naranja, CFN, Credicuotas y Finanzas
Digitales exactamente 0%. Usarlo invertiría el ordenamiento por puro artefacto de
reporte.

La respuesta no está en los datos, está en la norma. **Verificar en el t.o. de
Clasificación de Deudores** si la situación de cartera de consumo y vivienda es función
mecánica de días de atraso, con umbrales del orden de 31, 90, 180 y 365 días, y si los
PNFC están sujetos a la misma regla al reportar a la Central. Si cierra, la
discrecionalidad del acreedor desaparece para la población de interés y la crítica se
muere sin necesitar el campo. Si no cierra, el paper depende del test de secuencia de
§4 y hay que decirlo con todas las letras.

**5.3 Umbral de $25.000 sin indexar.** Las entidades informan deudor por deudor sólo
desde ese saldo, es nominal y no se actualiza, así que con inflación entra gente al
registro sin que cambie su situación. Pega más fuerte en el ticket chico, o sea en la
billetera, que es justo la población de interés. La mediana de mora de Mercado Pago
está alrededor de $116.000, cuatro veces el umbral, o sea cerca del corte. Réplica
obligatoria en la submuestra de relaciones siempre por encima del umbral en los 24
meses.

**5.4 Sesgo del `24DSF`.** El panel de 24 meses conserva los deudores sanos de entidades
dadas de baja y borra sus morosos, hacia atrás también. El nivel de mora pasado queda
subestimado y el crecimiento medido sobre el `24DSF` queda exagerado. Es acotable
comparando el corte `AAAAMMDEUDORES` de un mes contra la columna de ese mes en el
`24DSF`, y contando altas y bajas en `maeent`. Esto deja de ser una nota suelta y pasa
a ser una sección del paper en el momento en que se descompone el alza de la mora
(ver §8.1).

**5.5 Mezcla de períodos en el corte mensual.** 418 entidades informaron julio y 109 con
un mes de rezago, concentradas en no bancarias (90 PNFC). Filtrar a `period=202607` baja
la tasa de morosos de 28,2% a 26,9%, borrando siempre a los prestamistas con más mora.
Recomendación: no filtrar, controlar por `period`.

**5.6 Exclusión endógena por Ley 25.326.** El archivo no incluye a quien ejerció
rectificación o supresión. Quien reclama tiende a ser quien tiene registro adverso, y
quien sabe reclamar tiende a ser más sofisticado. No lo vi mencionado en el debate
público y conviene declararlo.

---

## 6. Personas contra empresas

El panel de firmas existe y es el universo, no muestra: `firm`, empresa × entidad × mes,
del orden de 14,3 millones de filas, 394.052 empresas en el panel de 24 meses y 285.419
en el corte de julio.

Argumentos para que las empresas sean la muestra principal y no el complemento. El
multi-acreedor es bastante más frecuente, así que el efecto fijo deudor×mes tiene más
potencia por observación. Hay actividad ClaNAE, o sea controles sectoriales que en
personas no existen. Y el mecanismo es más nítido: para un comercio el riel no es
opción de valor, es un torniquete sobre el flujo, porque el prestamista descuenta de la
liquidación de ventas por QR o POS. Eso es exactamente el setting de Rishabh y
Schäublin, con descuento automático de un porcentaje de cada venta, y ahí enforcement
deja de ser una interpretación y pasa a ser una cláusula.

Dos advertencias.

**El argumento institucional de §5.2 se da vuelta.** En cartera comercial la
clasificación es una evaluación de capacidad de repago, o sea discrecional. La salida
es la cartera comercial asimilable a consumo, que son las exposiciones por debajo de
cierto monto que el t.o. permite clasificar con el criterio mecánico, y que es
justamente el segmento donde presta el crédito con riel. **Verificar el umbral vigente.**

**El prefijo de CUIT no separa negocio de hogar.** Los monotributistas son personas
humanas, prefijos 20, 23, 24 y 27, y son la clientela típica del crédito a vendedores.
Buena parte de las firmas económicas está en el panel de personas. El campo de actividad
del padrón de ARCA es lo que permite separarlas, y hay que hacerlo explícitamente antes
de interpretar cualquier corte persona contra empresa.

---

## 7. Lo que la base no tiene, y lo que hay que pedir

El archivo distribuido **no trae tipo de asistencia**. El corte mensual tiene entidad,
período, tipo y número de identificación, actividad, situación, préstamos y garantías,
seis columnas de garantías y contragarantías, previsiones, deuda cubierta, proceso
judicial o revisión, refinanciaciones, recategorización obligatoria, situación jurídica,
irrecuperables y días de atraso. El panel de 24 meses tiene menos todavía: situación,
monto y proceso judicial por bloque mensual.

Tampoco hay tasa, plazo, monto original ni destino. Y los cambios de saldo mezclan
desembolsos, pagos, capitalización de intereses y refinanciación, así que no se puede
tratar cada aumento como préstamo nuevo. El campo `refinanced` es codificado, no dummy:
toma 0 (21,1 M), 9 (16,4 M, centinela de no informa) y 1 (0,47 M, el único informativo).

Proxies disponibles para producto: banda de monto, las columnas de garantías (sólo en
el corte mensual, no en el panel), el tipo de acreedor cuando determina casi
unívocamente el producto, y la actividad del deudor.

**Pedido.** El campo "tipo de asistencia" sí existe en lo que las entidades reportan bajo
la Sección 3, diseños 4301 y siguientes. No está en el archivo distribuido pero el BCRA
lo tiene. Es un pedido chico, va al mismo escrito de Ley 27.275 que ya está redactado en
`claude/mail_cendeu_historico.md`, y es exactamente lo que blinda el paper contra la
amenaza 5.1.

---

## 8. Qué se construye encima del hecho

Tres candidatos de segundo acto, en orden de cuánto rinden con los datos que hay.

### 8.1 Descomposición del alza de la mora de hogares

En julio de 2026 el 26,9% de las personas está en mora, contra 14,4% de las empresas, y
el problema es de hogares. La pregunta: cuánto de ese aumento es el hogar y cuánto es la
recomposición de acreedores.

Mecánica: varianza del alza explicada por los efectos deudor×t contra acreedor×t, más un
contrafactual que fija la composición de acreedores de cada deudor en agosto de 2024 y
repondera. Si la jerarquía es real y el crédito con riel crece, la mora bancaria medida
sube sin que el hogar esté peor, porque el default se está reasignando. No necesita
instrumento, es barato, y contesta la pregunta que el debate público argentino está
haciendo mal.

Condición previa: acotar el sesgo del `24DSF` de §5.4, porque no se puede descomponer un
crecimiento que el archivo exagera por construcción.

### 8.2 Incidencia de la dilución

El margen dominante en el panel no es sustitución sino apilamiento. Transiciones de
agosto de 2025 a julio de 2026, personas presentes al inicio, muestra 5%: de 410.322
personas sólo bancarias, el 19,0% suma un acreedor no bancario en once meses sin soltar
el banco, mientras que sólo el 1,3% pierde el banco y queda con no banco. La sustitución
pura es chica; la complementariedad es grande.

Pregunta: cuando entra un acreedor nuevo, cuál de los acreedores preexistentes del mismo
deudor paga el costo, y está ordenado por la posición de enforcement del incumbente.

El punto de identificación que lo hace viable: la decisión de apilar es endógena, pero se
absorbe, porque la comparación es entre incumbentes **del mismo deudor**. Nunca hace
falta que la entrada sea exógena. Es el truco de Khwaja y Mian aplicado a un evento a
nivel deudor en vez de un shock a nivel prestamista.

El gancho teórico: la externalidad de dilución de Bizer y DeMarzo supone igual prelación
entre acreedores. Si el entrante es senior de hecho porque controla el riel, la
externalidad es mayor y es asimétrica. Ahí la jerarquía deja de ser decorativa y pasa a
predecir la incidencia.

Límite honesto: para afirmar que el entrante **causa** la pérdida del incumbente, y no que
el deterioro se está simplemente asignando, hace falta entrada exógena. El instrumento
natural sería el shock de oferta a nivel CP tipo Greenstone, Mas y Nguyen, pero Mercado
Crédito es el 76% del crédito pnfc_fintech, así que el shift-share tendría un shock
dominante y la inferencia de Borusyak, Hull y Jaravel no se sostendría. Queda en
Goldsmith-Pinkham, Sorkin y Swift, o sea identificación por exogeneidad del share, y el
share de Mercado Crédito por CP es claramente endógeno. Sin instrumento creíble, el
enunciado defendible es de incidencia y asignación, no de causalidad de la entrada.

### 8.3 Contrafactual de política

La A 8206 del 12 de mayo de 2025, QR de transporte interoperable, escalonada por sistema
de transporte, es el único tramo de interoperabilidad adentro de la ventana de CENDEU.
Los tramos grandes de Transferencias 3.0 son de 2021 y 2022 y quedan afuera; el QR de
crédito interoperable del 30 de abril de 2024 queda justo antes del inicio.

Si el escalonamiento mapea a geografía, es el cierre causal: la ventaja del riel debería
caer donde y cuando el riel se vuelve disputable. Si no mapea, el gradiente de
multi-homing de §4 lo sostiene como evidencia consistente y hay que decirlo así, sin
vender identificación que no hay.

---

## 9. Literatura

**Pecking order de defaults de hogares.** Andersson, Chomsisengphet, Glennon y Li, JMCB
2013. Cohen-Cole y Morse. Liberty Street, 2017. Ganong y Noel, AER 2020, para la
separación entre iliquidez y default estratégico. Todos ordenan clases de producto. Es
el hueco.

**Tecnología de enforcement y oferta de crédito.** Gertler, Green y Wolfram, Digital
Collateral, QJE 2024, 139(3): 1713-1766: activos que el prestamista apaga a distancia.
Nuestro caso es la versión blanda, exclusión de un flujo en vez de apropiación de un
stock, más barata de implementar y más fácil de evadir. Assunção, Benmelech y Silva,
RFS 2014, sobre derechos de repossession y democratización del crédito en Brasil. Vig,
JF 2013, sobre SARFAESI y derechos del acreedor en India.

**El antecedente más cercano, y por qué no nos come el paper.** Rishabh y Schäublin,
Payment Fintechs and Debt Enforcement. Trabajan con un solo fintech indio que presta a
comercios con POS y descuenta automáticamente el 10% de cada venta. Diseño de
regresión discontinua en una ventana de siete días alrededor del desembolso. Encuentran
que los repetidores no performantes bajan las ventas registradas alrededor de 17%
inmediatamente después del desembolso, y que el mecanismo no es exclusión sino **desvío**:
rutean ventas a efectivo, que el fintech no captura. Su test de heterogeneidad es el
cash crunch de 2018, donde no hay efectivo y no hay desvío. Y el desvío aparece en
deudores de score alto, no bajo, consistente con default voluntario habilitado por
acceso alternativo al crédito.

Es complemento, no competencia. Ellos tienen el micro del desvío dentro de un
prestamista; nosotros tenemos el ordenamiento entre prestamistas, que ellos no pueden
ver. Y su cash crunch es nuestro test de interoperabilidad dado vuelta: donde rutear
alrededor del riel es caro, el enforcement funciona.

**Pagos y crédito.** Parlour, Rajan y Zhu, RFS 2022, modelan el flujo de pagos como
información para seleccionar a quién prestar. Ghosh, Vallee y Zeng sobre datos de pago
y crédito fintech. Berg, Burg, Gombović y Puri, RFS 2020, sobre huella digital y scoring.
Mester, Nakamura y Renault, RFS 2007, y Norden y Weber, sobre la cuenta transaccional
como tecnología de monitoreo, que es el ancestro directo del canal de información y el
que hay que vencer.

**No exclusividad y dilución.** Bizer y DeMarzo, JPE 1992, banca secuencial. Parlour y
Rajan, AER 2001, competencia en contratos de préstamo. Degryse, Ioannidou y von
Schedvin, JF 2016, respuesta del incumbente a la entrada con el registro sueco. Es el
antecedente más cercano para §8.2, y hace la respuesta del incumbente en volumen, no la
incidencia ordenada por posición de enforcement.

**Sustitución banco y no banco.** Tang, RFS 2019. Di Maggio y Yao, RFS 2021. Buchak,
Matvos, Piskorski y Seru. Tang escribe explícitamente que el econometrista no observa si
el deudor P2P tenía acceso bancario equivalente; nosotros observamos a la misma persona
en los dos sistemas, en el mismo mes, con el mismo identificador.

---

## 10. Orden de trabajo

1. **El test que mata o salva la idea.** Replicar la tabla de §1 dentro de bandas de
   monto y excluyendo relaciones con garantía preferida. Tabla cruda, sin regresión,
   igual que la primera vez. Si el ordenamiento no sobrevive, la idea se cae acá.
2. Réplica en la submuestra de relaciones siempre por encima del umbral de $25.000.
3. Verificación normativa de §5.2: clasificación mecánica por días de atraso en cartera
   de consumo, y alcance a los PNFC. Y de §6: umbral de cartera comercial asimilable a
   consumo.
4. Separar monotributistas dentro del panel de personas con la actividad del padrón, y
   rehacer el corte persona contra empresa.
5. Hazard de transición a situación 3 o peor con efectos fijos deudor×mes y
   deudor×acreedor: quién se deteriora primero dentro de la misma persona.
6. Gradiente de multi-homing sobre la ventaja del riel.
7. Acotar el sesgo del `24DSF` contra el corte mensual, como insumo de §8.1.
8. Agregar "tipo de asistencia" al pedido de Ley 27.275.

Regla de reporte, la misma de siempre: si un paso da nulo, se reporta el nulo con su
intervalo y su MDE. Un nulo sin potencia declarada no es un nulo, es ausencia de diseño.

---

## Primera exploración empírica, 23 de septiembre de 2026

Ver `Code/analysis/pecking_order/01_orden_de_repago.ipynb` y
`Code/analysis/pecking_order/resultados.md`. Resumen: el primer impago es parcial en 97% de
los casos y la selección persiste; el orden por acreedor lo fija el acceso al flujo de
ingresos del deudor (MercadoLibre, bancos digitales, mutuales y agentes pagadores de sueldos
provinciales arriba; retail y financieras de consumo abajo); Macro cobra primero en las
cuatro provincias donde es agente financiero y no fuera de ellas; la prioridad cambia con la
fuente de ingreso del deudor; y la recategorización obligatoria del corte de julio de 2026
reproduce el orden. Varias de las pruebas de las secciones 3 y 4 de esta nota quedan
respondidas ahí; las que no, están listadas en `resultados.md`.

---

## Comentario, 28 de septiembre de 2026: el mecanismo, en claro

**El enunciado.** En crédito no garantizado a hogares, cobrar judicialmente cuesta más que
la acreencia, así que la prelación contractual no existe en la práctica. La reemplaza una
prelación de hecho: cobra primero el acreedor que está sentado sobre la cuenta donde entra
el ingreso del deudor, porque puede debitar la cuota en el momento en que la plata se
acredita, antes de que el deudor decida nada. Sueldo en Macro, haber jubilatorio en el banco
pagador, código de descuento de la mutual, saldo de la billetera de Mercado Pago: es el mismo
mecanismo con cuatro nombres. Lo que ordena el default no es banco contra fintech ni
tecnología de originación. Es **quién controla el flujo**.

**Una corrección a la §1.** La clasificación de esa tabla asigna la tecnología de cobro por
acreedor ("banco: débito en cuenta, pero el deudor puede retirar antes"). Los resultados del
23-sep muestran que eso está mal planteado: Macro es tan senior como una mutual en Salta,
Jujuy, Misiones y Tucumán (0,21) y mucho menos fuera de ellas (0,62). El mismo banco es senior
para un deudor y no para otro. El tratamiento vive en la **relación**, no en el acreedor:

$$D_{ib} = \mathbb{1}\{b \text{ controla la cuenta donde } i \text{ cobra}\}$$

Eso resuelve de paso el problema de la §3. Como $D_{ib}$ varía entre deudores dentro del
mismo acreedor, se pueden meter a la vez efectos fijos deudor×mes y acreedor (o acreedor×mes):

$$\text{Cae}_{ibt} = \alpha_{it} + \gamma_{b} + \beta\, D_{ib} + \Gamma X_{ibt} + \varepsilon_{ibt}$$

$\alpha_{it}$ absorbe la capacidad de pago; $\gamma_b$ absorbe todo lo que es del acreedor
(producto típico, política de cobranza, criterio de reporte, marca). $\beta$ sale de comparar,
dentro de Macro, a sus deudores que cobran ahí con los que no. Es la especificación que hay
que escribir en el paper. Las razones de chances por categoría quedan como hecho descriptivo.

**Qué separa enforcement de información.** Las dos historias predicen el mismo ranking en el
corte transversal. Se separan con cambios en dónde cobra el deudor **después** de haber
tomado el crédito. La información se usa al originar; si la cuenta sueldo se mueve después,
el tamizado ya está hecho y no cambia. El enforcement sí cambia, porque cambia quién puede
debitar. Entonces la prueba es: relaciones originadas antes del cambio de cuenta, y cómo se
mueve su prioridad después. La edad jubilatoria es el primer cambio de ese tipo que tenemos
(`diag_edad_jubilatoria.py`, figura `10_edad_jubilatoria`): a los 60 las mujeres y a los 65 los
varones pasan a cobrar en el banco pagador de ANSES, y la protección de MercadoLibre se
debilita justo ahí, cinco años antes en mujeres que en varones. Falta restringir a relaciones
previas a la edad legal, que es lo que convierte esa figura en el test de enforcement contra
información. La saliencia de la app tampoco debería moverse con la jubilación, así que el
mismo corte la descarta.

**Qué separa débito de exclusión.** Para bancos y mutuales hay sólo débito. Para MercadoLibre
hay débito y amenaza de cortar la plataforma. El débito requiere que haya saldo en la
billetera; la exclusión no. Si la protección de MercadoLibre cae cuando el ingreso deja de
entrar a la billetera (jubilados, asalariados sin actividad registrada), el que opera es el
débito. Es lo que muestran los datos hasta ahora, pero sin separar por completo.

**Lo que puede matarlo, en una línea cada uno.** La situación es única por deudor-entidad, así
que un banco con varios productos cae más por construcción (el test es deudores con una sola
línea por entidad). Un prestamista que refinancia en silencio mantiene al deudor en situación
1, y eso es tolerancia, no prelación. La recategorización obligatoria no es una validación
independiente: se dispara por la misma dispersión de situaciones que mide el panel.

**Por qué importa fuera de Argentina.** Parlour, Rajan y Zhu dicen que competir por los flujos
de pago le quita al banco información. Acá el flujo le da al que lo controla algo más barato
que la información: le da prelación. Si eso es cierto, cada vez que un regulador decide dónde
se acredita un sueldo o un haber, o si una billetera puede recibirlo, está reasignando
prelación entre acreedores sin decirlo. Y el crecimiento de un prestamista senior de hecho
diluye a los demás (§8.2), lo que puede hacer subir la mora medida de bancos y retail sin que
el hogar esté peor.
