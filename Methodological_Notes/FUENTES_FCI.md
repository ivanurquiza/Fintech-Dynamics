# Fuentes de datos FCI / PSP

Documento de auditoria del pipeline CAFCI-CNV. Para cada fuente: URL exacta,
como se llega navegando (para reproducirla a mano), que contiene, estado al
2026-08-06, y que script la consume. Los crudos se guardan tal como llegaron
en data/raw/cafci/ con hash y fecha en manifest.csv.

## 1. Registro maestro de fondos y clases (CAFCI)

- URL: https://estadisticas.cafci.org.ar/consulta-de-fondos.json
- Como se llega: cafci.org.ar > menu "Encuentre su Fondo" > "Consulta de fondos"
  abre la app estadisticas.cafci.org.ar; la misma pagina servida con extension
  .json devuelve los datos crudos.
- Contiene: 1.190 fondos y 4.764 clases con id de fondo y de clase, nombre,
  codigo CNV, sociedad gerente y depositaria (id y nombre), tipo de renta,
  tipo de dinero (Clasico / Dinamico / No Aplica), fecha de inicio, estado
  (incluye fondos dados de baja), honorarios y datos por clase.
- Verificaciones hechas (2026-08-05): Mercado Fondo id 798, codigo CNV 956,
  gerente Mercado Pago Asset Management, depositaria Banco Industrial, inicio
  2018-03-05, clases 1982 a 1985. Ualintec Ahorro Pesos id 1307, gerente Uala
  Fondos, inicio 2022-02-17. Delta Pesos id 394, gerente Delta AM.
- Estado: funcionando.
- Script: data/scripts/descargar_cafci.py (snapshot fechado).

## 2. Resumenes mensuales de la industria (CAFCI, PDF)

- URL patron: https://www.cafci.org.ar/Publica/Estadistica/Resumenes/Mensual/AAAAMM01_Resumen_Industria.pdf
- Como se llega: cafci.org.ar > Estadisticas > "Resumen Mensual" (selector de
  anio y mes); el boton de descarga arma esa URL (verificado inspeccionando la
  llamada de red al descargar).
- Contiene: patrimonio y cuentas por tipo de inversor (personas humanas vs
  juridicas; mensual, visto al menos desde 2020), cita trimestral de CNV de
  cuentas de cuotapartistas via ACDI (serie verificada: dic-2019 1.151.444;
  sep-2021 4.753.328; mar-2022 5.840.492; mar-2023 8.091.961; sep-2025
  28.907.511), y en los reportes recientes el cruce money market x tipo de
  persona (dic-2025 si, jun-2023 no).
- Estado: funcionando (archivo desde 2010).
- Scripts: data/scripts/descargar_cafci.py (descarga) y data/scripts/extraer_cafci_agregados.py
  (extraccion de las series a csv, con reporte de que falto por PDF).

## 3. Series por fondo y clase (API publica CAFCI) - PENDIENTE POR CAIDA

- URL patron: https://api.pub.cafci.org.ar/fondo/{id_fondo}/clase/{id_clase}/ficha
  y .../rendimiento/{desde}/{hasta}; planilla diaria en /pb_get.
- Como se llega: es la API que llaman las propias paginas de cafci.org.ar
  (ficha-fondo.html e info-diaria.html); verificado inspeccionando las llamadas
  de red de esas paginas. Sin token ni autenticacion.
- Contiene: patrimonio, valor de cuotaparte y rendimientos por clase y fecha
  (historia completa via el selector de fecha de info-diaria.html). La cantidad
  de cuotapartes se deriva como patrimonio / valor de cuotaparte.
- Estado al 2026-08-06: servidor caido (503 y luego sin respuesta); afecta
  tambien a las paginas del propio sitio. Reintentar.
- Script: pendiente de escribir cuando el servidor responda.

## 4. Respaldo oficial: presentaciones diarias en CNV (AIF)

- URL: https://www.cnv.gov.ar/SitioWeb/FondosComunesInversion/CuotaPartes
- Como se llega: cnv.gov.ar > Registros Publicos / Fondos Comunes de Inversion >
  "Ultimos Valores Diarios de Cuotaparte". Cada entrada abre el visor AIF
  (aif2.cnv.gov.ar/Presentations/publicview/{id}).
- Contiene: la presentacion diaria "Valores Diarios de Cuotaparte" que CAFCI
  hace ante CNV, archivada con fecha. Mismo contenido que la planilla diaria,
  con caracter de filing regulatorio (fuente citable).
- Estado: funcionando; scraping mas artesanal (visor + adjunto por presentacion).
- Uso previsto: respaldo y cita oficial; alternativa si la API no vuelve.

## 5. Vinculo fondo - billetera (tratamiento) - EN EXPLORACION

- Fuente prevista: registros y documentos de CNV (convenios de colocacion en la
  AIF; agentes de colocacion por fondo), con fechas. Respaldo: terminos y
  condiciones de las apps archivados en Wayback Machine.
- Decision de diseno: la dummy de tratamiento se fija con los colocadores
  vigentes a dic-2021; incorporaciones posteriores son outcome, no tratamiento.
