# Review de `debate_paper_2026-09-20.md`

20 de septiembre de 2026. Comentario crítico sobre la nota de continuidad de la
búsqueda de paper y sobre el mecanismo de reemplazo de acreedor que se propone
ahí. Está escrita para el otro agente y para Ivo. No contiene estimaciones
nuevas. Las afirmaciones normativas o de datos marcadas como "verificar" no
están comprobadas. Nota hermana: `pecking_order.md`, en esta misma carpeta.

---

## 0. Resumen del juicio

La segunda fricción que plantea la nota, la del cliente que necesita encontrar
quién lo reemplace, es una buena pregunta y no se superpone con la línea de orden
de repago. Pero tal como está formulada tiene un problema de identificación que no
es un pendiente de robustez sino un defecto de diseño, y tiene un riesgo de
prioridad grande con un paper publicado en JFE en 2022. Las dos cosas se pueden
arreglar, y el arreglo pasa por combinarla con la otra línea en vez de correrlas
en paralelo.

---

## 1. Lo que está bien planteado

**La distinción entre las dos fricciones es correcta y útil.** Separar el problema
de fondeo del banco del problema de reemplazo del cliente es la manera adecuada de
pensarlo, y la segunda es la menos explorada de las dos.

**Dos advertencias de la nota son exactamente las que hay que tener.** Primero, no
suponer que la fintech puede financiar el reemplazo: su fondeo no se observa y
suponerlo sería suponer la conclusión. Segundo, y esto es lo mejor de la nota, un
aumento de participación de la fintech porque cayó el banco no alcanza; hace falta
que suba el **nivel absoluto** del crédito fintech. La mitad de los papers de
sustitución se caen exactamente por confundir share con nivel.

**El punto sobre sucursales es el correcto.** Lo que importa son las sucursales de
los otros bancos, no las del banco que recorta. Esa es la partición local contra no
local de Gilje, Loutskina y Strahan, bien traída al problema de reemplazo.

**La lista de "qué buscaríamos en los datos" está bien construida**, en particular
la idea de estudiar saldos y relaciones sin inventar tipos de crédito, que es la
única postura defendible dado que el archivo distribuido de CENDEU no trae tipo de
asistencia.

---

## 2. El problema estructural: el tratamiento vive en la dimensión equivocada

La nota lo anota como pendiente: "distinguir el efecto de fintech de la selección
de quienes ya la usaban. Los efectos fijos no resuelven ambos". Es más serio que un
pendiente.

**Tener relación fintech previa es una variable que varía a nivel deudor.** El
efecto fijo deudor×tiempo, que es lo único que esta base regala y la razón entera
por la que CENDEU vale la pena, no puede identificar nada que varíe a nivel deudor:
lo absorbe. En la primera etapa, comparar acreedores del mismo deudor, el efecto
fijo trabaja y está bien usado. En el momento en que la pregunta pasa a ser qué le
ocurre al deudor según tenga o no relación fintech previa, se agota la moneda de
identificación sin comprar nada.

Y el tratamiento no es una característica neutral. Tener relación fintech previa es
un indicador revelado de al menos tres cosas: ser thin-file, estar racionado por el
banco, u operar sobre una plataforma de pagos. Son precisamente los atributos que
hacen que la respuesta a un recorte bancario difiera por razones ajenas a la
tecnología. La comparación entre deudores con y sin relación fintech previa, ante
un recorte comparable, no está identificada por construcción.

### 2.1 El instrumento natural choca con la otra dimensión

Lo que arreglaría la selección es instrumentar la relación fintech previa. El
candidato obvio es la penetración local de la plataforma. El problema es que esa
variable es casi la misma que la otra dimensión de la interacción propuesta, que es
la escasez de alternativas bancarias locales: las localidades con poca banca son
también, en buena medida, las localidades donde la billetera entró primero y pesa
más. Instrumento y moderador colapsan sobre la misma variación territorial. No es
un detalle corregible con controles; es una colisión de diseño que hay que resolver
antes, eligiendo otra fuente de variación para el tratamiento.

---

## 3. El outcome es una composición de tres cosas

"Mantener mejor su financiamiento" mezcla capacidad de oferta de la fintech, demanda
del deudor y selección de quién tenía relación previa. Como el fondeo de la fintech
no se observa, cosa que la propia nota señala, ni siquiera el signo del coeficiente
es interpretable sin supuestos adicionales. Si la fintech está a su vez restringida
en el mismo momento, el coeficiente puede dar cero por una razón que no tiene nada
que ver con la hipótesis.

Recomendación: separar desde el principio el margen extensivo, si aparece un
acreedor nuevo, del intensivo, cuánto crece el saldo. Y recordar que en el panel de
24 meses los cambios de saldo mezclan desembolsos, pagos, capitalización de
intereses y refinanciación, así que el margen extensivo es el más limpio de los dos.

---

## 4. El shock de oferta bancaria no es un pendiente, es el paper

La nota lista "justificar qué variación identifica oferta bancaria" entre lo que
falta. Sin ese shock no hay primera etapa, y sin primera etapa no hay diseño. Vale
tanto para la línea de reemplazo como para la de orden de repago, así que conviene
tratarlo como el cuello de botella común y no como un apéndice de una de las dos.

Tres candidatos, en orden de solidez.

**(a) Shock idiosincrático por banco estimado sobre CENDEU**, al estilo de
Greenstone, Mas y Nguyen tal como lo implementan Gutierrez, Jaume y Tobal: se
descompone el cambio de crédito banco×mercado en un componente de mercado y uno de
banco, y el efecto fijo de banco por período se interpreta como oferta. Es el más
prometedor porque la estructura territorial de CENDEU lo permite: 2.558 códigos
postales con actividad crediticia, 1.955 con cinco o más bancos que concentran el
99,6% de los deudores, y 34 bancos prestando en una mediana de 613 códigos postales.
Esa densidad es exactamente lo que el método necesita y es lo que el panel provincial
no tiene.

Dos condiciones antes de usarlo. Primera, **leave-one-out**: al estimar el efecto
fijo de banco hay que excluir el mercado receptor, cosa que el archivo de shocks
guardado todavía no hace, según `estado_revision_2026-09-13.md`. Es el defecto que
Gutierrez, Jaume y Tobal tampoco corrigen y que acá sale gratis. Segunda, y es la
que decide todo: **el shock tiene que predecir crédito nuevo observado a nivel
mercado**. Gutierrez, Jaume y Tobal advierten explícitamente que con frecuencias más
finas que la anual los shocks dejan de ser informativos, o sea que dejan de predecir
el crédito. Con seis trimestres y un desvío conjunto de 0,162, hay que testearlo
antes de construir nada encima.

**(b) Sensibilidad a tasas por composición de balance previa.** Es el candidato más
débil de los tres y conviene decirlo con todas las letras. La variación de tasas
argentina entre 2024 y 2026 no es un shock monetario identificado, es un cambio de
régimen con desinflación, desarme de LEFI y cambios en el régimen cambiario
ocurriendo a la vez. Y la sensibilidad del banco a las tasas no es exógena: está
determinada por la misma composición de balance que determina a quién le presta.

Hay además un problema de medición que no se arregla con efectos fijos. Para
interpretar la interacción tipo de prestamista por cambio de tasa como costo de
fondeo hace falta observar, de mínima, una de las dos tasas del prestamista no
bancario. No observamos ninguna, y CENDEU no tiene producto ni plazo. Una tarjeta
bancaria y una línea revolvente de un prestamista no bancario se repactan a ritmos
distintos por construcción contractual, así que el coeficiente va a recoger
frecuencia de repricing y mezcla de productos. La vía para destrabarlo es el régimen
informativo de PNFC, Sección 59, que incluye `TASA.TXT` con tasa promedio ponderada
por entidad y no es público. Va al pedido, no al diseño.

**(c) Un evento discreto: Galicia y HSBC.** La nota dice que no se identificó ninguna
fusión argentina concreta. Existe y cae dentro de la ventana de CENDEU: Galicia
cerró la adquisición de HSBC Argentina el 6 de diciembre de 2024 y la fusión legal y
operativa se completó a fines de junio de 2025. Son cuatro meses de pre y diecinueve
de post.

Vale una observación de diseño. La versión fuerte de este evento **no necesita
geografía**. En lugar de hacer Nguyen con cierres de sucursales, que exige el join
de código postal y los puntos de acceso que terminan en 2025, se puede tratar como
disrupción de relación identificada dentro del deudor, comparando la relación ex
HSBC contra los otros acreedores del mismo deudor en el mismo mes. Eso esquiva todas
las restricciones de datos que la propia nota levanta. Advertencias: una fusión es un
paquete, cierres más política crediticia más integración de cartera, y HSBC aportaba
del orden de 600.000 clientes sobre 20,6 millones de deudores, así que hay que
calcular potencia antes de comprometerse.

---

## 5. Riesgo de prioridad

La nota ya identificó a Franco, "The fintech lending channel of monetary policy",
para la línea de tasas. Bien visto. Falta uno más grande y más cercano a la línea de
reemplazo:

**Erel, I. y Liebersohn, J. (2022), "Can FinTech reduce disparities in access to
finance? Evidence from the Paycheck Protection Program", Journal of Financial
Economics 146(1): 90-118** (antes NBER 27659, "Does FinTech Substitute for Banks?").
Encuentran que los prestamistas fintech sustituyen a los bancos justamente donde la
presencia bancaria es débil. Ese es el titular de la línea de reemplazo, publicado
hace cuatro años, con un programa de oferta de rollout limpio que nosotros no
tenemos.

No invalida la pregunta, pero sí obliga a que la contribución sea otra. "Fintech
sustituye densidad bancaria" ya está tomado. Lo que no está tomado es qué le pasa
después al deudor reemplazado, que es donde entra la sección siguiente.

Conviene además leer a fondo, antes de fijar la contribución, la literatura de
sustitución banco y no banco: Tang (RFS 2019), Di Maggio y Yao (RFS 2021), Buchak,
Matvos, Piskorski y Seru.

---

## 6. La síntesis que propongo

Las dos líneas se necesitan. Cada una tiene lo que a la otra le falta.

**La línea de reemplazo aporta el shock.** Sin un shock de oferta bancaria, el orden
de repago se queda en un hecho descriptivo con efectos fijos, que es bueno pero no
alcanza para un paper.

**La línea de orden de repago aporta la interpretación.** Si un banco recorta y una
fintech reemplaza, la pregunta de bienestar no es cuántos pesos se reemplazaron. Es
qué pasa después. Si el deudor reemplazado pasa a servir a la fintech y deja de
servir al banco, eso no es acceso restituido, es prelación reasignada: el crédito
total no cayó y el sistema quedó peor. Ese es un resultado publicable y es
exactamente la Pregunta 4 de `preguntas_investigacion.md` contestada con la parte que
ese documento dejó abierta, "en mejores o peores condiciones y con qué desempeño
posterior".

**Y separa los dos mecanismos que el diseño de reemplazo, solo, no puede separar.**
Si la ventaja de la fintech para reemplazar viene de información, porque ya conoce al
cliente, se ve en **a quién** reemplaza, o sea en la selección sobre observables del
deudor. Si viene de enforcement, porque puede cobrar, se ve en **cómo se comporta la
deuda después** del reemplazo. Son predicciones distintas sobre objetos distintos y
las dos son contrastables con lo que hay.

### 6.1 Predicciones del diseño combinado

Bajo la hipótesis de información, la fintech reemplaza a deudores con historial
observable y buen comportamiento previo, y el desempeño posterior del crédito
reemplazado no difiere del contrafactual.

Bajo la hipótesis de enforcement, la fintech reemplaza también a deudores que el
banco no querría, porque puede cobrarles aunque no pueda evaluarlos mejor, y el
desempeño posterior muestra reasignación: la nueva relación se sirve y las
preexistentes se deterioran.

La segunda predicción es la interesante y es la que conecta con el hecho de
`pecking_order.md`, donde dentro del deudor y mes el orden de mora sigue la
inmediatez del acceso del acreedor al flujo de caja.

---

## 7. Sobre la analogía con Koont

Una observación técnica que conviene dejar registrada. La forma econométrica de
Koont, Santos y Zingales requiere tres cosas: exposición regional predeterminada,
una característica del banco que module la sensibilidad, y un shock cuyo mecanismo se
mida por separado.

Del lado del panel bancario tenemos las dos primeras y ninguna funciona bien: 24
provincias contra más de 3.000 condados, montos sólo en cierres trimestrales, y sobre
todo el hecho ya verificado de que apenas 13 bancos reportan montos en diez o más
provincias con mediana de 2. Sumado a que la adopción provincial ponderada por
depósitos entre los bancos grandes va de 40,9 a 55,0 con desvío 3,8, o sea que el
interactivo regional no tiene varianza donde está el volumen. Con eso el cluster
efectivo es 24 y la inferencia no se sostiene.

Donde la forma sí entra es en CENDEU, por la densidad territorial citada en §4(a).
Pero ahí hay que ser explícito sobre qué se le pide a esa regresión: Koont puede
interpretar la interacción digital por cambio de tasa como costo de fondeo porque
mide tasas y cantidades de depósitos; del lado del crédito, sin tasas ni producto, la
forma queda bien y el mecanismo no queda identificado.

Sugerencia de división del trabajo entre las dimensiones: la geografía no como
interacción triple sino como **fuente del shock** de oferta a nivel prestamista, y el
efecto fijo deudor×mes como **núcleo de identificación**. Cada dimensión haciendo lo
que sabe hacer.

---

## 8. Orden de trabajo sugerido

1. **Validar el shock de oferta bancaria.** Reestimar con leave-one-out y testear si
   predice crédito nuevo observado a nivel código postal. Si no predice, las dos
   líneas se caen juntas y conviene saberlo antes de invertir en geografía.
2. **Correspondencia de entidades.** `pda_lender_depto` identifica por nombre; hay que
   unirlo con `ent` de balances y CENDEU antes de cualquier diseño territorial.
3. **Validar el join código postal.** Es el insumo de la dimensión de alternativas
   locales. Tener presente que el domicilio del padrón es fiscal y puede no reflejar
   dónde opera la persona.
4. **Calcular potencia del evento Galicia y HSBC**: cuántos deudores tienen relación
   con el ex HSBC dentro de la ventana.
5. **Elegir otra fuente de variación para la relación fintech previa**, o aceptar
   tratarla como heterogeneidad descriptiva y decirlo, que es lo que la propia nota
   sugiere y me parece la postura honesta mientras no haya instrumento.
6. **Agregar al pedido de Ley 27.275** dos cosas: el campo "tipo de asistencia" de la
   Sección 3, diseños 4301 y siguientes, y `TASA.TXT` del régimen de PNFC, Sección 59.
   El primero blinda contra composición de producto; el segundo es lo único que
   destrabaría la línea de tasas.

---

## 9. Referencias citadas en este comentario

- Erel, I. y Liebersohn, J. (2022). Can FinTech reduce disparities in access to
  finance? Evidence from the Paycheck Protection Program. *JFE* 146(1), 90-118.
- Franco, L. The fintech lending channel of monetary policy. Alojado en el sitio del
  BCE, 2024.
- Gilje, E., Loutskina, E. y Strahan, P. (2016). Exporting Liquidity: Branch Banking
  and Financial Integration. *JF* 71(3), 1159-1184.
- Gilje, E. (2019). Does Local Access to Finance Matter? *Management Science*.
- Greenstone, M., Mas, A. y Nguyen, H. (2020). Do Credit Market Shocks Affect the Real
  Economy? *AEJ: Economic Policy* 12(1), 200-225.
- Gutierrez, E., Jaume, D. y Tobal, M. (2023). Do Credit Supply Shocks Affect
  Employment in Middle-Income Countries? *AEJ: Economic Policy* 15(4), 1-36.
- Khwaja, A. y Mian, A. (2008). Tracing the Impact of Bank Liquidity Shocks. *AER*
  98(4), 1413-1442.
- Nguyen, H. (2019). Are Credit Markets Still Local? Evidence from Bank Branch
  Closings. *AEJ: Applied*.
- Degryse, H., Ioannidou, V. y von Schedvin, E. (2016). On the Non-Exclusivity of Loan
  Contracts. *JF*.
- Tang, H. (2019). Peer-to-Peer Lenders Versus Banks: Substitutes or Complements?
  *RFS* 32(5).

---

# Addendum, 21 de septiembre de 2026

Comentario sobre `diseno_identificacion_2026-09-20.md` y la actualización de
`debate_paper_2026-09-20.md`. Incluye investigación web sobre los puts y el
desarme de LEFI, y una comprobación directa sobre `balhist.txt`. Las fuentes
nuevas están al final del addendum.

Juicio general: `diseno_identificacion` es la mejor nota del proyecto hasta
ahora. Dos cosas en particular. La detección de que la celda de `shock_cendeu`
promedia el valor ajustado completo, que incluye el efecto del mercado atendido,
y por eso no recupera el coeficiente del banco: es un error real y cambiaba el
significado del archivo guardado. Y la insistencia en que forma Bartik no
equivale a exogeneidad, que es donde se cae la mitad de esta literatura.

La tabla de superposición de mayo de 2025 es exactamente el chequeo que había
que hacer, y el resultado ordena la muestra sin discusión: **3.951 personas
jurídicas con banco y `pnfc_fintech` contra 148.506 personas humanas** en la
muestra del 5%. Las firmas sirven para estimar oferta bancaria con multibanco,
74.958 con dos o más bancos, pero no para estudiar sustitución hacia el crédito
no bancario.

---

## A. Qué son los puts

Conviene dejarlo escrito porque el nombre confunde.

Un put, u opción de liquidez, es un seguro que el BCRA le vendió a los bancos
para que compraran deuda del Tesoro. El banco pagaba una prima y a cambio
obtenía el derecho de venderle ese título al Central a un precio pactado: en la
versión americana, cuando quisiera; en la europea, en fechas determinadas. En la
práctica le sacaba al banco el riesgo de precio del soberano. Si el bono se
desplomaba, el Central se lo compraba igual.

Fueron creados en **julio de 2022**, durante la gestión de Batakis, y siguieron
ofreciéndose después. El objetivo era que los bancos financiaran al Tesoro en un
momento en que el mercado no lo hacía. El costo es que constituyen un pasivo
monetario contingente: si los bancos ejercen, el Central tiene que emitir.

Cronología y magnitudes:

| Momento | Hecho | Magnitud |
|---|---|---|
| Julio 2022 | Creación | |
| Pico | Stock de títulos cubiertos | ~$18 billones |
| Julio 2024 | Recompra voluntaria | $13,17 billones, 78% del total; devolución de primas ~$90.000 millones |
| 10 de junio de 2025 | Rescisión del saldo remanente | $5,9 billones, ~22%; compensación por primas ajustadas $0,023 billones |

La lógica de la Ruta C es que perder el put cambia la demanda precautoria de
liquidez del banco, y por lo tanto su disposición a prestar, sin necesidad de
observar una salida contemporánea de depósitos. Es una idea buena y es
efectivamente distintiva.

---

## B. Por qué la Ruta C es más frágil de lo que la nota admite

La nota registra dos obstáculos, la tenencia elegida y la rescisión acordada.
Faltan dos, y son peores que los anotados.

**B.1 La selección corre en la dirección del resultado esperado.** El comunicado
dice que el BCRA y las entidades **acuerdan** la rescisión, y los bancos cobraron
por rescindir. Pero el problema serio no es el precio, es quién quedó. Los bancos
que llegaron a junio de 2025 con puts vigentes son un residuo auto-seleccionado:
conservaron el seguro durante un año entero en el que el Central estaba
visiblemente tratando de recomprarlo, y después del episodio de julio de 2024 en
que el 78% del stock se canceló. BST, por ejemplo, declara haber rescindido todos
los suyos en julio de 2024.

Ese residuo selecciona precisamente a los bancos que más valoraban la cobertura
de liquidez, que son los que con mayor probabilidad iban a recortar crédito en el
segundo semestre de 2025 por razones ajenas al put. La selección empuja el
estimador hacia el resultado que la hipótesis predice. Es el peor caso posible de
endogeneidad: no atenúa, confirma espuriamente.

**B.2 La fecha no se puede separar.** El anuncio de rescisión es del 10 de junio
de 2025. El anuncio del fin de la oferta de LEFI es del 9 de junio de 2025. Son el
mismo paquete de política, comunicado con un día de diferencia. A eso se le suman,
en las diez semanas siguientes, el desarme efectivo del 10 de julio, la integración
diaria de encajes desde el 18 de agosto y el incremento transitorio de cinco puntos
desde el 19 de agosto. Cuatro tratamientos superpuestos.

Sumado a lo que la propia nota reconoce, que si la exposición sólo distingue a unos
pocos bancos públicos no sostiene interpretación causal amplia, la conclusión es que
el put **no funciona como shock separable**. Sí funciona como componente de una
exposición compuesta, que es lo que propongo en la sección D.

---

## C. El desarme de LEFI: mecánica y magnitudes

Esto no estaba en ninguna de las dos notas y es lo que vuelve al episodio
interesante. La secuencia, con números:

**El día del desarme.** Los bancos tenían del orden de **$15,5 billones** en LEFI.
El 10 de julio de 2025 el BCRA dejó de ofrecerlas y ese stock se redirigió casi
íntegramente a cuentas corrientes en el Central, que subieron **$9,8 billones en un
solo día**, pasando de $9,4 a $19,2 billones.

**El derrumbe inmediato de tasas.** Caución de 23% a 16% anual. Call privado de 34%
a 18%. LECAP corta de 33% a 30%. El Tesoro había anticipado que los fondos irían a
LECAP y esa sustitución no se materializó en la magnitud esperada.

**La corrección, y el exceso.** El 16 de julio el Tesoro hizo una licitación
extraordinaria que absorbió **$4,7 billones** colocando LECAP a 47,8% y 47,1% TIREA
en los tramos cortos, contra 41,5% a 44,7% en la licitación previa. El BCRA absorbió
en paralelo **$5 billones** con pases pasivos al 35% y ventas de títulos en el
secundario. Las tasas volvieron a los niveles previos en la misma semana y después
los superaron.

**El resultado sobre las tasas relevantes**, promedios mensuales TNA según el
Informe Monetario de agosto de 2025, ya citado en `tasas_argentina_2026-09-20.md`:

| Serie | Junio 2025 | Julio 2025 | Agosto 2025 |
|---|---:|---:|---:|
| TAMAR bancos privados | 33,62 | 34,32 | 53,41 |
| Call interbancario a un día | 32,75 | 42,81 | 69,29 |
| Adelantos en cuenta corriente | 45,89 | 51,54 | 72,05 |

Tres razones por las que este episodio es mejor candidato que el put.

Es grande. No hay nada comparable en la ventana de CENDEU.

Es una perturbación al **precio y a la disponibilidad de liquidez bancaria** que no
nace de un cambio en la demanda de crédito de los hogares o las firmas. Eso es
exactamente lo que un diseño de oferta necesita, y es lo que la variación de tasas
de 2024 y principios de 2025 no ofrece, porque ahí la tasa baja acompañando la
desinflación.

Y la incidencia entre bancos es heterogénea y predecible desde la composición de
balance previa, que es la lógica de la Ruta B.

**El punto que nos toca directamente.** Los adelantos en cuenta corriente pasaron
de 45,9% a 72,1% en dos meses. Ese es el instrumento de capital de trabajo de los
comercios, que es la población del crédito no bancario con riel. Si el descubierto
bancario se vuelve prohibitivo y el crédito no bancario no repacta al mismo ritmo,
porque parte de tres dígitos y se fondea contra otra curva, lo que se observa es
sustitución empujada por el fondeo del banco y no por una decisión del deudor. Es
la primera etapa que a la línea de sustitución le falta.

---

## D. Junio a agosto de 2025 es un solo cambio de régimen, no cuatro shocks

Esta es la recomendación de diseño del addendum.

Tratar de separar el put de la LEFI y del encaje es pelear por una separación que
la política no hizo. Las Rutas B y C deberían fusionarse en **una exposición
compuesta a la reforma de liquidez de 2025**, medida antes del 9 de junio de 2025,
con cuatro componentes:

1. tenencia de LEFI sobre activos;
2. títulos cubiertos por puts vigentes sobre activos;
3. incidencia de encaje predicha por composición previa del pasivo, separando
   exigencia total de integración admitida en títulos, y representando la
   integración diaria de agosto como un cambio de régimen y no como una alícuota;
4. dependencia previa de fondeo remunerado y liquidez disponible.

El estimando deja de ser "el efecto causal de perder el put" y pasa a ser **"el
efecto de un endurecimiento del régimen de liquidez cuya incidencia varió según el
balance previo"**. Es menos elegante y mucho más defendible. Y admite el panel de
cambios sucesivos que la Ruta B ya proponía, en vez de un evento único.

Ventana sugerida: exposición fijada a mayo de 2025 o antes, para preceder al
anuncio del 9 de junio; tratamiento en julio y agosto; y post hasta julio de 2026,
con la relajación de encajes de octubre a diciembre de 2025 como fase de reversión
y no como parte del tratamiento. Entra cómoda en CENDEU, agosto de 2024 a julio de
2026, con once meses de pre.

Advertencias que hay que escribir en el paper antes que el referee. La política
responde a condiciones bancarias y macro, así que la exposición no es aleatoria;
lo que se puede defender es incidencia diferencial condicional a observables de
balance. Y los encajes afectan cantidades directamente, así que no se los puede
usar como instrumento de una tasa y hablar de elasticidad pura al precio. Eso ya
está bien dicho en la Ruta B y conviene mantenerlo.

---

## E. Por qué este shock conecta con la prioridad de repago

Si el crédito bancario se encarece y se raciona mientras el crédito no bancario no
lo hace al mismo ritmo, la composición de acreedores de cada deudor cambia **por
razones de oferta**. Eso es precisamente el mecanismo de reasignación que plantea
`pecking_order.md`, ahora con un empujón exógeno al deudor.

La predicción conjunta, que ninguna de las dos líneas genera por separado: un shock
de liquidez bancaria que empuja deudores hacia acreedores con riel debería, bajo la
hipótesis de enforcement, **deteriorar la mora bancaria medida de los mismos
hogares** sin que su capacidad de pago haya cambiado. Se contrasta con efectos fijos
deudor×mes comparando, dentro de la misma persona, la trayectoria de la relación
bancaria contra la del acreedor entrante.

Es el segundo acto que a la nota de pecking order le faltaba y la interpretación que
a la línea de sustitución le falta. Conviene no correrlas en paralelo.

---

## F. Hallazgo de datos: las cuentas de orden están en `balhist`

Comprobación directa sobre `Data/raw/bcra_balhist/balhist.txt`, 285 MB, formato de
cuatro columnas entidad, período, cuenta, saldo.

Conteo de filas por primer dígito de la cuenta en toda la historia:

| Prefijo | Filas |
|---|---:|
| 1 | 2.741.022 |
| 5 | 2.419.138 |
| 3 | 1.780.657 |
| 9 | 885.194 |
| 7 | 770.010 |
| 8 | 262.220 |
| 4 | 181.262 |
| 2 | 152.609 |
| 6 | 57.003 |

O sea que el pipeline actual, que usa 1, 3, 4 y 5, **está dejando afuera las
familias 6 y 7**, que son cuentas de orden. En diciembre de 2024 no aparecen
cuentas 9xxxxx, que parecen ser de períodos antiguos, pero sí aparecen 6xxxxx y
7xxxxx, con la misma estructura que los depósitos: el tercer dígito marca moneda,
1 para pesos y 5 para moneda extranjera.

Códigos presentes en 202412, con cantidad de entidades que reportan: 620004 (73),
711046 (69), 610005 (69), 711023 (63), 620002 (63), 711025 (58), 715053 (54),
711057 (53), 711084 (52), 620001 (46), 715023 (44), 711086 (41), 715025 (38),
715046 (35), más 651004, 653001, 656002, 656004, 721033, 721074, 721084, 721086,
725084, 725086 con menor cobertura.

**Implicancia para la Ruta C.** Si los puts se registran como cuenta de orden, que
es lo que sugiere el estado contable de Bancor con sus partidas fuera de balance,
entonces la exposición no hay que scrapearla PDF por PDF: está en la base mensual
para todo el sistema, con seis dígitos de detalle y desde hace décadas. Eso
convierte la Ruta C de un ejercicio artesanal sobre un puñado de bancos en un panel
completo.

**Lo que falta para cerrarlo.** El nomenclador. Hay que bajar el Manual de
Contabilidad y el Plan de Cuentas del BCRA e identificar qué código corresponde a
opciones de liquidez, presumiblemente en la familia de derivados. Es trabajo de
media hora y decide si la ruta existe.

**Advertencia de escala, y hay que resolverla antes de entusiasmarse.** Sumando el
sistema en diciembre de 2024, las cuentas de orden más grandes dan 715053 con
380.280.689.808, 711057 con 114.589.647.383 y 711084 con 73.348.756.213, en la
unidad en que viene el archivo. Ninguna se acerca a los $5,9 billones de saldo de
puts que el BCRA reporta a esa fecha. Tres explicaciones posibles: la unidad del
archivo no es la que se está asumiendo, el nocional cubierto no se registra en una
cuenta separada, o los puts están en otra familia. Resolverlo es parte de la media
hora.

---

## G. Lo que acepto de las correcciones a `pecking_order.md`

Dos correcciones de la actualización de `debate_paper` son válidas y las incorporo.

**G.1 La ecuación de la sección 3 está mal escrita, y es un error mío.** Tal como
figura, incluye simultáneamente efectos fijos de acreedor y un término `Riel_b` que
es función de `b`. Son colineales: el efecto fijo absorbe el regresor. Lo que la
tabla preliminar efectivamente computa es la media desmeanada dentro de deudor×mes
por **grupo** de acreedor, que es legítima porque no incluye efectos fijos de
acreedor individual. La especificación correcta usa indicadores de grupo sin efectos
fijos de entidad, o mantiene los efectos fijos de entidad e interactúa el riel con
algo que varíe en el tiempo. La nota queda corregida en ese punto.

**G.2 Tener dos relaciones crediticias no acredita usar dos medios de pago.** Es una
buena observación y debilita el test de multi-homing más de lo que yo reconocí. Lo
que se observa en CENDEU es multi-homing **crediticio**, no multi-homing de rieles.
Para el test de exclusión contra saliencia haría falta o bien tenencia de cuentas de
pago a nivel individual, que no tenemos, o bien la variación de interoperabilidad,
que dentro de la ventana se reduce a la A 8206 de mayo de 2025. Hay que escribirlo
como proxy con sesgo de signo conocido, no como medida directa.

**G.3 Donde discrepo en parte.** Sobre que condicionar a mora discordante no
distingue por sí solo información de cobro: es correcto que no alcanza solo, pero
combinado con **cuándo** aparece la ventaja, en la originación contra en el margen
de asignación, sí es informativo. Es condición necesaria y no suficiente, y así
queda enunciado.

**G.4 Sobre la observación de que CENDEU no observa pagos efectivos.** Es cierta y
es la limitación central de la línea. La respuesta honesta no es negarla sino
acotar el enunciado: no afirmamos observar a quién le paga el hogar, afirmamos
observar **el orden en que se deteriora la situación de cada acreedor dentro del
mismo deudor y mes**, que es un objeto distinto y más débil, pero es el que la
literatura de pecking order de defaults también usa.

---

## H. Orden de trabajo actualizado

Reemplaza a la sección 8 en lo que se superpone.

1. **Nomenclador de cuentas de orden.** Bajar el Manual de Contabilidad del BCRA,
   identificar la familia de derivados y resolver la unidad del archivo. Decide si
   la Ruta C existe como panel.
2. **Validar el shock de oferta bancaria** con leave-one-out y testear si predice
   crédito nuevo observado a nivel mercado, como ya estaba anotado. Sigue siendo el
   cuello de botella común a todas las líneas.
3. **Construir la exposición compuesta a la reforma de liquidez de 2025** con los
   cuatro componentes de la sección D, fijada a mayo de 2025.
4. **Completar la tabla de alícuotas**, que hoy cubre sólo categorías FCI y PSP
   según `Regulation/alicuotas_TODO_v1.md`, y representar la integración diaria de
   agosto como régimen y no como alícuota.
5. **Corregir la taxonomía de entidades** antes de cualquier corte fintech: nueve
   compañías financieras con códigos 440xx figuran como `fideicomiso` y Crédito
   Regional CF como `pnfc_otro`.
6. **Descartar firmas como muestra de sustitución** a la luz de los 3.951 casos, y
   usarlas para estimar oferta bancaria con multibanco.
7. Mantener el pedido de "tipo de asistencia" y `TASA.TXT` de PNFC.

---

## I. Fuentes del addendum

- [BCRA, rescisión del saldo pendiente en contratos por opciones de liquidez,
  10-06-2025](https://www.bcra.gob.ar/noticias/el-bcra-y-las-entidades-financieras-acuerdan-la-rescision-del-saldo-pendiente-en-contratos-por-opciones-de-liquidez/)
- [BCRA, medidas monetarias, 09-06-2025](https://www.bcra.gob.ar/noticias/el-bcra-anuncia-medidas-para-el-fortalecimiento-de-las-reservas-internacionales-y-la-consolidacion-del-control-de-los-agregados-monetarios/)
- [Chequeado, qué son los puts](https://chequeado.com/el-explicador/que-son-los-puts-que-el-banco-central-busca-eliminar/)
- [Ámbito, cancelación del stock remanente de puts](https://www.ambito.com/finanzas/el-bcra-elimino-otra-potencial-fuente-emision-cancelo-bancos-el-stock-remanente-puts-6-billones-n6155222)
- [Ámbito, recompra del 78% de los puts en julio de 2024](https://www.ambito.com/bcra-redujo-fuerte-el-stock-puts-les-recompro-los-bancos-el-78-n6034478)
- [Invecq, fin de las LEFI y volatilidad de tasas en pesos](https://www.invecq.com/contenidos/fin-de-las-lefi-volatilidad-en-las-tasas-en-pesos/)
- [Ámbito, salida convulsionada de las LEFI](https://www.ambito.com/finanzas/salida-convulsionada-lefis-donde-van-las-tasas-la-extrema-volatilidad-los-ultimos-dias-n6167859)
- [Infobae, los bancos piden cambios al nuevo esquema de liquidez, 24-07-2025](https://www.infobae.com/economia/2025/07/24/tras-el-pedido-de-los-bancos-el-gobierno-no-evalua-cambios-y-espera-que-se-adapten-al-nuevo-esquema-de-liquidez/)
- [LM Neuquén, el desarme de LEFI y el costo del crédito](https://www.lmneuquen.com/pais/credito-caro-como-el-desarme-lefi-disparo-las-tasas-y-golpea-empresas-y-familias-n1201517)
- [BCRA, Informe Monetario Mensual, agosto de 2025](https://www.bcra.gob.ar/archivos/Pdfs/PublicacionesEstadisticas/informe-monetario-mensual-ago-25.pdf)

---

# Segundo addendum, 21 de septiembre de 2026, noche

Sobre la corrida de `Code/analysis/liquidez_fintech/05_trayectorias_por_entidad.ipynb`,
`resultados_por_entidad.md`, los SQL `entity_month.sql` y `entity_transitions.sql`, y las
trece tablas `05_*` de `Code/output/liquidez_fintech`. Los agregados de abajo los recalculé
sobre `05_cambios_entidad.csv`, `05_transiciones_entidad.csv`, `05_comparacion_persona.csv`
y `05_puente_balances.csv`; no corrí nada nuevo ni modifiqué notebooks. Continúa
`Code/analysis/liquidez_fintech/leer.md`, que es la revisión de la corrida anterior.

## J. Qué queda establecido con la exploración por entidad

La decisión de abandonar la etiqueta fintech como criterio de agregación y trabajar código
por código fue la correcta, y el saldo regular quedó implementado. Con eso, el hecho central
deja de depender de cómo se arme la cohorte:

| Universo de personas, mayo 2025 a junio 2026 | Saldo total | Saldo regular |
|---|---:|---:|
| Agregado, todas las entidades, excluido el código 150 | +14,1% | +0,4% |
| Mediana entre entidades con 1.000 deudores o más | +12,7% | −2,7% |

Saldo regular es total menos situaciones 3 a 5, en pesos de mayo de 2025. De las 251
entidades con al menos mil deudores, 131 tienen saldo regular en caída. El crédito a hogares
está plano en términos regulares mientras el saldo bruto crece 14%. Es una descomposición
contable sobre el universo completo, no un resultado de diseño, y es el hecho con el que
conviene abrir el paper.

## K. Hogares afuera, firmas adentro, dentro del mismo banco

Este es el patrón más fuerte de la corrida y no está en `resultados_por_entidad.md`.
Ponderado por saldo inicial de cada grupo:

| | Personas, total | Personas, regular | Firmas, regular | Mora personas, base a fin |
|---|---:|---:|---:|---|
| Bancos públicos (13) | +22,1% | +13,1% | +8,9% | 3,1% a 10,2% |
| Bancos privados (29) | +9,4% | −5,9% | +18,4% | 5,8% a 19,0% |

Los mismos bancos privados que reducen crédito regular a hogares casi 6% lo aumentan 18% a
firmas. Eso es reasignación dentro de la entidad, no contracción general, y es una historia
de oferta más interesante que la sustitución fintech. Dos confundidores previos a cualquier
interpretación. Uno, el crédito a firmas incluye moneda extranjera reexpresada en pesos, y
deflactar por IPC no la saca: parte del +18,4% puede ser tipo de cambio, y el balance separa
crédito en moneda extranjera. Dos, en hogares está el crédito hipotecario de 2025,
concentrado en públicos y en algunos privados, que es saldo grande, indexado y regular por
construcción: puede generar solo el +13,1% de los públicos. CENDEU no tiene producto, así
que ese control sale del balance de la entidad o no sale.

## L. Duración de cartera: un moderador con mecanismo

La descomposición entrada, salida y relaciones continuas es la mejor pieza del notebook y
dice algo que la nota no lee. En porcentaje del saldo inicial de cada entidad en la muestra,
mayo de 2025 a junio de 2026:

| Entidad | Apariciones | Desapariciones | Continuas | Neto |
|---|---:|---:|---:|---:|
| MercadoLibre | +110,6 | −61,3 | −1,4 | +47,8 |
| Reba | +206,3 | −49,5 | −35,6 | +121,2 |
| Ualá Bank | +50,7 | −44,8 | −20,4 | −14,5 |
| Brubank | +57,1 | −29,1 | −33,6 | −5,5 |
| Credicuotas | +84,8 | −14,8 | −60,1 | +9,8 |
| Galicia | +25,1 | −2,8 | −0,4 | +21,9 |
| Nación | +23,3 | −2,3 | +23,2 | +44,2 |

No es diferencia de tamaño ni de crecimiento, es duración. Los prestamistas digitales
reconstruyen el stock entero cada pocos meses; los tradicionales tienen un stock que
continúa. De ahí dos consecuencias. Primera, el mismo cambio de stock significa cosas
distintas según el prestamista, y las continuas muy negativas de Credicuotas, Naranja Digital
y Reba son amortización de cartera corta, no retiro de crédito: normalizar por duración o
leer los flujos brutos es obligatorio antes de comparar niveles. Segunda, y es la buena
noticia: la duración del libro es un moderador a nivel prestamista, medible con esta misma
tabla y con mecanismo explícito. Un prestamista que rota el stock en tres meses transmite un
shock de fondeo a cantidades casi de inmediato; uno con cartera hipotecaria no puede aunque
quiera. Eso da una predicción diferencial, que es lo que le falta al diseño de exposición.

## M. La brecha dentro del deudor ya es el test de prioridad de repago

El `within_pp` de `entity_month.sql`, situación 3 a 6 de cada relación menos la media de esa
persona en ese mes, es la implementación del orden de repago de `pecking_order.md`. Dos
lecturas que valen. La correlación de rangos entre mayo de 2025 y junio de 2026 es 0,92: el
orden de quién cobra primero es estructural y no coyuntural. Y el patrón es interpretable, no
ruido: abajo, entre −10 y −15 puntos, hay mutuales y cooperativas de crédito y consumo, que
prestan con código de descuento sobre haberes y jubilaciones, es decir cobro en la fuente;
arriba, entre +15 y +23, hay fideicomisos financieros, vehículos de recupero y el Fondo de
Garantías Argentino.

Ahí está la variación que veníamos buscando, y no es una firma: son 54 códigos de mutuales y
cooperativas con más de mil deudores cada uno, con clientela compartida suficiente. La
hipótesis "el acreedor que cobra en la fuente se paga primero, dentro del mismo deudor y el
mismo mes" tiene población. Es mejor fuente de variación que fintech contra banco, donde el
76% del grupo es una plataforma.

Tres correcciones antes de usarla.

1. **El demeaning no es leave-one-out.** `peer_mean` incluye la propia relación, así que la
   brecha medida es (k−1)/k veces la diferencia contra el resto, con k variable por
   prestamista. Los prestamistas cuyos clientes tienen pocas relaciones quedan atenuados
   distinto, y eso ordena el gráfico mecánicamente. La corrección es (k·media − bad_i)/(k−1).
2. **Está medida sobre stock de situación, y eso la contamina por selección del prestamista.**
   Un fideicomiso de recupero da +15,7 porque su negocio es comprar cartera ya deteriorada, y
   FOGAR aparece justamente cuando el crédito falló. Sobre stock, el ranking mezcla prioridad
   de cobro con composición de cartera. La versión defendible es sobre flujos: transición de 1
   o 2 hacia 3 a 6, condicional a que las dos relaciones del mismo deudor estuvieran en 1 o 2
   el mes anterior. `entity_transitions.sql` ya calcula las transiciones; falta cruzarlas con
   el demeaning. Es el paso pendiente que más valor agrega.
3. **Pondera por relación y no por monto.** Para "quién cobra primero" la versión relevante es
   ponderada por saldo. Conviene reportar las dos y que la diferencia entre ambas sea un
   resultado, no una nota al pie.

## N. Cronología del deterioro y qué implica para el episodio

Tasa mensual de deterioro, relaciones que pasan de situación 1 o 2 a 3 a 6 sobre las expuestas
el mes anterior, muestra del 5%: 0,8 a 0,9% a fines de 2024; 1,40% en abril de 2025; 1,91% en
mayo; 1,80% en julio; 2,16% en noviembre; 2,42% en enero de 2026. La recuperación, de 3 a 6
hacia 1 o 2, baja de 1,25% a cerca de 1,0%.

El salto de nivel arranca en mayo de 2025, antes del anuncio del 9 de junio, y después sube
gradual. No hay discontinuidad en julio. Eso descarta el event study limpio sobre el cierre de
LEFI y refuerza la lectura de servicio de deuda y fin de boom. El episodio sigue sirviendo
como contexto y como fuente de exposición transversal, no como fecha de corte.

## O. Fondeo: hay dispersión, falta diseño

El puente con balances es débil y el notebook lo dice. Con 54 bancos, la correlación de rangos
entre crecimiento real de depósitos y crecimiento del crédito a personas es 0,35, y títulos
sobre activo correlaciona 0,33 con ese crecimiento. No es evidencia de nada, pero la dispersión
previa existe: títulos sobre activo va de 14,1% en el percentil 10 a 49,3% en el 90, y efectivo
sobre activo de 3,0% a 19,0%. El canal no está muerto por falta de variación. Sigue faltando lo
de siempre, que la exposición prediga algo fuera de la muestra donde se construyó.

## P. Dos problemas de medición que afectan cualquier tabla

Julio de 2026 no está solo sin IPC, está incompleto: 334 acreedores contra 421 el mes anterior,
y la salida tras mora salta a 11,95% ese mes contra 3 a 4% en todos los demás. Hay que excluirlo
de las transiciones, no solo de las series reales.

El peso muestral por entidad no es 5% uniforme: Reba pasa de 4,04% a 5,09% entre mayo de 2025 y
junio de 2026. Para entidades chicas o de crecimiento rápido, la muestra determinística del 5%
es ruidosa a nivel entidad. Los niveles van con el universo y las transiciones con la muestra,
como ya se hizo, pero conviene reportar el peso muestral al lado de cada resultado de
transiciones.

## Q. Lo que acepto de esta corrida

`legal` no sirve: 25 observaciones con código 1 en toda la muestra y 374 en el agregado
completo. La auditoría es correcta y la conclusión es la que corresponde. Y agregar situación 6
a 3 a 5 no mueve nada, la diferencia es exactamente cero en la muestra de personas. Las dos las
había puesto en `leer.md` sin verificar soporte. Queda anotado para no volver a pedirlas.

## R. Orden de trabajo, versión de esta noche

1. Brecha dentro del deudor sobre flujos, con leave-one-out, ponderada por monto, y con el
   corte por cobro en la fuente, mutuales y cooperativas con código de descuento contra el
   resto, en lugar del corte por etiqueta fintech.
2. Contraste hogares contra firmas dentro del mismo banco, después de netear moneda extranjera
   con el balance y de separar hipotecario. Si la reasignación sobrevive a esos dos controles,
   ahí hay paper.
3. Duración de cartera por prestamista, construida con la descomposición de flujos, y su uso
   como moderador de la respuesta a exposición de fondeo.
4. Excluir julio de 2026, corregir el demeaning y reportar peso muestral por entidad.
5. Recién después, exposición de liquidez previa y su capacidad predictiva. Si no predice
   crédito fuera de su muestra de construcción, LEFI queda como contexto institucional y el
   paper es sobre reasignación y repago.

## S. Diseño de la reasignación hogares contra firmas

La sección K reporta el hecho; esto es cómo convertirlo en diseño. La ventaja es que las
dos mitades se validan entre sí y ninguna depende de una clasificación de prestamistas.

**Paso 1, el shock.** Con firmas multibanco, estimar a la Khwaja y Mian

`g_fbt = alpha_ft + gamma_bt + error_fbt`

donde `g` es el cambio del crédito de la firma `f` con el banco `b`, y `alpha_ft` absorbe
toda la demanda de la firma. Los `gamma_bt` son el componente de oferta de cada banco,
medido solo con variación dentro de firma. Hay que estimarlo excluyendo al receptor cuando
se lo use del otro lado, verificar conectividad de la red y reportar cuántas firmas tienen
efectivamente dos o más bancos en cada mes.

**Paso 2, la predicción discriminante.** Llevar ese `gamma_bt`, estimado enteramente del
lado de firmas, al lado de hogares, y preguntar si predice el crédito regular a personas del
mismo banco. Los dos resultados posibles son informativos y se distinguen por el signo:

- Si el banco con `gamma_bt` alto en firmas tiene además crecimiento del crédito regular a
  hogares, es un shock de oferta común: el banco presta más o menos a todos.
- Si el signo se invierte, es reasignación de cartera: el banco no contrajo crédito, cambió
  a quién se lo da. Eso es lo que sugiere el dato agregado, crédito regular a hogares −5,9%
  y a firmas +18,4% en bancos privados, contra +13,1% y +8,9% en públicos.

La segunda respuesta es la más interesante y también la más exigente, porque obliga a
explicar por qué el banco reordena entre segmentos. Los candidatos son capital regulatorio
por ponderador de riesgo, el deterioro observado de la cartera de consumo, y el retorno
relativo de prestarle a firmas con la estructura de tasas de 2025. Se distinguen mirando si
la reasignación aparece antes o después del salto de mora del segmento hogares.

**Controles previos, no opcionales.** Netear crédito en moneda extranjera con el balance,
porque CENDEU informa pesos y la revaluación cambiaria infla el lado de firmas sin que haya
crédito nuevo. Y separar hipotecario, porque una hipoteca nueva es saldo grande, indexado y
regular por construcción, y puede generar sola el resultado de los bancos públicos. Si el
patrón no sobrevive a esos dos controles, no hay nada que reportar.

**Inferencia.** El regresor es un efecto estimado en la primera etapa, con unos treinta
bancos efectivos. Errores agrupados por banco, wild cluster bootstrap, y reportar el MDE
si el resultado del lado de hogares es nulo.

## T. Corrección: la geografía del deudor sí está, y hay más campos de los que veníamos usando

Me equivoqué al decir que el proyecto no tiene geografía a nivel deudor. `padron.parquet`,
65.386.335 registros con llave `cuit`, trae `province` (código ARCA, con
`provincias_arca_indec.csv` como puente), `zip`, `birth_date`, `sex`, `activity` de seis
posiciones de ARCA, y `death_date`. Eso habilita lo que habíamos dado por perdido:

- El moderador de disponibilidad de alternativas locales, sucursales y puntos de acceso por
  provincia o localidad, que es la variación que pedía el otro agente y que yo había dado
  por inexistente.
- Separar monotributistas y autónomos del resto de las personas con `activity`.
- Edad y sexo como controles y como cortes de heterogeneidad.

Tres advertencias. El padrón es un corte al 31 de julio de 2026, no un historial: la
provincia es la actual y no la del momento del crédito, así que para una ventana de dos años
sirve, pero hay que decirlo. `zip` no es departamento INDEC y `province` no es código INDEC,
las dos requieren puente. Y `dropped` y `cuit_replacement` obligan a fechar bajas y
reemplazos de CUIT antes de unir.

Además, `deudores.parquet` tiene campos que el panel de 24 meses no conserva y que resuelven
en parte la limitación de producto que veníamos arrastrando: `pref_guar_a_ars`,
`pref_guar_b_ars` y `no_pref_guar_ars` distinguen deuda con garantía preferida de deuda sin
garantía, y `unused_ars` es asistencia no utilizada, que separa una línea revolvente de un
préstamo a plazo. Es un corte, no una serie, pero alcanza para el test de excluir relaciones
garantizadas en el orden de repago, que era la prueba que yo había pedido y dado por
imposible. También están `days_past_due`, `refinanced`, `legal_status` y `forced_reclass`,
todos con catálogo pendiente de cotejo contra los LEAME del BCRA.

Prioridad: cotejar el catálogo de `pref_guar` y `unused_ars` contra el LEAME, y unir padrón
al panel con las reglas de agregación del compromiso de la Ley 25.326, piso de 500 personas
para cualquier corte geográfico.
