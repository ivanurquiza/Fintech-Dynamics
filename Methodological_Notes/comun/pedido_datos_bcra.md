# Datos del BCRA: qué existe, qué es público y qué pedir

Nota de agosto de 2026, revisada el 12-oct-2026. El punto sobre CENDEU quedó resuelto por la vía de descarga con Clave Fiscal (`acceso_cendeu.md`); el resto sigue vigente.

## 1. Lo público que ancla el lado del pasivo

La API de estadísticas monetarias (v4.0), categoría "Depósitos por tipo de titular", publica desde dic-1999 los depósitos de FCI por instrumento y moneda (ids 986 total, 1030 cuenta corriente en pesos, 1063 caja de ahorros en pesos), además de prestadoras de servicios financieros (995, 1094) y personas humanas (993). El campo de unidad dice miles pero la escala es de millones.

Contraste con los balances, abr-2026: FCI a la vista según la API, $10,5 billones (3,68 en cuenta corriente y 6,83 en caja de ahorros); partida 311724, $7,63 billones; partida 311723, $0,47 billones. La vista de los FCI se reparte entre varias partidas contables: 311724 no es "la cuenta de los FCI" ni es despreciable. La relación entre la cuenta corriente de FCI y la 311724 cae de 0,87 (2021) a 0,40 (2023) y vuelve a 0,48 (2026m4). Con datos públicos el problema se acota a nivel sistema, no a nivel banco.

## 2. Qué se reporta al BCRA por entidad

| Régimen | Unidad | Contenido |
|---|---|---|
| Efectivo mínimo (Sec. 6), `SALDOSDIARIOS.TXT` | entidad × partida × día | Partida `102190/001`: depósitos a la vista de FCI money market. Partida `102200/001`: cuentas de PSP con fondos de clientes |
| SISCEN 0011 | entidad × titular × instrumento × mes | Fuente de las series por titular de la API. Sólo se publica agregado. Secreto estadístico (Ley 17.622) |
| SISCEN 0013 | entidad × tramo de monto | Separa minorista de mayorista |
| SISCEN 0002, 0018, 0019 | entidad × día | Tasas efectivas por depósitos, préstamos y plazo fijo mayorista |
| R.I.-PSP (Sec. 69, A 8284) | PSP × día | `20000dd` saldos a la vista por entidad financiera (por CBU); `40000dd` saldos invertidos por fondo, con CUIT del agente colocador |
| PNFC (Sec. 59, A 8047) | proveedor | Saldos por tipo de asistencia y `TASA.TXT` con tasa promedio por entidad |
| Sec. 44 y 47 | cliente / punto de atención | Padrón con código postal (incluye PSP) y unidades de servicio con coordenadas |

## 3. Pedidos, en orden de retorno

1. **SISCEN 0011 por entidad** (depósitos por titular e instrumento, 2018 a la fecha). Exposición de cada banco al fondeo de FCI y de PSP sin proxies. Alternativa: identificador de entidad anonimizado y consistente.
2. **Efectivo mínimo, partidas `102190/001` y `102200/001`, entidad × mes**, con la Guía de Correlación con Balance de Saldos (Sec. 5) y las alícuotas efectivas por partida. Régimen prudencial: menor fricción que SISCEN.
3. **R.I.-PSP Apartado A** (`20000dd` y `40000dd`), desde la primera fecha disponible. Red PSP × banco y PSP × fondo. El IMPM ya publica participaciones por PSP, lo que debilita la objeción de confidencialidad.
4. **Registro de PSP con altas, bajas y bancos patrocinantes.**
5. **CENDEU histórico**: los `AAAAMMDEUDORES` de meses anteriores, `morexent.txt`, `AAAAMMMOROSOS` y la tabla de códigos de situación. Para el orden de repago: tipo de asistencia (diseño 4301 y siguientes) y `TASA.TXT` de PNFC.
6. **PNFC por entidad y registro de restricciones de acceso al financiamiento bancario** (puntos 3.1.2 y 3.2.2 del texto ordenado).
7. **SISCEN 0013** por entidad.

## 4. Cómo redactar

Pedir por sección, archivo y campo. Separar los pedidos por régimen (17.622 para SISCEN, art. 39 de la Ley 21.526 para los prudenciales) para que la denegación de uno no arrastre al resto. Ofrecer anonimización y acceso en sede como alternativa. Citar los precedentes de publicación y que el BCRA ya distribuye microdato identificado de CENDEU bajo declaración jurada. La vía de convenio de investigación corre en paralelo.

## 5. Sin verificar

Qué partidas contables mapea el BCRA a cuenta corriente y caja de ahorros en la estadística por titular; si "prestadoras de servicios financieros" contiene a los FCI; desde cuándo el R.I.-PSP trae el detalle por CBU y por fondo.
