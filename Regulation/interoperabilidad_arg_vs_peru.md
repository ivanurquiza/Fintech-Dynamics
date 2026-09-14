# Las reformas de pagos en Argentina, y en qué se diferencian del caso peruano

_Nota de trabajo. Fintech-Dynamics, agosto 2026._
_Los PDF están en `Regulation/interoperabilidad/`; la cronología completa en `cronologia_normativa.csv`._

---

## Antes que nada: cómo se llama lo que pasó en Argentina

**No es "interoperabilidad de billeteras".** Las transferencias entre personas ya eran
interoperables desde 2019. Lo que las reformas argentinas abrieron fue **la aceptación en
el comercio** y, después, **el fondeo de la billetera desde la cuenta bancaria**.

Términos correctos del BCRA, para usar en el paper:

- **Pago con transferencia (PCT)** — el instrumento creado por Transferencias 3.0.
- **Interfaz Estandarizada de Pagos (IEP)** — la capa técnica de mensajería común.
- **Interoperabilidad de códigos QR** — el mandato propiamente dicho.
- Roles del esquema: **PSPCP** (cuentas de pago), **PSI** (iniciación), **aceptador**
  (adhiere comercios), **agregador/subadquirente**, **administrador de esquema**.

> *Transferencias 3.0 mandated the interoperability of QR-initiated transfer-based payments
> at the point of sale, unbundling payment initiation from merchant acceptance.*

---

## Reforma 0 — Los rieles (2016-2019)

Sin esto no se entiende el resto.

| Norma | Emisión | Aplicación | Qué involucró |
|---|---|---|---|
| A 6044 | 22/08/2016 | — | Crea el **alias-CBU**. Solo cuentas bancarias. |
| A 6099 | 14/11/2016 | 15/11/2016 | Crea el **DEBIN**: riel de débito (*pull*), alguien pide plata y el titular autoriza. |
| **A 6510** | **15/05/2018** | **+120 días ≈ sep-2018** | Crea la **CVU**, la "cuenta bancaria" de una billetera. Los bancos quedan obligados a procesar transferencias contra CVU. Cada CVU tiene alias, en el **mismo espacio de nombres** que el CBU. |
| CIMPRA 518 | 17/07/2018 | — | Define la operatoria: CVU→CBU, CBU→CVU y CVU→CVU, inmediatas, y **no rechazables**. |
| **A 6697** | **05/06/2019** | **30/06/2019** | Una transferencia con CVU debe cursarse **"en idénticas condiciones"** que una con CBU, en todos los canales, incluido mobile. |

**Resultado:** transferir entre una billetera y un banco, o entre dos billeteras, quedó
abierto **de derecho desde 2019**.

**El detalle que importa para identificación:** en la práctica no funcionó bien hasta fines
de 2021. Los bancos aplicaban topes de $50.000 diarios sin base normativa, demoras de 24 h
e interfaces diferenciadas para CBU→CVU. El **16/12/2021** el BCRA les mandó nota formal a
ABA y ADEBA exigiendo eliminarlos, con un mínimo de 15.000 UVA diarios sin solicitud
especial. El "encendido" del P2P no es una fecha limpia: es una rampa 2018→2021 con
cumplimiento desparejo por banco. Si se consigue el detalle por entidad, eso es variación
cross-bank en enforcement.

---

## Reforma 1 — Transferencias 3.0: nace el pago con transferencia (2020-2021)

| Norma | Emisión | Aplicación | Qué involucró |
|---|---|---|---|
| **A 7153** | **30/10/2020** | **07/12/2020** | Crea **Transferencias 3.0** y el **pago con transferencia (PCT)**: el comercio cobra recibiendo una transferencia inmediata e irrevocable en segundos, en lugar de una operación de tarjeta a 48 h. Arancel tope al comercio **0,8%**. Crea las normas complementarias y la **IEP**. |
| A 7175 | 05/12/2020 | 07/12/2020 | Emite los textos ordenados del régimen. |
| A 7361 | 08/09/2021 | 09/09/2021 | 15 segundos, 24×7×365, límites mínimos en UVA. |
| A 7367 | 17/09/2021 | +30 días | Prohíbe conductas anticompetitivas a los **administradores de esquema** que además compiten como participantes. |
| **A 7400** | **16/11/2021** | **29/11/2021 (vigencia plena)** | **La fecha clave.** Cualquier billetera debe poder leer **cualquier** QR para pagar por transferencia. Se termina el QR propietario. |
| A 7409 | 25/11/2021 | hasta 01/03/2022 | Tolerancia transitoria de 25 segundos cuando hay que interoperar entre esquemas. |
| **A 7462** | **24/02/2022** | 15/04, 01/05 y 01/06/2022 | Crea el **Registro de Billeteras Digitales Interoperables**. El administrador de esquema **no puede habilitar un QR** sin constatar que lo leen todas las entidades y PSP. |

### Qué estaba cerrado, exactamente

Antes de esto, cada billetera tenía su QR y el comercio necesitaba uno por billetera. Pero
el problema no era solo el lector. **Mercado Pago era simultáneamente** el que adhería al
comercio, el que fijaba las reglas del esquema, el que emitía la cuenta del pagador y el
que liquidaba. Un pago por QR era o bien una transferencia interna entre dos cuentas de
Mercado Pago, o bien una operación de tarjeta donde Mercado Pago era el adquirente. **En
ninguno de los dos casos había puerta de entrada para un tercero.**

T3.0 separa la capa de **iniciación** (quién dispara el pago) de la de **aceptación** (quién
adhiere al comercio).

**Límite:** esto abrió **solo el QR pagado con transferencia**. El QR pagado con tarjeta
siguió cerrado dos años y medio más.

---

## Reforma 2 — El QR con tarjeta de crédito (2023-2025)

| Norma | Emisión | Aplicación | Qué involucró |
|---|---|---|---|
| **A 7769** | **18/05/2023** | original 01/12/2023 | Todo QR de un adquirente o agregador que acepte crédito debe (a) aceptar también PCT en el mismo QR y (b) poder ser usado por **cualquier** billetera del Registro, sin discriminar comisión ni plazo por marca. |
| A 7905 | 30/11/2023 | posterga a 01/02/2024 | Primera prórroga. |
| A 7942 | 11/01/2024 | posterga a **30/04/2024** | Segunda prórroga. **Esta es la fecha efectiva.** |
| **A 8032** | **30/05/2024** | ≈29/07/2024; prepagas ≈24/02/2025 | **Reciprocidad**: la billetera debe poder leer el QR de **todo** adquirente o agregador. Responsabilidad por fraude en cabeza de la billetera. Comisión máxima de la billetera al emisor: **0,07%**. |
| A 8114 | 08/10/2024 | 09/10/2024 | Consolida lo anterior en el texto ordenado. |

**Dos detalles prácticos:** el BCRA fecha el arranque el 30/04/2024, pero la prensa reportó
operatoria efectiva recién el 03/06/2024 — cinco semanas de brecha entre vigencia y
funcionamiento. Y en noviembre de 2024 Mercado Pago bloqueó los pagos QR con Visa desde
MODO. La interoperabilidad de derecho no fue instantánea de hecho.

---

## Reforma 3 — El fondeo de la billetera (2022-2024)

La menos contada, y la que toca más directamente al banco.

| Norma | Emisión | Aplicación | Qué involucró |
|---|---|---|---|
| **A 7514** | **19/05/2022** | **30/09/2022** | Transferencias **"pull"**: la billetera puede debitar una cuenta provista por **otra** entidad, con consentimiento del titular. Es lo que permite cargar saldo tirando de la cuenta del banco. |
| A 7841 | 14/09/2023 | 01/12/2023 | **Discontinúa el DEBIN recurrente** como herramienta de fondeo. |
| A 7905 / A 7942 | 30/11/2023 / 11/01/2024 | → 01/03/2024 → **30/04/2024** | Dos prórrogas. |
| A 7996 | 30/04/2024 | 30/04/2024 | Pull mismo titular con consentimiento **expreso vía OAuth2** o tácito; arancel 0,3% solo si es tácito; límite 2.500 UVA/día. |
| A 8030 | 30/05/2024 | 30/05/2024 | **Elimina el arancel del pull.** |

**Por qué importa:** el banco pasa de controlar cuándo sale la plata de su cliente (el
DEBIN lo autorizaba operación por operación) a un régimen donde la billetera tira del saldo
con consentimiento permanente y sin costo. Es un cambio en el poder de negociación
banco-billetera sobre el depósito minorista.

---

## Reforma 4 — Precios y afinado (2024-2026)

| Norma | Emisión | Aplicación | Qué involucró |
|---|---|---|---|
| A 8091 | 16/08/2024 | 17/08/2024 | Los precios de transferencias **no pueden definirse como % del monto**. |
| **A 8162** | **19/12/2024** | acreditación 01/08/2025; identificación 01/06/2025 | Acreditación al comercio en ≤2 días hábiles. **Elimina la exigencia de arancel uniforme por rubro** → aparece dispersión de precios entre comercios. Obliga a identificar en la mensajería **qué billetera** inició y **si fue por QR**. |
| A 8206 | 27/02/2025 | 12/05/2025 | **VQR**: transporte público con QR. Todo administrador QR debe integrarse con toda billetera, y viceversa, en 30 días hábiles desde el requerimiento. |
| A 8406 | 02/03/2026 | 31/08/2026 | **"Cobro con transferencia"**: reemplaza el débito recurrente para cobrar cuotas. |

---

## Perú, breve: cómo lo cuenta el paper

Burga, Céspedes, Parra, Cerón & Quispe (2025), IDB-WP-1767.

El paper describe un sistema **fragmentado en dos billeteras dominantes y no
interoperables**: **Yape**, de BCP (el banco más grande), lanzada en 2016; y **Plin**,
consorcio defensivo de Interbank, BBVA y Scotiabank, lanzado en 2020. Textual: *"both
maintained a closed network"* — no se podía mandar plata de una a la otra. Yape era ~6×
más grande en cantidad de operaciones.

La norma es la **Circular 0024-2022-BCRP, del 06/10/2022**:

| Fase | Fecha | Alcance |
|---|---|---|
| **1** | **31/03/2023** | Yape y Plin deben interconectarse para **transferencias entre personas**, direccionadas por **número de celular**. |
| **2** | 30/06/2023 → **13/09/2023** (postergada por Circular 0013-2023) | Resto del sistema financiero (bancos, cajas municipales, financieras) + **QR interoperable**. |
| **3** | durante 2024 | Emisores de dinero electrónico. |
| **4** | desde fines de 2024 | Fintechs, telcos y bigtechs, vía iniciación de pagos. |

El paper toma como tratamiento **abril de 2023** (el piloto de la Fase 1) y considera
implementación plena en enero de 2024. La disponibilidad general para usuarios fue
alrededor del 10/05/2023.

**Dos cosas que el paper no dice:** que Perú ya tenía transferencias interbancarias
inmediatas desde 2016 (24×7 desde dic-2020) sobre la Cámara de Compensación Electrónica —
o sea que los rieles existían y lo que faltaba era interconectar dos capas propietarias por
encima. Y que la Fase 2 (13/09/2023), que incorpora a las cajas municipales — justamente
las prestamistas de microcrédito —, cae dentro de su ventana post-tratamiento, pero tratan
todo como un evento único.

### Diseño y resultados

DiD con exposición continua a nivel **ciudad**, medida en 2019Q4:
`exposición = share de depósitos de bancos-Yape × share de bancos-Plin`.

HHI de depósitos **+2%**; depósitos de bancos adoptantes **+9,6%**; tasas pasivas
**−50/−80 pb**; microcrédito **−13 a −20%**. Interpretación: el efecto *amenity* (la
billetera vale más cuando alcanza a todos, y el dominante captura la mayor parte del
excedente) domina al efecto *entrada*. **La interoperabilidad concentró en vez de
competir.**

Dos reparos antes de citarlo:

1. **La medida de exposición es casi el inverso mecánico de su propio outcome.**
   `s_Y × s_P` se maximiza cuando el mercado está balanceado, o sea cuando el HHI es bajo.
   Y el outcome es el HHI. Cualquier reversión a la media genera el signo estimado sin que
   la interoperabilidad haga nada.
2. **Contaminación de la Fase 2** dentro de la ventana post, como se dijo arriba.

Y sobre todo: **no tocan a la banca tradicional por el lado del fondeo.** Miran tasas
pasivas, pero no composición del pasivo, ni estabilidad, ni duración, ni sustitución hacia
fondos. Nada tipo Khwaja-Mian. Ahí está el hueco.

---

## La diferencia, en una tabla

| | Perú (2023) | Argentina (2021 / 2024) |
|---|---|---|
| Qué estaba cerrado | transferencias entre billeteras | el QR y la adquirencia |
| Qué se mandó abrir | direccionamiento por celular | lectura del QR; separación iniciación / aceptación |
| Lado del mercado | consumidor–consumidor | consumidor–comercio |
| Mecanismo económico | externalidades de red, fin del multihoming | fin del lazo cerrado vertical, reparto de la renta entre capas |
| Estructura previa | duopolio 6:1 (Yape vs Plin) | un dominante en aceptación (Mercado Pago) |
| P2P previo | cerrado entre billeteras | **abierto desde 2019** |

---

## El hecho argentino que vale la pena

Informe de Pagos Minoristas del BCRA, participación **intra-esquema** en el total de pagos
con transferencia:

| | intra-esquema | interoperable |
|---|---|---|
| 2S-2021 | **75,4%** | 24,6% |
| 2022 | **81,0%** | 19,0% |
| sep-2023 | **88,7%** | 11,3% |

*(Restringido a QR presencial, sep-2023 da ~69% intra. Usar ese número: el agregado mezcla
checkout de e-commerce dentro de Mercado Libre.)*

**Después del mandato, la participación intra-esquema no cayó: subió.** Interoperabilidad
*de jure* ≠ contestabilidad *de facto*, cuando persisten la base instalada de comercios,
los defaults de la app y el subsidio cruzado del saldo remunerado.

Y en 2026 el resultado es de **reparto entre capas**, no de desconcentración: iniciación
52,8% bancos / 47,2% billeteras; recepción 52,4% billeteras / 47,6% bancos. El par más
frecuente es **MODO inicia + Mercado Pago acepta**. La interoperabilidad redistribuyó el
margen sin mover quién tiene la base instalada.

---

## Qué podríamos hacer distinto

Perú mira concentración de depósitos. Nosotros podemos mirar **la interacción con la banca
tradicional por el lado del fondeo y del crédito**, que ellos no tocan:

1. **Composición del pasivo, no nivel.** Qué le pasa al depósito a la vista de un banco
   cuando el comercio de su zona empieza a cobrar por QR de otra billetera.
2. **El canal del comercio.** Un comercio que cobra por PCT recibe en CVU, no en su cuenta
   bancaria. Eso mueve depósito transaccional de PyME, que es la contraparte del crédito
   relacional. Perú no lo puede ver porque su shock era P2P.
3. **Enganche con el otro bloque del paper.** El saldo que se acumula en la billetera del
   comercio termina en un FCI money market y vuelve al banco como fondeo mayorista.

### Advertencias

- Todos los tramos argentinos son **nacionales y simultáneos**. La identificación tiene que
  venir de exposición predeterminada, no de la fecha.
- **Colisión de fechas:** abril-mayo 2024 tiene a la vez el QR-tarjeta (30/04), el fin del
  DEBIN recurrente (30/04), la A 7996 y la A 8030/8032 — y el primer encaje a los FCI
  (A 7988, 15/04). Ese mes es inutilizable para separar mecanismos.
- El BCRA **dejó de publicar la desagregación intra vs. interoperable** en 2024-2025. Sin
  esa serie no se mide el efecto del segundo shock. Incluirlo en el pedido de datos.
- **Mejor variación disponible**, en orden: VQR (A 8206, escalonado por sistema de
  transporte); fecha de inscripción en el Registro de Billeteras (A 7462, firma×tiempo, si
  se publica); umbrales de 100.000 y 500.000 UVA de la tasa de intercambio (RD a nivel
  comercio); A 8162 desde ago-2025 (dispersión de aranceles).
- Antecedente de competencia útil: caso **Prisma** (CNDC, compromiso de desinversión 2017,
  multiadquirencia enero 2019) y las denuncias cruzadas de 2024 — MODO contra Mercado Libre
  (may-2024) y Mercado Libre contra 36 bancos por cartelización (ago-2024).
