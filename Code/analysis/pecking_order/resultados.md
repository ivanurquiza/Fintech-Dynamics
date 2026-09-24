# Orden de repago: resultados de la primera exploración

23 de septiembre de 2026. Notebook `01_orden_de_repago.ipynb`, muestra del 5% de personas
de CENDEU, agosto de 2024 a junio de 2026. Todas las cifras salen de las tablas de
`Code/output/pecking_order`.

## En una línea

Cuando un hogar empieza a dejar de pagar, elige a quién, y el orden de la elección lo fija
el acceso de cada acreedor a su flujo de ingresos. No es banco contra fintech: es la cuenta
donde entra la plata contra todo lo demás.

## Lo que se encontró

**1. La primera mora casi nunca es total.** 7.039.932 persona-mes elegibles (dos o más
relaciones con saldo, todas en situación 1) y 282.580 primeros eventos. El 96,9% son
parciales: caen algunas relaciones y otras no. Con dos relaciones, 93,5%. La tasa mensual
de primer evento va de 2,83% en septiembre de 2024 a 5,36% en noviembre de 2025 y vuelve a
3,4% en junio de 2026. Es la serie de flujo más limpia del deterioro que tenemos.

**2. La selección persiste.** De las relaciones que se siguieron pagando en el mes del
evento, 55,6% sigue sana seis meses después y 30,8% entró en mora. De las que cayeron,
62,5% sigue en mora y 20,4% se normalizó. No es desfasaje de vencimientos.

**3. El orden es marcado.** Logit condicional con efecto fijo de persona-mes, eventos con
una sola caída, controles de tamaño relativo y antigüedad. Razón de chances de ser la
relación que cae, contra banca privada:

| MercadoLibre | Banco digital | Mutual o coop. | Cía. financiera | Tarjeta no bancaria | Fin. de consumo | Retail |
|---:|---:|---:|---:|---:|---:|---:|
| 0,33 | 0,54 | 0,75 | 0,87 | 1,18 | 1,67 | 1,73 |

Las otras fintech, que prestan online sin billetera, quedan en 1,00. La medida sin modelo,
observado sobre esperado bajo elección al azar, da el mismo orden: MercadoLibre 0,43, retail
1,36.

**4. Las lecturas alternativas no se sostienen.** Excluir salidas no mueve nada. Todas las
categorías entran al evento por situación 2 en más del 95% de los casos, así que no hay una
que reporte con demora. Las relaciones protegidas no alcanzan a las demás después: seis meses
más tarde, las de MercadoLibre (23,7% en mora) y las mutuales (18,1%) tienen menos mora que
las de la banca privada (28,3%). MercadoLibre sigue protegido aun cuando es la deuda más
grande de la persona (0,60), y más cuando es chica (0,27). La excepción son los bancos
digitales: se los protege en el mes del evento pero sus relaciones protegidas caen después
a 46% a seis meses. En ellos la ventaja es demora, no prioridad.

**5. Por entidad aparecen los agentes pagadores.** Contra Galicia, los bancos más protegidos
son Santiago del Estero (0,21), Industrial (0,25), Chaco (0,32), Macro (0,37), Corrientes
(0,38), Entre Ríos (0,45) y Santa Fe (0,52). Brubank 0,34, Ualá 0,42, MercadoLibre 0,24.
Naranja Digital, la entidad detrás de la billetera Naranja X, 0,68 contra Tarjeta Naranja
0,86. Al fondo, Cencosud 1,53, CFN 1,41, Frávega 1,33.

**6. El agente pagador cobra primero donde paga.** Macro en Salta, Jujuy, Misiones y Tucumán:
0,21. Macro fuera de esas provincias: 0,62. Es el mismo banco. Los bancos provinciales en su
provincia van de 0,19 (Santiago del Estero) y 0,30 (Formosa) a 0,99 (Provincia de Buenos
Aires): más protección cuanto más chica la provincia, que es donde más pesa el empleo público.
La comparación con deudores fuera de la provincia solo tiene soporte para cinco bancos y no
es uniforme (Santiago y Provincia a favor, Ciudad sin diferencia, el Municipal de Rosario en
contra), así que el contraste casa contra fuera descansa sobre todo en Macro.

**7. La prioridad sigue a la fuente de ingreso.** Con el padrón:

| | Sin actividad, <65 | Comercio, <65 | Otra actividad, <65 | 65 o más |
|---|---:|---:|---:|---:|
| MercadoLibre | 0,32 | 0,18 | 0,20 | 0,56 |
| Bancos digitales | 0,56 | 0,30 | 0,36 | 0,95 |
| Banca pública nacional | 1,02 | 1,11 | 1,36 | 0,66 |
| Banco provincial en casa | 0,63 | 0,78 | 0,82 | 0,59 |
| Macro en sus provincias | 0,18 | 0,29 | 0,27 | 0,28 |

Los jubilados protegen al banco que les paga el haber y dejan de proteger a MercadoLibre y a
los bancos digitales. Quienes tienen actividad registrada, al revés. Los asalariados, que no
tienen actividad en el padrón, protegen más al banco provincial y a Macro. La excepción son
las mutuales: esperaba más protección entre jubilados por el código de descuento sobre
haberes y es al revés (0,56 sin actividad contra 0,71 entre jubilados).

**8. El orden no reacciona al estrés.** Estimado por separado en 09/2024 a 05/2025,
06/2025 a 12/2025 y 2026, los extremos no se mueven: MercadoLibre 0,27, 0,26 y 0,31; Macro en
casa 0,22, 0,20 y 0,24. Se mueve el medio: las financieras digitales pasan de 1,14 a 0,53, y
en 2026 la banca pública y las tarjetas no bancarias caen algo más.

**9. Una medida independiente da el mismo orden.** En el corte de deudores de julio de 2026,
`forced_reclass` es la recategorización obligatoria: en 99% de las relaciones marcadas en
situación 2 y 3 hay otra entidad que clasifica peor al deudor, y en situación 4 el 89% está
exactamente un nivel por encima de la peor. La proporción de la mora de cada acreedor que es
recategorización mide cuánto se le pagaba mientras el deudor caía en otros. Es 51% en
Santiago del Estero, 32% en Macro, 25% en MercadoLibre, 23% en mutuales; 4% en retail, 2% en
financieras de consumo y otras fintech. Correlación de rangos con el panel entre entidades que
aplican la regla: −0,59 (n = 41), con el signo esperado.

## Hallazgos sobre los datos, útiles para todos

- `days_past_due` del corte de deudores es cero en casi todas las relaciones, aun en
  situación 5. No sirve.
- `unused_ars` es cero en todo el corte. No sirve para separar tarjetas de préstamos, como
  yo había sugerido en `review_debate_paper.md`.
- `refinanced` y `legal_status` son distintos de cero en el 100% de las relaciones de PNFC y
  fondos de garantía. Es un problema de parser o de codificación del archivo de PNFC.
- `pref_guar_a_ars` y `pref_guar_b_ars` sí tienen contenido: 2,4% de las relaciones de
  entidades financieras y 18,7% de las de fideicomisos.
- `forced_reclass` está validado (punto 9) y es aprovechable.
- Dos entidades con mucha mora y 0% exacto de recategorización (Credicuotas, CFN) no parecen
  aplicar la regla. Hay que confirmarlo antes de usar la medida con ellas.

## Lo que no quedó resuelto

- Débito sobre el flujo contra exclusión futura. MercadoLibre puede debitar la billetera y
  también cortar el acceso a la plataforma. El corte por actividad favorece al débito, no lo
  aísla.
- Acceso local contra sueldo en los bancos provinciales. Hace falta puntos de acceso por
  localidad y el código postal del padrón.
- Empleo público por provincia: con ese dato el gradiente del punto 6 pasa de sugerencia a
  test.
- Producto dentro de la relación bancaria.
- Neuquén, Ciudad y el Municipal de Rosario tienen mucha mora recategorizada y protección
  moderada en el panel. No está explicado.

## Lo que abre

1. **El paper.** "El orden de repago sigue al sueldo" es una contribución en sí misma, con
   diseño dentro del deudor, un mecanismo que predice cortes que las alternativas no predicen,
   y una validación regulatoria independiente. Vecindad: Andersson, Chomsisengphet, Glennon y
   Li (2013, JMCB) sobre el orden de impago entre productos; Coelho, de Mello y Funchal (2012,
   REStat) sobre descuento de nómina en Brasil; la literatura de fintech de pagos y cobro sobre
   flujos. La diferencia es comparar contra todos los acreedores del mismo deudor.
2. **Precio de la prioridad.** Si retail y consumo cobran últimos, deberían cobrar más caro al
   mismo deudor. Las tasas de PNFC pedidas al BCRA lo permitirían.
3. **Dilución.** Un acreedor senior de hecho impone una externalidad sobre los demás. ¿Sube el
   riesgo de las deudas con retail cuando la persona toma crédito de MercadoLibre?
4. **Conexión con la expansión fintech.** MercadoLibre creció 48% real mientras el crédito
   regular de la banca privada a hogares caía. Un prestamista que cobra primero puede
   expandirse hacia una población en deterioro con menos pérdida. Es una explicación de la
   sustitución que no depende de la liquidez bancaria, y une las dos líneas del proyecto.
5. **La recategorización como canal.** La regla contagia la mora reportada entre acreedores y
   obliga a previsionar préstamos que se están pagando: un cuarto de la mora reportada de
   MercadoLibre es de ese tipo.
