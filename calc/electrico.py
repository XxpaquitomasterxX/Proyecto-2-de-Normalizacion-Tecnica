"""Cálculos eléctricos, estructurales y de viento - memoria de cálculo."""
import math

# ---------------- Datos de hojas técnicas ----------------
MOD = dict(P=580, Vmp=43.1, Imp=13.46, Voc=52.2, Isc=13.93, bVoc=-0.0025,
           aIsc=0.0005, g=-0.0029, peso=31.6, L=2.278, W=1.134)   # CS6W-580TB-AG
OPT = dict(P=650, Vin_max=85.0, Isc_max=15.0, Iout_max=15.0, Vout_max=80.0,
           eff=0.986, Vsafe=1.0, peso=0.79)                           # S650B
INV = dict(Pac=10000, Iac=27.8, Pdc_max=17500, Vdc_max=600, Vop_min=370,
           Idc_max=27.8, P_string_max=7800, P_string_nom=6000, n_min=8, n_max=25)  # SE10KUS + S650B, red 208 V
N_MOD, N_STR, N_INV = 36, 4, 2
MOD_STR = N_MOD // N_STR

out = {}
# ---------------- Potencias ----------------
out['Pdc_kWp'] = N_MOD * MOD['P'] / 1000
out['Pac_kW'] = N_INV * INV['Pac'] / 1000
out['DC_AC'] = out['Pdc_kWp'] / out['Pac_kW']
out['Pdc_inv'] = N_MOD / N_INV * MOD['P'] / 1000
out['P_string'] = MOD_STR * MOD['P']

# ---------------- Tensión por temperatura (módulo -> optimizador) ----------------
T_MIN, T_CEL_MAX = 5.0, 70.0
out['Voc_frio'] = MOD['Voc'] * (1 + MOD['bVoc'] * (T_MIN - 25))
out['Isc_cal'] = MOD['Isc'] * (1 + MOD['aIsc'] * (T_CEL_MAX - 25))
out['Vmp_cal'] = MOD['Vmp'] * (1 + MOD['g'] * (T_CEL_MAX - 25))     # cribado
out['Vsafe_string'] = MOD_STR * OPT['Vsafe']

# ---------------- Corriente de string (salida de optimizadores) ----------------
out['I_str_Vmin'] = out['P_string'] * OPT['eff'] / INV['Vop_min']
out['I_inv_Vmin'] = 2 * out['I_str_Vmin']
out['I_str_400'] = out['P_string'] * OPT['eff'] / 400

# ---------------- Conductores DC (NEC 690.8) ----------------
I_dc_max = OPT['Iout_max']               # 690.8(A)(1)(b): salida del convertidor
out['I_dc_max'] = I_dc_max
out['I_dc_cond'] = 1.25 * I_dc_max       # 690.8(B)(1)
A10_90 = 40.0                            # #10 Cu 90 °C, Tabla 310.16
F_T = 0.96                               # 90 °C, ambiente 31-35 °C, Tabla 310.15(B)(1)
F_AG = 0.80                              # 4-6 conductores portadores, Tabla 310.15(C)(1)
out['A10_corr'] = A10_90 * F_T * F_AG
L_DC = 30.0                              # m, ruta más larga medida sobre planos
R10 = 4.07e-3                            # ohm/m, #10 Cu trenzado a 75 °C, NEC Cap. 9 Tabla 8
out['dV_dc'] = 2 * L_DC * out['I_str_Vmin'] * R10
out['dV_dc_pct'] = out['dV_dc'] / INV['Vop_min'] * 100

# ---------------- Conductores y protecciones AC ----------------
out['I_ocpd_inv'] = 1.25 * INV['Iac']
A8_75 = 50.0; A4_75 = 85.0; F_T75 = 0.94
out['A8_corr'] = A8_75 * F_T75
out['I_tot'] = N_INV * INV['Iac']
out['I_ocpd_tot'] = 1.25 * out['I_tot']
out['A4_corr'] = A4_75 * F_T75
R8, R4 = 2.551e-3, 1.01e-3               # ohm/m a 75 °C, Cap. 9 Tabla 8 (0,778 y 0,308 ohm/kft)
L_INV, L_ALIM = 3.0, 6.0                # m: INV->TFV; TFV->IFV->CD-FV (con holgura)
out['dV_inv_pct'] = math.sqrt(3) * INV['Iac'] * R8 * L_INV / 208 * 100
out['dV_alim_pct'] = math.sqrt(3) * out['I_tot'] * R4 * L_ALIM / 208 * 100
# Nuevo interruptor secundario IS-TS01 de 400 A a la salida de TS-01 (240.21(C)(2)):
# el tramo IS-TS01 -> ATS pasa a ser un alimentador protegido en su origen.
I_prim = 200
IS_TS01 = 400
out['IS_TS01'] = IS_TS01
# regla de derivación de 3 m (240.21(B)(1)) con 705.12(B)(2)(2): OCPD del alimentador + 125 % de la fuente FV
out['tap_10'] = (IS_TS01 + 1.25 * out['I_tot']) / 10
# regla de alimentadores (NEC 705.12, alimentadores) sobre secundario TS-01
A_sec = 2 * 230.0                        # 2 x #4/0 Cu 75 °C por fase
out['A_sec'] = A_sec
out['TP_main'] = 400
# 240.21(C)(2): conductores TS-01 -> IS-TS01 (<= 3 m): ampacidad >= capacidad del interruptor
out['C2_ok'] = A_sec >= IS_TS01
# 450.3(B): protección de TS-01 (primario 200 A; secundario LA36400 de 400 A)
I1n, I2n = 112.5e3 / (math.sqrt(3) * 480), 112.5e3 / (math.sqrt(3) * 208)
out.update(TS01_I1n=I1n, TS01_I2n=I2n, TS01_prim_max=2.5 * I1n, TS01_sec_max=1.25 * I2n)
# comprobación alternativa A (barras del TP instalado: 800 A, principal 400 A)
out['regla120_lim'] = 1.2 * 800
out['regla120_req'] = 400 + out['I_ocpd_tot']

# ---------------- Corriente de falla disponible (NEC 110.9, 110.10, 110.24) ----------------
# TS-01: Z = 3,57 % de placa; X/R = 3 (supuesto típico para transformador seco de 112,5 kVA);
# fuente aguas arriba considerada infinita (cota superior).
V_LL = 208.0
Zb = V_LL ** 2 / 112.5e3
Zt = 0.0357 * Zb
Rt = Zt / math.sqrt(1 + 3 ** 2); Xt = 3 * Rt
def falla(R, X):
    return V_LL / math.sqrt(3) / math.hypot(R, X)
out['Icc_TS01_kA'] = falla(Rt, Xt) / 1000
# Conductor #4 Cu en EMT (NEC Cap. 9 Tabla 9): R = 1,02 ohm/km, XL = 0,187 ohm/km
R4c, X4c = 1.02e-3, 0.187e-3
L_IFV, L_TFV = 3.0 + 3.0, 3.0 + 3.0 + 1.0     # derivación+C-AC4 hasta IFV; +C-AC3 hasta TFV
out['Icc_CD_FV_kA'] = out['Icc_TS01_kA']
out['Icc_IFV_kA'] = falla(Rt + R4c * L_IFV, Xt + X4c * L_IFV) / 1000
out['Icc_TFV_kA'] = falla(Rt + R4c * L_TFV, Xt + X4c * L_TFV) / 1000
out['I_aporte_FV'] = 1.2 * out['I_tot']   # aporte típico de inversores (≈ 1,2 In)

# ---------------- Ocupación de canalizaciones (NEC Cap. 9, Tablas 1, 4 y 5) ----------------
D_PV = 5.8e-3                            # m, diámetro exterior PV Wire #10 (supuesto de compra)
A_pv = math.pi / 4 * (D_PV * 1e3) ** 2   # mm2
out['fill_dc_mm2'] = 4 * A_pv + 13.6     # 4 PV Wire + EGC #10 THWN-2
out['fill_dc_lim_34'] = 0.40 * 343
out['fill_ac4_mm2'] = 4 * 53.2 + 23.6    # 4 #4 + EGC #8 (THWN-2)
out['fill_ac4_lim_114'] = 0.40 * 965
out['fill_ac8_mm2'] = 4 * 23.6 + 13.6    # 4 #8 + EGC #10
out['fill_ac8_lim_34'] = 0.40 * 343

# ---------------- Cargas muertas ----------------
m_extra = 4.0
out['m_total'] = N_MOD * (MOD['peso'] + OPT['peso'] + m_extra)
A_arr = (9 * MOD['W'] + 8 * 0.025) * (4 * MOD['L'] + 3 * 0.025)
out['A_arr'] = A_arr
out['q_D'] = out['m_total'] * 9.81 / A_arr

# ---------------- Viento (Lineamientos CFIA 2023, procedimiento prescriptivo) ----------------
# Zona III: todos los distritos del cantón de Alajuela (Tabla 3-1); Vb = 115 km/h (Figura 3-1, TR = 50 años)
G = 9.80665
Vb = 115.0
qb = 0.005 * Vb ** 2          # kg/m2 (Ec. 3-1)
h = 8.2                       # m (A02)
Ce = 2.01 * (max(h, 4.0) / 274) ** (2 / 9.5)    # exposición C: alfa = 9,5; zg = 274 m; zmin = 4 m (Tabla 3-2)
Ct = 1.0
def Cr(TR):                   # Tabla 3-3, zonas II a V
    return (0.36 + 0.10 * math.log(12 * TR)) ** 2
# Categoría de diseño por viento II (Especial) -- SUPUESTO conservador (CSCR grupo C: > 300 estudiantes)
# servicio: TR = 50 años, Cd = 1,0 (3.3.4); último NDU-1: TR = 1700 años, Cd = 0,85 (Tabla 3-5)
CASOS = {'serv_II': (50, 1.0), 'ult_II': (1700, 0.85), 'serv_III': (10, 1.0), 'ult_III': (700, 0.85)}
out.update(Vb=Vb, qb=qb, Ce=Ce)
for k, (TR, Cd) in CASOS.items():
    out['Cr_' + k] = Cr(TR)
    out['qh_Pa_' + k] = qb * Ce * Cr(TR) * Ct * Cd * G
# Componentes de techo de un agua, 3° < theta <= 10° (Figura A-13), zona interior 1: GCp = -1,1;
# positivo +0,3 (<= 0,9 m2) a +0,2 (>= 9,3 m2), interpolado en log(A) para el área de un módulo.
# Edificio cerrado: GCpi = +/-0,18 (Tabla 4-1). Ec. 4-8: p = q_h [(GCp) - (GCpi)].
A_mod = MOD['L'] * MOD['W']
GCp_neg = -1.1
GCp_pos = 0.3 - 0.1 * math.log10(A_mod / 0.93) / math.log10(9.3 / 0.93)
GCpi = 0.18
out.update(A_mod=A_mod, GCp_neg=GCp_neg, GCp_pos=GCp_pos)
for k in ('serv_II', 'ult_II'):
    out['p_up_' + k] = out['qh_Pa_' + k] * (GCp_neg - GCpi)
    out['p_down_' + k] = out['qh_Pa_' + k] * (GCp_pos + GCpi)
P_MIN = 80 * G                # 4.4.3.1: presión neta mínima de componentes, 80 kg/m2 (carga última)
out['p_min_comp'] = P_MIN
p_ult = max(abs(out['p_up_ult_II']), P_MIN)
p_serv = abs(out['p_up_serv_II'])
out['p_up_diseno_ult'] = p_ult
out['a_borde'] = max(min(0.1 * 15.05, 0.4 * h), max(0.04 * 15.05, 0.9))
W_mod = (MOD['peso'] + OPT['peso']) * 9.81
# Combinación última 0,9 CP - CV (Ec. 5-4); servicio CP - CVs (Ec. 5-5, sin carga temporal)
F_ult = p_ult * A_mod - 0.9 * W_mod
F_serv = p_serv * A_mod - 1.0 * W_mod
out['F_mod_ult'] = F_ult
out['F_mod_serv'] = F_serv
# Cada módulo se apoya en 4 abrazaderas (2 costillas x 2 líneas de apoyo). En las 3 líneas
# interiores cada abrazadera recibe la mitad de dos módulos contiguos (2 x F/4).
out['F_clamp_borde_ult'] = F_ult / 4
out['F_clamp_ult'] = 2 * F_ult / 4                 # abrazadera interior, carga mayorada
out['F_clamp_serv'] = 2 * F_serv / 4               # abrazadera interior, servicio
out['F_clamp_ensayo_req'] = 2 * out['F_clamp_ult'] # factor de seguridad 2 de S-5! sobre la carga mayorada
out['F_total_ult_kN'] = N_MOD * F_ult / 1000
out['n_clamps'] = 5 * 2 * 9
out['p_ult_vs_mod'] = p_ult / (4000 / 1.5)         # carga de diseño del módulo: 4000 Pa / 1,5
out['p_ult_vs_pvkit'] = p_ult / (30 * 47.88)       # 30 psf de succión, tabla UL 2703 del PVKIT

# ---------------- Riesgo por rayo (NFPA 780-2023, Anexo L, método simplificado) ----------------
Ng = 15.0                     # rayos/km2/año, SUPUESTO conservador para el Valle Central
L_ed, W_ed, H_ed = 18.0, 15.05, 10.0          # m (A04, A02)
Ae = L_ed * W_ed + 6 * H_ed * (L_ed + W_ed) + 9 * math.pi * H_ed ** 2
C1 = 0.5                      # rodeado de estructuras y árboles de menor o igual altura
out['rayo_Ae_m2'] = Ae
out['rayo_Nd'] = Ng * Ae * C1 * 1e-6
C2, C3, C4, C5 = 0.5, 1.0, 1.0, 1.0           # metal/metal, contenido normal, ocupado, sin continuidad crítica
out['rayo_Nc'] = 1.5e-3 / (C2 * C3 * C4 * C5)
out['rayo_Ng_umbral'] = out['rayo_Nc'] / (Ae * C1 * 1e-6)

# ---------------- Consumo estimado ----------------
P_dia, P_base = 35.0, 8.0
E_lab = 250 * (12 * P_dia + 12 * P_base)
E_fin = 115 * 24 * P_base
out['E_cons_MWh'] = (E_lab + E_fin) / 1000

for k, v in out.items():
    print(f"{k:20s} {v:10.3f}" if isinstance(v, float) else f"{k:20s} {v}")
