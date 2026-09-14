# Preguntas de investigacion

Documento interno de trabajo, pensado como base para un pedido de datos.
Plantea las preguntas y la estrategia general de identificacion sin
especificar tipos de dato, granularidad ni formatos, a proposito.

## Contexto

El proyecto estudia la competencia entre los proveedores de servicios de
pago (billeteras digitales) y la banca tradicional en Argentina. El pais
ofrece una secuencia regulatoria inusual, con fechas exactas y direcciones
opuestas, que movio el atractivo relativo de mantener saldos en billeteras:
la interoperabilidad de pagos (Transferencias 3.0, 2020-2021, con refuerzos
en 2024), el tratamiento de los fondos de clientes de los PSP en custodia
(enero 2022) y la serie de cambios sobre la remuneracion de los saldos
canalizados a fondos comunes de dinero (2024-2025). Esa secuencia es la
fuente de variacion exogena que ordena todas las preguntas.

## Pregunta 1. Interoperabilidad e inclusion financiera

La interoperabilidad de pagos, al derrumbar el valor de la exclusividad de
red, sube el valor de tener una billetera. Preguntamos si esto acelero la
adopcion de cuentas y el acceso al credito, y con que heterogeneidad
territorial: donde la banca tradicional tenia poca presencia fisica, la
billetera puede ser la primera puerta de entrada al sistema.

Approach: shock normativo nacional con fecha exacta, combinado con
exposicion territorial predeterminada (adopcion previa, presencia previa de
infraestructura financiera fisica). Estudios de eventos comparando la
evolucion de jurisdicciones mas y menos expuestas alrededor de las fechas,
con las tendencias previas como test de validez.

## Pregunta 2. Competencia por saldos transaccionales y credito bancario

Si las billeteras captan y retienen saldos que antes eran depositos a la
vista, los bancos mas dependientes de ese fondeo deberian mostrar presion
relativa sobre depositos y, via el canal de credito bancario, sobre su
oferta de prestamos.

Approach: heterogeneidad ex ante entre bancos en dos dimensiones que no se
eligen en respuesta al shock: la composicion previa del fondeo y la huella
geografica previa (que determina cuanta adopcion de billeteras le crecio
encima a cada banco). Diseños de diferencias en diferencias y de exposicion
tipo shift-share alrededor de las fechas regulatorias, con efectos fijos de
banco y tiempo.

## Pregunta 3. Efectos no buscados de la regulacion de saldos

La regulacion de 2022 volvio ultra seguros los fondos en custodia pero
elimino el incentivo de los PSP a mantenerlos, empujando el ahorro
transaccional hacia vehiculos de mercado de dinero; la regulacion de
2024-2025 fue removiendo el tratamiento preferencial de esa segunda via.
Preguntamos si esta cascada reasigno el ahorro transaccional entre
instrumentos e intermediarios, alargando la cadena de intermediacion y
cambiando la estabilidad del fondeo y el perfil de riesgo que enfrentan
los hogares (de deposito asegurado a cuotaparte rescatable sin seguro).

Approach: comparacion de vehiculos alcanzados y no alcanzados por cada
norma alrededor de las fechas exactas (los vehiculos cuyo canal de fondeo
no fue tocado funcionan como control), midiendo flujos de entrada y salida
en frecuencia alta y la recomposicion de instrumentos.

## Pregunta 4. Sustitucion o complementariedad en el credito

Cuando un banco se retira de una zona o restringe su oferta, quien absorbe
a sus deudores: otros bancos, o los otorgantes no bancarios (incluido el
credito fintech)? Y los deudores que migran, lo hacen en mejores o peores
condiciones y con que desempeño posterior? Esta es la pregunta clasica de
sustitucion versus complementariedad, que en Argentina se puede responder
con ventaja porque los otorgantes no bancarios reportan al mismo registro
de deudores que los bancos.

Approach: logica within-deudor: seguir al mismo deudor a traves de sus
distintos otorgantes alrededor de shocks que afectan a un otorgante y no a
otro (cierres de sucursales, shocks de fondeo especificos del banco segun
la pregunta 2). La comparacion dentro del deudor absorbe la demanda de
credito y aisla la oferta. Transiciones banco a no-banco, condiciones de
originacion y desempeño posterior (situacion del deudor) como resultados.

## Nota sobre alcance

Las cuatro preguntas comparten la misma columna vertebral: fechas
regulatorias exactas mas exposicion predeterminada (de jurisdicciones,
bancos, vehiculos o deudores). El detalle de que informacion se necesita
para cada una se conversa por separado; este documento fija las preguntas
para que ese pedido se pueda evaluar con libertad.
