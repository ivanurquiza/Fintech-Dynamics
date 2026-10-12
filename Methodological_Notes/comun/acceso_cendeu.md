# Central de Deudores: acceso, archivos y sesgos

Nota del 30-ago-2026, revisada el 12-oct-2026. Ruta de acceso verificada con Clave Fiscal. El diccionario de las bases construidas está en `Data/docs/diccionario_cendeu.md`.

## Acceso

El BCRA distribuye la Central de Deudores completa (deudor × entidad × mes, identificada) a cualquier persona con Clave Fiscal de ARCA que acepte una declaración jurada bajo la Ley 25.326. Norma: texto ordenado de Centrales de Información (`t-ceninf.pdf`), sección Difusión y Anexo.

1. arca.gob.ar con Clave Fiscal > servicio "BCRA - Cheques y Deudores" > agregar.
2. El servicio abre `https://www5.bcra.gob.ar/ChequesyDeudores`, sección Deudores.
3. Cada archivo pide aceptar la declaración jurada (conocimiento de la Ley 25.326 y del deber de inscripción en el Registro Nacional de Bases de Datos cuando corresponda).
4. La descarga sale por `mft.bcra.gob.ar` en formato `.7z`.

Sólo está el período corriente. Un mes que no se baja se pierde. Guardar el `.7z` original con hash y fecha de descarga.

## Archivos

| Archivo | Contenido |
|---|---|
| `AAAAMMDEUDORES` | Todos los deudores del mes, 24 campos |
| `24DSFAAAAMM` | Panel de 24 meses en formato ancho: por deudor-entidad, un bloque {situación, monto, proceso judicial} por mes |
| `1DSFAAAAMM` | Fecha desde la que el deudor está en situación 1 |
| `AAAAMMINFRET`, `INFRETPA` | Información rectificada |
| `AAAAMMDDPADRON` | Padrón de ARCA (actividad, sexo, fecha de nacimiento, código postal, provincia) |

Los archivos distribuidos tienen el layout de `t-ceninf.pdf`, no el de reporte de `t-so-s03.pdf`. Códigos de proceso judicial o revisión: 0 no observado, 1 proceso judicial, 2 información sometida a revisión. Situación: 1 a 6, 11 y 99; el proyecto define irregular como 3, 4 o 5.

## Sesgos que hay que acotar

**El 24DSF filtra por entidad.** Entran todos los deudores de entidades activas y sólo los deudores en situación normal de entidades dadas de baja. La mora de entidades que salieron se borra del pasado y la cartera sana se conserva: la mora de los meses viejos queda subestimada y su crecimiento, exagerado. Se acota comparando el corte mensual con la columna del mismo mes del panel.

**El registro se reescribe.** Las rectificaciones modifican el pasado. Dos descargas del mismo período en fechas distintas no son el mismo dato.

**El umbral de $25.000 es nominal.** Los deudores con saldo menor se informan agregados. Con inflación el umbral se licúa y entra gente al registro identificado; pesa más en crédito fintech de ticket chico.

## Datos personales

Procesamiento local, nada identificable en el repo ni en las salidas, piso de 500 personas en cortes geográficos, intermedios con hash fuera del repo. Declarar fuente, vía de acceso y declaración jurada en la sección de datos del paper. Pendiente evaluar la inscripción de la base derivada.

## Pendientes

Tabla oficial de códigos de situación del archivo distribuido; vigencia y actualizaciones del umbral; contenido exacto de `INFRET` e `INFRETPA`; disponibilidad de `maeent.txt`, `nomdeu.txt` y `morexent.txt` (morosos de ex entidades).
