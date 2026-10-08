"""Estimación mensual de producción FV - Edificio CAA-TEC (Alajuela).

Método (documentado en la memoria de cálculo):
1. Irradiación global horizontal media diaria mensual: IMN, estación Aeropuerto
   Juan Santamaría (10°00'N, 84°12'W, 932 m) [Castro, 1987].
2. Para cada mes se usa el día característico (Klein, 1977); el perfil horario
   de cielo despejado (Ineichen) se escala para reproducir la GHI diaria del IMN.
3. Separación difusa/directa con Erbs; transposición Hay-Davies al plano de la
   cubierta (8,53°, azimut 60°, ENE: orientación confirmada con la imagen
   satelital y el registro fotográfico del 5/10/2026).
4. Temperatura de celda con el modelo SAPM "close_mount_glass_glass" (montaje
   coplanar cercano a la cubierta); ambiente: media anual 22,3 °C ± 5 °C.
5. Sombras de las condensadoras (losa eje 01-04): obstáculo continuo en el
   extremo alto de la cubierta (azimut AZ + 180°).
6. Horizonte lejano: árboles 4 m más altos que la cubierta (escenario
   representativo según las fotografías) en los sectores medidos en la imagen
   satelital.
7. Pérdidas restantes por tabla (supuestos declarados).
"""
import json
import numpy as np
import pandas as pd
import pvlib

LAT, LON, ALT = 10.0057, -84.2164, 950.0    # GPS de las fotografías del 5/10/2026 (V7)
TILT = np.degrees(np.arctan(0.15))          # 8.53°
AZ = 60.0                                   # cubierta cae hacia el ENE (confirmado en sitio, V8)
PDC = 36 * 580.0                            # W
GAMMA = -0.0029                             # 1/°C (CS6W-580TB-AG)

# IMN, Aeropuerto Juan Santamaría, MJ/m2/día (Castro, 1987)
GHI_MJ = [20, 22, 24, 23, 19, 18, 18, 18, 17, 17, 16, 17]
# Sensibilidad: estación Fabio Baudrit (840 m)
GHI_MJ_FB = [19, 21, 22, 20, 17, 15, 16, 16, 16, 15, 15, 17]
DIAS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
DIA_CAR = [17, 16, 16, 15, 15, 11, 17, 16, 15, 15, 14, 10]  # Klein (1977)

TAMB_MEDIA, TAMB_AMP, VIENTO = 22.3, 5.0, 2.0

# Geometría de sombra (condensadoras al oeste del arreglo)
D_OBS = 3.24          # m, distancia horizontal borde losa -> fila superior
H_OBS = 1.50          # m, altura de condensadora + base sobre la cubierta (supuesto)
DH = H_OBS + 0.15 * D_OBS   # la cubierta desciende 15 % hacia el arreglo
PSI_LIM = np.degrees(np.arctan(DH / D_OBS))
FRAC_FILA = 9 / 36    # la fila superior (string S1) es 1/4 del arreglo

# Horizonte lejano (árboles/edificios): lista de (azimut_min, azimut_max, elevación °).
# Caso de diseño: árboles 4 m más altos que la cubierta, a 15, 14 y 17 m del borde
# (imagen satelital; altura de copa estimada con las fotografías).
import math as _m
def sectores(dh):
    el = lambda d: _m.degrees(_m.atan(dh / d))
    return [(280, 315, el(15)), (100, 180, el(14)), (190, 210, el(17))]
HORIZONTE = sectores(4.0)

loc = pvlib.location.Location(LAT, LON, tz='America/Costa_Rica', altitude=ALT)
temp_par = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS['sapm']['close_mount_glass_glass']


def mes(m, ghi_mj):
    dia = pd.Timestamp(2026, m + 1, DIA_CAR[m], tz='America/Costa_Rica')
    t = pd.date_range(dia, dia + pd.Timedelta('23h55min'), freq='5min')
    sp = loc.get_solarposition(t)
    cs = loc.get_clearsky(t, model='ineichen', solar_position=sp)
    ghi_obj = ghi_mj / 3.6 * 1000            # Wh/m2/día
    k = ghi_obj / (cs['ghi'].sum() * 5 / 60)
    ghi = cs['ghi'] * k
    dni_extra = pvlib.irradiance.get_extra_radiation(t)
    erbs = pvlib.irradiance.erbs(ghi, sp['apparent_zenith'], t)
    poa = pvlib.irradiance.get_total_irradiance(
        TILT, AZ, sp['apparent_zenith'], sp['azimuth'],
        erbs['dni'], ghi, erbs['dhi'], dni_extra=dni_extra, model='haydavies')
    aoi = pvlib.irradiance.aoi(TILT, AZ, sp['apparent_zenith'], sp['azimuth'])
    iam = pvlib.iam.physical(aoi).fillna(0)
    poa_eff = poa['poa_direct'] * iam + poa['poa_diffuse'] * 0.95
    hora = t.hour + t.minute / 60
    tamb = TAMB_MEDIA + TAMB_AMP * np.cos((hora - 14) / 24 * 2 * np.pi)
    tcel = pvlib.temperature.sapm_cell(poa['poa_global'], tamb, VIENTO, **temp_par)
    # sombra: ángulo de perfil en el plano de la pendiente; las condensadoras están
    # en el extremo alto, en la dirección AZ + 180°
    alt = 90 - sp['apparent_zenith']
    daz = np.radians(sp['azimuth'] - (AZ + 180.0))
    with np.errstate(divide='ignore', invalid='ignore'):
        psi = np.degrees(np.arctan(np.tan(np.radians(alt)) / np.cos(daz)))
    sombra = (np.cos(daz) > 0) & (alt > 0) & (psi < PSI_LIM)
    beam_sombra = (poa['poa_direct'] * iam).where(sombra, 0) * FRAC_FILA
    if HORIZONTE:
        bloq = pd.Series(False, index=t)
        for az1, az2, el in HORIZONTE:
            bloq |= (sp['azimuth'] >= az1) & (sp['azimuth'] <= az2) & (alt > 0) & (alt < el)
        beam_sombra = (poa['poa_direct'] * iam).where(bloq, beam_sombra)
    dt = 5 / 60
    H_ghi = ghi.sum() * dt
    H_poa = poa['poa_global'].clip(lower=0).sum() * dt
    H_eff = poa_eff.clip(lower=0).sum() * dt
    H_shd = beam_sombra.sum() * dt
    # energía DC antes de pérdidas por tabla (W h/día), con temperatura
    p_dc = PDC * (poa_eff - beam_sombra).clip(lower=0) / 1000 * (1 + GAMMA * (tcel - 25))
    E_dc = p_dc.sum() * dt
    tcel_pond = (tcel * poa['poa_global'].clip(lower=0)).sum() / poa['poa_global'].clip(lower=0).sum()
    return dict(H_ghi=H_ghi, H_poa=H_poa, H_eff=H_eff, H_shd=H_shd, E_dc=E_dc,
                tcel=tcel_pond)


# Pérdidas restantes (fracciones), supuestos declarados
PERDIDAS = {
    'suciedad': 0.03,
    'sombras del entorno no modeladas (árboles/edificios)': 0.01,
    'calidad del módulo / LID / degradación año 1': 0.01,
    'desajuste (mismatch) con optimizadores': 0.005,
    'optimizadores S650B (eficiencia ponderada 98,6 %)': 0.014,
    'cableado DC': 0.009,          # 0,92 % (R #10 = 4,07 ohm/km, NEC Cap. 9 T8)
    'inversor (eficiencia CEC 97 %)': 0.03,
    'cableado AC': 0.005,          # 0,46 % (R #8 = 2,55; #4 = 1,01 ohm/km)
    'disponibilidad': 0.01,
}
f_rest = np.prod([1 - v for v in PERDIDAS.values()])


def anual(ghi_list):
    filas = []
    for m in range(12):
        r = mes(m, ghi_list[m])
        n = DIAS[m]
        filas.append(dict(mes=m + 1,
                          GHI=r['H_ghi'] / 1000 * n, POA=r['H_poa'] / 1000 * n,
                          E_dc=r['E_dc'] / 1e6 * n, H_eff=r['H_eff'] / 1000 * n,
                          H_shd=r['H_shd'] / 1000 * n, tcel=r['tcel']))
    df = pd.DataFrame(filas)
    df['E_ac'] = df['E_dc'] * f_rest
    return df


df = anual(GHI_MJ)
df_fb = anual(GHI_MJ_FB)
G, P = df.GHI.sum(), df.POA.sum()
res = {
    'tilt': TILT, 'psi_lim': PSI_LIM,
    'GHI_anual': G, 'POA_anual': P, 'f_transp': P / G,
    'f_iam': df.H_eff.sum() / P,
    'f_sombra': 1 - df.H_shd.sum() / df.H_eff.sum(),
    'E_ac_anual_MWh': df.E_ac.sum(), 'E_ac_FB_MWh': df_fb.E_ac.sum(),
    'yield_kWh_kWp': df.E_ac.sum() * 1000 / (PDC / 1000),
    'PR_vs_POA': df.E_ac.sum() * 1e3 / (PDC / 1000 * P),
    'PR_vs_GHI': df.E_ac.sum() * 1e3 / (PDC / 1000 * G),
    'f_rest': f_rest,
    'mensual': df.round(3).to_dict(orient='records'),
}
# pérdida por temperatura: energía DC con temperatura vs. sin temperatura
E_sin_t = (df.H_eff - df.H_shd).sum() * PDC / 1e6   # MWh
res['f_temp'] = df.E_dc.sum() / E_sin_t
res['tcel_media_pond'] = float((df.tcel * df.POA).sum() / df.POA.sum())
print(json.dumps({k: v for k, v in res.items() if k != 'mensual'}, indent=1))
print(df.round(2).to_string())
json.dump(res, open('energia.json', 'w'), indent=1, default=float)
