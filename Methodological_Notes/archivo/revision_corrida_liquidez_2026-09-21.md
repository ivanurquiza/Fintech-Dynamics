# Leer antes de seguir

21 de septiembre de 2026. Revisión de la primera corrida de `01_datos_y_muestra.ipynb` y
`03_credito_y_sustitucion.ipynb`, hecha desde los CSV de `Code/output/liquidez_fintech`,
los cuatro SQL, `common.py`, el `README` y `Data/docs/nota_lefi_leliq.md`. Las series se
recalcularon sobre `cohortes_mensuales.csv`; no se corrió nada nuevo ni se tocó ningún
notebook. Complementa `Methodological_Notes/review_debate_paper.md` y
`Methodological_Notes/pecking_order.md`.

## Lo primero

La auditoría está bien hecha y la decisión de no correr una regresión de tratamiento antes
de verificar la exposición fue la correcta. El problema no es de ejecución. Es que el objeto
descriptivo elegido no es interpretable, y el hecho más grande de la corrida está calculado
en `cohort_month.sql` y no se graficó ni se mencionó: la mora.

## La mora invierte el resultado principal

`npl_amount` (situaciones 3 a 5) existe en la salida y nunca se usa. Entre mayo de 2025 y
junio de 2026, dentro de la cohorte fija:

| Cohorte | Mora / saldo, may-25 | Mora / saldo, jun-26 | Saldo total | Saldo regular |
|---|---|---|---|---|
| Con fintech PNFC previa | 9,92% | 34,53% | +1,3% | −26,4% |
| Sin fintech PNFC previa | 3,79% | 10,95% | +12,7% | +4,3% |

El saldo regular es total menos mora, en pesos de mayo de 2025, sobre su propia base. En la
cohorte con fintech previa cae 23,7 puntos del saldo total inicial mientras el saldo total
figura subiendo 1,3%. En la otra cohorte, el crédito regular crece 4,3% y no 12,7%.

La razón es contable y conviene escribirla en el paper, no en una nota al pie. El saldo es
originación menos amortización más intereses devengados y punitorios, y la deuda que deja de
pagarse permanece en el saldo hasta la baja contable, que en el régimen local llega bastante
después de la mora. Con un tercio de la cartera en situación 3 a 5, la frase "el componente
bancario aporta +2,14 puntos" no describe crédito nuevo. Ninguna lectura de sustitución
sobrevive sin netear mora primero.

Dos advertencias sobre la medida. La cartera irregular del BCRA son las situaciones 3 a 6, y
el filtro actual excluye la 6, así que es un piso. En cartera de consumo la situación 2 ya
son 31 a 90 días de atraso, de modo que conviene reportar las dos definiciones. Y una cohorte
fija no incorpora deudores nuevos, así que su ratio de mora sube más rápido que el ratio de
sistema: la comparación con el agregado del Informe sobre Bancos no es directa.

## La caída del componente fintech admite una lectura más simple

Los −1,63 puntos que el `README` destaca pueden ser baja contable más rápida y no sustitución
inversa. Si las PNFC castigan antes que los bancos, el saldo fintech cae en la misma cohorte
donde la mora explota, sin que el deudor haya hecho nada. Es separable con la situación del
mes anterior al cero.

## Tres problemas de la cohorte

**Condicionar en un estado en t=0 y después graficar el pre-período.** El notebook advierte
que las pre-tendencias no prueban tendencias paralelas, y la figura las muestra igual. En el
dato: la proporción con fintech de la cohorte "sin fintech previa" es 3,0% en agosto de 2024,
2,2% en abril de 2025 y 0% en mayo por construcción. La V de los cuatro componentes es
artefacto de condicionar en el medio de una ventana inflacionaria, no un hecho. Propongo
sacar el pre-período de la figura principal, o pasar directamente a un panel de relación con
efectos fijos de deudor y de mes, que es de todos modos lo que hay que estimar.

**La matriz conjunta no es comparable entre cohortes, ni descriptivamente.** "Banco cae y
fintech sube" es 13,8% contra 8,0% con umbral de 1%, pero en la cohorte con fintech previa eso
es margen intensivo desde una base positiva y en la otra es margen extensivo desde cero. Son
dos objetos distintos. Y el 52,2% de la cohorte sin fintech que cae en "banco cae, fintech
estable" es casi enteramente el cero: los bins confunden ausencia de relación con estabilidad
del saldo. Conviene reportar la celda condicionando a fintech estrictamente positivo en los
dos meses, y por separado el margen extensivo como una tasa de entrada.

**El corte por estado fintech del deudor es selección por riesgo, no tratamiento.** La mora en
mayo de 2025 es 9,92% contra 3,79%, antes de que pase nada. Cualquier divergencia posterior es
persistencia de riesgo más ciclo. El corte tiene que ser por exposición del acreedor, con el
deudor como efecto fijo. Si el tratamiento varía a nivel de deudor, la base no está comprando
nada que no compre una encuesta.

## Fintech es una entidad, y hay un límite de medición sin resolver

Siete entidades y MercadoLibre es 71,6% del grupo en mayo de 2025 y 75,9% en junio de 2026.
La advertencia del notebook es correcta y alcanza para descartar cualquier shift-share sobre
fintech: los millones de relaciones no son millones de shocks independientes.

Falta un paso más. MELI se fondea securitizando, y cuando securitiza el saldo se muda al código
del fideicomiso financiero, que `lender_taxonomy()` manda a "Otros prestamistas". Eso mueve
mecánicamente el componente fintech contra el de otros prestamistas y puede explicar parte de
los −1,63. Hay que cerrarlo antes de leer esa serie como comportamiento.

De paso, las once entidades que la propia revisión marca como `fideicomiso` son en realidad
compañías financieras cautivas de automotrices (Volkswagen, FCA, GPAT, Mercedes-Benz, Rombo,
John Deere, PSA, Toyota) más Compañía Financiera Argentina y Crédito Regional. La etiqueta del
crosswalk no es fiable, así que "Otros prestamistas", el 13,8% del saldo de personas, hoy mezcla
captive finance, fideicomisos financieros y cooperativas en una bolsa sin abrir.

## Lo que queda en pie del canal LEFI

`nota_lefi_leliq.md` es el mejor trabajo de las últimas corridas. La cobertura de 20% a 60%
moviéndose en contra del stock oficial, la verificación de que las especies suman exacto al
subtotal `121000`, y la hipótesis de custodia con los money market como tenedores, son un
diagnóstico bien fundado. Matar `lefi` como intensidad de tratamiento es la decisión correcta.

Dos cosas para agregar.

Primera, hay una desincronización: `lefi`, `leliq` y `liq_publica` no están en
`Data/processed/balances_bancos.dta`. La última celda de `01` las muestra las tres en `False`.
La nota documenta variables que la base que leen los notebooks no tiene. Por eso el notebook 02
no puede arrancar.

Segunda, y más importante para la narrativa: `liq_publica` sobre activo cae de 48,1% en mayo de
2024 a 33,5% en diciembre de 2024, y después queda plana, 32,9% en junio de 2025 y 33,1% en
abril de 2026. La rotación desde instrumentos del Central hacia crédito es anterior al cierre de
LEFI, y después del cierre no hay rotación adicional en el agregado. Sumado a que en el universo
de personas el crédito bancario se aplana pero no cae (índice 62,2 en agosto de 2024, 100 en
mayo de 2025, 112,4 en junio de 2026), el episodio de 2025 no se ve como un shock de cantidades.

Se ve en el repago. Eso reordena la prioridad: el shock de tasas es un shock de servicio de
deuda, CENDEU es una base de repago y no de originación, y la variación grande de la ventana
está en la mora. El puente con los datos que hay es el producto. Los préstamos personales son en
general de tasa fija a la originación y la financiación de saldos de tarjeta repricea todos los
meses. CENDEU no identifica producto, pero el balance del acreedor separa personales de tarjetas,
así que la participación previa de tarjeta da una exposición a nivel prestamista al canal de
repricing. Interactuada dentro del deudor, con efectos fijos de deudor y mes, eso es un diseño
con mecanismo explícito y no una correlación agregada.

## Qué cambiar, en orden

1. **Netear mora.** Un `FILTER` más en `cohort_month.sql` para abrir `npl_amount` por tipo de
   acreedor, y rehacer las figuras de componentes sobre saldo regular. Reportar mora con 3 a 5
   y con 2 a 6. Es el cambio más chico y el que más cambia la lectura.
2. **Usar los ceros en lugar de descartarlos.** `cendeu_reshape.py` conserva cada relación desde
   su primer mes con actividad, con los ceros posteriores, y deja `active` para distinguirlos de
   la ausencia. Los cuatro SQL filtran `amount_ars > 0` y tiran justamente esa información. Con
   la situación del mes anterior al cero se separa cancelación (situación 1 o 2) de baja o cesión
   (situación 3 a 5). Esa distinción decide si los −1,63 son sustitución o castigo.
3. **Usar `legal`.** Está en el panel desde el reshape y no aparece en ningún notebook. Es acción
   judicial observada, es decir enforcement, que es exactamente el objeto de `pecking_order.md`.
4. **Cerrar el límite MELI/fideicomiso y abrir "Otros prestamistas"** antes de interpretar
   cualquier serie por tipo de acreedor.
5. **Reemplazar el corte por estado fintech del deudor por un corte por exposición del acreedor,**
   con efectos fijos de deudor y mes. El tratamiento tiene que variar a nivel prestamista.
6. **Sincronizar el `.dta` con la nota de liquidez** y reportar la dispersión de `liq_publica`
   sobre activo entre bancos en mayo de 2025. Con el agregado plano, la dispersión de corte
   transversal es lo único que queda del canal.

## Qué no hace falta cambiar

La auditoría mensual, el chequeo de hash, el control de peso de la muestra (4,98% a 5,02% del
universo de personas en saldo y en filas, todos los meses), las dos formas independientes de
calcular el saldo inicial de la cohorte, la sensibilidad a umbrales y el chequeo de concentración.
Eso es lo que un referee pide en el apéndice y casi nadie hace primero. El estilo de los gráficos
y de los notebooks también está bien para paper.

## Cifras de referencia de la corrida

Superposición en mayo de 2025, muestra del 5%: 970.955 personas con saldo, 711.225 con banco,
168.005 con dos o más bancos, 148.506 con banco y fintech, 47.245 con dos o más bancos y fintech.
Multibanco es solo 23,6% de quienes tienen banco, muy lejos del 90% de las firmas multibanco de
Khwaja y Mian, así que el soporte del diseño dentro del deudor hay que reportarlo como fracción
de la muestra y no solo como N.

Composición del saldo de personas en mayo de 2025: bancos tradicionales 81,2%, otros prestamistas
13,8%, fintech PNFC 3,1%, financieras digitales 1,4%, bancos digitales 0,5%.

Universo, índice real con mayo de 2025 igual a 100: bancos 62,2 en agosto de 2024 y 112,4 en junio
de 2026; fintech PNFC 41,6 y 139,9; otros prestamistas 60,4 y 111,4. Los nueve meses previos a
mayo son un boom de crédito, y conviene decirlo cuando se reporta el 12,4% y el 39,9%: la ventana
posterior es desaceleración, no contracción.

El panel de personas tiene `ent`, `cuit`, `ym`, `year`, `month`, `status`, `amount_ars`, `legal`,
`active` y `npl`. No tiene geografía, producto ni moneda. Cualquier diseño que necesite esas tres
cosas las tiene que traer de afuera, y eso condiciona el orden de trabajo.

---

## Continuación: revisión de la corrida por entidad

La revisión del notebook `05_trayectorias_por_entidad.ipynb` y de
`resultados_por_entidad.md` está en el segundo addendum de
`Methodological_Notes/review_debate_paper.md`, secciones J a R. Resumen de lo que
está ahí, para no duplicar:

- El hecho de saldo bruto contra saldo regular queda establecido sobre el universo:
  +14,1% y +0,4% en personas, con 131 de 251 entidades en caída del saldo regular.
- Patrón no leído en la nota: los bancos privados bajan crédito regular a hogares
  5,9% y suben 18,4% a firmas, con moneda extranjera e hipotecario como los dos
  confundidores a netear antes de interpretar.
- La descomposición de flujos mide duración de cartera, que sirve como moderador con
  mecanismo; las continuas negativas de los prestamistas cortos son amortización.
- `within_pp` ya es el test de prioridad de repago, con orden estable (correlación de
  rangos 0,92). Tres correcciones: leave-one-out, flujos en lugar de stock de
  situación, y ponderación por monto. Las mutuales con código de descuento dan la
  variación de cobro en la fuente con población, no con una firma.
- El deterioro salta en mayo de 2025, antes del anuncio del 9 de junio, y sube
  gradual: no hay discontinuidad en julio.
- Julio de 2026 está incompleto, 334 acreedores contra 421, y hay que excluirlo de
  las transiciones.
- Quedan aceptadas las dos correcciones de la corrida: `legal` no tiene soporte y la
  situación 6 no mueve nada. No volver a pedirlas.
