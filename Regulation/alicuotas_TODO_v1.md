# Alicuotas de efectivo minimo, pendiente v1

La v0 (alicuotas_efectivo_minimo.csv) cubre solo las dos categorias que no dependen
del grupo de entidad: haber a la vista de FCI money market (1.3.12) y cuentas de
custodia de PSPCP (1.3.14). Fechas de vigencia verificadas contra los PDF de
Regulation/ y el Texto Ordenado de Efectivo Minimo.

Falta (v1): caja de ahorros, cuenta corriente, cuenta sueldo y plazo fijo. NO se
pueden cargar como un numero por mes porque la exigencia general depende de
(i) la categoria de la entidad (grupo A / resto, por tamano y localizacion),
(ii) el plazo residual en las imposiciones a plazo, y (iii) los regimenes de
integracion (LELIQ/bonos) que cambian el costo efectivo sin cambiar la alicuota
nominal. Cargarlas sin esas dimensiones introduce error correlacionado con el
tamano del banco. Fuente para v1: Textos Ordenados de Efectivo Minimo (versiones
historicas en bcra.gob.ar), seccion 1.3, mas la tabla de alicuotas por grupo.
