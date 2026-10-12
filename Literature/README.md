# Literatura: guía de lectura para Fintech-Dynamics

Revisión del corpus local: 13 de septiembre de 2026. Secciones 17 a 19 agregadas el 12 de octubre de 2026.

Esta nota resume los 19 PDF guardados en esta carpeta. Se revisaron planteos,
métodos, resultados y limitaciones de los textos principales; no se replicaron
estimaciones ni se verificaron todas las demostraciones y apéndices. Las referencias
corresponden a las versiones locales, que pueden diferir de versiones posteriores.
Las observaciones bajo **Aplicación y límites** son nuestra lectura para el proyecto,
no resultados adicionales de los autores. Los localizadores de páginas se refieren
al contador del PDF cuando se indica «PDF».

## Mapa del corpus

| Pregunta | Lecturas principales | Objeto que ayudan a separar |
|---|---|---|
| ¿Un shock de fondeo cambia la oferta bancaria? | Khwaja–Mian; Gutierrez–Jaume–Tobal; Bernini et al. | Oferta del banco frente a demanda de sus clientes |
| ¿Otros prestamistas reemplazan al banco? | Tang; Gopal–Schnabl; Erel–Liebersohn | Sustitución, expansión y composición de prestatarios |
| ¿Por qué importa la red física? | Gilje–Loutskina–Strahan; Gilje; Petersen–Rajan | Movilidad del fondeo frente a producción local de información |
| ¿Digitalizar pagos altera los depósitos? | Balan–Klötzle–Norden; Koont–Santos–Zingales; Benmelech–Yang–Zator | Nivel, movilidad, costo y estabilidad del fondeo |
| ¿Pagos e información afectan el crédito? | Parlour–Rajan–Zhu | Información transaccional frente al canal de fondeo |
| ¿Cómo estudiar interoperabilidad? | Casiano; Anchorena | Uso de pagos, inclusión y resultados bancarios |
| ¿Cuándo es válido un instrumento de exposición? | Borusyak–Hull–Jaravel | Exogeneidad de shocks o participaciones e inferencia |
| ¿Importa el shock de crédito para la actividad? | Greenstone–Mas–Nguyen | Caída de crédito frente a efecto real |
| ¿Cómo transmiten la política monetaria la liquidez bancaria y los no bancos? | Bianchi–Bigio; Franco | Riesgo de liquidez del banco y canal no bancario |

## 1. Khwaja y Mian (2008)

**Tracing the Impact of Bank Liquidity Shocks: Evidence from an Emerging Market.**
AER 98(4), 1413–1442. [PDF](khwaja2008.pdf).

**Pregunta y diseño.** Usa el shock de liquidez posterior a las pruebas nucleares
de Pakistán de 1998 y la exposición diferencial de los bancos a depósitos en moneda
extranjera. Compara cambios de crédito entre bancos que prestan a la misma firma.
Los efectos fijos de firma en una regresión en diferencias absorben el componente
común de su cambio de demanda. El experimento económico y la comparación dentro
de la firma se complementan; el efecto fijo no reemplaza al experimento.

**Resultado.** Los bancos transmiten pérdidas de liquidez a sus prestatarios. La
contracción de una relación bancaria no equivale a la contracción del crédito total:
las firmas grandes pueden compensarla mejor que las pequeñas.

**Aplicación y límites.** Es la distinción central para estudiar reemplazo por no
bancos. Primero se estima el efecto sobre cada relación; después, sobre crédito
total y desempeño del deudor. Al agregar a deudor se pierde la comparación entre
acreedores dentro del mismo deudor y período: hay que justificar nuevamente la
exogeneidad. La demanda específica de una relación y la selección de quienes
tienen varios bancos siguen siendo amenazas. Ver sección II, especialmente B–C
(PDF 9–11), y análisis de resultados a nivel firma.

## 2. Gutierrez, Jaume y Tobal (2023)

**Do Credit Supply Shocks Affect Employment in Middle-Income Countries?**
AEJ: Economic Policy 15(4), 1–36. [PDF](Credit_Supply_Shocks%28Martin%29.pdf).

**Datos y diseño.** Originaciones bancarias a firmas mexicanas, 2010–2015, unidas a
empleo formal por mercado laboral. Por año descompone el crecimiento del crédito
banco–mercado en efectos fijos de mercado y banco. Pondera los componentes bancarios
por participaciones del año anterior para construir exposición local. El 74% de
las firmas tiene relación con un solo banco, lo que motiva este enfoque territorial.

**Resultado.** Un shock positivo de un desvío estándar se asocia causalmente, bajo
sus supuestos, con 1,4 puntos porcentuales adicionales de crecimiento anual del
empleo de empresas pequeñas y medianas. Encuentra mayor participación de crédito
sin garantías y a firmas jóvenes, familiares o sin crédito reciente.

**Aplicación y límites.** Es el antecedente directo del `gamma` banco–trimestre del
proyecto, pero el paper mide **originaciones** y CENDEU **saldos**. El saldo incorpora
uso de líneas, amortización, castigos y transferencias de cartera. Sus pruebas de
balance y correlaciones con indicadores bancarios apoyan el diseño; ninguna
correlación aislada prueba oferta ni su ausencia la refuta. Debemos evaluar demanda
diferencial por banco, concentración de shocks y construcción excluyendo el mercado
receptor. Ver sección III y tablas 2–4, PDF 13–17.

## 3. Bernini, Donaldson, Garcia-Lembergman y Juarez (2024)

**The Financial Channel of Tax Amnesty Policies.** Versión agosto de 2024.
[PDF](taxamnesty.pdf).

**Diseño.** Estudia el blanqueo argentino de 2016. Mide exposición bancaria con los
depósitos en cuentas especiales del blanqueo, promedio octubre–diciembre de 2016,
divididos por depósitos privados previos. Combina diferencias en diferencias y
comparaciones dentro de la firma; la exposición de la firma pondera la de sus
bancos por relaciones iniciales.

**Resultado.** Los bancos más expuestos expanden crédito; sus firmas prestatarias
aumentan endeudamiento y presentan mejoras en comercio exterior y empleo. La
moneda del fondeo es parte del mecanismo, no un detalle de conversión.

**Aplicación y límites.** Es el antecedente institucional argentino más cercano al
canal fondeo–crédito. A diferencia del proxy `311724`, aquí existe una cuenta ligada
al episodio. El numerador de exposición se observa durante el shock: no debemos
describirlo como completamente predeterminado. La participación previa de depósitos
en dólares sirve como contraste. El panel local de CENDEU no alcanza 2016. Ver
sección 4, desde PDF 12, figuras 2–5 y estimaciones banco–firma.

## 4. Tang (2019)

**Peer-to-Peer Lenders Versus Banks: Substitutes or Complements?** RFS 32(5),
1900–1938. [PDF](tang2019.pdf).

**Diseño.** La consolidación contable de activos bajo FAS 166/167 presiona el capital
de bancos afectados. Usa su presencia geográfica previa para comparar mercados
expuestos y no expuestos; fija el período posterior desde 2011Q1. Combina solicitudes
y préstamos de LendingClub con predicciones sobre volumen, calidad y tamaño.

**Resultado.** P2P sustituye crédito bancario para prestatarios que ya eran atendidos
por bancos, pero complementa en el margen de préstamos pequeños. Un aumento del
crédito fintech no demuestra por sí solo acceso de personas previamente excluidas.

**Aplicación y límites.** Orienta la separación entre deudores bancarizados, usuarios
mixtos y nuevos observados. Su medición de calidad previa y solicitudes es más rica
que la nuestra: mora posterior y saldo no reemplazan FICO, solicitudes rechazadas
o montos originados. La validación del shock utiliza también crédito a pequeñas
empresas porque falta el equivalente territorial de consumo bancario; es una
limitación explícita del texto. Ver secciones 1, 3 y 4; PDF 14–17 para identificación.

## 5. Gopal y Schnabl (2020, versión local)

**The Rise of Finance Companies and FinTech Lenders in Small Business Lending.**
Versión septiembre de 2020. [PDF](TheRiseOfFinanceCompaniesInUnited_preview.pdf).

**Datos y diseño.** Registros UCC de 13,7 millones de préstamos empresariales
garantizados, excluyendo inmuebles. Explota dependencia bancaria territorial previa
a 2008; contrasta industrias, tipos de garantía, firmas con ambos tipos de acreedor
y financieras pertenecientes a bancos frente a independientes.

**Resultado.** La expansión no bancaria compensa gran parte de la caída bancaria
durante la recuperación hasta 2016. Los resultados reales no muestran daños
persistentes comparables a la contracción del crédito bancario considerado solo.

**Aplicación y límites.** Es un antecedente directo de nuestra pregunta de reemplazo.
El argumento exige que la dependencia bancaria inicial no capture tendencias de
demanda específicas de préstamos no bancarios. UCC cubre una clase de crédito, no
el universo del financiamiento empresarial; conteos de registros tampoco equivalen
automáticamente a pesos prestados. Parte de la cuantificación de volúmenes utiliza
tamaños de préstamo imputados. No extrapolar una compensación a diez años a una
ventana argentina de 24 meses. Ver secciones III y IV.A–D.

## 6. Erel y Liebersohn (2022)

**Can FinTech Reduce Disparities in Access to Finance? Evidence from the Paycheck
Protection Program.** JFE 146, 90–118.
[PDF](Can-FinTech-reduce-disparities-in-access-to-finance-Evidence-from-the-Paycheck-Protection.pdf).

**Diseño.** Compara provisión de un mismo producto, préstamos PPP, entre bancos y
fintech. Para estudiar sustitución construye una medida de respuesta bancaria
usando originaciones por sucursal **en otros estados** y participaciones de
sucursales en el código postal receptor. Examina balance y pesos de Rotemberg.

**Resultado.** Dentro de condados, fintech atiende más a áreas con menos sucursales,
menores ingresos y mayor presencia de minorías. La sustitución estimada es pequeña:
en este programa predomina la expansión del servicio.

**Aplicación y límites.** Aporta una construcción concreta de exposición excluyendo
el área receptora, y muestra por qué comparaciones nacionales pueden ocultar
gradientes locales. PPP tiene garantías y condiciones particulares; no es evidencia
directa sobre riesgo de préstamos ordinarios de consumo. Tampoco ausencia de
sucursal equivale a ausencia de clientes bancarios. Ver secciones 5–6 y tablas 9–10.

## 7. Gilje, Loutskina y Strahan (2016)

**Exporting Liquidity: Branch Banking and Financial Integration.** Journal of
Finance 71(3). [PDF](gilje2016.pdf).

**Diseño.** Descubrimientos de shale generan ingresos y depósitos locales. Estudia
préstamos hipotecarios de bancos expuestos en condados que no experimentaron el
boom, con efectos fijos condado–año. Usa la red de sucursales de 2002 como
instrumento de exposición para abordar entradas posteriores endógenas.

**Resultado.** El shock eleva depósitos y reduce su costo, consistente con mayor
oferta de fondeo. Los bancos exportan liquidez a mercados donde tienen sucursales,
especialmente en hipotecas que conservan en balance y son menos titulizables.

**Aplicación y límites.** Fundamenta que el lugar donde se capta el depósito puede
ser distinto de aquel donde se presta, y la importancia de mirar cantidad y precio.
En Argentina, ponderar adopción por geografía no hereda la exogeneidad del shale:
la adopción puede responder a actividad y políticas locales. Ver sección III,
ecuaciones 1a–2 y discusión del instrumento; PDF 10–12.

## 8. Gilje (archivo `gilje2019.pdf`)

**Does Local Access to Finance Matter? Evidence from U.S. Oil and Natural Gas
Shale Booms.** La copia local es Articles in Advance, publicada online el 13 de
septiembre de 2017; se conserva el nombre recibido. [PDF](gilje2019.pdf).

**Diseño y resultado.** Usa el aumento de depósitos por shale y heterogeneidad de
la estructura bancaria local. Encuentra efectos reales más fuertes en mercados
dominados por bancos pequeños. Los bancos con mercados internos de capital amplios
dependen menos del fondeo de un solo lugar. Estudia también dependencia de
financiamiento externo de las actividades económicas.

**Aplicación y límites.** Permite distinguir dos fricciones: acceso del banco a
fondeo y acceso de la firma a prestamistas. El resultado no demuestra que reemplazar
bancos pequeños por grandes mejore bienestar: pueden atender a deudores distintos.
Para nuestro diseño, tamaño y extensión de red pueden modificar la transmisión,
además de actuar como controles. Ver secciones 2–3 y 5–6.

## 9. Petersen y Rajan (2002)

**Does Distance Still Matter? The Information Revolution in Small Business
Lending.** Journal of Finance. [PDF](petersen2002.pdf).

**Datos y enfoque.** Encuestas NSSBF, principalmente 1993 y complementos de 1988.
Reconstruye año de inicio de relaciones, distancia al prestamista y forma de
comunicación. Examina composición de firmas, transparencia informativa,
consolidación bancaria y selección de relaciones sobrevivientes.

**Resultado.** Las relaciones más recientes son más distantes e impersonales, y
el crédito a distancia deja de limitarse a firmas de máxima calidad. El patrón es
consistente con mejoras de productividad y uso de información transmisible.

**Aplicación y límites.** Es el marco para preguntar si la tecnología sustituye
información obtenida localmente. Es evidencia histórica, no un experimento de
entrada fintech. En nuestro registro, el domicilio fiscal y la red del acreedor
no indican necesariamente la sucursal donde se evaluó al cliente. Ver secciones
de datos, regresiones de distancia y comunicación, y conclusión.

## 10. Parlour, Rajan y Zhu (2022)

**When FinTech Competes for Payment Flows.** RFS 35(11), 4985–5024.
[PDF](ParlourRajanZhu_FinTechPayment.pdf).

**Modelo.** Un banco monopolista presta y procesa pagos; fintechs competitivas
procesan pagos. Los datos transaccionales informan calidad crediticia. La elección
del procesador modifica información, selección y contratos del banco.

**Resultado.** La competencia puede ampliar acceso a pagos con efectos ambiguos
sobre crédito y bienestar. Venta de datos y portabilidad pueden recuperar
información para prestar, pero distribuyen las rentas de manera distinta.

**Aplicación y límites.** Ofrece un mecanismo rival al fondeo: la migración de
pagos puede modificar crédito por pérdida de información aunque no caigan depósitos.
El modelo excluye que la fintech preste directamente; por eso no debe presentarse
como un modelo completo de competencia crediticia banco–fintech. La conclusión de
bienestar depende de la estructura competitiva supuesta. Ver modelo y discusión
PDF 5–8, y secciones 2–4.

## 11. Koont, Santos y Zingales (2023)

**Destabilizing Digital “Bank Walks”.** Versión mayo de 2023.
[PDF](bankwalks%28knoot%29.pdf).

**Diseño.** Relaciona cambios de tasas con crecimiento y costo de depósitos según
plataforma digital y servicios de brokerage. Añade una comparación banco–condado–año
con efectos fijos banco–año y condado–año, usando diferencias en acceso a internet.

**Resultado.** Bancos digitales, especialmente con brokerage, presentan mayor
sensibilidad del fondeo a tasas. La movilidad también alcanza depósitos asegurados.
Una valoración modelizada implica menor valor de la franquicia de depósitos.

**Aplicación y límites.** Motiva tasas implícitas y sensibilidad al ciclo monetario,
además del nivel de depósitos. La adopción digital y brokerage no son aleatorios;
la especificación territorial es una defensa adicional, no una garantía universal.
Los cálculos de valoración no son estimaciones directas de probabilidad de corrida.
Ver sección 3, ecuaciones 2–3, PDF 11–14, y sección 4 para valoración.

## 12. Benmelech, Yang y Zator (2023)

**Bank Branch Density and Bank Runs.** NBER WP 31462, julio de 2023.
[PDF](BankBranches.pdf).

**Diseño.** Relaciona densidad de sucursales previa con retornos bursátiles y
salidas de depósitos durante episodios de la crisis bancaria estadounidense de
2023, controlando tamaño, seguro de depósitos, pérdidas de valoración y crecimiento
previo. La densidad se mide respecto de depósitos, no de población.

**Resultado.** Bancos con menos sucursales por unidad de depósitos presentan peor
desempeño y mayor salida de depósitos no asegurados. Los autores aclaran que no
afirman que baja densidad por sí misma causó las quiebras.

**Aplicación y límites.** Ayuda a caracterizar modelos de captación y estabilidad.
No confundir sucursales/depósitos con sucursales/habitante o presencia local: el
denominador cambia el concepto y puede introducir relaciones mecánicas con el
resultado. Ver sección de crisis, PDF 14–15, y tablas de flujos.

## 13. Balan, Klötzle y Norden (2026)

**Fast Payment Systems and Deposit Dynamics: Evidence from Brazil’s Pix.**
Versión 13 de marzo de 2026. [PDF](Fast_Payments_Deposit_Dynamics.pdf).

**Diseño.** Panel banco–municipio, 2010–2025, con indicador nacional post-Pix y
medidas de intensidad. Estudia niveles y volatilidad mediante ventanas móviles,
wavelets y filtros; añade el episodio de desconfianza de enero de 2025.

**Resultado.** Reporta mayores depósitos y volatilidad local, pero menor
volatilidad a nivel banco nacional, consistente con diversificación territorial.

**Aplicación y límites.** Es muy útil para definir resultados y niveles de
agregación. Su ecuación principal incluye un post nacional y efectos de banco y
municipio; ese post sería colineal con efectos completos de mes. La obligatoriedad
de participar no vuelve exógena la intensidad elegida por usuarios. Un indicador
de enero de 2025 tampoco elimina por sí solo shocks nacionales concurrentes. La
ventana centrada de 13 meses mezcla observaciones anteriores y posteriores cerca
del evento. Estas son cautelas nuestras al evaluar causalidad, no una refutación
de sus hechos descriptivos. Ver PDF 10–13 y sección 5.

## 14. Casiano (2026)

**The War on Cash: Interoperability, Digital Payments, and Household Financial
Fragility in Peru.** Preliminar, 23 de febrero de 2026.
[PDF](The%20War%20on%20Cash%20Interoperability%20-%20Denys%20Casiano%20%28vEnglish%29.pdf).

**Diseño.** ENAHO 2022–2024 y exposición distrital predeterminada con depósitos de
diciembre de 2022. Construye coexistencia entre bloques de instituciones como
`4s(1-s)` y asigna cohortes según la primera fase a la que el distrito queda
expuesto. Usa Callaway–Sant’Anna, controles aún no tratados y errores por distrito.

**Resultado.** Reporta sustitución de efectivo y tarjetas por canales digitales;
el efecto en apertura/tenencia de cuenta no es significativo. La reducción de
fragilidad es de significancia marginal. El cuestionario cambia en 2024 y limita
la comparabilidad de algunas medidas de uso.

**Aplicación y límites.** Separar acceso, uso y bienestar. Hay que verificar soporte
de cohortes, significado de exposición positiva y efectos de fases posteriores.
La apertura de redes peruanas no equivale automáticamente a los cambios argentinos
en aceptación QR y fondeo. Este documento **no es** el paper de Burga et al. sobre
concentración de depósitos citado en las notas; ese otro PDF no está en el corpus.
Ver sección 5 (PDF 16–19), resultados y advertencias de medición.

## 15. Borusyak, Hull y Jaravel (2025)

**A Practical Guide to Shift-Share Instruments.** JEP 39(1), 181–204.
[PDF](borusyak-et-al-2025-a-practical-guide-to-shift-share-instruments.pdf).

**Marco.** Distingue identificación basada en muchos shocks exógenos de la basada
en participaciones exógenas. Predeterminar una participación no garantiza su
exogeneidad. La ruta de shocks exige una fuente de variación defendible, suficiente
dispersión y una inferencia que reconozca exposición compartida.

**Aplicación y límites.** Contar millones de deudores no crea millones de shocks.
Tampoco 50 bancos por seis trimestres son necesariamente 300 shocks independientes.
Hay que medir concentración y dependencia, decidir qué ruta se defiende, revisar
restricción de exclusión, participaciones incompletas y pruebas de balance. Excluir
el receptor de la construcción evita contaminación mecánica, pero no elimina toda
endogeneidad económica. No hay un umbral universal por el cual 24 provincias
garanticen validez. Ver marcos conceptuales, PDF 6–8, y recomendaciones/tablas.

## 16. Anchorena (2026)

**Interoperabilidad de pagos, competencia de billeteras digitales y crédito
bancario en Argentina.** Trabajo del proyecto, 22 de enero de 2026.
[PDF](Proyecto_Ignacio.pdf).

**Diseño.** DiD banco–mes, corte junio de 2024, terciles alto y bajo de exposición
a depósitos a la vista previa. Usa 42 bancos y 42 meses. Distingue resultado de
crédito y diagnóstico de depósitos; los FCI agregados son evidencia descriptiva.

**Resultado.** Depósitos: coeficiente 0,0133, error estándar 0,2023; crédito:
0,1376 y 0,2227. Ambos positivos y no significativos. Son estimaciones imprecisas,
no evidencia concluyente de efecto nulo ni prueba de compensación vía FCI.

**Aplicación y límites.** Es la base histórica del proyecto y deja claro qué
pregunta ya se intentó. La hipótesis de recomposición de fondeo puede explicar
por qué los niveles agregados son insuficientes, pero necesita evidencia propia.
El shock nacional y la exposición deben distinguirse de reformas y cambios
macroeconómicos concurrentes. Ver PDF 7–10, cuadros 1–2.

## 17. Greenstone, Mas y Nguyen (2020)

**Do Credit Market Shocks Affect the Real Economy? Quasi-experimental Evidence from the Great Recession and "Normal" Economic Times.** AEJ: Economic Policy 12(1), 200–225. [PDF](greenstone2020.pdf).

**Pregunta y diseño.** Mide si los shocks al crédito para pequeñas empresas afectan el empleo. Predice shocks de crédito por condado con un diseño shift-share: participaciones de mercado previas de cada banco en el condado por los desplazamientos de oferta del banco a nivel nacional. Datos de préstamos a pequeñas empresas (CRA) y de establecimientos, 1997–2010.

**Resultados.** Los condados con shocks negativos previstos tienen menos originaciones a pequeñas empresas, lo que indica que cambiar de prestamista es costoso. El efecto sobre el empleo de las pequeñas empresas y sobre el empleo total es económicamente chico y en general no significativo, tanto en la Gran Recesión como en tiempos normales.

**Aplicación y límites.** El nulo real se explica con que las firmas tienen otras fuentes de crédito, pero no lo miden. CENDEU permite observar esas otras fuentes en el mismo deudor. Es además un antecedente directo del shift-share de oferta bancaria y de sus problemas de inferencia (ver Borusyak–Hull–Jaravel).

## 18. Franco (2024)

**The Fintech Lending Channel of Monetary Policy.** Documento de trabajo, versión de septiembre de 2024. [PDF](Franco_paper.pdf).

**Pregunta y diseño.** Compara la transmisión de la política monetaria a hipotecas originadas por prestamistas fintech no bancarios y por el resto. Usa unos 2,5 millones de hipotecas a tasa fija de la FHA entre 2012 y 2019, con 230 bancos y 188 no bancos, de los cuales 9 son fintech, más datos de balance y fondeo de los no bancos obtenidos por pedidos a reguladores estatales.

**Resultados.** Los prestamistas fintech aceleran el traspaso de la tasa de política a la tasa hipotecaria y atenúan el traspaso a los volúmenes.

**Aplicación y límites.** Es un antecedente sobre no bancos y transmisión monetaria, no sobre pagos ni depósitos. Con nueve prestamistas fintech la variación efectiva es chica y los errores estándar no se agrupan por prestamista: no usarlo como evidencia para nuestras preguntas más allá del antecedente.

## 19. Bianchi y Bigio (2022)

**Banks, Liquidity Management, and Monetary Policy.** Econometrica 90(1), 391–454. [PDF](bianchi-bigio2022.pdf) (versión de marzo de 2021).

**Pregunta y diseño.** Modelo de gestión de liquidez bancaria con mercado interbancario OTC. Los depósitos circulan entre bancos y se liquidan con reservas; la política monetaria cambia el costo de quedar corto de reservas y, con eso, el trade-off entre prestar y asumir riesgo de liquidez.

**Resultados.** La implementación de la política (tasas de ventanilla y de remuneración de reservas, fricciones interbancarias) afecta el traspaso a tasas activas. Una descomposición cuantitativa atribuye parte de la caída del crédito en 2008 a shocks de liquidez y a la disfunción del interbancario.

**Aplicación y límites.** Es el marco para la línea de liquidez: los encajes sobre la vista de FCI y la salida de la LEFI son cambios en el costo de la liquidez del banco. Deja un punto que conviene resolver en el papel: el depósito del PSP con encaje 100% queda esterilizado y no circula por el interbancario.

## Implicaciones para la siguiente etapa

1. **Separar las dos preguntas causales.** El efecto en una relación bancaria y
   el reemplazo a nivel deudor son objetos distintos, con supuestos distintos.
   Una regresión dentro del deudor no valida automáticamente la segunda etapa.
2. **Definir qué mide el crédito.** Con CENDEU podemos estudiar stocks, relaciones
   y situación. Originación, precio y límite disponible histórico requieren otros
   datos. Una caída de saldo puede tener varias causas.
3. **Medir reemplazo en unidades comparables.** Un cociente de coeficientes en
   logaritmos es una relación de elasticidades, no pesos sustituidos por peso
   perdido. Esa interpretación necesita niveles o una transformación con bases
   y denominadores explícitos.
4. **Mantener separados los canales de pagos.** Fondeo, información transaccional
   y acceso remoto tienen predicciones diferentes. La presencia de una billetera
   no identifica cuál opera.
5. **Evitar equiparar primera observación con inclusión.** Hay censura izquierda,
   umbrales nominales, rezagos de reporte y transferencias de cartera. La primera
   relación con un nuevo acreedor no necesariamente es entrada al registro.
6. **Tomar los resultados existentes como preliminares.** El shock estimado aún
   necesita validación, inferencia y tratamiento de la participación del propio
   mercado. Las notas de estado del proyecto detallan problemas concretos de código.

Las notas metodológicas citan además a Xiao, Drechsler–Savov–Schnabl,
Chernenko–Sunderam, Ivashina–Scharfstein–Stein y otros.
Esta revisión no afirma haber leído esos trabajos completos: sus PDF no están
en esta carpeta.
