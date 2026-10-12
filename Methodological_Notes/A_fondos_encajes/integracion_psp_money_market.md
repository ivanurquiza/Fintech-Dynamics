# Billeteras, fondos money market e integración vertical: costo de fondeo y franquicia del float

Nota de idea, 12 de octubre de 2026. Desarrolla una propuesta para la línea A. Registra la hipótesis de partida, cómo la reformulan los hechos institucionales que ya verificamos, qué se puede medir con las bases del repo y cuáles son sus límites. No contiene estimaciones.

## 1. La idea de partida

Un proveedor de servicios de pago (PSP) custodia el saldo de sus clientes. Tiene dos destinos posibles para ese float: dejarlo a la vista en su banco depositario o invertirlo, con autorización del cliente, en un fondo money market. La hipótesis original es que antes de los cambios regulatorios el PSP estaba aproximadamente indiferente entre los dos destinos. Cuando el banco depositario dejó de poder remunerar el saldo del PSP, el destino bancario dejó de rendir y el PSP pasó a tener incentivos a mandar los saldos al money market.

El argumento distingue dos tipos de fondo:

- **Integrados.** El fondo lo administra una sociedad gerente del mismo grupo que el PSP (Mercado Fondo, de Mercado Pago Asset Management; Ualintec Ahorro Pesos, de Ualá; Cocos Ahorro).
- **No integrados.** El fondo es de una gerente independiente y recibe el float de uno o más PSP a través de una clase propia o de un convenio de colocación (Delta Pesos clase X con Personal Pay; Allaria Ahorro clase E con Prex; Fima Premium y después Vinci Compass Liquidez con Lemon).

La predicción es que el cambio no altera el costo de fondeo del fondo integrado y sí baja el de los no integrados, que pasan a recibir un flujo de saldos que antes quedaba en el banco. El marco conceptual está en tres lugares de la literatura: los costos de agencia en la distribución de fondos (el distribuidor elige el fondo que mejor le paga a él), el valor de franquicia de los depósitos (saldos transaccionales inelásticos a la tasa) y la integración vertical entre el canal de distribución y el administrador.

## 2. Dos shocks distintos

El término "cambio de encaje" mezcla dos regulaciones con efectos distintos sobre el fondo.

**Encaje sobre la cuenta del PSP en el banco (punto 1.3.14 de Efectivo Mínimo).** Es el shock de la idea de partida.

| Norma | Vigencia | Contenido |
|---|---|---|
| A 6859, A 6885 | ene-2020 | Habilitan a los PSP a invertir los saldos de clientes en fondos money market |
| A 7429 | 1-ene-2022 | Encaje de 100% sobre las cuentas donde los PSP depositan los fondos de sus clientes |
| A 7611 | 22-sep-2022 | Permite integrar hasta 45 pp de esa exigencia con bonos del Tesoro en pesos; el banco vuelve a poder remunerar parte del saldo |
| A 7825 | 25-ago-2023 | La retribución que pague el banco por esas cuentas debe trasladarse totalmente a los clientes del PSP |

La A 7429 le quita al banco la capacidad de remunerar; la A 7611 la devuelve en parte, y la A 7825 le quita al PSP la posibilidad de quedarse con el spread. Visto desde el PSP, el shock más limpio a la rentabilidad del float en el banco es la A 7825.

**Encaje sobre la vista de los fondos money market (punto 1.3.12).** Creado en 0% en abril de 2020; 10% desde el 15-abr-2024, 15% desde el 15-may-2024, 20% desde el 1-nov-2024, 40% desde el 1-ago-2025, con un adicional general de 3,5 pp entre septiembre y noviembre de 2025. Desde diciembre de 2025 sigue en 40%. Este shock no actúa sobre el fondeo del fondo sino sobre el rendimiento de sus activos: la vista bancaria rinde menos y el fondo recompone hacia plazo fijo y caución (en el agregado, la vista pasa de 69% del patrimonio en 2023Q4 a 32% en 2024Q4).

La idea de partida corresponde al primer bloque, 2022 a 2023. El segundo bloque es útil como shock de activo, que afecta por igual a integrados y no integrados, y como contraste.

## 3. Lo que ya sabemos y cómo cambia la hipótesis

Mercado Fondo opera desde 2018 y la habilitación normativa es de enero de 2020, dos años antes del encaje de 100%. Para el PSP dominante no había indiferencia previa: ya tenía el float en su fondo. Por eso en el agregado no se ve un desplazamiento hacia los money market después de 2022, y la versión agregada de la hipótesis no se sostiene. `Regulation/README.md` lo documenta.

La distinción integrado/no integrado convierte ese hecho en evidencia a favor de una versión más precisa de la idea. El PSP integrado captura los honorarios de la gerente (en Mercado Fondo clase A, 1,94% anual sobre el patrimonio), así que prefiere el fondo propio con cualquier remuneración bancaria. El PSP no integrado no cobra esos honorarios, salvo lo que obtenga por convenio con la gerente, y le convenía el banco mientras el banco remunerara. La hipótesis reformulada es:

- **H1.** Los PSP integrados están en el fondo desde antes de 2022 y su asignación no responde a los shocks del punto 1.3.14.
- **H2.** Los PSP no integrados entran a fondos de terceros o aumentan sus saldos en ellos después de los shocks del punto 1.3.14 (A 7429 y, sobre todo, A 7825), y menos después de la A 7611.
- **H3.** Los fondos no integrados que reciben ese flujo pueden ofrecer una remuneración menor por unidad de saldo: su costo de fondeo baja.
- **H4.** Las clases de billetera tienen menor sensibilidad de la tasa neta a la tasa de mercado que las clases institucionales. En el fondo integrado esa franquicia la captura el grupo del PSP vía honorarios; en el no integrado se reparte entre la gerente y el PSP.

## 4. Qué es el costo de fondeo de un money market

El fondo se fondea con cuotapartes. Su costo de fondeo es lo que tiene que pagarle al cuotapartista para que se quede, medido contra la alternativa de mercado. Con la planilla diaria por clase se observan tres cosas:

- La **tasa neta** de cada clase, $i^{net}_{c,t}$, que es lo que recibe el cuotapartista.
- La **tasa bruta** del fondo, $i^{gross}_{f,t} = i^{net}_{c,t} + \text{fee}_{c,t}$, igual para todas las clases del fondo (verificado: desvío mediano 0,004 pp).
- Los **honorarios** de cada clase, $\text{fee}_{c,t}$ (gerente, depositaria y gastos).

Dos medidas de costo de fondeo:

1. **Spread contra la tasa de mercado:** $s_{c,t} = i^{m}_t - i^{net}_{c,t}$, con $i^m$ la tasa de caución a un día o TAMAR. Un spread mayor es un fondeo más barato para el fondo.
2. **Beta de la tasa neta:** el traspaso de cambios en la tasa de mercado a la tasa neta de la clase. Una beta baja es la firma de la franquicia, como en el canal de depósitos de Drechsler, Savov y Schnabl (2017).

Dentro de un mismo fondo, la tasa bruta es común, así que cualquier diferencia de tasa neta entre clases es una diferencia de honorarios. La franquicia a nivel clase aparece entonces como fijación y ajuste de honorarios. Entre fondos, la diferencia en la beta bruta refleja la cartera. Conviene separar las dos cosas desde el principio.

## 5. Diseño

### 5.1 Cronología de entrada (primer paso)

Para cada PSP no integrado, la fecha en que aparece su clase en la planilla y la trayectoria de su patrimonio y flujo, contra Mercado Fondo y contra las clases no asociadas a billeteras. Es una figura por PSP con las fechas de la A 7429, la A 7611 y la A 7825 marcadas. Sirve para ver si H1 y H2 tienen soporte antes de estimar nada.

### 5.2 Flujos dentro del fondo

$$
\frac{\text{flujo}_{c,t}}{\text{PN}_{c,t-1}} = \alpha_{f(c),t} + \gamma_c + \beta\,\big(\text{PSP}_c \times \text{Post}_t\big) + \varepsilon_{c,t}
$$

con $c$ clase, $f(c)$ su fondo y $t$ semana. El efecto fijo fondo × semana absorbe cartera, rendimiento bruto y cualquier shock del fondo. $\beta$ es el flujo diferencial de la clase de billetera después del evento, respecto de las otras clases del mismo fondo. Se estima por separado para fondos integrados y no integrados; H2 predice $\beta$ positivo en los no integrados y cercano a cero en los integrados. El flujo se mide en cuotapartes para no mezclar rendimiento.

### 5.3 Traspaso de tasas

$$
\Delta i^{net}_{c,t} = \alpha_c + \beta_0\,\Delta i^m_t + \beta_1\,\Delta i^m_t \times \text{PSP}_c + \beta_2\,\Delta i^m_t \times \text{PSP}_c \times \text{NoInt}_{f(c)} + \text{(interacciones con Post)} + \varepsilon_{c,t}
$$

en frecuencia mensual para limpiar ruido diario. H4 predice $\beta_1 < 0$. La interacción con el período posterior a la A 7825 dice si la franquicia de los no integrados cambia con el shock. La variación de tasas en Argentina entre 2020 y 2026 es muy grande, y eso da potencia a esta parte aunque el número de fondos sea chico.

### 5.4 Lado del activo y de los bancos (complementario)

El encaje del punto 1.3.12 permite medir qué bancos dependían del fondeo de los money market. Con las carteras semanales se arma, para cada banco, la vista y el plazo fijo que recibe de cada fondo sobre sus depósitos, con composición previa fija. Es una exposición banco por banco construida desde el fondo, que no depende de supuestos geográficos. Requiere el cruce de los nombres de banco de las carteras con el código de entidad del BCRA.

## 6. Datos

**Disponibles en el repo.**
- Planilla diaria por clase, ene-2020 a sep-2026: cuotapartes, patrimonio, VCP, honorarios, tasa neta y bruta (`panel_clase_dia.parquet`).
- Carteras semanales por fondo (`carteras_lineas`, `carteras_ancha`).
- Mapa billetera → fondo → clase → gerente → depositaria (`Data/crosswalks/psp_fci_map.csv`), con unos diez PSP.
- Balances bancarios, incluida la partida 311723 (cuenta especial de persona jurídica sin interés, el candidato a float de PSP en el banco).
- Cronología normativa y alícuotas (`Regulation/`).

**A construir con fuentes públicas.**
- Completar y fechar el mapa PSP → clase: la mitad de las filas está "a confirmar". La planilla da la fecha de alta de cada clase; los reglamentos de gestión y los hechos relevantes de la ficha CNV, el destinatario de cada clase y los cambios de colocador.
- Clasificar cada fondo como integrado o no integrado según el grupo de su gerente.
- Series de tasas de mercado: caución a un día (BYMA) y TAMAR y BADLAR (API del BCRA).

**No observable.** Cuánto deja cada PSP en cada banco: la partida 311723 está a nivel banco y mezcla a todos los titulares, y es chica (0,3% a 0,6% de los depósitos del sector privado). Los términos económicos de los convenios entre PSP y gerente (reparto de honorarios o reintegros). La hipótesis H3 se testea por sus implicancias sobre precios y flujos, no midiendo el reparto directamente.

## 7. Límites

**Pocos fondos tratados.** Los fondos no integrados con billetera son entre cinco y ocho. Para 5.2 la inferencia con errores agrupados por fondo no es confiable; hay que usar inferencia por randomización sobre la asignación de fechas o métodos para pocos tratados (Conley y Taber, 2011; wild bootstrap con pocos clusters). 5.3 depende menos de esto porque la variación viene del tiempo.

**Concentración.** Mercado Pago concentra cerca del 88% de los saldos en cuentas de pago. Cualquier agregado es Mercado Pago. Los resultados sobre no integrados son sobre una parte chica del mercado, y hay que presentarlos como evidencia sobre el mecanismo, no sobre la magnitud agregada.

**Superposición de eventos.** La A 7825 (25-ago-2023) cae diez días después de la devaluación del 14-ago-2023 y en plena suba de tasas. La A 7429 coincide con el cierre de 2021 y la A 7611 con cambios de tasa de política. El efecto fijo fondo × semana absorbe todo lo común a las clases de un fondo, pero no un shock que afecte de manera distinta a la demanda de los clientes de billeteras.

**La A 7611 hace que el shock no sea monótono.** Entre ene-2022 y sep-2022 el banco no podía remunerar; después sí en parte. El evento de 2022 tiene dos fechas con signos opuestos.

**La integración es una elección.** Que un PSP tenga gerente propia no es aleatorio: lo hacen los más grandes. La comparación integrado contra no integrado es descriptiva del mecanismo, y conviene apoyarla en los cambios dentro del PSP: entrada de clases, cambio de gerente (Lemon, de Fima a Vinci en 2026) o creación de gerente propia.

**Mapa incompleto.** Si un PSP coloca a través de una clase general y no de una clase propia, su flujo no se separa del resto. Esos casos quedan fuera del grupo tratado o se tratan como contaminación del control.

## 8. Por qué no una exposición regional

Una alternativa es medir la exposición de cada banco a las regiones con más uso de billeteras. La revisión de agosto la descartó como diseño principal. Los bancos grandes replican la distribución nacional de depósitos, así que su exposición geográfica casi no varía (entre 41 y 55 puntos de adopción para los trece mayores). La dispersión viene de bancos públicos provinciales chicos, de modo que la variable termina siendo un indicador de banco provincial, confundido con depósitos públicos y ciclo fiscal. Además mide otro canal: la pérdida de depósitos minoristas hacia las billeteras, no el efecto del encaje sobre el float. La exposición construida desde las carteras de los fondos (5.4) responde mejor a la pregunta.

## 9. Literatura a ubicar

- Canal de depósitos y franquicia: Drechsler, Savov y Schnabl (2017, QJE); Koont, Santos y Zingales (en `Literature/`).
- Money market y transmisión de política: Xiao (2020, RFS).
- Pagos y crédito con fintech: Parlour, Rajan y Zhu (2022, RFS, en `Literature/`).
- Incentivos del distribuidor en fondos: Christoffersen, Evans y Musto (2013, JF) sobre pagos de los fondos a los distribuidores; Bergstresser, Chalmers y Tufano (2009, RFS) sobre fondos vendidos por intermediarios.

Verificar las referencias exactas antes de citarlas.

## 10. Primer paso

Completar y fechar el mapa PSP → clase con la planilla y las fichas CNV, clasificar las gerentes, y armar las figuras de 5.1. Si la cronología no muestra entrada o crecimiento de las clases no integradas alrededor de la A 7429 o la A 7825, la hipótesis se reformula antes de estimar.
