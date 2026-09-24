# Instrumentos de liquidez del BCRA y del Tesoro en los balances

_Nota de construccion. Acompaña al bloque de `codes_act` y `codes_pase` en `Code/build/build_dta.do`._

## Que se agrego

El plan de cuentas del BCRA tiene cuentas propias para cada instrumento de
liquidez, con alta y baja en las fechas de la reforma monetaria.

| Cuenta | Descripcion | Vigencia observada en baldet |
|---|---|---|
| `121058` | Letras de Liquidez del BCRA (LELIQ), pesos | hasta 2024m1 |
| `121091` `121092` `121093` | Letras Fiscales de Liquidez (LEFI), pesos, por criterio de medicion | 2024m7 a 2025m6 |
| `125058` | Letras del BCRA LEDIV a tasa cero, moneda extranjera | 2024 |
| `121003` `121016` `121040` | Titulos publicos en pesos, por criterio de medicion | toda la serie |
| `141104` `141124` `141134` `141143` `141144` `141433` `145120` | Deudores por pases activos | toda la serie |
| `111015` `111025` `141153` `141169` `141170` `145153` | Cuentas y depositos en el BCRA | toda la serie |

Las cuentas del activo llevan saldo deudor, asi que la convencion de signo
que ya tenia el build (`cond(substr(v4,1,1)=="1", debe-haber, haber-debe)`)
las deja positivas sin necesidad de tocar nada.

## La reconciliacion no cierra, y eso condiciona el uso

Sumando las tres cuentas de LEFI sobre todas las entidades y comparando
contra el stock agregado que publica el propio BCRA (API de estadisticas
monetarias, `idVariable` 196, "LEFI en cartera de entidades financieras, en
valor tecnico"), en miles de millones de pesos:

| Mes | Balance (3 cuentas) | BCRA, serie 196 | Cobertura |
|---|---|---|---|
| 2024m7 | 5.749 | 9.605 | 60% |
| 2024m8 | 2.416 | 8.828 | 27% |
| 2024m12 | 2.112 | 10.742 | 20% |
| 2025m3 | 2.065 | 10.255 | 20% |
| 2025m6 | 3.338 | 11.017 | 30% |

La cobertura no solo es baja: se mueve entre 20% y 60% y en sentido
contrario al stock oficial. Entre 34 y 44 entidades reportan las cuentas
cada mes, y no existe ninguna otra cuenta en el plan cuya descripcion
mencione la letra, de modo que no es un problema de codigos faltantes.

La explicacion no es que falten codigos dentro del balance. Las especies del
bloque en pesos suman exactamente al subtotal `121000` mes a mes (49,71 =
49,71 en 2024m6; 57,26 = 57,26 en 2024m7; idem 2024m12, 2025m6 y 2026m4, en
billones de pesos), de modo que no hay ninguna partida escondida. Lo que si
se mueve es la composicion interna: en julio de 2024 los pases caen 15,9,
la LEFI aparece con 5,7 y dentro de titulos publicos `121016` sube 6,2
mientras `121003` y `121040` caen 4,4. Distintos bancos usan distinto
renglon para el mismo instrumento.

Queda un desnivel de 8 billones entre la caida de pases y la suma de LEFI
mas titulos. No es un agujero de datos: el activo total apenas se mueve en
ese mes (155,3 a 156,8) mientras los prestamos suben cerca de 5 y el
efectivo 1,7. Es la rotacion hacia credito del segundo semestre de 2024.

Sobre la brecha contra la serie 196 conviene ser prudente antes de llamarla
error. El titulo de la serie es "en cartera de entidades financieras" y muy
probablemente se mida en el registro de custodia, donde el banco figura como
tenedor tanto de lo propio como de lo que custodia para terceros, en
particular los fondos money market, que fueron tenedores grandes de la
letra. Eso encajaria con que el exceso crezca junto con el patrimonio de los
money market. Es una hipotesis: verificarla exige preguntarle al BCRA por la
fuente de la serie.

**Consecuencia para el diseño.** `lefi` no sirve como intensidad de
tratamiento. El error de medicion no es clasico: depende del renglon que usa
cada entidad, que esta correlacionado con el tamaño y con el tipo de banco.
Usarla como regresor produciria atenuacion sesgada, no ruido.

## Que usar en su lugar

`liq_publica` = `121000` (subtotal de titulos en pesos, que ya contiene LEFI,
LELIQ y titulos publicos) + pases activos + cuentas y depositos en el BCRA.

La construccion va sobre subtotales y no sobre especies justamente porque el
subtotal es exactamente aditivo sobre sus especies y absorbe la eleccion de
renglon. El costo es que `121000` tambien incluye titulos privados, pero esos
se mantienen por debajo del 2% del subtotal en toda la ventana (0,76 en
2024m6, 2,00 en 2026m4), asi que la contaminacion es de segundo orden.
Economicamente es ademas lo que interesa: la posicion liquida del banco
frente al sector publico, no cual de las tres letras la instrumenta.

Sobre activos totales:

| | 2024m5 | 2024m6 | 2024m7 | 2024m12 | 2025m6 | 2026m4 |
|---|---|---|---|---|---|---|
| liq_publica / activo | 48,1% | 46,9% | 41,3% | 33,5% | 32,9% | 33,1% |

La caida es la rotacion desde instrumentos del BCRA hacia credito que arranca
en el segundo semestre de 2024.

`lefi` y `leliq` quedan en la base como variables descriptivas, puestas a
missing fuera de la vida de cada instrumento para que ningun promedio lea un
cero artificial como tenencia nula. `titpub_ars` y `titpub_usd`, que suman
solo las especies de titulos publicos, quedan tambien como descriptivas.

## Verificacion

`Code/output/tablas/chk_liq_publica_agregado.csv` tiene la serie agregada
mensual de cada componente, 2018m1 a 2026m4, construida directamente desde
los `baldet.txt` del IEF. Sirve para contrastar que el build reproduce estos numeros.
