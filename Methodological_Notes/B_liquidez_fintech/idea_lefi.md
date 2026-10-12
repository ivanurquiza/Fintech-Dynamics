# Idea LEFI

21 de septiembre de 2026. Nota de idea. Explica el episodio de julio y agosto de
2025, por qué generó la volatilidad de tasas que generó, y cómo podría usarse
como shock de oferta bancaria en el proyecto. Es una propuesta de diseño, no una
identificación validada ni un resultado. Las magnitudes citadas provienen de las
fuentes listadas al final; lo que es interpretación propia está marcado como tal.
Notas hermanas: `tasas_argentina_2026-09-20.md`, `diseno_identificacion_2026-09-20.md`,
`review_debate_paper.md`, `pecking_order.md`.

---

## 1. Qué era la LEFI

Letra Fiscal de Liquidez. Formalmente, una letra del Tesoro que sólo podían
tener las entidades financieras. Económicamente no era una inversión: era la
cañería con la que el sistema bancario administraba su caja diaria.

El BCRA la compraba y la vendía **a la par, todos los días, contra pesos**. Un
banco con excedente al cierre compraba LEFI; uno con faltante vendía LEFI y se
hacía de efectivo. Siempre al mismo precio.

De ahí tres propiedades, y las tres importan para el diseño:

1. **Pagaba la tasa de política**, con lo cual fijaba el piso de todas las tasas
   en pesos.
2. **Era convertible a efectivo a la par y a demanda**, sin riesgo de precio, con
   lo cual funcionaba como colchón de liquidez perfecto.
3. **Estaba disponible para todos los bancos en los mismos términos.**

En el vocabulario de bancos centrales eso es una **facilidad permanente
remunerada y simétrica** (standing facility). Interpretación propia, pero es la
lectura estándar de un instrumento con esas tres propiedades.

Origen: mediados de 2024, como parte del traspaso de los pasivos remunerados del
balance del BCRA al del Tesoro. **Verificar la fecha exacta de creación y la
comunicación que la instituye.** Era, desde el diseño, una pieza de transición.

---

## 2. Cronología y magnitudes

| Fecha | Hecho | Magnitud |
|---|---|---|
| 09-06-2025 | El BCRA anuncia el fin de la oferta de LEFI a partir del 10 de julio, dentro de un paquete de medidas monetarias | |
| 10-06-2025 | Rescisión del saldo remanente de puts | $5,9 billones; compensación $0,023 billones |
| 10-07-2025 | Fin efectivo de la oferta de LEFI | Stock en poder de bancos ~$15,5 billones |
| 10-07-2025 | Redirección a cuentas corrientes en el BCRA, que no se remuneran | +$9,8 billones en un día, de $9,4 a $19,2 billones |
| 10 al 15-07-2025 | Derrumbe de tasas cortas | caución 23% a 16%; call privado 34% a 18%; LECAP corta 33% a 30% |
| 16-07-2025 | Licitación extraordinaria del Tesoro | absorbe $4,7 billones a 47,8% y 47,1% TIREA contra 41,5% a 44,7% en la licitación previa |
| julio 2025 | Absorción del BCRA vía pases pasivos y ventas en secundario | ~$5 billones, pases al 35% |
| 18-08-2025 | Comienza la integración diaria de efectivo mínimo | |
| 19-08-2025 | Incremento transitorio de cinco puntos; A 8302 publicada en Boletín Oficial | |

Promedios mensuales de tasas, TNA en por ciento, según el Informe Monetario
Mensual de agosto de 2025:

| Serie | Junio 2025 | Julio 2025 | Agosto 2025 |
|---|---:|---:|---:|
| TAMAR bancos privados | 33,62 | 34,32 | 53,41 |
| Call interbancario a un día | 32,75 | 42,81 | 69,29 |
| Adelantos en cuenta corriente | 45,89 | 51,54 | 72,05 |

Nota de calendario, relevante para fijar exposición: **el anuncio es del 9 de
junio, no del 10 de julio**. Cualquier variable de exposición tiene que medirse
en mayo de 2025 o antes.

---

## 3. Por qué hubo tanta volatilidad, y en qué tasas

Tres canales, en orden de inmediatez. La descripción de los hechos es de las
fuentes; la articulación del mecanismo es interpretación propia apoyada en la
literatura de implementación monetaria.

**3.1 Se perdió el colchón.** El stock de LEFI se convirtió en saldos en cuenta
corriente en el BCRA, que no pagan interés. El sistema pasó de tener $15,5
billones remunerados y líquidos a tener una masa equivalente de efectivo ocioso.
El activo líquido dejó de rendir.

**3.2 Se perdió el piso, y con él la ancla de la tasa overnight.** Este es el
canal central. Una facilidad permanente simétrica **fija** la tasa de un día:
ningún banco presta por debajo de lo que le paga el central, ni toma prestado por
encima de lo que le cuesta. Es la lógica de los sistemas de corredor y de piso
(Whitesell 2006; Bech y Klee 2011, **verificar citas**).

Cuando se retira la facilidad, la tasa overnight deja de ser administrada y pasa
a determinarse por el desbalance diario entre bancos con sobrante y bancos con
faltante. Y la demanda de reservas a un día es muy inelástica en el corto plazo:
si al banco le falta, le falta hoy. Con liquidez concentrada en pocas entidades,
desbalances pequeños producen movimientos de precio grandes. Eso explica por qué
los que estallaron fueron el **call interbancario**, que es el préstamo overnight
sin garantía entre bancos, y la **caución bursátil**, que es el repo con garantía
en la bolsa.

Antecedentes empíricos del mismo fenómeno, aunque originados en estrés y no en un
cambio de régimen: Afonso, Kovner y Schoar (2011) sobre el mercado de fed funds en
la crisis, y Acharya y Merrouche (2013) sobre acaparamiento precautorio de
liquidez y su efecto sobre las tasas interbancarias.

**3.3 Transmisión hacia arriba en la curva.** De las tasas de un día a las LECAP,
de ahí a TAMAR, que es el plazo fijo mayorista, y finalmente a las tasas activas.
Dentro del activo, la que más se movió fue **adelantos en cuenta corriente**,
45,9% a 72,1% en dos meses, porque es el instrumento más corto y repacta de forma
prácticamente continua.

**Una frase para el paper:** se convirtió una tasa administrada en una tasa de
mercado sin haber construido antes el mercado que la determinara.

---

## 4. Los dos shocks que hay que separar

Adentro del episodio hay dos objetos distintos. Confundirlos invalida el diseño.

**(a) Shock de nivel.** Las tasas se duplicaron entre junio y agosto. No está
identificado como shock monetario: es endógeno al cambio de régimen, responde a
inflación esperada y a la política cambiaria, y además le pegó a todo el sistema
al mismo tiempo, así que no genera variación transversal. Queda absorbido por
cualquier efecto fijo de tiempo.

**(b) Shock de gestión de liquidez.** El sistema perdió el instrumento con el que
administraba la caja diaria, y el costo de quedarse corto de pesos de un día para
otro pasó a ser alto e incierto. Este sí tiene **incidencia diferencial**: no le
pega igual al banco que dependía de la facilidad que al banco con depósitos
granulares y estables que rara vez la usaba, o al que tenía títulos vendibles en
el secundario.

Ahí vive la identificación. Y la distinción también decide en qué literatura se
para el paper, que es el punto siguiente.

---

## 5. Dónde se para el paper, y por qué esto importa

Si el paper se plantea como **transmisión monetaria**, compite con una literatura
grande y reciente, incluyendo Franco (2024) sobre el canal de crédito fintech,
alojado en el sitio del BCE. Además necesita aislar innovaciones de política, que
en la Argentina de 2025 no se puede hacer de forma creíble.

Si se plantea como **gestión de liquidez y oferta de crédito**, entra en una
literatura menos poblada y conceptualmente más ajustada al episodio:

- **Bianchi y Bigio (2022), Econometrica.** Es el modelo del episodio. El banco
  elige cuánto prestar enfrentando incertidumbre sobre el costo de cubrir un
  déficit de reservas al cierre. Retirar la LEFI es exactamente subir ese costo y
  su varianza. Si hay un marco teórico para citar como referencia del mecanismo,
  es este.
- **Kashyap y Stein (2000), AER.** El canal de préstamo bancario opera a través de
  la capacidad del banco de gestionar su liquidez, y la sensibilidad es mayor en
  bancos menos líquidos.
- **Cornett, McNutt, Strahan y Tehranian (2011), JFE.** Los bancos con mayor
  exposición a riesgo de liquidez redujeron más el crédito durante la crisis. Es
  el antecedente empírico más directo de la forma reducida que proponemos.
- **Ivashina y Scharfstein (2010), JFE.** Crédito bancario durante un shock de
  fondeo.
- Literatura de encajes en emergentes como instrumento que afecta cantidades y no
  sólo precios: Camors, Peydró y Rodríguez-Tous sobre Uruguay con datos a nivel
  préstamo, y Glocker y Towbin sobre efectividad de los encajes (**verificar
  citas y estado de publicación**). Relevante porque el paquete de agosto de 2025
  incluye encajes, y porque marca por qué no se puede usar el encaje como
  instrumento de una tasa.
- **Khwaja y Mian (2008), AER**, para el método: comparación dentro del deudor.
- **Gutierrez, Jaume y Tobal (2023), AEJ: Economic Policy**, para la construcción
  del shock a nivel banco y su agregación a mercados locales.

---

## 6. La narrativa

Durante diez semanas de 2025 la Argentina corrió, sin proponérselo, un
experimento sobre qué le pasa al crédito bancario cuando el banco central retira
el instrumento con el que los bancos administran su liquidez.

La pregunta del paper no es qué le hace una suba de tasas al crédito, que está
contestada muchas veces. Es: **cuando administrar liquidez se vuelve caro e
incierto, qué bancos cortan crédito, a qué deudores, y quién ocupa el lugar.**

El tercer acto es el que conecta con el resto del proyecto. Quien ocupa el lugar
es un prestamista que **no se fondea en el mercado overnight bancario**: los no
bancos. Y esos prestamistas son, en buena medida, los que controlan el riel de
cobro del deudor. Es decir que un shock de liquidez bancaria termina reasignando
crédito hacia acreedores que son senior de hecho, que es la hipótesis de
`pecking_order.md`. Ese empalme es el que permite correr las dos líneas del
proyecto como un solo paper en vez de dos.

---

## 7. Identificación

### 7.1 Exposición

Fijada en **mayo de 2025 o antes**, para preceder al anuncio del 9 de junio.

Medida principal candidata: tenencia de LEFI sobre activos. Medida más general y
probablemente más robusta: **fracción de los activos líquidos del banco que estaba
colocada en la facilidad del BCRA**, en lugar de en títulos negociables o en
exceso de reservas.

Advertencia que hay que escribir en el paper y no esconder: los encajes de agosto
son simultáneos y su incidencia correlaciona con la composición del pasivo, que a
su vez correlaciona con la tenencia de LEFI. La exposición es **compuesta**
quiérase o no. El nombre honesto del tratamiento es exposición al cambio de
régimen de liquidez de 2025, no efecto de la LEFI. Ver la sección D del addendum
de `review_debate_paper.md`, donde se propone la exposición de cuatro componentes.

### 7.2 Primera etapa, dentro del deudor

$$\Delta \ln L_{ibt} = \alpha_{it} + \nu_{ib} + \beta\,\big(E_{b,\text{pre}} \times \text{Post}_t\big) + \Gamma X_{b,\text{pre}} \times \text{Post}_t + \varepsilon_{ibt}$$

con $i$ deudor, $b$ banco, $t$ mes. El efecto fijo deudor×mes $\alpha_{it}$
absorbe la demanda de crédito del deudor **y también el shock de nivel**, que le
pegó a todos los bancos por igual. Lo que queda identificado es la incidencia
diferencial de la pérdida de la facilidad, bajo el supuesto estándar de Khwaja y
Mian: la demanda del deudor es común entre sus acreedores.

Muestra: deudores con dos o más bancos. Según la auditoría de
`diseno_identificacion_2026-09-20.md`, en mayo de 2025 hay 74.958 personas
jurídicas con dos o más bancos y 168.005 personas con dos o más bancos en la
muestra del 5%. Alcanza.

Pre-tendencias: hay diez meses, de agosto de 2024 a mayo de 2025. Es suficiente
para un event study mensual con ventana simétrica.

Advertencia de medición ya registrada en las notas del proyecto: el panel es de
**stocks**, no de originaciones, y los cambios de saldo mezclan desembolsos,
amortizaciones, capitalización de intereses y refinanciación. Hay que usar
transformaciones que admitan ceros, entradas y salidas, y no llamar crédito nuevo
al cambio de stock.

### 7.3 Segunda etapa, a nivel deudor

Exposición del deudor como promedio ponderado de la exposición de sus bancos
previos, con ponderadores fijados antes del anuncio. Acá ya no se pueden usar
efectos fijos deudor×mes porque absorberían el tratamiento. Se usa efecto fijo de
deudor, mercado×mes y actividad o riesgo previo×mes.

Resultados separados, y en **montos absolutos deflactados**, no en
participaciones: deuda con bancos expuestos, deuda con otros bancos, deuda con no
bancos, y deuda total. Una participación fintech mayor porque cayó el denominador
no es sustitución.

### 7.4 Tercera etapa, la que conecta con el resto del proyecto

Entre los deudores que perdieron crédito bancario: quién lo repone, y qué pasa
después con el desempeño de las relaciones bancarias sobrevivientes. Bajo la
hipótesis de enforcement de `pecking_order.md`, un empujón hacia acreedores con
riel debería deteriorar la situación medida de los acreedores sin riel del mismo
deudor, sin que la capacidad de pago del hogar haya cambiado. Se contrasta con
efectos fijos deudor×mes.

---

## 8. Amenazas, sin maquillar

**8.1 Exposición compuesta.** Ya tratada en 7.1. La solución no es pretender
aislar la LEFI sino nombrar el tratamiento por lo que es.

**8.2 Selección por modelo de negocio.** El banco con mucha LEFI es un banco con
liquidez excedente, que muchas veces es un banco con poca demanda de crédito o con
una clientela distinta. Entonces el grupo tratado puede ser, de entrada, el menos
crediticio. La comparación dentro del deudor ataca exactamente eso, porque compara
dos bancos que le prestan a la misma persona. La pre-tendencia es obligatoria, y
conviene reportar balance de características de balance previas.

**8.3 El signo puede invertirse, y hay que estar dispuesto a aceptarlo.** El banco
que tenía mucha LEFI también es el que quedó con mucha liquidez para reasignar
cuando la LEFI dejó de existir. Es concebible que el más expuesto **aumente** el
crédito. Si eso aparece, es un resultado y no un fracaso, y de hecho sería más
interesante que el signo esperado. Lo que no se puede hacer es fijar el signo por
adelantado.

**8.4 Anticipación.** El anuncio es del 9 de junio y la vigencia del 10 de julio.
Hay un mes de anticipación posible y tres semanas de reacomodamiento observable.
Fijar exposición en mayo y testear si hay movimiento en junio.

**8.5 Pocos bancos.** Del orden de 25 a 30 entidades relevantes. Cluster a nivel
banco con wild bootstrap desde la primera tabla, no como respuesta a un referee.

**8.6 Los no bancos no son un control inmune.** Muchos prestamistas no bancarios
se fondean con bancos. Si el shock también los alcanza, la sustitución observada
subestima el efecto, o directamente no aparece. Es una hipótesis contrastable, no
un supuesto: se puede mirar si el crédito no bancario también cae.

---

## 9. Qué chequear antes de comprometerse

1. **Si la LEFI se puede separar en los balances.** `titulos` agrega públicos y
   privados y no equivale a LEFI, según la revisión guardada. Pero en
   `caracteristicas_bancos` están los indicadores 800010500010, 800010500080 y
   800010500090, y la revisión señala que la descripción del último incorpora
   referencias a LELIQ, pases y LEFI según el período. Si con eso se puede
   construir tenencia de facilidad sobre activos a mayo de 2025, la exposición
   existe. Si no, hay que ir al plan de cuentas y buscar la especie. Es el chequeo
   que decide si la idea arranca.
2. **Unidades y denominador** del indicador que se termine usando, antes de
   interpretar una diferencia entre indicadores como exposición a un activo.
3. **Cobertura temporal.** Los balances construidos llegan a abril de 2026 y
   CENDEU a julio de 2026. Para la primera etapa alcanza; para la tercera hay que
   declarar que los últimos tres meses no tienen balance.
4. **Primera etapa real.** Que la exposición prediga efectivamente el crédito del
   banco, y no sólo su liquidez. Si el banco absorbe el shock con el activo
   líquido y no toca el crédito, el diseño mide algo y ese algo es cero.
5. **Serie diaria de call y caución** para la figura de apertura. La volatilidad
   del episodio es visible en el dato diario y se pierde en promedios mensuales.

---

## 10. Figura de apertura sugerida

Tres paneles, dato diario, de mayo a septiembre de 2025, con líneas verticales en
el 9 de junio, el 10 de julio, el 16 de julio y el 18 de agosto.

Panel A: saldos en cuenta corriente en el BCRA y stock de LEFI. Muestra el salto
de $9,4 a $19,2 billones en un día.
Panel B: call interbancario y caución bursátil. Muestra el derrumbe y la
sobrecorrección.
Panel C: adelantos en cuenta corriente y TAMAR. Muestra la transmisión al activo.

Es la figura que explica el paper sin texto.

---

## 11. Fuentes

Institucionales:

- [BCRA, medidas para el fortalecimiento de reservas y la consolidación del
  control de los agregados monetarios, 09-06-2025](https://www.bcra.gob.ar/noticias/el-bcra-anuncia-medidas-para-el-fortalecimiento-de-las-reservas-internacionales-y-la-consolidacion-del-control-de-los-agregados-monetarios/)
- [BCRA, rescisión del saldo pendiente en contratos por opciones de liquidez,
  10-06-2025](https://www.bcra.gob.ar/noticias/el-bcra-y-las-entidades-financieras-acuerdan-la-rescision-del-saldo-pendiente-en-contratos-por-opciones-de-liquidez/)
- [BCRA, Informe Monetario Mensual, agosto de 2025](https://www.bcra.gob.ar/archivos/Pdfs/PublicacionesEstadisticas/informe-monetario-mensual-ago-25.pdf)
- [BCRA, datos monetarios diarios](https://www.bcra.gob.ar/datos-monetarios-diarios/) y [tasas de interés](https://www.bcra.gob.ar/tasas-de-interes/)

Prensa y análisis del episodio, para magnitudes y secuencia:

- [Invecq, fin de las LEFI y volatilidad de tasas en pesos](https://www.invecq.com/contenidos/fin-de-las-lefi-volatilidad-en-las-tasas-en-pesos/)
- [Ámbito, salida convulsionada de las LEFI](https://www.ambito.com/finanzas/salida-convulsionada-lefis-donde-van-las-tasas-la-extrema-volatilidad-los-ultimos-dias-n6167859)
- [Infobae, los bancos piden cambios al nuevo esquema de liquidez, 24-07-2025](https://www.infobae.com/economia/2025/07/24/tras-el-pedido-de-los-bancos-el-gobierno-no-evalua-cambios-y-espera-que-se-adapten-al-nuevo-esquema-de-liquidez/)
- [LM Neuquén, el desarme de LEFI y el costo del crédito](https://www.lmneuquen.com/pais/credito-caro-como-el-desarme-lefi-disparo-las-tasas-y-golpea-empresas-y-familias-n1201517)

Literatura:

- Bianchi, J. y Bigio, S. (2022). Banks, Liquidity Management, and Monetary
  Policy. *Econometrica*.
- Kashyap, A. y Stein, J. (2000). What Do a Million Observations on Banks Say
  About the Transmission of Monetary Policy? *AER* 90(3), 407-428.
- Cornett, M., McNutt, J., Strahan, P. y Tehranian, H. (2011). Liquidity risk
  management and credit supply in the financial crisis. *JFE* 101(2).
- Ivashina, V. y Scharfstein, D. (2010). Bank lending during the financial crisis
  of 2008. *JFE* 97(3), 319-338.
- Afonso, G., Kovner, A. y Schoar, A. (2011). Stressed, Not Frozen: The Federal
  Funds Market in the Financial Crisis. *JF* 66(4).
- Acharya, V. y Merrouche, O. (2013). Precautionary Hoarding of Liquidity and
  Interbank Markets. *Review of Finance* 17(1).
- Khwaja, A. y Mian, A. (2008). Tracing the Impact of Bank Liquidity Shocks. *AER*
  98(4), 1413-1442.
- Gutierrez, E., Jaume, D. y Tobal, M. (2023). Do Credit Supply Shocks Affect
  Employment in Middle-Income Countries? *AEJ: Economic Policy* 15(4), 1-36.
- Camors, C., Peydró, J.L. y Rodriguez-Tous, F. Macroprudential and Monetary
  Policy: Loan-Level Evidence from Reserve Requirements. **Verificar estado de
  publicación.**
- Glocker, C. y Towbin, P. Reserve requirements as a macroprudential instrument.
  **Verificar cita.**
- Whitesell, W. (2006). Interest rate corridors and reserves. *JME*. **Verificar
  cita.**
- Bech, M. y Klee, E. (2011). The mechanics of a graceful exit. *JME*. **Verificar
  cita.**
- Franco, L. (2024). The fintech lending channel of monetary policy. Alojado en el
  sitio del BCE.
