# Diseño candidato: shocks bancarios, sustitución fintech y alternativas locales

Fecha: 2026-09-20. Continúa `debate_paper_2026-09-20.md`. Propuesta de investigación, no identificación validada ni resultado causal. La elección de pregunta sigue abierta.

## Recomendación

Pregunta principal: **¿pueden las fintech sostener el financiamiento de un deudor cuando su banco restringe crédito, especialmente donde escasean otros bancos?**

Separar tres objetos: (1) shock de oferta del banco, (2) reemplazo por otras fuentes, (3) efecto neto sobre saldo total y continuidad de relaciones. La transmisión de tasas puede ser el origen del primer objeto; la sustitución es la respuesta al primero. No se necesitan balances fintech para observar esa respuesta en CENDEU. Sí se necesitan para atribuirla específicamente a su fondeo, por lo que este último mecanismo no está identificado hoy.

La contribución candidata es la dependencia de relaciones bancarias y de alternativas territoriales. No afirmar que la transmisión monetaria fintech es una pregunta nueva: existe, entre otros, el trabajo de Lavinia Franco alojado por el ECB. Originalidad de las variaciones propuestas aquí significa una pista para nuestro proyecto, no una primicia demostrada en toda la literatura.

## Qué se comprobó directamente en la base

La auditoría reproducible está en `Code/analysis/audit_identificacion_2026-09-20.ipynb`. No exporta identificadores de deudores ni modifica las fuentes. Además se leyeron esquemas, código de construcción y notas regulatorias existentes.

- `balances_bancos.dta`: 7.681 observaciones, 328 columnas, 84 entidades, enero 2018–abril 2026; clave entidad×mes sin duplicados. Corresponde a entidades financieras reguladas; **no ofrece balances del conjunto de PNFC fintech**. En mayo 2025 también aparecen Brubank y Ualá Bank, y las compañías financieras Naranja Digital y Reba. Su presencia permite comparaciones exploratorias entre tecnología y régimen regulatorio, no una asignación exógena a esas categorías.
- Hay depósitos por categorías, préstamos, patrimonio, títulos y liquidez. `titulos` agrega instrumentos públicos y privados: no es LEFI. `efectivo` tampoco equivale sin ajustes a liquidez libre. `dep_fci_proxy` no identifica exclusivamente fondos comunes.
- `caracteristicas_bancos.dta` tiene indicadores adicionales, incluidos códigos `800010500010`, `800010500080` y `800010500090`. Las descripciones cambian; el último incorpora referencias a LELIQ/PASES/LEFI según período. Verificar definición, denominador y moneda antes de usar una diferencia entre indicadores como exposición a un activo.
- `prestamos_depositos_prov.dta`: banco×provincia, montos en cierres trimestrales y sucursales mensuales. `pda_lender_depto.dta`: puntos de acceso por entidad y departamento, 2019–2025. Validar correspondencia entre nombres/códigos y geografía de CENDEU antes de construir mercados finos.
- CENDEU: 24 meses, agosto 2024–julio 2026. Historia con identificadores, saldo, situación y campos derivados; no producto, precio, plazo ni originación. La residencia/actividad proviene de un padrón de corte, no de una historia de ubicación verificada. El panel de firmas no aporta por sí mismo empleo, ventas ni inversión.

Cruce preliminar en **mayo de 2025**, con saldo positivo y fintech definida estrictamente como `pnfc_fintech`:

| Población | Deudores | Con al menos dos bancos | Con banco y PNFC fintech |
|---|---:|---:|---:|
| Personas jurídicas (`firm`) | 254.195 | 74.958 | 3.951 |
| Personas, muestra existente `person_lender_5pct` | 970.955 | 168.005 | 148.506 |

Esto favorece investigar oferta bancaria con firmas multibanco y sustitución con personas. Es factibilidad, no representatividad certificada ni evidencia de sustitución. La taxonomía debe auditarse: nueve compañías financieras con códigos 440xx figuran como `fideicomiso`; Crédito Regional CF figura como `pnfc_otro`. Para este conteo se usó `es_banco` del panel regulado y una definición fintech acotada, aún provisional. No se alteró el crosswalk.

## Ruta A: construir shocks desde la red de préstamos

Inspiración: Gutiérrez, Jaume y Tobal, *Do Credit Supply Shocks Affect Employment in Middle-Income Countries?*, AEJ Policy (2023). El trabajo separa efectos banco y mercado en crecimiento del crédito y pondera shocks bancarios con exposiciones previas. Nuestra ventaja potencial es observar deudor×acreedor; nuestra desventaja es observar stocks y una ventana corta, no préstamos nuevos.

1. Comparar cambios de saldo de distintos bancos **al mismo deudor en el mismo mes**. Especificación orientativa:

   `g(i,b,t) = efecto(i,t) + efecto(i,b) + gamma(b,t) + error(i,b,t)`.

   La transformación del saldo debe admitir ceros/entradas/salidas: comparar crecimiento simétrico, variaciones escaladas por saldo total previo y margen intensivo. Deflactar y separar amortización/mora hasta donde se observe. No llamar al cambio de stock “nuevo crédito”.

2. Recuperar correctamente `gamma(b,t)` con normalización explícita y verificar conectividad. Es un shock **relativo** de oferta bajo el supuesto de demanda común del deudor entre bancos, no una sorpresa monetaria exógena. Productos/plazos no observados, reasignación de demanda y selección de relaciones pueden violarlo. No restringir a relaciones sobrevivientes sin examinar sesgo.

3. Usar participaciones de crédito fijadas antes de la variación: `Z(i,t) = suma_b s(i,b,0) * gamma(b,t)`. Reestimar shocks sin el propio deudor y, cuando sea viable, sin su mercado receptor. No actualizar los pesos con la respuesta al shock. Mantener una escala/normalización comparable entre particiones y controlar cambios en la red conectada.

4. Variante útil: estimar shocks en firmas multibanco y evaluar personas en una muestra separada. Evita reutilizar mecánicamente el saldo de la persona para construir su tratamiento. **No elimina shocks comunes ni garantiza que un banco ajuste igual crédito empresario y personal**; exige primer estadio en relaciones bancarias de la población receptora. Validar también shocks estimados dentro de personas con particiones independientes.

5. Para saldos totales del deudor ya no pueden incluirse efectos deudor×mes: absorberían el tratamiento y el resultado. Usar efectos deudor, mercado×mes y actividad/riesgo previo×mes cuando el soporte lo permita; evaluar tendencias previas y shocks directos correlacionados con el banco elegido.

Que `Z` tenga forma Bartik no lo vuelve exógeno. Debe justificarse independencia condicional de shocks o de participaciones, según el argumento elegido. Omitir al propio deudor elimina retroalimentación mecánica, no toda demanda correlacionada. Pocos bancos/grupos económicos implican pocos shocks efectivos: inferencia a ese nivel y métodos adecuados para exposiciones compartidas; reestimar el shock generado en el procedimiento de incertidumbre.

### Problema concreto del código existente

En `cendeu_summ_stats.ipynb`, la celda que produce `shock_cendeu` sustrae sucesivamente medias por código postal y banco para obtener residuos, y luego calcula `(dlog - residuo).groupby(ent).mean()`. Esto promedia **todo el valor ajustado**, que incluye el efecto del mercado atendido. No recupera por sí solo el coeficiente del banco. Puede confundir oferta con composición de mercados. Reestimar efectos y conectividad antes de interpretar el archivo como shock. También comprobar consecutividad temporal, escalas de stocks y referencias a nombres de depósitos. No se corrigió ni ejecutó una nueva estimación de ese shock en esta tarea.

## Ruta B: presión de encajes predicha por cartera previa

Construir, por banco y fecha, el cambio de exigencia que habría ocurrido **manteniendo fijos depósitos, plazos y composición previos**:

`E(b,t) = suma_k [depositos(b,k,0) / activos(b,0)] * cambio_regulatorio_efectivo(k,grupo_b,t)`.

La lógica económica es que un cambio regulatorio inmoviliza distinta liquidez según la composición previa del fondeo. Primero verificar respuesta de liquidez disponible, costo implícito de fondeo y crédito al mismo deudor. Luego asignar exposición a clientes según bancos previos.

Esta ruta permite un panel de cambios sucesivos; no obliga a un evento único. Pero requiere reconstruir categorías, grupo de entidad, plazo residual, integración admitida en bonos, deducciones y vigencias. La tabla regulatoria existente solo cubre categorías FCI y PSP, como reconoce `Regulation/alicuotas_TODO_v1.md`; no alcanza todavía para esta fórmula. La reforma de agosto 2025 incluyó además integración diaria: no representarla solo con una alícuota mensual.

Riesgos: composición de depósitos vinculada a clientela, política que responde a condiciones bancarias, otras reformas contemporáneas y efectos sobre depósitos/consumo del propio cliente. Efectos comunes por mes no eliminan efectos diferenciales de esos canales. Examinar exposiciones previas alternativas, primer estadio, pretrayectorias y resultados placebo.

Interpretación posible: efecto de una restricción regulatoria de liquidez sobre crédito y sustitución. **No usar encajes como IV de una tasa y afirmar una elasticidad pura a tasas:** los encajes pueden afectar cantidades directamente.

## Ruta C: retiro del seguro de liquidez sobre bonos — candidata más distintiva

El 10 de junio de 2025 se rescindió el saldo restante de opciones de liquidez del BCRA sobre títulos públicos. La cancelación mayoritaria de julio 2024 cae antes de nuestra ventana CENDEU, pero el saldo remanente de 2025 cae dentro.

Hipótesis: perder la opción de convertir ciertos bonos en liquidez puede modificar la precaución de un banco frente a retiros y su disposición a prestar, incluso sin observarse una salida contemporánea de depósitos. Construir exposición previa como **valor de títulos cubiertos por opciones vigentes / activos**, con tipo y vencimiento de opciones, y estudiar su cambio institucional. No confundir valor contable de la prima con monto de bonos protegido; no sustituirlo por títulos totales. La dirección debe comprobarse: compensación, otras facilidades y reasignación de cartera pueden neutralizarla o revertirla.

Ya existe una pista pública comprobada para recolectar el dato: los estados de Bancor a junio 2025 revelan puts al cierre 2024 y partidas fuera de balance; BST declara haber rescindido todos en julio 2024. Los anexos de títulos también pueden identificar LEFI por especie. Estos dos ejemplos muestran que hay información y diferencias entre bancos, **no** que exista aún un panel homogéneo ni un experimento válido.

Obstáculos principales: la tenencia remanente fue elegida; la rescisión fue acordada; hubo cambios regulatorios ligados a la tenencia soberana y reformas monetarias próximas. Comparar bancos con exposición soberana, duración, capital, liquidez y clientela similares; medir cobertura al menos antes del anuncio; reconstruir por separado exposición a LEFI y encajes. Si la exposición solo distingue unos pocos bancos públicos, no sostendría una interpretación causal amplia. Comprobar anticipación y soporte. La prueba de pretrayectorias ayuda pero no demuestra exogeneidad.

Una extensión, solo si aparecen contratos suficientes, sería explotar vencimientos de cobertura fijados previamente y una regla verificable de elegibilidad/rescisión. **No se encontró todavía una regla que justifique una discontinuidad o lotería**, por lo que no proponer un RD nominalmente original sin ese dato.

## Estructura empírica y mecanismo que distinguir

1. **Oferta:** banco expuesto ajusta crédito para deudores comparables; balances muestran si hubo presión de liquidez, fondeo o cartera. Usar regulados digitales como contraste de mecanismo cuando la muestra lo permita, sin equiparar licencia con tecnología.
2. **Reemplazo:** para clientes previos, medir por separado saldo con bancos expuestos, con otros bancos y con PNFC fintech. Medir cantidades reales y relación nueva/continuada. No basta una participación fintech mayor por caída del denominador.
3. **Continuidad:** saldo total, conservación de alguna relación y situación posterior. Medir respuesta fintech y bancaria en la misma escala —por ejemplo, variación sobre deuda inicial— para cuantificar compensación. Si se usa cociente de formas reducidas, reportar incertidumbre y no confundirlo con sustitución estructural universal.
4. **Fracción geográfica:** sucursales previas de **otros bancos** y diversidad de alternativas, distinguiendo al incumbente. Controlar shocks locales. Si fintech reemplaza más donde faltan otras entidades, es evidencia coherente con costos de acceso/switching; no prueba sola el mecanismo digital. Una sucursal contemporánea puede ser respuesta al mismo shock.
5. **Relación fintech previa:** permite probar si una relación ya establecida facilita ajuste rápido. Su interacción con el shock identifica heterogeneidad bajo supuestos, no el efecto causal de adoptar fintech. Para ese último objeto haría falta otra fuente de asignación a acceso/eligibilidad.

Una fintech puede sustituir, complementar o amplificar la restricción si depende del mismo fondeo bancario. Mantener esos resultados abiertos. Mayor deuda no equivale a mayor bienestar; faltan precio, plazo y uso. Hablar primero de continuidad de financiamiento formal reportado, no de inclusión neta de toda la población.

## Orden de trabajo y criterios para abandonar una ruta

Primero corregir taxonomía, comprobar red multibanco y rehacer shocks. En paralelo de investigación —sin asumir una estimación ya implementada— inventariar puts en estados previos de varios bancos y completar reglas de encajes. Elegir un anclaje institucional si ofrece cobertura y una justificación defendible; no acumular instrumentos débiles para obtener significancia. Si el ajuste bancario no predice crédito de la población objetivo, descartar la extrapolación firmas→personas. Si la aparente respuesta fintech desaparece al medir montos absolutos, no vender sustitución.

Las tasas pueden explicar cuándo se manifiesta la vulnerabilidad bancaria, pero para llamar al paper transmisión causal de política monetaria necesitamos aislar innovaciones de política frente a inflación, expectativas y demanda. Hasta entonces, el título honesto es shocks de oferta bancaria y sustitución fintech.

## Fuentes consultadas

- Archivos y notebook mencionados; `Data/README_data.md`; `Regulation/alicuotas_TODO_v1.md`.
- Gutiérrez, Jaume y Tobal (2023), [AEA](https://www.aeaweb.org/articles?id=10.1257/pol.20210354); copia local `Literature/Credit_Supply_Shocks(Martin).pdf`, sección de construcción de shocks.
- [BCRA, cancelación de puts, 10-06-2025](https://www.bcra.gob.ar/noticias/el-bcra-y-las-entidades-financieras-acuerdan-la-rescision-del-saldo-pendiente-en-contratos-por-opciones-de-liquidez/).
- [BCRA, medidas monetarias, 09-06-2025](https://www.bcra.gob.ar/noticias/el-bcra-anuncia-medidas-para-el-fortalecimiento-de-las-reservas-internacionales-y-la-consolidacion-del-control-de-los-agregados-monetarios/).
- [BCRA, Informe Monetario, agosto 2025](https://www.bcra.gob.ar/publicaciones/informe-de-monetario-mensual-agosto-de-2025/).
- [Bancor, estados al 30-06-2025](https://www.bancor.com.ar/downloads/institucional/eeff-30-06-2025.pdf), notas sobre derivados y partidas fuera de balance; anexo de títulos.
- [BST, estados al 31-03-2025](https://www.bst.com.ar/wp-content/uploads/2025/06/EEFF-BST-032025-1.pdf), nota 12.
- [Franco, The fintech lending channel of monetary policy](https://www.ecb.europa.eu/press/conferences/shared/pdf/20241007_monpolconf/Franco_paper.pdf).
