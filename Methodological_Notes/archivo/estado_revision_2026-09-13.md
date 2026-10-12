# Estado de revisión del proyecto

13 de septiembre de 2026. Revisión local de documentación, código, metadatos y
resultados guardados. No constituye una replicación integral ni una nueva
verificación de normativa vigente. Los materiales anteriores se conservan como
antecedentes; esta nota explicita diferencias relevantes para usarlos.

## Bases verificadas

- `balances_bancos.dta`: 7.681 filas, 328 columnas, 84 entidades; enero de 2018 a
  abril de 2026. Llave entidad–mes sin duplicados. Se conservan nominales y
  versiones reales `_r`.
- `caracteristicas_bancos.dta`: 528.714 filas, 7 columnas, 85 entidades; igual
  cobertura temporal, formato largo.
- `prestamos_depositos_prov.dta`: 48.115 filas, 25 columnas. Llave
  entidad–provincia–mes sin duplicados. Los montos se observan solo en marzo,
  junio, septiembre y diciembre; presencia física mensual. No es un panel de
  montos mensuales completos.
- `inclusion_prov.dta`: 2.592 filas, 24 provincias, enero de 2017 a diciembre
  de 2025; llave provincia–mes sin duplicados. Tenencia de cuentas disponible
  solo en cierres trimestrales.
- Puntos de acceso: 2019–2025; 43.851 filas departamento–mes, 2.016
  provincia–mes y 594.214 entidad–departamento–tipo–mes. `pda_provincia.dta`
  tiene 15 columnas, no 16. `pda_lender_depto` identifica a la entidad por nombre;
  requiere correspondencia para unir con el código `ent` de balances/CENDEU.
- CENDEU: el panel ancho tiene 59.292.141 relaciones y 24 bloques, agosto de
  2024 a julio de 2026. Los derivados incluyen 14.335.169 filas de firmas y
  54.958.697 de la muestra de personas del 5%; sus conteos incluyen la
  persistencia de relaciones canceladas definida por el constructor.
- CAFCI: maestro fechado, resúmenes de industria y agregados. No se encontró
  un panel histórico construido de carteras fondo–banco ni de flujos por clase.

La documentación de directorios IEF hasta diciembre de 2026 no establece que
haya observaciones hasta esa fecha. La cobertura comprobada del panel bancario
termina en abril de 2026. Los datos de acceso físico terminan antes que CENDEU;
los joins deben explicitar la fecha de referencia.

## Convenciones que importan

`ym` en Stata usa meses desde enero de 1960; el constructor CENDEU usa
`year * 12 + month - 1`. La diferencia es 23.520. Por ejemplo, julio de 2026
es 24.318 en CENDEU y 798 en Stata. El notebook descriptivo convierte los
balances a la convención de CENDEU; cualquier otro join debe hacer lo mismo
o convertir ambas fuentes a fechas.

`dep_fci_proxy` es la cuenta especial de personas jurídicas con interés
(`311724`). No identifica al depositante como FCI. Las notas sobre una red
fondo–banco públicamente accesible describen una posibilidad de obtención, no
una base histórica ya disponible en esta copia del proyecto.

## Análisis existente: pendientes concretos

En `Code/analysis/cendeu_summ_stats.ipynb`:

1. La sección de dinámica conserva un error SQL que intenta leer
   `status_-1` y `amount_-1_ars`. Revisar los extremos del recorrido entre
   bloques antes de volver a producir la tabla.
2. La validación del shock conserva `AttributeError` por `dep_pfijo`, columna
   ausente en balances. Existe `dep_pf_total`, pero hay que confirmar la
   definición económica y el denominador deseados antes de sustituirla.
3. La función `tabla_entrantes` calcula primera actividad por relación
   deudor–acreedor y luego elige una relación por monto. Eso no asegura primera
   entrada del **deudor al registro**: puede incorporar clientes que ya tenían
   otro acreedor. Revisar la fecha mínima cronológica entre todos los acreedores
   y excluir a quienes ya estaban al inicio. Además permanece la censura
   izquierda de la ventana de 24 meses.
4. `tabla_top` calcula `share_deudores` sobre la suma de los acreedores
   seleccionados en el ranking. Ese denominador no es el total del sistema ni
   personas únicas. Revisar las participaciones trasladadas a presentaciones.
5. El archivo de shocks contiene 294 estimaciones, 50 bancos y seis trimestres;
   desvío conjunto aproximado 0,162. Es una descripción del resultado guardado,
   no validación de oferta. El código señala que falta excluir el mercado
   receptor de la estimación del shock.
6. La clasificación manual de entidades con billetera necesita cotejo antes
   de usarse como tratamiento; la taxonomía regulatoria no coincide necesariamente
   con el modelo económico del prestamista.

Estos pendientes se documentan sin alterar estimaciones ni borrar resultados.
No tratar las tablas como una replicación terminada. La guía de
[literatura](../Literature/README.md) explica qué supuestos requieren las
estrategias propuestas.

Se repararon los saltos de línea de `cendeu_explore.ipynb`, que concatenaban
instrucciones y producían errores de sintaxis. Se verificó sintaxis de los
scripts Python y las celdas de código de los cuatro notebooks, sin ejecutar
sus consultas completas ni inspeccionar un nuevo render de resultados. Para
completar la validación del exploratorio con los microdatos locales:

```bash
python3 -m jupyter nbconvert --execute --to notebook --output cendeu_explore_verificado --output-dir /tmp Code/analysis/cendeu_explore.ipynb
```

Requiere Jupyter, un kernel Python con DuckDB/pandas y las bases locales. La
copia ejecutada es de uso local: el exploratorio incluye una vista de diez
registros identificados, cuyos resultados no deben subirse al repositorio.

## Conservación en GitHub

Se conserva código, documentación, literatura, presentaciones, tablas/figuras
agregadas y bases procesadas públicas en Stata. Se excluyen datos crudos,
microdatos CENDEU, parquet, archivos comprimidos y temporales.

Se normaliza la carpeta `Data/` en el índice Git para coincidir con las rutas
del código en sistemas sensibles a mayúsculas. El descargador de inclusión
financiera se conserva en `Code/build/descargar_datos_bcra.py`: antes estaba
dentro de datos crudos excluidos del versionado.
