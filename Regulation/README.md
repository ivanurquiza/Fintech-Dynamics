# Corpus normativo: encajes a PSP y FCI, e interoperabilidad

_Fintech-Dynamics. Última revisión: agosto 2026._

Esta carpeta reúne las normas del BCRA que sostienen las Preguntas 1 y 3 de
`Methodological_Notes/preguntas_investigacion.md`.

```
Regulation/
├── descargar_normativa.py     baja todo y escribe manifiesto.csv con hash
├── cronologia_normativa.csv   54 normas, fecha, vigencia, alcance, valor p/identificación
├── encajes_psp_fci/           24 comunicaciones
├── interoperabilidad/         42 comunicaciones
├── textos_ordenados/          8 t.o. consolidados
└── publicaciones_bcra/        IEF, Inclusión Financiera, Monetario, Pagos Minoristas
```

Correr `python Regulation/descargar_normativa.py`. Los textos ordenados se
actualizan sin aviso; por eso el manifiesto guarda hash y fecha de descarga.

---

## 1. La hipótesis, eslabón por eslabón

**Hipótesis (Pregunta 3):** el encaje del 100% sobre los depósitos de PSP
volvió ese fondeo inútil para los bancos, lo que eliminó el incentivo del PSP
a dejar la plata ahí y lo empujó a girar los saldos hacia FCI money market;
después, cuando ese canal creció, el BCRA le puso encajes a los depósitos de
FCI para tapar el agujero.

Verifiqué los cuatro eslabones contra los PDF. **Dos se caen.**

### Eslabón 1 — El encaje del 100% (A 7429): verificado, pero mal fechado

Emitida el **30/12/2021**, vigente **01/01/2022**. El punto 1.3.14 de Efectivo
Mínimo fija 100% sobre "las cuentas de depósito de los PSPOCP en las que se
encuentren depositados los fondos de sus clientes".

La justificación pública del BCRA **no fue monetaria ni de nivelación
competitiva**: fue custodial — "preservarlos de contingencias y garantizar que
estén siempre a disposición de los y las ahorristas". La lectura de que le
quitaba rentabilidad a las billeteras fue de analistas y prensa (Ámbito,
Cronista, Perfil, 30-31/12/2021), no del regulador.

**El problema:** el efecto se revirtió parcialmente nueve meses después. La
**A 7611 (22/09/2022)** permitió integrar hasta **45 puntos porcentuales** de
esa exigencia con Bonos del Tesoro en pesos (BONTE 23/05/2027). O sea que el
banco recuperó rendimiento sobre casi la mitad del saldo y podía volver a
remunerarle al PSP. La prueba de que efectivamente lo hacía es que en agosto de
2023 el BCRA tuvo que dictar la **A 7825**, que obliga a que esa retribución
"deberá ser trasladada totalmente a sus clientes". Si la remuneración se
hubiera muerto en enero de 2022, la A 7825 no tendría objeto.

> **Conclusión operativa: el shock limpio a la monetización del float por parte
> del PSP es la A 7825, 25/08/2023, no la A 7429.** Es específica de PSP,
> discreta, sin contaminación macro simultánea comparable, y su mecanismo es
> transparente. Es el mejor candidato a shock de todo este corpus para la
> Pregunta 3.

### Eslabón 2 — Que eso empujó hacia los FCI: REFUTADO

Este es el que hay que sacar del paper.

La habilitación a girar saldos de clientes a "fondos comunes de dinero"
**no la trajo la A 7495 (abr-2022)**. Está textualmente en la **A 6859
(09/01/2020)** y en la **A 6885 (30/01/2020)**, punto 3.1.2. La A 7495 es una
Circular SINAP de *actualización*: renumera 3.1.2 → 4.1.2 y consolida. El
propio texto ordenado atribuye el 4.1.2 a "A 6885 (mod. por A 7495, 7825 y
8038)".

Y la práctica precede a la norma: **Mercado Fondo opera desde 2018**, con
rendimientos diarios desde octubre de ese año. Dos años antes del marco PSP y
tres antes del encaje del 100%.

Orden temporal real:

```
práctica (2018) → habilitación normativa (ene-2020) → encaje 100% (ene-2022)
```

El encaje no pudo empujar a los PSP hacia un canal que ya existía, ya estaba
autorizado y ya era masivo. Si esto queda en el paper, cae en el primer
referee report.

### Eslabón 3 — La escalera de encajes a FCI: fechas verificadas, motivo distinto

| Com. "A" | Vigencia | Tasa | Justificación contemporánea |
|---|---|---|---|
| 6992 | 24/04/2020 | 0% (crea) | no verificada; probable paquete COVID |
| 7988 | 15/04/2024 | 10% | "normalizar el tratamiento prudencial de cuentas de naturaleza similar"; simultánea a la baja de tasa 80%→70% |
| 8000 | 15/05/2024 | 15% | comunicado BCRA: "absorber el excedente de liquidez… eliminar distorsiones entre instrumentos similares" |
| 8119 | 01/11/2024 | 20% | sesgo contractivo; crédito creciendo con plazos fijos estancados |
| 8189 | 31/01/2025 | 20%, base ampliada | **anti-elusión**: los MM migraban a precancelables |
| 8281 | 01/08/2025 | 30% | "encaje de las partidas que generan mayor volatilidad y encarecen el crédito" |
| 8286 | 25/07/2025 | (pases) | **anti-arbitraje** |
| 8289 | 01/08/2025 | 40% | post-desarme LEFI: absorber pesos, contener el dólar |
| 8302 | 18/08/2025 | +5 pp transitorios | integración diaria, cargo 3×TAMAR |
| 8306 | 01/09/2025 | +3,5 pp | presión cambiaria pre-electoral |
| 8355 | 01/12/2025 | 40% | elimina los +3,5 pp |

**Ninguna comunicación ni comunicado del BCRA menciona billeteras como
objetivo.** Las justificaciones son tres y se repiten: nivelación
anti-arbitraje regulatorio, absorción de pesos, y volatilidad del fondeo.
Bausili (jul-2025): "heredamos un sistema de encajes súper distorsionado" — el
mismo depósito tenía 0% si venía vía FCI y 36% si venía de una empresa.

Además, casi todas las tandas coinciden con episodios monetarios que las
explican solas. La más nítida: el **desarme de la LEFI el 10/07/2025** hundió
la tasa de caución de ~35% a ~15% por exceso de liquidez, con el dólar +14% en
el mes; el BCRA subió encajes dos veces en julio.

> El canal billetera → FCI → banco es el **vehículo** por el que pasa la
> política, no su **blanco declarado**.

### Eslabón 4 — "Tapar el problema": no como intención, sí como efecto

Lo que el BCRA hizo entre 2024 y 2025 se describe mejor como **convergencia a
la neutralidad del encaje respecto de la identidad del depositante**: un
depósito a la vista es un depósito a la vista, venga de un hogar, de una
empresa o de un FCI que fondea a un PSP. La escalera 0→10→15→20→30→40 es la
trayectoria de ese ajuste.

---

## 2. Por qué esto es una buena noticia, no una mala

Si las subas del punto 1.3.12 hubieran estado motivadas por el crecimiento de
las billeteras, tendríamos **endogeneidad de manual**: política que responde al
outcome. Como están motivadas por el desarme de la LEFI, la presión cambiaria y
una doctrina general de nivelación, hay un argumento defendible de que el shock
es **exógeno a la demanda de saldos en billeteras**, con incidencia diferencial
por banco según su composición de pasivo previa.

Eso es un diseño à la Khwaja-Mian con tratamiento regulatorio. El episodio
**LEFI de julio 2025** es el candidato más limpio: shock grande, fechado, y con
una causa próxima (el rediseño del instrumento de política) que no tiene nada
que ver con billeteras ni con bancos individuales.

La narrativa correcta para el paper deja de ser "el BCRA persigue billeteras" y
pasa a ser "el BCRA converge a neutralidad de encaje, y en el camino revela
cuánto del fondeo bancario depende del canal fintech". Es más defendible y más
interesante.

---

## 3. Interoperabilidad (Pregunta 1)

### Calendario del QR, en limpio

Cinco tramos, todos **nacionales y simultáneos**:

| # | Hito | Fecha efectiva | Norma |
|---|---|---|---|
| 1 | Arranca T3.0 / pago con transferencia | 07/12/2020 | A 7153 |
| 2 | QR interoperable pleno entre billeteras | **29/11/2021** | A 7153 §7.1, reordenado en A 7400 |
| 3 | Registro de billeteras interoperables operativo | 15/04–01/06/2022 | A 7462 |
| 4 | Fondeo por *pull*; fin del DEBIN recurrente | 30/09/2022; migración forzosa **30/04/2024** | A 7514; 7841; 7905; 7942 |
| 5 | **QR con tarjeta de crédito interoperable** | ordenado 18/05/2023, dos prórrogas, efectivo **30/04/2024** | A 7769; 7905; 7942 |
| 5b | Reciprocidad (billetera lee QR de cualquier adquirente) | ≈29/07/2024 y ≈24/02/2025 | A 8032 |
| 6 | Viaje con QR (VQR) en transporte | **12/05/2025** | A 8206 |

Precisión que importa: el BCRA fecha el QR-crédito el 30/04/2024, pero la
prensa reportó operatoria efectiva recién el 03/06/2024. Cinco semanas de
brecha entre vigencia normativa y funcionamiento. Usar la fecha equivocada
rompe el event study.

### El problema, dicho sin vueltas

**Todos los tramos son nacionales y simultáneos.** No hay fases geográficas ni
por entidad. Un event study puro sobre 07/12/2020, 29/11/2021 o 30/04/2024 no
distingue interoperabilidad de cualquier otra cosa que haya pasado ese mes — y
en Argentina siempre pasó algo. Como está planteada en `preguntas_investigacion.md`
("shock normativo nacional con fecha exacta + exposición territorial
predeterminada"), la Pregunta 1 depende enteramente de que la exposición
territorial sea creíble, porque el shock por sí solo no identifica nada.

### Dónde sí hay variación explotable, por orden de calidad

1. **VQR (A 8206, 12/05/2025).** La adopción es **por sistema de transporte**,
   o sea geográfica y escalonada. Es un shock local a la adopción de billetera,
   plausiblemente exógeno a la banca local. Es el mejor instrumento que sale de
   todo este corpus, y encaja con el diseño territorial que ya tenemos.
2. **Fecha de inscripción en el Registro de billeteras interoperables**
   (A 7462). Variación firma×tiempo, escalonada, con fecha administrativa dura.
   Hay que verificar si el registro publica fecha de inscripción — es la
   verificación de mayor valor marginal pendiente.
   `https://www2.bcra.gob.ar/SistemasFinancierosYdePagos/Registro_Billeteras_Digitales_Interoperables.asp`
3. **Umbrales de 100.000 y 500.000 UVA** de la tasa de intercambio
   (t.o. Transferencias-NC §6.3.1.3). La clasificación del comercio usa la
   recaudación del mes anterior con débito: hay un *running variable* con
   umbrales. Es un RD a nivel comercio que nadie explotó.
4. **A 8162 desde 01/08/2025**: elimina el arancel uniforme por rubro →
   dispersión de precios a nivel comercio.

### Colisión de fechas: hay que declararla antes de que la declare el referee

**Abril-mayo de 2024 es un mes imposible.** Concentra:

- A 7988 (15/04/2024): encaje FCI money market 0% → 10%
- A 7769 + prórrogas: QR de crédito interoperable, efectivo 30/04/2024
- A 7841 + prórrogas: fin del DEBIN recurrente como fondeo, 30/04/2024
- A 7996 (30/04/2024): pull con OAuth2
- A 8000 (15/05/2024): encaje 10% → 15%
- A 8030 y A 8032 (30/05/2024): fin del arancel del pull, reciprocidad de QR

Si un efecto de la escalera de encajes aparece pegado a abril-mayo de 2024, no
se puede atribuir a los encajes. Los dos bloques normativos del paper chocan
literalmente en el mismo mes. Conviene usar el resto de la escalera (oct-2024,
ene-2025, jul-ago-2025) como identificación y tratar abril-2024 como período
contaminado.

### El comparador que hay que citar

**Burga, Céspedes, Parra, Cerón & Quispe (2025), "When Interoperability
Increases Market Power: Evidence from Peru's Instant Payment Systems", BID.**
DiD sobre el mandato peruano de 2023: la concentración de depósitos **sube**
~2%, por un efecto "amenity" que favorece al incumbente. O sea que el signo de
la interoperabilidad sobre la estructura de mercado es **ambiguo a priori**, y
la hipótesis nula relevante ya está escrita. Es el paper contra el que hay que
posicionarse.

Complementarios: Copestake, Kirti, Martinez Peria & Zeng (2025), IMF WP
2025/126, sobre UPI en India; Aurazo, Franco, Frost & McIntosh (2025), BIS
Papers 153, donde Argentina aparece solo descriptivamente.

**No existe evaluación causal publicada de Transferencias 3.0.** Es un hueco
real, no una laguna de búsqueda.

### El canal económico correcto

No es "interoperabilidad → adopción". Es **interoperabilidad → destrucción del
valor del closed-loop de Mercado Pago → reasignación del pasivo**. El QR de MP
dejó de ser un activo excluyente en nov-2021; el fondeo por DEBIN dejó de serlo
en abr-2024. Si la interoperabilidad hizo algo a los depósitos, es por ahí.

---

## 4. Qué queda pendiente

1. **Leer el Apartado 1 del IEF enero-2026** (pág. 48): "FCI de Mercado de
   Dinero y sus depósitos en entidades financieras". Es el documento del BCRA
   más cercano a la tesis del paper y todavía no lo leyó nadie del equipo.
2. **Verificar el Registro de billeteras interoperables**: ¿publica fecha de
   inscripción por entidad? Si sí, es variación firma×tiempo.
3. **Verificar la tasa del 1.3.12 entre sep y nov 2025.** La reconstrucción da
   40% + 5 pp (A 8302, transitorio) + 3,5 pp (A 8306) = **48,5%**, volviendo a
   40% en diciembre. Coherente pero no contrastado contra un t.o. de esa fecha
   (`texord_viejos/v-efemin_25-09-xx.pdf`).
4. **Ojo con la numeración**: la categoría de FCI money market es **1.3.13** en
   los textos ordenados de 2024 y **1.3.12** desde 2025. Comparar t.o. de
   distintas fechas sin corregir esto cruza mal las series.
5. **A 8032**: los plazos son "60 días" y "270 días" desde el 30/05/2024.
   Calculé 29/07/2024 y 24/02/2025 asumiendo días corridos. Verificar si el
   texto dice corridos o hábiles.
6. **Fecha exacta de lanzamiento de Mercado Fondo.** Verificado el año (2018)
   por tres fuentes, sin día ni mes oficial. Buscar el prospecto en CNV.
