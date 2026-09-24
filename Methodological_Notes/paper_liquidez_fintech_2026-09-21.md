# Liquidez bancaria y límites de la sustitución fintech

21 de septiembre de 2026. Investigación y propuesta de paper a partir de `idea_lefi.md`, las notas anteriores, normativa y publicaciones del BCRA, y literatura. No contiene nuevas estimaciones ni certifica una identificación. No modifica la nota del otro agente.

## 1. Propuesta principal

**Pregunta:** ¿cuándo una alternativa digital permite al deudor escapar de una restricción bancaria, y cuándo comparte la misma restricción a través de su fondeo?

Las LEFI pueden ser el laboratorio institucional de esta pregunta. La contribución candidata combina dos límites a la sustitución: conseguir otro acreedor y que ese acreedor consiga fondos. La tecnología digital podría reducir el primer límite sin eliminar el segundo. Esto permite integrar balances, CENDEU, relaciones de crédito, sucursales y eventualmente fondeo de no bancos. No requiere que el signo de la respuesta fintech sea positivo.

Una versión más acotada y factible es cuantificar sustitución y continuidad de financiamiento ante shocks bancarios, usando la reforma de 2025 para estudiar el mecanismo de liquidez. La versión más ambiciosa agrega cadenas banco→PNFC→deudor. Si no observamos estas cadenas con cobertura razonable, no prometer ese mecanismo como resultado principal. La prioridad de cobro queda como extensión sobre desempeño posterior, no como condición para que el paper exista.

## 2. Qué cambia la investigación sobre LEFI

### Mecánica y correcciones a la nota

La Comunicación A 8060, del 11/07/2024, habilitó desde el 22/07/2024 la operatoria de LEFI y suspendió nuevos pases pasivos en la rueda BCRA. Las compras y ventas se liquidaban a **valor técnico**. La venta estaba limitada al saldo disponible de cada entidad y tenía horarios de liquidación. Por eso no corresponde describirla como una facilidad simétrica que permite prestar y tomar prestado ilimitadamente a la misma tasa. Tampoco “siempre al mismo precio” equivale a valor técnico, que incorpora la capitalización.

Fuente: [A 8060](https://www.bcra.gob.ar/archivos/Pdfs/comytexord/A8060.pdf).

El banco podía recuperar caja vendiendo un activo propio; no estaba recibiendo un crédito nuevo del Central por encima de esa tenencia. Su desaparición cambia remuneración, instrumentos y posibilidades de administración de caja; no destruye mecánicamente el patrimonio ni la liquidez agregada por el valor de todas las LEFI.

### Secuencia que importa

| Fase | Hecho verificado | Consecuencia para el diseño |
|---|---|---|
| 9 de junio de 2025 | Anuncio del cierre de la oferta desde el 10 de julio, junto con otras medidas | Fijar exposición antes del anuncio; junio puede contener anticipación |
| 10–17 de julio | Cese de operatoria/oferta, canje del stock en poder del BCRA por títulos negociables y vencimiento | Distinguir cartera del BCRA de cartera de bancos; no asumir canje obligatorio idéntico para cada banco |
| Julio | El BCRA describe excesos iniciales de liquidez y operaciones de mercado para acompañar la transición | La salida no fue una contracción uniforme de liquidez desde el primer día |
| Agosto | Cambios de encajes, integración diaria y otras intervenciones | El ajuste posterior no se atribuye exclusivamente a LEFI |
| Últimos meses de 2025 | Desarrollo de mercados y cambios en incertidumbre electoral | La normalización posterior no es un placebo limpio ni una reversión experimental |

Fuentes: [anuncio del 9 de junio](https://www.bcra.gob.ar/noticias/el-bcra-anuncia-medidas-para-el-fortalecimiento-de-las-reservas-internacionales-y-la-consolidacion-del-control-de-los-agregados-monetarios/), [Informe Monetario de julio](https://www.bcra.gob.ar/publicaciones/informe-monetario-mensual-julio-de-2025/), [Informe Monetario de agosto](https://www.bcra.gob.ar/publicaciones/informe-de-monetario-mensual-agosto-de-2025/).

El IPOM de diciembre describe mercados de liquidez fragmentados, relaciones bilaterales estables en call y diferencias de acceso entre ruedas. También atribuye gran parte del estrés a incertidumbre política y electoral. Es la interpretación del BCRA, no una identificación causal independiente; hay que confrontarla con la hipótesis de implementación monetaria, no citar solo los pasajes favorables. Ver recuadro III.2.2 y sección III.3 del [IPOM de diciembre 2025](https://www.bcra.gob.ar/archivos/Pdfs/PublicacionesEstadisticas/informes/informe-politica-monetaria-2025-T4.pdf).

### Dos fuerzas de signo opuesto

- Al perder una colocación líquida remunerada, un banco puede buscar rentabilidad prestando más.
- Si financiar faltantes se vuelve más incierto o caro y el mercado redistribuye mal la caja, puede mantener buffers mayores o restringir crédito.

Mucho saldo LEFI previo puede indicar tanto uso de la facilidad como abundancia de liquidez. **El stock de fin de mes no mide por sí solo dependencia ni intensidad de uso diario.** La pregunta interesante es qué condiciones determinan el predominio de cada fuerza. Por eso propondría medir aparte stock LEFI, estabilidad del fondeo y acceso a alternativas de liquidez; no sumarlos automáticamente en un índice.

La distinción entre nivel, volatilidad y dispersión de tasas también importa. Con un episodio y 24 meses no atribuiría efectos causales separados a la media y la varianza mediante dos regresores muy correlacionados. La serie diaria sirve para mostrar fases, spreads comparables, volumen y funcionamiento del mercado; no convierte el saldo mensual de crédito en dato diario.

## 3. Benchmark de literatura

**Bianchi–Bigio:** la versión local es un manuscrito de marzo de 2021, anterior a la publicación en Econometrica de 2022. Se leyeron introducción y mecanismo de gestión de liquidez, y pasajes sobre operaciones de mercado. Fundamenta el trade-off entre préstamos rentables e ilíquidos y cobertura de retiros en un mercado interbancario con fricciones. No demuestra que retirar LEFI aumente necesariamente el costo marginal de todos los bancos, ni es un modelo literal de Argentina. Archivo: `Literature/bianchi-bigio2022.pdf`.

**Greenstone–Mas–Nguyen:** se leyeron introducción y sección III de la versión publicada. Estiman componentes banco y mercado del crecimiento de originaciones y construyen exposición con participaciones previas. Justifican el diseño con supuestos, controles y comprobaciones de asignación; no afirman que el efecto fijo sea exógeno por definición. Sus efectos son relativos, y el resultado sobre crédito no implica automáticamente un efecto real. Archivo: `Literature/greenstone2020.pdf`.

**Antecedente especialmente cercano que debe incorporarse:** Cucic y Gorea, *Nonbank Lending and the Transmission of Monetary Policy*, RFS 39(4), 966–1014, 2026, publicado online en noviembre de 2025. Ya examina sustitución banco/no banco en hogares y firmas, fondeo y efectos reales. Se revisaron el registro editorial y las secciones de identificación/fondeo del working paper disponible: aprovecha el vínculo cambiario danés con el euro y shocks monetarios externos. Esa fuente de variación no se traslada automáticamente a Argentina.

Fuentes: [artículo RFS](https://academic.oup.com/rfs/article/39/4/966/8320039), [working paper de Nationalbanken](https://www.nationalbanken.dk/media/2spduuhc/nonbank-lending-and-the-transmission-of-monetary-policy.pdf).

Gopal–Schnabl ya estudia reemplazo bancario por financieras y fintech en pequeños negocios. La red de fondeo tampoco es un territorio vacío: Krainer–Vaghefi–Wang estudian banca hacia no bancos en crédito sindicado, y encuentran que estos vínculos pueden sostener crédito. Esto hace importante distinguir un shock de liquidez de uno de capital y mantener ambos signos posibles. Revisadas las descripciones y resúmenes disponibles, no todos sus apéndices: [Gopal–Schnabl](https://pages.stern.nyu.edu/~pschnabl/research/GS_Aug2021.pdf), [Krainer–Vaghefi–Wang](https://www.dallasfed.org/-/media/documents/research/events/2025/25cemla/25cemla_wang_paper.pdf).

El benchmark top field exige un objeto económico que aprendamos, un mecanismo respaldado y una afirmación causal proporcional al diseño. “Argentina + fintech + suba de tasas” no alcanza como contribución. Una oportunidad es medir cómo interactúan acceso minorista digital, dependencia de fondeo bancario y capacidad de sustitución del mismo deudor durante una transición de gestión de liquidez. La originalidad de esa combinación aún debe investigarse, no declararse resuelta.

## 4. Cómo se vería el paper

### Acto 1: el sistema tiene liquidez, pero distribuirla puede ser costoso

Figura de apertura con stock LEFI, reservas, tasas diarias y volumen por mercado. Distinguir TNA/TEA, operaciones garantizadas/no garantizadas, plazo y tasa promedio ponderada de máximos intradiarios. Marcar anuncio, cierre, intervenciones y encajes. Construir después la heterogeneidad bancaria: fondeo, posición interfinanciera, liquidez libre y costo efectivo. No inferir destrucción de liquidez de un ratio cuya definición cambia.

El Informe sobre Bancos de julio advierte cambios en los componentes del ratio amplio de liquidez, y que la reexpresión del crédito en moneda extranjera influyó en el crecimiento del crédito total. Ver [informe](https://www.bcra.gob.ar/publicaciones/informe-sobre-bancos-julio-de-2025/). Esto es relevante para no confundir cambios contables con oferta.

### Acto 2: transmisión a relaciones bancarias

Comparar acreedores bancarios del mismo deudor en el mismo mes. Empezar con cohortes y evolución de saldos reales, entradas, salidas y situación. Después estimar un modelo con efectos deudor×mes, relación y componentes banco×mes. No condicionar la muestra principal a que el crédito efectivamente haya caído ni a supervivencia posterior.

Firmas multibanco ayudan a estimar oferta, pero no son necesariamente la mejor muestra para fintech. La extrapolación a personas requiere validación en relaciones bancarias de personas. El shock estimado de firmas puede estar contaminado por exposición cambiaria: CENDEU no separa moneda/producto, mientras balances sí separan parte del crédito en moneda extranjera. Deflactar pesos con IPC no elimina revaluación cambiaria. Evaluar bancos y segmentos con poca exposición cambiaria y controlar exposición previa×tipo de cambio, sin vender esa corrección agregada como exacta a nivel préstamo.

### Acto 3: alternativas y compensación

Asignar a cada deudor su exposición por relaciones y pesos fijados antes del shock. Mostrar cuatro respuestas en la misma escala: crédito de bancos afectados, de otros bancos, de fintech/no bancos, y total. Desagregar PNFC fintech de bancos digitales y otros PNFC; medir cantidades absolutas y nuevas relaciones reportadas, no solamente participaciones. Usar crédito total previo como denominador común cuando corresponda y admitir ceros.

Las sucursales de otros bancos miden alternativas de distribución. La relación fintech previa mide una relación de crédito, no uso de billetera ni adopción exógena. La geografía entra después de establecer sustitución; no hace falta que sea la fuente principal de identificación.

### Acto 4 opcional: ¿cuán independiente es la alternativa?

**Cruce nuevo para intentar:** registro de prestamistas (código acreedor↔CUIT legal) → mismo CUIT como deudor en `firm` → cartera que ese prestamista ofrece a personas en CENDEU.

El código `cendeu_reshape.py` define `firm` por prefijos de CUIT 30/33/34 y no aplica en esa selección una exclusión explícita por actividad financiera. El [registro de PNFC del BCRA](https://www.bcra.gob.ar/proveedores-no-financieros/) publica código y CUIT. Por tanto, hay una vía técnicamente plausible de buscar vínculos banco→PNFC con datos del proyecto, **pero no se ejecutó el cruce ni se verificó su cobertura**.

No usar automáticamente el CUIT del PSP: puede ser distinto del prestamista. Un CUIT empresarial multiproducto no permite atribuir toda su deuda a crédito fintech. Cambios societarios, fideicomisos y entidades de un mismo grupo deben fecharse. La ausencia en CENDEU no prueba ausencia de fondeo bancario: pueden existir líneas no dispuestas, deuda exterior, vehículos o préstamos a una matriz. El saldo bancario observado tampoco informa la proporción de fondeo bancario sobre activos totales de la fintech.

Si el cruce funciona, construir dos exposiciones: restricción de los bancos del cliente y restricción de los bancos que financian a su prestamista alternativo. Predecir más sustitución cuando hay alternativas accesibles cuyo fondeo no enfrenta el mismo shock. Puede ocurrir también que los bancos prioricen crédito a PNFC y estos sostengan el crédito final: eso es intermediación indirecta, no independencia de la banca.

### Acto 5 opcional: persistencia y riesgo

Examinar continuidad de crédito y deterioro posterior para todos los deudores definidos ex ante. No convertir cambios de situación en pagos observados. El shock bancario puede empeorar directamente la posibilidad de refinanciar; por tanto, no es automáticamente un IV válido para probar que tomar crédito fintech causa mora bancaria. Para pecking order/enforcement haría falta variación adicional y evidencia contractual. Mantenerlo como resultado posterior o paper separado si amenaza con dispersar la contribución principal.

## 5. Métodos: una secuencia, no una colección de instrumentos

### A. Base operativa: red de crédito durante todo el panel

`g_ibt = alpha_it + mu_ib + gamma_bt + error_ibt`.

Recuperar correctamente efectos relativos `gamma_bt`, con conectividad, normalización, ceros y entradas/salidas. El error detectado en el notebook anterior debe corregirse antes. Estimar en particiones independientes y excluir al receptor o su mercado cuando sea viable. No usar simples promedios del ajuste completo como efecto bancario. Contrastar shocks con balances y episodios; no usar su correlación con liquidez como demostración automática de exogeneidad.

El supuesto sustantivo es que, condicional a controles, demanda específica por relación/producto no explica el componente atribuido al banco. Comparar personas y firmas, redes y segmentos; revisar adquisiciones y transferencias contables, incluida la integración HSBC/Galicia. Los efectos banco estimados son relativos: no identifican el efecto agregado nacional de la reforma.

### B. Exposición institucional para anclar la interpretación

Medir por separado, antes del anuncio: LEFI, caja libre, fondeo exigible/volátil, acceso previo al interbancario, exigencias normativas predichas y cartera soberana. Comparar dinámicas de bancos con exposiciones distintas al mismo deudor. Una presentación con coeficientes por fase permite examinar anticipación y diferencias entre julio y agosto; no obliga a que el paper sea un único event study.

Priorizar medidas con vínculo mecánico documentado. El saldo previo es predeterminado, no aleatorio. Un índice compuesto puede construirse con teoría/reglas fijas, pero no elegir pesos para maximizar la contracción observada. Colocar LEFI y encajes juntos sin soporte independiente no permite identificar sus efectos separados.

### C. Exposición del deudor tipo shift-share

`Z_it = suma_b s_ib,pre * gamma_bt^(-receptor)`.

Estimar primero formas reducidas sobre cada fuente y el total, con efectos deudor y mercado×mes, y riesgo/actividad previos×mes cuando el soporte lo permita. Los efectos deudor×mes no pueden permanecer en una regresión con resultado agregado al deudor. El banco elegido anteriormente y los shocks deben satisfacer un argumento de exogeneidad condicional; ni leave-out ni la forma Bartik lo generan por sí solos.

Si se instrumenta la contracción de crédito bancario para medir compensación, explicitar exclusión, monotonicidad y efectos indirectos a través del fondeo fintech. Primero entender la forma reducida; reportar incertidumbre de cocientes/2SLS y debilidad. Muchos deudores no compensan pocos shocks bancarios correlacionados. La inferencia debe reflejar bancos/grupos, shocks compartidos y estimación del shock; wild bootstrap puede ayudar pero no rescata identificación ni falta de soporte.

### D. Candidato adicional para variación: vencimientos de cartera previa

Recolectar la cartera por especie antes del anuncio y su calendario de pagos contratado. Construir caja **programada**, no ventas o reinversiones efectivamente elegidas:

`M_bt = suma_s tenencia_bs,pre * pago_contractual_st / activos_b,pre`.

Pregunta: durante la transición, ¿un vencimiento preprogramado amortiguó el ajuste de crédito de bancos con menor acceso a liquidez alternativa? Es una variación temporal dentro del banco con mecanismo de caja explícito. Los anexos públicos identifican especies, incluida LEFI código 9285; por ejemplo, [presentación bancaria ante SEC](https://www.sec.gov/Archives/edgar/data/913059/000129281425003413/ex99-1.htm).

Esto es una propuesta para explorar, no un instrumento validado. Elegir la duración de la cartera es endógeno; vencimientos soberanos tienen efectos macro y oportunidades de reinversión; existen canjes y cambios de tenencia. Requiere composición preanuncio, moneda, duración y controles, y evaluar cuánta variación independiente queda. Todos los bancos tenían la misma LEFI: **su único vencimiento no crea por sí solo muchos shocks**. No llamar Bartik de muchos shocks a un evento común multiplicado por tenencias.

## 6. Modelo y narrativa sin sobrecargar

Un modelo mínimo puede ordenar tres objetos: costo marginal de liquidez bancaria, costo del cliente de formar otra relación y costo/capacidad de fondeo del prestamista alternativo. La sustitución aumenta cuando la alternativa es accesible y no comparte la restricción; cae cuando ambos acreedores dependen del mismo fondeo. No hace falta empezar con equilibrio general estimado. Un modelo estilo Bianchi–Bigio, ampliado a un prestamista no bancario y costos de relación, solo se justificaría si añade predicciones discriminantes o un contrafactual creíble.

Predicciones útiles: respuesta distinta según buffers y acceso interbancario previos; ajuste financiero anterior o simultáneo al crediticio; compensación fintech en montos; más reemplazo donde existen relaciones alternativas; heterogeneidad por fondeo del reemplazante. Información, cobro, producto y riesgo pueden generar patrones parecidos: priorizar observables que distingan explicaciones.

No afirmar bienestar a partir de saldo total. Para efectos reales, buscar ventas, consumo o empleo vinculables; para costos del reemplazo, precios/plazos. La ausencia de esos datos no impide un paper de intermediación financiera, pero limita el enunciado a disponibilidad, composición y riesgo del financiamiento formal observado.

## 7. Qué haría primero y cuándo pivotear

1. Verificar exposición LEFI exacta y reglas de indicadores con varios bancos, sin suponer que diferencias de ratios aíslan el instrumento. Revisar si los archivos que el extractor selectivo no conserva contienen apertura de títulos. No está comprobado.
2. Auditar código↔CUIT del prestamista y probar cobertura de su deuda bancaria; incorporar emisores, fideicomisos y balances públicos de los PNFC principales para distinguir fondeo observado de total.
3. Construir hechos de crédito a nivel relación, separados por tipo de acreedor, conservando cohortes y salidas; corregir el shock y probar su capacidad predictiva fuera de la muestra de construcción.
4. Reunir series diarias de tasas/volúmenes, cartera por especie y normativa. Datos de saldos diarios por banco, operaciones interbancarias, concentración de depositantes y líneas serían especialmente valiosos para el mecanismo.

Si exposición institucional predice liquidez y crédito con soporte suficiente, LEFI/reforma de 2025 puede ser central. Si solo predice redistribución de activos líquidos, el paper de crédito no está respaldado. Si los shocks de red predicen crédito y sustitución pero la atribución a LEFI es débil, mantener LEFI como episodio ilustrativo y centrar el paper en límites de sustitución. Si solo aumenta la participación fintech, no presentarlo como compensación. Si la respuesta está dominada por una sola plataforma, delimitar el resultado a esa plataforma o buscar apoyo adicional; no simular muchos tratamientos independientes.

**Recomendación actual:** avanzar con la pregunta general de sustitución condicionada por acceso y fondeo. Usar LEFI como candidato fuerte para estudiar el origen de la restricción, y dejar que la medición y los primeros hechos determinen cuánto protagonismo merece. Esto mantiene una narrativa clara sin prometer desde hoy ni un instrumento perfecto ni una historia de bienestar.
