# Fuentes de FCI: dónde está cada dato y cómo se llega

Registro de fuentes verificadas en vivo entre el 25 y el 28 de septiembre de 2026. Reemplaza a `archivo/fuentes_fci_cafci_2026-08.md`, que documentaba la API de CAFCI (caída desde agosto de 2026). Las variables y la construcción de las bases están en `Data/docs/diccionario_fondoscnv.md`.

## 1. Planillas diarias por clase (CNV, provistas por CAFCI)

- Ruta: cnv.gov.ar > Fondos Comunes de Inversión > "Últimos valores diarios de cuotaparte" > Ver más.
- Índice: https://www.cnv.gov.ar/SitioWeb/FondosComunesInversion/CuotaPartes (3.137 presentaciones desde el 2-ene-2020, con versiones corregidas del mismo día).
- Cada día: `https://aif2.cnv.gov.ar/Presentations/publicview/{GUID}`, con un adjunto `AAAAMMDD_Planilla_Diaria_A.xlsx`.
- Contenido: por clase, cuotapartes (hoy y ayer), VCP, PN, honorarios, código CNV, código CAFCI, gerente y depositaria. Todos los tipos de fondo. Entre 2020 y 2023 tiene 44 columnas; las recientes, 47 (se agregan Ley 27.743, tipo de dinero y calificado).
- Descarga: el id del archivo está en un input oculto de la presentación (`nombreArchivo`, `guid`); `GET https://aif2.cnv.gov.ar/api/ValetKeyProvider/GetPublicValetKey/{guid}?operation=DownloadBlob` devuelve la clave; `POST https://blob.cnv.gov.ar/BlobWebService.svc/DownloadBlob/{guid}` con el form `ValetKey=<clave>` y Referer/Origin de aif2 devuelve el xlsx. El servicio da 503 a rachas.
- Cuidado: la columna Fecha es la del último valor informado por cada clase. Una clase que no reportó repite un valor viejo; se marca como `desactualizado`.

## 2. Ficha de cada fondo: cartera semanal, estados contables, hechos relevantes, reglamentos

- Ruta: cnv.gov.ar > Fondos Comunes de Inversión > buscador "por Fondo Común de Inversión" > elegir el fondo > Buscar. Abre `DetallesFCI/{lfc}`.
- URL directa: `https://www.cnv.gov.ar/SitioWeb/FondosComunesInversion/DetallesFCI/{lfc}?denominacion=x&estado=Aprobado%20Lanzado&idEstado=5`.
- Cartera a una fecha: agregar `&compo=true&fecha=AAAA-MM-DD` (es lo que hace el selector "Composición de carteras anteriores"). Devuelve la última cartera informada a esa fecha. El historial empieza el 8-nov-2019.
- Ids: el `<select id="Lfc">` de https://www.cnv.gov.ar/SitioWeb/FondosComunesInversion lista 1.703 fondos. No coinciden con el código CNV de la planilla; el puente es `Data/crosswalks/fondos_cnv_lfc.csv`.
- Formato: las filas en negrita son rubros, con el valor en la tercera columna (Disponibilidades, Operaciones a Plazo, Títulos de Deuda, Certificados de Participación, Otros Activos, Pasivos). Las filas de detalle traen el valor en la segunda columna. Una fila sin texto trae el 100,00 y otra "(Peso Argentina)" trae el PN en pesos.
- El id puede cambiar de fondo en el tiempo (renombres y conversiones de tipo de fondo): guardar el nombre de la cartera en cada fecha.
- Otras secciones: Reglamento de gestión (define las clases), Estados Contables (trimestrales y anuales desde 2018, PDF), Hechos Relevantes (cambios de honorarios con fecha).

## 3. Ficha de la sociedad gerente

cnv.gov.ar > Empresas y Personas > buscar por razón social > Ver más. Trae estados contables de la gerente, actas y hechos relevantes de todos sus fondos.

## 4. Otras fuentes

- Maestro CAFCI de fondos y clases, incluidos los liquidados: https://estadisticas.cafci.org.ar/consulta-de-fondos.json
- Resúmenes mensuales CAFCI, con la fila de agentes de colocación y distribución integral: `www.cafci.org.ar/Publica/Estadistica/Resumenes/Mensual/AAAAMM01_Resumen_Industria.pdf`
- Registro de ACDI: cnv.gov.ar > Registros Públicos > Agentes > "ACD - FCI Integral".
- API de estadísticas monetarias del BCRA (v4.0), depósitos de FCI por instrumento a nivel sistema: series 986 (total), 1030 (cuenta corriente, pesos) y 1063 (caja de ahorros, pesos), desde dic-1999. El campo de unidad dice miles pero la escala es de millones.
- Cronología de encajes sobre la vista de FCI money market: `Regulation/cronologia_normativa.csv`.

## 5. No público

Apertura de disponibilidades por banco, convenios de colocación (art. 28), informe mensual del colocador por fondo (RG 1089/2025), suscripciones y rescates brutos, cuotapartistas por tipo de inversor. Pedido en `pedido_cnv_fci.md`.
