# Fintech-Dynamics

Adopción de pagos digitales y composición del fondeo bancario en Argentina.

## Estructura

| Carpeta | Contenido |
|---|---|
| `Data/` | Datos y su documentación. Ver `Data/README_data.md` |
| `Code/` | `build/` construye las bases, `analysis/` las usa, `output/` recibe figuras y tablas |
| `Literature/` | Papers de referencia y [guía de lectura](Literature/README.md) de los 16 PDF locales |
| `Methodological_Notes/` | Notas de método, fuentes y preguntas de investigación |
| `Regulation/` | Cronología normativa, alícuotas de efectivo mínimo y comunicaciones del BCRA |
| `Presentations/` | Presentaciones de avance |

## Cómo correr

Todo el código resuelve la raíz del repositorio por sí solo, así que se ejecuta desde
cualquier subcarpeta. Los scripts de Python la deducen de su propia ubicación; los `.do`
de Stata suben directorios hasta encontrar este archivo y definen `$root`, `$raw`,
`$proc`, `$cross`, `$tab` y `$fig`.

```
python3 Code/build/descargar_ief_selectivo.py     # descarga IEF del BCRA
stata -b do Code/build/build_dta.do               # arma Data/processed/*.dta
python3 Code/build/cendeu_build.py deudores       # arma las bases de la Central de Deudores
```

El orden completo del pipeline de datos está en `Data/README_data.md`.

El [estado de revisión](Methodological_Notes/estado_revision_2026-09-13.md)
documenta la cobertura comprobada y las limitaciones pendientes del análisis.

## Datos que no están en el repositorio

`Data/raw/` y `Data/processed/cendeu/` están fuera de control de versiones: pesan
alrededor de 11 GB y la Central de Deudores contiene microdato identificado sujeto a la
declaración jurada de la Ley 25.326. Se reconstruyen corriendo los scripts de
`Code/build/`, salvo los archivos de la Central, que el BCRA sólo publica para el mes
corriente.
