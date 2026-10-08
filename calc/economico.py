"""Evaluación económica preliminar (viabilidad) - sistema FV 20,88 kWp CAA-TEC.

Todos los precios están en colones (CRC) salvo el CAPEX, en USD.
BASE FISCAL: todo el análisis se hace ANTES DE IMPUESTOS (sin IVA ni otros cargos).
El pliego ordinario del ICE se publica sin impuestos y las tarifas RED se publican
"sujetas a IVA"; para comparar en una misma base se usan los montos base de ambos.
Fuentes de tarifas: pliego ICE 2026 (Alcance N.o 161, La Gaceta N.o 236, 16/12/2025;
rige del 01/01/2026 al 31/12/2026) y "Tarifas aplicables a recursos energéticos
distribuidos, julio 2026" (ICE, actualizado 29/07/2026; RE-0031-IE-2026).
Los valores marcados SUPUESTO son supuestos de diseño declarados en el documento.
"""
import numpy as np

import json, os
E1 = round(json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                       'energia.json')))['E_ac_anual_MWh'] * 1000)  # kWh, año 1 (energia.py, az 60°)
DEG = 0.004             # degradación anual a partir del año 2 (SUPUESTO, TOPCon)
VIDA = 25               # años
F_AUTO = 0.90           # fracción autoconsumida (SUPUESTO, sección de consumo)
TC = 505.0              # CRC/USD (SUPUESTO, tipo de cambio de referencia BCCR, oct. 2026)
P_KWP = 20.88
P_KW = 20.0

# Tarifas (CRC/kWh), pliego ICE 2026, sin impuestos
T_CS = 50.72            # T-CS bloque > 3000 kWh (binómica): energía; demanda 8382.41 CRC/kW
T_CO = 59.67            # T-CO bloque > 3000 kWh (binómica): energía; demanda 9861.68 CRC/kW
T_CS_MONO = 84.76       # T-CS bloque <= 3000 kWh (monómica)
ACCESO = 25.0           # tarifa de acceso sobre energía autoabastecida (SOLO tarifa monómica)
EXCED = 27.40           # compraventa de excedentes (punta/valle)
TDER = 255.0 * P_KWP * 12     # reconocimiento económico, CRC/año (SUPUESTO: sobre kWp)
INTERCON_ETAPAS = 16453 + 125978 + 116590   # etapas 1 a 3, CRC sin IVA (escenario base)
ETAPA4 = 79803                 # reinspección, CRC sin IVA, solo si la etapa 3 resulta infructuosa (DC-03-PR-21-001): contingencia
LEE_USD = 135.0                # verificación documental del inversor por ICE-LEE (DC-03-PR-21-001, etapa 2; costo externo)

OM_USD = 10.0 * P_KWP   # USD/año (SUPUESTO)
INV_REP_USD = 4000.0    # reemplazo de inversores en el año 13 (SUPUESTO)
TASA = 0.08             # tasa de descuento (SUPUESTO)


INTERCON = INTERCON_ETAPAS + LEE_USD * TC   # costo regulatorio base, CRC


COM_USD = 400.0                # SUPUESTO: router LTE + fuente con batería >= 2 h para el punto único SCADA del ICE
                               # (DC-03-IT-21-001, 5.4.7-5.4.12), solo si el abonado es binómico (escenarios A y C)


def evaluar(precio_auto, capex_usd_wp, contingencia_etapa4=False, extra_usd=0.0):
    capex = (capex_usd_wp * P_KWP * 1000 + extra_usd) * TC + INTERCON + (ETAPA4 if contingencia_etapa4 else 0)
    flujos, energia = [], []
    for n in range(1, VIDA + 1):
        e = E1 * (1 - DEG) ** (n - 1)
        ingreso = e * F_AUTO * precio_auto + e * (1 - F_AUTO) * EXCED - TDER
        costo = OM_USD * TC + (INV_REP_USD * TC if n == 13 else 0)
        flujos.append(ingreso - costo)
        energia.append(e)
    flujos = np.array(flujos)
    desc = (1 + TASA) ** -np.arange(1, VIDA + 1)
    van = -capex + (flujos * desc).sum()
    acum = np.cumsum(flujos) - capex
    pb = next((i + 1 for i, v in enumerate(acum) if v >= 0), None)
    costos_vp = capex + sum((OM_USD * TC + (INV_REP_USD * TC if n == 13 else 0) + TDER)
                            * (1 + TASA) ** -n for n in range(1, VIDA + 1))
    lcoe = costos_vp / (np.array(energia) * desc).sum()
    return dict(capex_crc=capex, ahorro1=flujos[0], pb=pb, van=van, lcoe=lcoe)


ESC = {   # (precio evitado, equipo adicional en USD)
    'A: T-CS sin tarifa de acceso': (T_CS, COM_USD),          # binómico: requiere SCADA/telecontrol
    # B: SENSIBILIDAD HIPOTÉTICA, no es un caso tarifario real del edificio: la tarifa de acceso
    # solo aplica a la tarifa monómica (T-CS <= 3000 kWh), pero ~12,6 MWh/mes llevan al bloque
    # binómico > 3000 kWh. Se evalúa de forma coherente: precio monómico menos acceso.
    'B: hipotético T-CS monómica + acceso': (T_CS_MONO - ACCESO, 0.0),   # monómico: sin SCADA
    'C: T-CO sin tarifa de acceso': (T_CO, COM_USD),          # binómico: requiere SCADA/telecontrol
}

if __name__ == '__main__':
    print(f"E1={E1:.0f} kWh  T_CS={T_CS:.1f}  T_CO={T_CO:.1f}  TDER={TDER:.0f}")
    print(f"Etapas 1-3 (sin IVA) = {INTERCON_ETAPAS:.0f} CRC; ICE-LEE = {LEE_USD*TC:.0f} CRC; base regulatoria = {INTERCON:.0f} CRC; "
          f"etapa 4 (contingencia) = {ETAPA4:.0f} CRC")
    for nombre, (p, x) in ESC.items():
        r = evaluar(p, 1.10, extra_usd=x)
        print(f"{nombre:38s} precio={p:6.1f}  ahorro1={r['ahorro1']/1e6:5.2f} MCRC "
              f"({r['ahorro1']/TC:6.0f} USD)  PB={r['pb']}  VAN={r['van']/1e6:6.2f} MCRC "
              f"({r['van']/TC:7.0f} USD)  LCOE={r['lcoe']:5.1f} CRC/kWh")
    print("\nSensibilidad del retorno simple (años) al CAPEX:")
    for capex in (0.9, 1.1, 1.3, 1.5):
        print(capex, [evaluar(p, capex, extra_usd=x)['pb'] for p, x in ESC.values()],
              [round(float(evaluar(p, capex, extra_usd=x)['lcoe']), 1) for p, x in ESC.values()])
    print("\nContingencia: reinspección (etapa 4) si la etapa 3 resulta infructuosa:")
    for nombre, (p, x) in ESC.items():
        r = evaluar(p, 1.10, contingencia_etapa4=True, extra_usd=x)
        print(f"{nombre:38s} PB={r['pb']}  VAN={r['van']/1e6:6.2f} MCRC  LCOE={r['lcoe']:5.1f} CRC/kWh")
