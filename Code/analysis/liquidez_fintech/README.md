# Liquidez y sustitución fintech

Exploración del paper. Datos fuente de solo lectura; salidas agregadas en
`Code/output/liquidez_fintech`. Los notebooks guardan sus tablas y figuras ejecutadas.

1. `01_datos_y_muestra.ipynb`: cobertura de los 24 meses, integridad de claves,
   clasificación de acreedores, muestra y comparación con el agregado completo.
2. `03_credito_y_sustitucion.ipynb`: evolución real del universo de personas y
   cohortes fijadas en mayo de 2025, composición y continuidad del crédito reportado.

La numeración `02` y `04` queda disponible para medición bancaria y diseño,
sin comprometer la investigación con un episodio. No se crearon notebooks vacíos ni regresiones sin diseño.

## Ejecutar

Desde esta carpeta, con Python y las dependencias de `requirements.txt`:

```sh
python -m jupyter nbconvert --execute --to notebook --inplace --ExecutePreprocessor.timeout=1800 01_datos_y_muestra.ipynb
python -m jupyter nbconvert --execute --to notebook --inplace --ExecutePreprocessor.timeout=1800 03_credito_y_sustitucion.ipynb
```

Cada notebook es independiente y resuelve la raíz del proyecto desde `common.py`.
DuckDB procesa un mes a la vez, con 3 GB de memoria y cuatro hilos. No se guarda
el panel identificado ni los CUIT de la cohorte. Las SQL están en `sql/`; el
resto de las operaciones se ve en las celdas. `common.py` solo comparte fuentes,
clasificación, estilo y trazabilidad.

## Convenciones que importan

- En 01/03, fintech principal = PNFC del grupo `pnfc_fintech` del crosswalk existente.
  En 05/06 se estudian entidades individuales: esa agrupación no define las comparaciones.
  Bancos digitales y financieras digitales se muestran separados en la auditoría;
  no se asume que cada préstamo implique uso de la billetera.
- Los bancos se identifican con el corte IEF de mayo de 2025, usando como respaldo
  la clasificación fuente para entidades fuera del corte. Falta fechar licencias,
  fusiones y cesiones. Las categorías fuente sospechosas quedan visibles.
- SGR y fondos de garantía se excluyen del saldo crediticio principal para no
  sumar garantías como si fueran otro préstamo. El archivo distribuido tampoco
  permite separar todos los productos/garantías dentro de cada relación.
- Los saldos son stocks reportados. Un cero o una ausencia no identifica pago,
  cancelación ni cierre. Una aparición puede reflejar umbral, cesión o reporte.
- IPC nacional, pesos de mayo de 2025. No se imputan meses sin IPC. El saldo en
  pesos puede incluir deuda en moneda extranjera reexpresada: deflactar no elimina
  efectos cambiarios.
- La muestra existente usa hash de CUIT y no se expande por veinte. La auditoría
  compara el hash con la versión instalada; esa función puede cambiar entre versiones.
- Toda la historia proviene de un corte retrospectivo; no son 24 archivos de
  vintage independiente. Permanecen riesgos de selección, rectificaciones y reporte.
- La clasificación es constante y provisional. Son hechos descriptivos, no efectos
  LEFI ni evidencia causal de sustitución. No confundir expansión agregada con
  compensación de una pérdida bancaria individual.

La nueva nota `Data/docs/nota_lefi_leliq.md` de otro agente reporta problemas de
reconciliación de LEFI. No se usa esa variable ni `liq_publica` como tratamiento;
un agregado de títulos/pases no equivale necesariamente a liquidez libre.

Para la siguiente fase se propone PyFixest para efectos fijos y statsmodels para
diagnósticos. No son dependencias obligatorias de estos dos notebooks descriptivos.

## Primera corrida: 21 de septiembre de 2026

Ambos notebooks se ejecutaron completos, sin errores. Se revisaron los HTML y
las seis figuras. La auditoría mensual no detectó claves duplicadas, montos
negativos ni faltantes en los controles implementados. Esto no resuelve los
riesgos de cobertura histórica señalados arriba.

Entre mayo de 2025 y junio de 2026, el saldo real del universo de personas crece
12,36% en bancos y 39,86% en PNFC fintech. En cambio, dentro de la cohorte que ya
tenía banco y fintech en mayo, el componente fintech cae: aporta −1,63 puntos
porcentuales al cambio del saldo total inicial. Son poblaciones distintas; no
se puede atribuir su diferencia íntegramente a nuevos clientes sin descomponerla.
Las tablas correspondientes están en `universo_cambio_desde_mayo.csv` y
`cohortes_contribuciones_finales.csv`.

El cruce individual (`cambios_individuales_conjuntos.csv`) mantiene a toda la
cohorte y compara el signo de ambos componentes. Incluye sensibilidad a umbrales
de 0%, 1% y 5% del saldo total inicial individual. El patrón banco cae / fintech
sube sigue siendo descriptivo y no identifica sustitución inducida por oferta.

La prioridad actual está documentada en `viabilidad_paper.md` y en el notebook 06.
Las propuestas anteriores sobre LEFI son hipótesis pendientes, no el diseño elegido.

## Exploración por entidad, sin clasificación fintech impuesta

`05_trayectorias_por_entidad.ipynb` amplía la exploración con todas las entidades,
trayectorias de personas y firmas, transiciones mensuales de personas, comparación
dentro de deudor-mes, auditoría del código legal y cruce con balances. Ejecutado
completo; diez figuras y un atlas por entidad. Las tablas se prefijan `05_`.
La interpretación y los próximos contrastes están en `resultados_por_entidad.md`.
Las etiquetas originales se conservan solo como metadatos, sin agrupar resultados.

## Viabilidad de acceso, competencia y geografía

`06_viabilidad_acceso_competencia.ipynb` se ejecutó completo e independientemente
de las salidas anteriores. Incluye primeras relaciones con diez entidades, historia
previa, seguimiento a seis meses, soporte multibanco de personas y firmas, pares de
acreedores, cobertura del padrón, banca provincial y exposiciones alternativas con
depósitos y sucursales. Cuatro figuras revisadas y tablas `06_`; HTML en outputs.

La interpretación y las decisiones abiertas están en `viabilidad_paper.md`.
En 06 los conteos consideran todos los códigos reportantes; los montos agregados
no se presentan como deuda neta depurada de garantías. No se impone una definición
fintech ni se estima un efecto causal de tasas, LEFI o inclusión.
