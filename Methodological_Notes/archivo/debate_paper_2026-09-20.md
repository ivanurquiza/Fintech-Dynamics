# Continuidad de la búsqueda de paper

Actualizado: 20 de septiembre de 2026. Registro de la conversación con el usuario;
son hipótesis y diseños candidatos, no resultados ni una identificación validada.

Continuación: [contexto argentino de tasas y episodios candidatos](tasas_argentina_2026-09-20.md).
La revisión favorece explorar julio–agosto 2025 como restricción de liquidez
e incidencia regulatoria diferencial, sin llamarlo shock puro de tasa.

## Preferencias y estado de la búsqueda

Última corrección del usuario: no presuponer un event study. Considerar un panel
de sensibilidades a tasas como en Koont y evaluar identificación por separado.
El episodio de julio–agosto es contexto/candidato, no decisión de diseño.
Se mantienen como dos líneas principales tasas–crédito–sustitución y red física–
continuidad del acceso; no afirmar que cierres observados son exógenos.

Verificación directa de esquemas parquet al retomar: `firm` tiene 24 particiones
y campos `ent, cuit, ym, year, month, status, amount_ars, legal, active, npl`.
El padrón contiene actividad, provincia y código postal, entre otros campos
administrativos/demográficos; hay que unirlo y validar vigencia/cobertura.
El panel de firmas no es un panel de balances empresariales: no se verificaron
ventas, empleo ni inversión. Personas jurídicas por prefijo CUIT tampoco
equivalen automáticamente a PyMEs; saldo pequeño no prueba tamaño de empresa.
El atractivo es observar relaciones simultáneas, saldos, situación y sustitución.
Primera comprobación pendiente: cuántas firmas tienen crédito fintech, y cuánto
solapamiento existe con bancos. No elegir firmas como muestra definitiva sin eso.

El usuario quiere un paper sobre fintech, acceso al crédito o competencia con
bancos tradicionales. Le interesan especialmente tasas de interés y crédito,
y la red de sucursales. Leyó Gilje, Exporting Liquidity, y está leyendo Koont,
Santos y Zingales, Destabilizing Digital “Bank Walks” (versión local mayo 2023).
Pide explicaciones breves, intuitivas y discusión conjunta.

**No cerrar la búsqueda prematuramente.** Las dos líneas siguientes son
disparadores; se permite pivotar. No insistir en que todo paper necesita el
canal depósitos–fondos. No hay todavía buena data histórica de fondos de
inversión en el proyecto. La geografía de la transmisión bancaria interesa
menos por ahora, aunque puede complementar las otras preguntas.

## 1. Tasas y respuesta diferencial del crédito

Pregunta abierta: ¿cómo responde el crédito de bancos y prestamistas fintech
a movimientos de tasas, y qué prestatarios consiguen sustituir acreedores?

Mecanismos candidatos, con signo por determinar:

- Fondeo con depósitos, deuda mayorista o capital propio puede generar
  distinta sensibilidad de costos y restricciones de financiamiento.
- Una baja de tasas podría abaratar más el fondeo de una fintech endeudada
  a tasas de mercado que el de un banco con depósitos baratos. También
  podría beneficiar más al banco si relaja una restricción bancaria relevante.
- Plazos, renovación de préstamos, regulación y composición de productos
  pueden explicar diferencias sin que sean un efecto de la tecnología.

El usuario corrigió acertadamente un encuadre demasiado estrecho: demostrar
salidas de depósitos NO es requisito para investigar tasas y crédito. Sí sería
necesario aportar evidencia de depósitos/costos si se atribuye el resultado
específicamente a ese mecanismo. Una baja de tasas seguida por más crédito
no distingue oferta de mayor demanda de los clientes.

Diseño candidato: comparar acreedores del mismo deudor y período, con efectos
fijos deudor×tiempo y controles adecuados de la relación. La interacción
fintech×cambio de tasa mide una respuesta diferencial bajo supuestos; no
identifica automáticamente un efecto causal ni su mecanismo. Buscar una
exposición de fondeo previa y una fuente defendible de variación monetaria.
Los movimientos de tasas argentinos pueden responder a otros shocks macro.
La demanda específica de cada producto/acreedor sigue siendo una amenaza.

Después mirar deuda total y sustitución por deudor. Allí ya no se conserva la
comparación dentro deudor×tiempo y se debe justificar otra vez la identificación.
Tener una relación fintech previa podría facilitar sustitución, pero esa
relación no es aleatoria: tratar inicialmente como heterogeneidad, no tratamiento.

### Restricción institucional que no se debe olvidar

PSP y prestamista fintech no son sinónimos. Los saldos de cuentas de pago de
clientes no son fondos que el PSP pueda usar libremente para prestar. Separar
servicio de pagos, actividad crediticia y entidad legal que otorga el crédito.
También separar fintech con licencia de entidad financiera de prestamistas no
bancarios. No afirmar que todas las fintech tienen el mismo fondeo.

Ver `Regulation/README.md` y `Regulation/comunicaciones_encajes_psp_fci.md`.
Son antecedentes: las etiquetas de esas notas como “shock limpio”, sus
afirmaciones de exogeneidad y las alícuotas requieren evaluación para cada
episodio. Una norma fechada no basta para identificar. Algunas notas antiguas
se contradicen en fechas y disponibilidad de datos; no copiarlas como hechos
verificados. La habilitación de fondos comunes de dinero ya aparece en 2020,
no nace en 2022 según la revisión normativa posterior del proyecto.

## 2. Koont: qué leímos y cómo podría inspirar el diseño

Fuente local: `Literature/bankwalks(knoot).pdf`, sección 3.2.3, ecuación (3),
páginas impresas 10–12 (PDF 13–15). Se releyeron introducción, datos y sección 3.

El mecanismo es que digitalizar facilita mover saldos hacia alternativas de
mayor rendimiento. Cuando suben tasas, los depósitos de bancos digitales son
más sensibles y esos bancos deben ajustar más su remuneración. El paper
estudia fondeo y valor de la franquicia de depósitos; llevarlo al crédito es
una extensión candidata, cuya originalidad todavía no está establecida.

La regresión territorial interactúa cambio de tasa nacional, internet del
condado y condición digital/broker del banco. Incluye efectos fijos banco×año
y condado×año. Pregunta si la diferencia digital–tradicional en respuesta a
tasas es mayor en condados con más internet. No basta comparar condados
conectados y desconectados: los dos conjuntos de efectos fijos exigen también
variación entre tipos de bancos. Una mera interacción tasa×internet queda
absorbida por condado×año.

El numerador de la ecuación (3) es el cambio de depósitos banco–condado; el
denominador escrito es depósitos totales del banco del año anterior. No
describirlo sin aclaración como crecimiento porcentual del depósito local.

En la regresión bank-level, un efecto fijo de banco absorbe diferencias
permanentes del outcome, pero no sensibilidades diferentes a las tasas por
características omitidas. Una dummy digital constante queda absorbida; su
interacción con tasas cambiantes no. El usuario planteó explícitamente esta
objeción de selección. La comparación territorial ayuda pero tampoco elimina
toda posible heterogeneidad omitida.

**Internet:** proporción de hogares con suscripción a internet por condado,
ACS del Census de EE.UU., estimaciones de cinco años de 2019. No es una
medición de intensidad de uso ni una serie anual de adopción en esa regresión.

**Analogía argentina candidata:** tenencia de cuentas de pago por provincia,
medida antes del episodio. Es adopción de cuentas, no uso, saldo ni tenencia
de inversiones remuneradas. Podría ponderarse con distribución previa de
depósitos de cada banco para construir exposición bancaria. Esa exposición
es una elección/composición previa, no un instrumento automáticamente exógeno.
Un cambio de tasas×adopción provincial sería absorbido por provincia×tiempo;
no prometer la especificación territorial de Koont sin otra dimensión bancaria.

Cadena a explorar, no presumir: alternativas digitales → sensibilidad del
fondeo a tasas → ajuste de crédito → sustitución entre acreedores. No asumir
que una salida hacia billeteras elimina depósitos del sistema: puede cambiar
su composición, costo o banco receptor. No necesitamos reconstruir toda esta
cadena para explorar primero el crédito.

## 3. Sucursales y continuidad del acceso

Pregunta: si desaparece atención bancaria presencial, ¿los clientes pasan a
otro banco, a fintech o pierden crédito? ¿Quiénes quedan afuera según tamaño
de deuda e historial previo? Reemplazar montos no equivale a sostener acceso
para los mismos clientes.

Por “episodio” nos referimos a un evento que genere cierres por un motivo
distinto del deterioro de demanda local: por ejemplo, consolidación de oficinas
duplicadas tras una fusión. Es una estrategia inspirada en Nguyen (2019),
Are Credit Markets Still Local? Evidence from Bank Branch Closings.
No se ha identificado ni validado una fusión argentina concreta para esto.
La fusión puede tener otros efectos sobre el crédito: habría que distinguirlos
del cierre y verificar tendencias, selección y cobertura temporal.

Tenemos puntos de acceso por entidad y localidad, y código postal del padrón
asociado a CENDEU. Eso NO significa que ya exista una unión geográfica fina
validada, coordenadas de cada oficina o distancia cliente–sucursal. El domicilio
fiscal puede no reflejar ubicación económica actual. Falta correspondencia
código postal–geografía y comprobar resolución suficiente para el diseño.

Posible cruce con la primera línea: ¿la presencia física estabiliza el fondeo
frente a alternativas digitales y protege crédito durante cambios de tasas?
Es otra hipótesis abierta, no un resultado.

## Datos disponibles y límites que condicionan ambas líneas

Consultar `Data/README_data.md` y `estado_revision_2026-09-13.md` antes de estimar.
Coberturas según la revisión local guardada, no una nueva auditoría de archivos:

- Balances banco×mes: enero 2018–abril 2026; composición de depósitos y cuentas
  de resultados. Tasas implícitas requieren construir flujos desde acumulados
  y denominadores coherentes; no son tasas contractuales de préstamos.
- `prestamos_depositos_prov.dta`: SÍ existe crédito y depósitos por banco×provincia,
  con montos solo en cierres trimestrales; presencia física mensual.
- Inclusión provincial: crédito hasta diciembre 2025; cuentas bancarias/de pago
  trimestrales desde 2019. Grupos de tenencia incluyen solo bancaria, solo pago
  y ambas. No confundir cuentas de pago con prestamistas fintech.
- Puntos de acceso: 2019–2025, con archivos por localidad, departamento y
  entidad. El nombre de entidad necesita correspondencia con `ent`.
- CENDEU 24 meses: agosto 2024–julio 2026. Stock nominal por deudor–acreedor–mes;
  no originaciones, tasas, plazos ni tipo de producto. Cambios de saldo mezclan
  desembolsos, pagos y otros ajustes; no asumir que cada aumento es préstamo nuevo.
  La ventana es corta para cambios de política y eventos con pre/post suficientes.
- El código postal está en el padrón asociado, no en los tres campos mensuales
  del panel. Hay unión provincial documentada, no unión fina validada.
- La cuenta `311724` NO identifica exclusivamente depósitos de FCI. No usarla
  como exposición fintech comprobada. No hay panel histórico fondo×banco
  construido y validado en la revisión guardada.
- El diccionario `Data/docs/diccionario_cendeu.md` fue cuestionado por el usuario:
  distinguir campos fuente de derivados/rezagos. No son 158 atributos originales
  independientes. En el panel histórico hay tres campos por bloque mensual,
  además de identificadores; el corte detallado tiene otros campos.

## Qué explorar a continuación

### Integración candidata: tasas, dependencia bancaria local y sustitución digital

Hipótesis de trabajo, no diseño elegido: fintech puede reducir la dependencia
del crédito de un deudor respecto de la salud de su banco y de la red bancaria
local. Dos fricciones: fondeo del prestamista y costo de establecer/reemplazar
una relación crediticia. Un cambio de tasas afecta de forma diferente al
fondeo de bancos; donde hay pocas alternativas bancarias, la contracción puede
afectar más al deudor. Una relación fintech previa podría facilitar reemplazo
sin sucursal, siempre que fintech tenga capacidad de fondeo. El signo neto no
se presupone. Sucursales de OTROS bancos son la medida candidata de alternativas;
la presencia del banco incumbente mide algo distinto (relación/fondeo).

Predicción informativa: ante una contracción bancaria comparable, menor caída
de deuda total y aumento absoluto de deuda fintech para clientes con relación
fintech previa, especialmente donde faltan otros bancos. Si solo sube la
participación fintech, no alcanza. Si no aumenta deuda total puede haber
compensación parcial. Si fintech también contrae, examinar dependencia de fondeo
común. Estos patrones no prueban solos efectos causales de adopción fintech.

Usar un panel de sensibilidad y respuestas rezagadas es compatible con la idea;
no requiere cierres ni un evento único. Identificar shocks monetarios y exposición
previa sigue pendiente. Efectos deudor×mes ayudan en relaciones, pero deuda total
requiere otro diseño. Geografía y relación fintech previa tienen selección.

Versión geográfica opcional: exposición de fondeo del banco construida con
depósitos previos en OTRAS provincias; comparar crédito al mismo deudor o en
el mismo mercado receptor. Puede reducir contaminación por demanda local,
pero shocks correlacionados, vínculos comerciales y adopción endógena impiden
llamarlo instrumento válido sin más evidencia. No extrapolar la exogeneidad
del shale de Gilje a adopción de billeteras. Solo 24 provincias y pocos ciclos.

Corrección pedagógica: Bank Walks 3.2.3 usa variación banco–condado e interacciones,
no un IV de sucursales. Exporting Liquidity sí usa red histórica para construir
exposición instrumental a booms de depósitos; el origen externo del boom importa.

Datos adicionales de mayor valor: geografía postal/oficinas validada; fuente
y vencimientos de fondeo de los principales prestamistas fintech; tasas y
expectativas comparables; producto/plazo crediticio si se obtiene acceso.
Tenencia provincial de cuentas de pago no prueba acceso individual a crédito.
No utilizar todos los archivos solo porque existen. La pregunta ya tiene
antecedentes de transmisión monetaria fintech (Franco); la contribución candidata
es continuidad de financiamiento para el mismo deudor y dependencia territorial,
no afirmar que descubrir respuestas diferenciales fintech es novedoso.

### Nueva tercera candidata: prioridad de repago

Se leyó completa `pecking_order.md`, escrita por otro agente. Su hipótesis:
controlar cobros/pagos podría dar al prestamista prioridad efectiva frente a
otros acreedores. Sus cifras se consideran resultados preliminares reportados
por esa nota, no replicados en esta revisión. No adoptar sus afirmaciones de
originalidad o reglas normativas como verificadas.

Evaluación: pregunta potencialmente distintiva y directamente ligada a situación
crediticia entre acreedores de la misma persona, pero CENDEU no observa pagos
efectivos ni productos. Mora diferencial no prueba elección de a quién pagar,
cobro automático ni control efectivo del flujo de ese cliente.

Dos correcciones de identificación al leer la nota: `Riel_b` constante queda
absorbido por efectos fijos de acreedor en su ecuación de sección 3; requiere
otra especificación/variación para estimar un coeficiente. Efectos deudor×mes
no vuelven exógena la entrada de un acreedor ni eliminan shocks específicos de
relación/producto. Condicionar a mora discordante tampoco distingue por sí solo
información de cobro. Tener dos acreedores no acredita usar dos medios de pago.

Sobre sustitución: transmisión es la respuesta de oferta del acreedor a tasas;
sustitución es la respuesta del deudor entre fuentes. Puede sustituir montos
manteniendo ambos acreedores. Las bajas tasas de cambio completo de grupo
reportadas en la nota no descartan sustitución en el margen de montos.
Acceso y bienestar: sostener deuda total puede ser un resultado positivo de
continuidad, pero CENDEU no observa precio ni bienestar; no buscar un signo
positivo por diseño. Persisten como preguntas abiertas las tres líneas.

1. Seguir ayudando a leer Koont con ejemplos simples; no confundir ese trabajo
   con un experimento aleatorio de digitalización.
2. Mapear entidades crediticias y fondeo observable antes de decidir la
   comparación fintech–banco. Evaluar si hay deudores con ambos tipos de acreedor.
3. Encontrar episodios de tasas con suficiente ventana común y examinar otras
   reformas simultáneas; contrastar mecanismo antes de fijar el signo esperado.
4. Para sucursales, buscar eventos y validar geografía antes de proponer una
   regresión causal sobre cualquier cierre.
5. Revisar originalidad frente a literatura de transmisión monetaria fintech;
   ya se encontró “The fintech lending channel of monetary policy” alojado
   en el ECB (2024), pero no se ha leído a fondo en esta conversación:
   https://www.ecb.europa.eu/press/conferences/shared/pdf/20241007_monpolconf/Franco_paper.pdf

No se ejecutaron nuevas estimaciones durante este debate. No hay aún un paper
elegido, un shock validado ni un resultado causal. Mantener abiertas alternativas.

### Continuación: revisión de identificación y datos

Ver [diseno_identificacion_2026-09-20.md](diseno_identificacion_2026-09-20.md).
Incluye una auditoría nueva y reproducible de cobertura y superposición de
acreedores (sin estimar efectos), corrección sobre qué identifica el código
actual de shocks, y tres rutas: red de crédito, encajes predichos y retiro de
opciones de liquidez del BCRA. Los balances no cubren las PNFC fintech; sí hay
algunas entidades digitales reguladas. Se verificaron ejemplos de información
sobre puts en estados públicos, pero no se validó un instrumento.

### Investigación LEFI y estructura de paper. 21 de septiembre

Ver [paper_liquidez_fintech_2026-09-21.md](paper_liquidez_fintech_2026-09-21.md).
Relee `idea_lefi.md`, contrasta la mecánica con A 8060 y los informes del BCRA,
incorpora Cucic–Gorea (RFS 2026) al benchmark y propone distinguir acceso digital
de independencia de fondeo. Una vía por comprobar es identificar a los PNFC como
deudores en CENDEU para reconstruir vínculos banco→PNFC→cliente. Otra variación
candidata es la caja programada por vencimientos de carteras preanuncio. No se
construyeron esos cruces ni se estimaron efectos nuevos en esta investigación.
