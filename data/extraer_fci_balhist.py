"""
Extrae de raw/balhist.txt las cuentas de deposito relevantes para el canal
billeteras-FCI y las guarda en raw/fci_cuentas.csv (ent, fecha, cuenta, saldo):
  311706  cuentas corrientes sin interes, sector privado no financiero
  311723  cta cte especial de personas juridicas, sin interes
  311724  cta cte especial de personas juridicas, con interes (aca depositan los FCI MM)
Los saldos vienen con signo debe-haber: las cuentas de pasivo quedan negativas.
Uso: python extraer_fci_balhist.py
"""
import os

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "raw", "balhist.txt")
dst = os.path.join(here, "raw", "fci_cuentas.csv")
codigos = {"311706", "311723", "311724"}

n = 0
with open(src, encoding="latin1") as f, open(dst, "w") as g:
    g.write("ent,fecha,cuenta,saldo\n")
    for line in f:
        p = line.rstrip("\r\n").split("\t")
        if len(p) >= 4 and p[2].strip('"') in codigos:
            g.write(f"{p[0].strip(chr(34))},{p[1].strip(chr(34))},{p[2].strip(chr(34))},{p[3]}\n")
            n += 1
print(f"{n} filas -> {dst}")
