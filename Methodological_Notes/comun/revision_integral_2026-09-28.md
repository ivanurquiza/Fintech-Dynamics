# Revisión integral del repo, 28 de septiembre de 2026

Lectura completa de `Code/analysis` (notebooks, `po.py`, SQL, resultados), de las notas de `Methodological_Notes` posteriores al 13 de septiembre, de la memoria del proyecto y de los 19 PDF de `Literature/`. Agrego un diagnóstico nuevo, corrido sobre la muestra del 5% de CENDEU: `Code/analysis/pecking_order/diag_edad_jubilatoria.py`, con salida en `Code/output/pecking_order/10_edad_jubilatoria.{csv,png,pdf}`. No toqué ningún otro archivo.

## 1. Dónde está parado el proyecto

Hoy conviven tres proyectos que comparten repo y no mucho más.

El primero es el del pasivo bancario: billeteras, FCI money market, partida 311724, encajes. Es el que describe la memoria v9 y `diseno_empirico.md`. Desde el 13 de septiembre no se tocó, salvo el pipeline `FondosCNV` que se escribió hoy y todavía no bajó nada (`Data/raw/FondosCNV/carteras` está vacío).

El segundo es el de liquidez bancaria y sustitución fintech en el crédito: LEFI, puts, encajes de agosto de 2025, shocks banco-mes con CENDEU. Ahí se concentró casi todo el trabajo de la última semana (`liquidez_fintech/01` a `06`, cuatro notas metodológicas).

El tercero es el orden de repago dentro del deudor (`pecking_order/`). Es un solo notebook, corrido el 23 de septiembre, y es lo mejor que tiene el repo.

El problema no es que haya tres líneas, es que las notas de la semana pasada no eligen. Hay más de 100 KB de notas escritas en modo "hipótesis abierta, no diseño elegido, no afirmar", y el `README` lo dice: "no hay todavía un diseño elegido". Ese tono protege contra el sobre-enunciado, pero a esta altura también funciona como excusa para no decidir. Mi recomendación, que desarrollo abajo, es convertir la línea 3 en el paper, dejar la 1 como segundo paper con los datos de CNV, y bajar la 2 a contexto institucional salvo que el shock banco-mes pase una prueba concreta que todavía nadie corrió.

Tres cosas de mantenimiento, antes de lo sustantivo. Existe una copia huérfana en `GitHub/personal/Fintech-Dynamics` que sólo tiene `FondosCNV` y es idéntica a la del repo; hay que borrarla para que ningún script escriba ahí. La memoria del proyecto todavía apunta a `personal/`, y el repo volvió a `GitHub/Fintech-Dynamics` el 24 de septiembre (commit `959e033`). `Literature/README.md` dice 16 PDF y afirma que Greenstone, Mas y Nguyen no está en la carpeta; hay 19 y sí está, y tampoco reseña a Franco ni a Bianchi y Bigio. `build_dta.do.bak` está versionado.

## 2. Orden de repago: qué muestra y qué no

### Lo que está bien

El diseño es un Khwaja-Mian aplicado al repago. Con efecto fijo persona-mes, el shock de ingreso del deudor se reparte igual entre sus acreedores y lo que queda es variación entre acreedores. Los hechos son nítidos: el 96,9% de los primeros eventos de mora son parciales, la selección persiste a seis meses, y el orden por acreedor es grande (MercadoLibre 0,33 contra banca privada, retail 1,73) y estable entre períodos. Los cortes que más valen son los que el mecanismo predice y las lecturas alternativas no: Macro 0,21 en sus cuatro provincias contra 0,62 fuera, el gradiente de los bancos provinciales por tamaño de provincia, y el cambio del orden con la fuente de ingreso del deudor. El estimador propio coincide con `ConditionalLogit` hasta 0,004 en coeficientes. El código es limpio y no deja identificadores en el repo.

### Lo que hay que corregir en la interpretación

**No es una elección del hogar.** `resultados.md` abre con "el hogar elige a quién". Lo que el diseño identifica es un diferencial de hazard entre acreedores del mismo deudor. Si el mecanismo es el débito automático sobre la cuenta sueldo o la billetera, el hogar no elige nada: el acreedor se cobra antes de que la plata esté disponible. Eso es senioridad de hecho por compensación sobre el flujo, no un pecking order de preferencias. La distinción importa para el paper, porque cambia la pregunta de "a quién prefiere pagar el hogar" a "qué le compra a un prestamista controlar el riel de pagos", que es una pregunta de diseño contractual y de competencia, y es la más interesante de las dos.

**La relación bancaria es un paquete y la situación es única por deudor-entidad.** La clasificación de CENDEU es una sola por deudor en cada entidad: si falla cualquier producto, cae toda la relación. Un banco con tarjeta, préstamo personal y descubierto al mismo cliente tiene mecánicamente más chances de ser "la relación que cae" que un prestamista monoproducto como MercadoLibre. El control por tamaño relativo no lo resuelve. Esto sesga contra los bancos en general y a favor de los monolínea, y no afecta por igual a Macro dentro y fuera de sus provincias, así que el corte de Macro sobrevive, pero el ranking de categorías no. Hace falta el campo "tipo de asistencia" (ya está en el pedido) o, mientras tanto, una prueba con deudores que en el corte de julio de 2026 tienen una sola línea por entidad.

**Frecuencia de cuota y refinanciación.** MercadoLibre debita en forma diaria o semanal contra el saldo; un banco cobra la cuota mensual. Con atraso definido en días, el prestamista que cobra más seguido detecta y recupera antes. Y un prestamista que refinancia al deudor en problemas lo mantiene en situación 1: "protección" puede ser tolerancia. El campo `refinanced` está roto para PNFC, pero se puede aproximar con saltos de saldo en el mes del evento.

**La validación con `forced_reclass` no es independiente.** La recategorización obligatoria se dispara exactamente cuando un acreedor clasifica mejor que los demás al mismo deudor, que es el mismo fenómeno que mide el panel, sólo que en stock y sobre toda la población. La correlación de −0,59 es un chequeo de consistencia entre stock y flujo, útil, pero no una "medida independiente". En el paper hay que presentarla así.

**Criterio de reporte de las PNFC.** Verificar en la normativa si los proveedores no financieros aplican las mismas reglas de clasificación y la misma regla de recategorización que las entidades. Que Credicuotas y CFN tengan 0% exacto de recategorización sugiere que no, o que no la aplican.

### Lo que lo convierte en paper: variación en quién controla el ingreso

Hoy la evidencia sobre el mecanismo es transversal: comparar acreedores o grupos de deudores que difieren en muchas cosas. Lo que falta es variación, dentro de la misma persona o de personas comparables, en dónde entra la plata. Corrí la primera versión de una que me parece la mejor disponible con los datos que ya están.

**Edad jubilatoria, mujeres a los 60 y varones a los 65.** Al jubilarse el ingreso pasa a entrar por el banco pagador de ANSES. Si la prioridad sigue al flujo, el banco que paga el haber tendría que ganar prioridad y la billetera perderla, y eso tendría que ocurrir cinco años antes en las mujeres que en los varones. Es una diferencia en discontinuidades con un corrimiento legal por sexo, que limpia la tendencia por edad común a ambos.

El resultado descriptivo (caídas observadas sobre esperadas, misma definición de evento que el notebook 01) es este:

| Edad | Banco público, M | Banco público, V | MercadoLibre, M | MercadoLibre, V |
|---:|---:|---:|---:|---:|
| 58 | 0,98 | 1,05 | 0,40 | 0,49 |
| 59 | 0,97 | 0,99 | 0,42 | 0,41 |
| 60 | 0,95 | 1,07 | 0,44 | 0,48 |
| 61 | 0,83 | 0,98 | 0,58 | 0,43 |
| 62 | 0,79 | 0,90 | 0,57 | 0,42 |
| 64 | 0,71 | 0,79 | 0,62 | 0,52 |
| 65 | 0,74 | 0,77 | 0,60 | 0,56 |
| 66 | 0,75 | 0,75 | 0,61 | 0,72 |

En MercadoLibre el patrón es el que predice el mecanismo: las mujeres saltan de 0,44 a 0,58 entre los 60 y los 61 y los varones se quedan en 0,42 a 0,46 hasta los 63, y saltan entre los 64 y los 66. En banco público las mujeres caen de 0,95 a 0,83 al pasar los 60; en los varones la caída empieza antes de los 65, lo cual no me sorprende (regímenes especiales, jubilación anticipada, empleados públicos), pero hace que el lado bancario sea menos limpio que el de la billetera.

Advertencias, antes de entusiasmarse. Son celdas de 300 a 1.000 relaciones en la muestra del 5%; con el universo (`panel24_wide`) son veinte veces más. No hay controles: al jubilarse aparecen préstamos nuevos del banco pagador, que son relaciones jóvenes con más mora temprana, y eso cambia la composición del conjunto de elección. La versión seria es el logit condicional con antigüedad de la relación, interacciones sexo × edad y ventana de ±5 años, y el banco pagador de ANSES no es necesariamente público (hay que agrupar por "entidad donde la persona abrió relación en los 12 meses siguientes a la edad legal", o conseguir el dato de ANSES). Pero como prueba de que la variación existe y va en la dirección correcta, alcanza.

Otras fuentes de variación a explorar, en orden de lo que creo que rinde: cambios de agente financiero provincial dentro de la ventana (renovaciones o pérdidas de contrato de Macro, Santa Fe, etc.; hay que buscarlas); cambios en la política de débito de MercadoLibre o en la habilitación de pago de salarios en cuentas de pago (verificar la normativa vigente desde el DNU 70/2023, no lo tengo confirmado); y la entrada de la persona a un empleo registrado, que se observa sólo en corte con el padrón.

### El resultado que falta: dilución

Un acreedor senior de hecho le impone una externalidad al resto. La predicción testeable es que cuando una persona toma su primera relación con MercadoLibre, el hazard de sus otras relaciones (en particular retail y financieras de consumo) sube, con efecto fijo persona y comparando con personas del mismo perfil que la toman meses después. Es Bizer y DeMarzo (1992) con senioridad tecnológica en lugar de contractual, y es lo que convierte un hecho de orden en un resultado de equilibrio. También es el nexo con la línea 2: MercadoLibre creció 48% real mientras el crédito regular de la banca privada a hogares caía, y un prestamista que cobra primero puede expandirse hacia una población en deterioro con menos pérdida.

### Dónde se ubica

Los vecinos obvios son Andersson, Chomsisengphet, Glennon y Li (2013, JMCB) sobre orden de impago entre productos, y Coelho, de Mello y Funchal (2012, REStat) sobre descuento de nómina en Brasil. Del lado fintech, Parlour, Rajan y Zhu (RFS 2022), que está en el repo, modela a la fintech que compite por los flujos de pago para quitarle al banco la señal informativa; acá el flujo le da a la fintech algo distinto de la información, le da enforcement. Esa es la parte destacable: el valor del riel de pagos para un prestamista no es sólo saber más, es cobrar primero. Conviene leer y ubicar contra Ghosh, Vallee y Zeng sobre préstamos fintech y pagos sin efectivo, y contra Degryse, Ioannidou y von Schedvin (2016, JF) sobre no exclusividad; verificar las referencias exactas antes de citarlas.

## 3. Liquidez 2025 y sustitución fintech: por qué no es el paper

Las notas de la semana pasada son cuidadosas y, en varios puntos, correctas: la detección de que la celda `shock_cendeu` promedia el valor ajustado completo y no recupera el efecto banco es un error real; la corrección de que la LEFI se liquidaba a valor técnico y con venta limitada al saldo (A 8060) es correcta; que la forma Bartik no da exogeneidad también. Pero la línea tiene tres problemas que no son de robustez.

El primero es que los propios datos ya dicen que no hay evento. La tasa de deterioro pega el salto en mayo de 2025, antes del anuncio del 9 de junio, y después sube en forma gradual; la tasa de primer evento del notebook de repago empieza a subir también antes de junio. Entre el 9 de junio y el 19 de agosto hay cuatro tratamientos superpuestos (fin de LEFI, rescisión de puts, integración diaria, cinco puntos de encaje). La propuesta de fusionarlos en una "exposición compuesta" es honesta pero deja un estimando sin nombre económico.

El segundo es que la exposición no mide lo que se necesita. El stock de LEFI a fin de mes no mide intensidad de uso como colchón, y el agregado de títulos en pesos mezcla la elección contable del renglón (ya documentado en la memoria v9). Los puts remanentes son un residuo auto-seleccionado que empuja en la dirección del resultado esperado.

El tercero es que no hay primera etapa validada. Todo el andamiaje (shock banco-mes, extrapolación de firmas a personas, exposición del deudor) depende de que $\gamma_{bt}$ estimado con firmas multibanco prediga crédito fuera de la muestra de construcción, y esa prueba no se corrió. Con 24 meses de stocks, sin originaciones, y con Gutierrez, Jaume y Tobal advirtiendo que a frecuencias menores a la anual los shocks dejan de predecir, no la daría por descontada.

De esta línea rescataría dos hechos que sí son buenos y no dependen de LEFI. Uno, la reasignación dentro del banco: la banca privada reduce 5,9% el crédito regular a hogares y aumenta 18,4% el de firmas, contra +13,1% y +8,9% en la pública. Antes de leerlo como oferta hay que netear moneda extranjera y separar hipotecario, como dice la nota. Dos, la duración de cartera: MercadoLibre, Reba o Credicuotas reconstruyen el stock en pocos meses, Galicia y Nación no. Eso vuelve incomparables los cambios de stock entre prestamistas y, bien usado, es un moderador con mecanismo para la transmisión. Los dos entran mejor como hechos de contexto del paper de repago que como paper propio.

## 4. El pasivo bancario: lo que hay que corregir de mi propio diseño

El diseño 1 de `diseno_empirico.md` (banco × instrumento × mes con FE banco×mes y alícuota de encaje por instrumento) tiene un problema que en su momento no escribí con suficiente claridad. Con $\alpha_{bt}$ y $\gamma_k$, la alícuota $\text{Encaje}_{k,t}$ se identifica sólo por variación instrumento-tiempo, idéntica para todos los bancos. Es un DiD entre ocho instrumentos con un puñado de cambios normativos: cualquier shock de demanda específico del instrumento en el mismo mes (el rendimiento relativo de los money market, por ejemplo) lo confunde, y el número efectivo de experimentos es el número de cambios de alícuota, no el de bancos. La variación que sirve es la incidencia diferencial entre bancos: $\sum_k s_{bk,0}\,\Delta\text{Encaje}_{kt}$, con composición previa fija, que es la Ruta B de la nota del 20 de septiembre. Y hay que aceptar que eso mide la respuesta a una restricción regulatoria de liquidez, no una elasticidad a la tasa.

El diseño 2 (Khwaja-Mian fondo→banco con FE fondo×semana) sigue siendo la mejor idea de esa línea y ahora es factible con `FondosCNV`. Pero conviene tener clara la inversión: el FE fondo×tiempo absorbe la oferta de fondeo del fondo, de modo que lo que se identifica es la demanda de fondeo del banco, y el regresor tiene que ser un desplazador del lado del banco (encaje, liquidez, exposición a LEFI), no la tasa que paga, que es un resultado de equilibrio. Tres cosas lo rompen y hay que tratarlas desde el principio: la afiliación entre sociedad gerente y banco, los topes de concentración por entidad, y que el fondo persiga tasa.

Y el primer cuadro de esa línea, antes que cualquier regresión, es cuantificar la premisa. El proyecto afirma que el peso de la billetera vuelve al banco. Una parte de la cartera de los money market es caución bursátil, cuyo tomador no es necesariamente un banco. Con las carteras semanales hay que mostrar qué fracción de cada fondo está en cuentas remuneradas y plazos fijos bancarios, qué fracción en caución y qué fracción en títulos, a lo largo del tiempo. Si la caución pesa mucho, la frase "no hay desintermediación" hay que matizarla.

## 5. Qué me llevo de la literatura del repo

Resumo sólo lo que muerde sobre nuestras decisiones.

**Khwaja y Mian (2008)** colapsan pre y post y clusterizan por banco (42 clusters). La lógica OLS contra FE para firmar el sesgo es directamente trasladable al repago: comparar el orden sin FE persona-mes y con él dice cuánto de la protección de MercadoLibre es selección de deudores.

**Gilje, Loutskina y Strahan (2016)** y **Gilje (2019)** piden primero mostrar que el shock mueve cantidad y precio del fondeo, y fijan la red en un período previo como instrumento. Para cualquier cosa del lado del pasivo, esa es la plantilla. Gilje agrega que la respuesta es mayor en bancos sin acceso a fondeo mayorista, lo cual da una heterogeneidad testeable en balances BCRA.

**Greenstone, Mas y Nguyen (2020)** explican su nulo real con "las firmas tienen otras fuentes de crédito" y no lo pueden medir; con CENDEU se puede. **Gutierrez, Jaume y Tobal (2023)** es la plantilla de construcción del shock. Un referee va a mirar que la primera etapa tiene $t\approx 2{,}2$ (0,413 con EE 0,187) mientras la forma reducida sobre empleo tiene $t\approx 2{,}9$; conviene saberlo si reutilizamos el método con Martín. **Bernini et al. (2024)**, el blanqueo, es el antecedente más cercano en datos; tiene una inconsistencia en el número de bancos (28 en el texto, 46 en el apéndice) y clusteriza a nivel banco-firma con tratamiento a nivel banco. No repetir eso.

**Balan, Klötzle y Norden (Pix)** es un before-after nacional sin grupo de control y con volatilidad medida en niveles nominales. Sirve de contraste, no de benchmark. **Casiano (Perú)** construye $E=4s(1-s)$ y después usa sólo $E>0$; los nunca tratados son distritos rurales. De ahí se toma Benjamini-Hochberg, no la exposición. **Koont, Santos y Zingales** da la fórmula de franquicia y el within banco-año entre condados; su resultado del 40% es muy sensible a $c/f$, que en Argentina tiende a cero. **Benmelech, Yang y Zator** da densidad de sucursales como heterogeneidad barata. **Bianchi y Bigio (2022)** es el marco correcto para la línea de liquidez y deja un punto incómodo: el depósito del PSP con encaje 100% queda esterilizado del interbancario.

**Erel y Liebersohn (2022)** ya tiene el titular "la fintech sustituye donde hay poca banca", con un programa de oferta limpio que nosotros no tenemos; en su Bartik un solo banco tiene peso de Rotemberg 2,23. **Gopal y Schnabl** es el antecedente de finance companies, con un test útil de afiliadas contra no afiliadas a bancos (en Argentina, Naranja X y Galicia). **Tang (2019)** muestra que el volumen no discrimina sustitución de complementariedad y la distribución sí; CENDEU permite la versión individual. **Petersen y Rajan (2002)** es la microfundamentación del repago: la información dura y oportuna reemplaza a la cercanía y habilita monitoreo ex post.

**Borusyak, Hull y Jaravel (2025)**: el shift-share geográfico no pasa ninguna de las dos rutas (pocos shocks y shares genéricas); el de fondos, con $K_{\text{eff}}\approx 5$ o 6, sólo puede defenderse por la ruta de shares y hay que presentarlo como un DiD sobre exposición previa a uno o dos fondos. **Proyecto de Ignacio**: el "nulo" no es nulo, es ruido (MDE de ~0,57 log puntos), y la exposición CC+CA mete en el grupo tratado a los bancos que reciben el retorno del float. Es la mejor motivación para cualquier paper del pasivo. **Franco (2024)** trata sobre hipotecas y transmisión monetaria, no sobre pagos ni depósitos; con 9 fintech y errores robustos sin cluster, no hay que citarlo como evidencia de nada nuestro más allá del antecedente.

## 6. Orden de trabajo que propongo

1. Correr el notebook de repago sobre el universo de personas (`panel24_wide`), no sobre la muestra del 5%. Todo lo que hoy es un corte con 300 relaciones pasa a tener 6.000.
2. Diferencia en discontinuidades por edad jubilatoria con logit condicional, antigüedad de relación y ventana de ±5 años, separando al banco donde la persona abre relación después de la edad legal.
3. Test de paquete: repetir el orden con deudores que tienen una sola línea por entidad en el corte de julio de 2026, y reportar la versión ponderada por monto.
4. Dilución: evento de primera relación con MercadoLibre, hazard de las otras relaciones de la misma persona, cohortes escalonadas con estimador robusto a efectos heterogéneos.
5. En paralelo y sin prisa: bajar las carteras de CNV y armar el cuadro de destino del dinero de los money market (banco, caución, títulos).
6. Sólo si queda tiempo: validar fuera de muestra el $\gamma_{bt}$ de firmas multibanco. Si no predice, la línea de liquidez queda como contexto.

Pedidos al BCRA que valen para la línea principal: tipo de asistencia (diseño 4301 y siguientes), tasas de PNFC (`TASA.TXT`), y, si se puede, el banco pagador de haberes de ANSES a nivel persona o al menos por entidad y provincia.
