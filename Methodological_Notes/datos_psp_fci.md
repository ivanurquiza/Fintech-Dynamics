# PSP, FCI money market y fondeo bancario: qué se observa y qué diseño habilita

_Nota de trabajo. Fintech-Dynamics, julio 2026._

---

## 1. La plomería institucional (esto define el paper)

Un peso que un usuario deja en una billetera puede estar en tres lugares, y los
tres tienen tratamiento regulatorio distinto. No es un detalle contable: es lo
que determina si hay o no desintermediación.

| Dónde está el peso | Norma | Efectivo mínimo | ¿Es fondeo prestable? |
|---|---|---|---|
| Caja de ahorro minorista en un banco | — | ~45% con integración | Sí, barato (tasa ~0) |
| Cuenta de pago del PSP, no invertida | t.o. PSP 4.1.2: 100% depositado a la vista en EEFF del país | **100%** desde 1-ene-2022 (A 7429, punto 1.3.14) | **No.** Esterilizado |
| Invertido en FCI money market | t.o. PSP 4.1.2 (habilitado por A 7495, abr-2022) | 0% → 40% (ver cronología) | Sí, pero caro y crecientemente encajado |

**Cronología del encaje sobre depósitos de FCI money market (punto 1.3.12):**

| Com. "A" | Vigencia | Tasa |
|---|---|---|
| 6992 | 24-abr-2020 | 0% (crea la categoría) |
| 7988 | 15-abr-2024 | 10% |
| 8000 | 15-may-2024 | 15% |
| 8119 | 1-nov-2024 | 20% |
| 8189 | 31-ene-2025 | 20%, **amplía la base** a precancelables desde que la opción es ejercible |
| 8281 | 1-ago-2025 | 30% |
| 8289 | 1-ago-2025 | 40% |
| 8306 | 1-sep-2025 | 43,5% |
| 8355 | 1-dic-2025 | 40% |

La aritmética cierra exactamente contra el t.o. vigente (A 8443), lo que valida
la reconstrucción. Las dos que conviene re-leer en PDF antes de citar son la
8119 y la 8189.

**Consecuencia.** El relato estándar de "las billeteras desintermedian a los
bancos" es falso como descripción de primer orden en Argentina. El peso vuelve
al sistema bancario casi siempre. Lo que cambia es **de quién es el pasivo, a
qué precio, con qué encaje y en qué banco**. El objeto de estudio no es el
nivel del fondeo sino su composición, su costo y su reasignación entre bancos.

Esto explica por qué el DiD de Ignacio da nulos: si la exposición se define
sobre el nivel de depósitos y el nivel no cae, el tratamiento no tiene mordida.
No es falta de poder, es que la variable de resultado está mal elegida.

---

## 2. Qué se puede observar y qué no

### 2.1 Sí se observa, y es público

**a) Float por billetera, diario, a nivel CLASE de cuotaparte.**
API no documentada de CAFCI (`api.cafci.org.ar`). El nivel correcto es la clase,
no el fondo: varias billeteras comparten fondo y se separan por clase (Delta
Pesos: clase X es Personal Pay, clase A es retail). La web muestra patrimonio
solo por fondo; la API lo da por clase. Script: `data/scripts/descargar_cafci.py`.

Limitación seria: las fichas son **foto del día**, no serie. Para panel diario
hay que correr un cron; para reconstruir hacia atrás sirven las carteras
semanales, que traen el patrimonio del fondo en el pie de cada corte.

**b) La matriz fondo × banco, semanal.** Esto es lo importante y es lo que no
teníamos. La composición de cartera de cada FCI detalla plazos fijos,
precancelables y cuentas remuneradas **con el nombre del banco**. Endpoint
`interfaz/semanal/resumen/cartera/{id}`, indexado por un contador secuencial
(no por fecha), con archivo histórico enumerable hacia atrás.

Encadenando (a) y (b) con el mapeo billetera→clase se obtiene, sin ningún dato
supervisorio:

```
billetera  →  FCI (clase)  →  banco
   float        cartera        exposición
```

**c) Nómina de PSP.** El registro del BCRA no publica descarga, pero la tabla
sale de un endpoint público: `bcra.gob.ar/api/endpoints/proveedores-psp.php?tipoPSP=N`,
N = 1..9. Trae código BCRA, CUIT, denominación, domicilio y provincia.
**219 PSPCP** y 202 firmas en los otros ocho tipos (iniciador, aceptador,
agregador, adquirente, red de cajeros, red TEF, cobranza extrabancaria,
administrador QR). Script: `data/scripts/descargar_registro_psp.py`.
El registro es una foto sin historia: hay que guardar el JSON fechado en cada
corrida para reconstruir altas y bajas.

**d) Agregados del BCRA.** El IMPM (`Series-Informe-Mensual-de-Pagos-Minoristas-<mes>-<año>.xlsx`)
publica saldos en cuentas de pago y saldos en FCI vía PSPCP, mensual. Es el
primer estadio agregado natural: permite ver el salto de composición cuenta de
pago → FCI tras la A 7429 (encaje 100%) y la A 7495 (habilitación).
El Boletín Estadístico abre depósitos por "Prestadoras de Servicios Financieros"
(PSF), que mezcla FCI MM y billeteras, pero solo a nivel sistema.

### 2.2 No se observa

**El plan de cuentas del BCRA clasifica por instrumento, no por depositante.**
No hay partida de "depósitos de FCI" ni de "depósitos de PSP" en el balance de
saldos por entidad. La identificación del depositante existe, pero vive en el
régimen informativo de Efectivo Mínimo (partidas 102190 = depósitos a la vista
de FCI MM, 102200 = cuentas de PSPOCP), que no se publica por entidad.

Lo más cerca que llega el dato público es el proxy por instrumento que ya
incorporé a `build_dta.do`:

| Partida | Descripción |
|---|---|
| 311712 | Cuenta corriente con interés |
| 311723 / 311724 | Cta cte especial personas jurídicas, sin / con interés |
| 311736 / 311744 | Plazo con opción de cancelación anticipada, transf. / intransf. |

`dep_mayorista` = 311724 + 311712 + 311736 + 311744. Es el conjunto de
instrumentos que un money market puede tener bajo 1.3.12. **Está contaminado**
(cualquier persona jurídica los usa: empresas, aseguradoras, ART) y además es
incompleto por el otro lado (parte del haber del fondo está en plazo fijo común,
311740, indistinguible de un plazo fijo minorista).

Buena noticia: **el proxy sucio no hace falta para la pata que importa.** La
cartera del FCI da el vínculo fondo→banco directamente. El dato que falta es la
pata PSP→banco (float no invertido), que es chica y está encajada al 100%, o
sea que es económicamente la menos interesante.

**Lo que sí valdría un pedido formal.** El R.I.-PSP (Com. "A" 8284, vigente
1-jul-2025) obliga a los PSPCP a reportar, mensualmente: código 20000dd, saldos
en cuentas a la vista **por entidad financiera, con CBU**; código 40000dd,
saldos invertidos **por fondo, con número de registro CNV y CUIT**. Es decir, el
BCRA tiene el panel PSP × banco × mes y el panel PSP × FCI × mes. Pedido por
Ley 27.275 a subgcia.autorizacion.enof@bcra.gob.ar. También el punto 2.2.2.11
del t.o. PSP exige declarar el o los **bancos patrocinantes** al inscribirse.
No bloquear el proyecto en esto, pero pedirlo ya.

### 2.3 Lo que no existe (para cerrar la discusión)

- **Cantidad de cuotapartistas**: no es pública. Es reporte supervisorio. Y aun
  si lo fuera, los agentes colocadores operan con **cuentas ómnibus**, así que
  ni el registro de la depositaria identifica al inversor final. No hay serie de
  adopción en el margen extensivo por esta vía.
- **Registro de tenencias por inversor**: no existe públicamente.
- **Vínculo clase↔agente colocador en fuente oficial**: no está. Se infiere de
  T&C y reglamentos. El mapeo es a mano, ~14 billeteras, y **rota** (Lemon pasó
  de Fima Premium a Vinci Compass Liquidez). Esa rotación es a la vez una
  amenaza de error de medición y una fuente de variación explotable.
- **Los T&C no nombran el banco.** Revisé ocho: ninguno. La norma exige el
  disclaimer ("no son depósitos en una entidad financiera"), no identificar al
  custodio.

---

## 3. Qué muestran los balances que ya tenemos

Extraje las partidas nuevas de `baldet` para los 100 meses disponibles
(2018m1–2026m4). Dos hechos:

**El fondeo mayorista remunerado pasó de marginal a sistémico.**
Como porcentaje de los depósitos del SPNF en pesos: 1,6% en 2018m1, 9,7% en
2021m1, **28,5% en 2024m1**, 11,5% en 2026m4. El pico y la reversión coinciden
con el ciclo de tasas y con la escalera de encajes de 2024–2025, no con la
adopción de billeteras — advertencia importante para no confundir mecanismos.

**La dispersión cross-section es enorme y no es ruido.** Exposición promedio
2021 (pre-boom), como % de depósitos SPNF, entre los 37 bancos de mayor escala:
media 15,9%, sd 21,6, p90 41,1.

| Banco | Exposición pre-2021 |
|---|---|
| Mariva | 86,9% |
| Banco de Valores | 79,2% |
| Banco Industrial (BIND) | 51,6% |
| Comafi | 46,5% |
| BMA | 37,5% |
| Hipotecario | 33,1% |
| Supervielle | 31,3% |
| ... | |
| San Juan, Chubut, Formosa, TdF, Municipal de Rosario | 0,0% |

Los de arriba son exactamente los bancos ligados a la industria de fondos:
Valores es depositaria de Delta, SBS y Southern Trust; BIND es la depositaria de
Mercado Fondo; Comafi la de Cocos. Los de abajo son bancos provinciales de
depósito minorista puro. **Eso es una discontinuidad de modelo de negocio, no
una variable continua de exposición** — y por lo tanto no es exógena. Cualquier
diseño que use esta exposición como tratamiento está comparando bancos
mayoristas contra bancos minoristas, no billeteras contra no-billeteras.

Por terciles de exposición pre-2021, el ratio evoluciona así:

| | 2021-06 | 2024-03 | 2025-06 | 2026-04 |
|---|---|---|---|---|
| tercil bajo | 0,2 | 6,5 | 6,2 | 9,9 |
| tercil medio | 9,0 | 20,0 | 7,0 | 7,0 |
| tercil alto | 25,6 | 43,5 | 43,7 | 24,1 |

Hay convergencia parcial del tercil bajo (los minoristas empiezan a tomar
fondeo mayorista) y reversión del alto después de 2025. Es un hecho estilizado
publicable por sí mismo, pero no identifica nada todavía.

---

## 4. Qué diseño habilita esto, y cuál no

### 4.1 El mecanismo que propongo

Las billeteras no destruyen depósitos: **convierten depósitos minoristas
inelásticos en fondeo mayorista elástico, sin que el depositante haga nada.** El
barrido automático a money market es una tecnología que sube la beta de depósito
del sistema. Es Xiao (2020, QJE) — flujo de bancos a shadow banks cuando suben
las tasas — pero con la fricción de atención eliminada por software, y en un
país donde la tasa real relevante cambia de mes a mes.

Predicciones que se siguen y son testeables con lo que hay:

1. La beta de depósito de un banco sube con su exposición a fondeo canalizado
   por billeteras.
2. El fondeo se vuelve más volátil (rotación semanal en la cartera del FCI).
3. Reasignación: el banco que pierde depósito minorista **no** es el que gana
   fondeo del fondo. Neto agregado ≈ 0, composición muy distinta.
4. Si los bancos que ganan fondeo mayorista no son los que tienen la relación
   con PyMEs, la reasignación reduce crédito relacional aunque el agregado de
   fondeo no caiga. Esa es la consecuencia de bienestar.

El punto 3 es el que hace publicable el nulo de Ignacio: el nulo agregado es el
resultado, no el fracaso.

### 4.2 Diseños, en orden de defendibilidad

**(A) Khwaja-Mian sobre la red fondo–banco. Es el mejor y lo habilita la cartera semanal.**
Unidad: fondo f × banco b × período t. Δ(fondeo de f a b) sobre el shock del
fondo f, con **efectos fijos banco × t**. Los FE de banco×t absorben toda la
demanda de fondeo del banco; lo que queda identificado es la oferta del fondo.
Segunda etapa: agregar el shock estimado a nivel banco y llevarlo al crédito.
Es literalmente Khwaja-Mian con fondos en lugar de bancos y bancos en lugar de
empresas. Requiere que un banco se fondee con varios fondos — hay que chequearlo
en la cartera, pero con ~20 money markets grandes y ~60 bancos debería sobrar.

**(B) DiD con tratamiento continuo sobre los cambios de encaje (1.3.12).**
Ocho cambios entre 2024 y 2025, comunes a todos los bancos en la tasa pero
diferenciales en la incidencia vía composición del pasivo. Problema serio: los
encajes son endógenos a la política monetaria del momento, y el momento coincide
con el programa de estabilización. Sirve como evidencia de mecanismo, no como
identificación principal.

**(C) Shift-share (SSIV) sobre la red fondo–banco. Lo pondría como robustez, no como diseño principal.**
Y esto va en contra de lo que veníamos planeando, así que lo justifico. Borusyak
et al. (2025) requieren, para la ruta de shocks exógenos, **muchos shocks con
concentración limitada**. Acá los shocks serían el crecimiento del float por
fondo, y hay ~15-20 money markets relevantes con Mercado Fondo dominando el
patrimonio. El número efectivo de shocks (1/HHI) queda en el orden de 5 o 6. Con
eso la inferencia SSIV no se sostiene, por más que la fórmula se pueda calcular.
La ruta alternativa —shares exógenos— es peor todavía: los shares son la
decisión de cartera del fondo, o sea exactamente la variable endógena.
Un shift-share **geográfico** (el plan original: shares provinciales del banco ×
crecimiento provincial de adopción) sí tiene muchos shocks (24 provincias, y se
puede bajar a localidad con `Suc_loc`), pero identifica **otro mecanismo**: la
pérdida de depósito minorista en la sucursal, no la recomposición del fondeo
mayorista, que es nacional y no tiene nada que ver con dónde vive el usuario.

**La lectura que me parece correcta: son dos canales distintos y el paper los
necesita a los dos.** Geografía identifica la salida del depósito minorista;
la red de fondos identifica la vuelta como fondeo mayorista. Mostrar que se
compensan, y que la compensación ocurre entre bancos distintos, es el aporte.

### 4.3 Amenazas que hay que resolver antes de escribir

1. **El crecimiento de los money market es casi todo tasa e inflación, no
   billeteras.** Hay que separar. El mejor test disponible: comparar clases
   dentro del mismo fondo — la clase de la billetera contra la clase
   institucional o retail — que comparten cartera, gerente y tasa. Si la clase
   billetera crece distinto, es adopción y no rendimiento. Es un control
   fondo×tiempo perfecto y está disponible en el dato.
2. **La exposición pre no es exógena** (§3): son bancos mayoristas por modelo de
   negocio. El diseño (A) lo resuelve con FE banco×t; el (B) y el (C) no.
3. **El canal de crédito puede estar mudo por razones ajenas.** En 2020-2023 los
   bancos argentinos tenían el activo dominado por instrumentos del BCRA; el
   margen de ajuste ante un shock de fondeo pudo ser LELIQ/pases, no préstamos.
   Hay que testear el margen de ajuste antes de asumir que el crédito responde.
4. **Ualá y Naranja X internalizan el float** en licencia propia (ent 384 y
   Naranja Digital CF). Aparecen directamente en el panel de balances, no en
   CAFCI. Es un contraste útil, y a la vez un problema de selección: la elección
   de licencia está correlacionada con el tamaño y la estrategia.
5. **Sesgo de supervivencia en CAFCI**: la API se consulta con `estado=1`
   (activos). Los fondos liquidados no aparecen. Guardar el maestro fechado.
6. **El matching de bancos en la cartera es por texto libre** (`nombreActivo`,
   sin ISIN, del tipo "Cta Cte U$S Bco Valores"). Hay que auditar a mano los no
   matcheados antes de usar las participaciones como pesos.

---

## 5. Literatura donde enchufa

El canal money-market → banco tiene literatura hecha y es donde hay que
posicionarse, más que en "fintech y bancos" genérico:

- **Xiao (2020, QJE)**, transmisión monetaria vía shadow banks: depósitos
  minoristas inelásticos vs. money market elásticos. Es el marco.
- **Chernenko & Sunderam (2014, RFS)** y **Ivashina, Scharfstein & Stein (2015,
  QJE)**: MMF como fondeo mayorista de bancos y qué pasa cuando se corta.
- **Kacperczyk & Schnabl**: toma de riesgo de los money market.
- **Drechsler, Savov & Schnabl (2017, QJE)**: deposits channel y poder de
  mercado en depósitos — el mecanismo que las billeteras erosionan.
- **Khwaja & Mian (2008)**: el diseño.
- **Borusyak, Hull & Jaravel (2025)**: por qué acá el SSIV no es la primera
  opción (número efectivo de shocks).

El aporte propio: en Argentina el barrido a money market es **automático y por
default**, no una decisión del depositante. Eso convierte lo que en EE.UU. es un
margen de sofisticación del inversor en un cambio tecnológico del sistema de
pagos. Y el dato de cartera semanal por banco permite ver la red completa, que
en EE.UU. requiere el Form N-MFP.

---

## 6. Próximos pasos concretos

1. Correr `descargar_registro_psp.py` y `descargar_cafci.py maestro`.
2. `descargar_cafci.py sondear` para ubicar el `interfazId` de hoy, y bajar
   carteras hacia atrás. Verificar hasta qué fecha llega el archivo.
3. Poner `descargar_cafci.py fichas` en un cron diario desde ya: cada día que
   pasa sin correrlo es un día de panel que no se recupera.
4. Completar `psp_fci_map.csv` (los "a verificar") leyendo T&C y reglamentos.
5. Correr `build_dta.do` con las partidas nuevas.
6. Pedido Ley 27.275 al BCRA por: R.I.-PSP códigos 20000dd y 40000dd, y bancos
   patrocinantes declarados (t.o. PSP 2.2.2.11). Es el dato que nadie tiene.
