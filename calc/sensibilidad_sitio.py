"""Sensibilidad de la producción a la orientación y a las sombras del entorno.

Caso de diseño (energia.py): azimut 60° (ENE, confirmado con la imagen satelital y
los rumbos del registro fotográfico del 5/10/2026) y árboles 4 m más altos que la
cubierta. Se comparan:
- Azimut 90°: orientación nominal deducida de las fachadas de A02 (ejes alineados
  con los puntos cardinales).
- Azimut 150°: la otra lectura posible de la imagen satelital, descartada con las
  fotografías; se conserva como referencia.
- Horizonte: sin árboles, árboles 4 m y 10 m más altos que la cubierta, en los
  sectores medidos en la imagen satelital (ONO 280-315° a ~15 m, ESE-S 100-180°
  a ~14 m, SSO 190-210° a ~17 m).
"""
import contextlib
import io

with contextlib.redirect_stdout(io.StringIO()):
    import energia as e

BASE = e.df.E_ac.sum()


def correr(az, horizonte):
    e.AZ, e.HORIZONTE = az, list(horizonte)
    return e.anual(e.GHI_MJ).E_ac.sum()


if __name__ == '__main__':
    print(f"Caso de diseño (az 60°, árboles +4 m): {BASE:.2f} MWh")
    for nombre, hz in (('Sin árboles', []), ('Árboles +4 m', e.sectores(4.0)),
                       ('Árboles +10 m', e.sectores(10.0))):
        fila = []
        for az in (60.0, 90.0, 150.0):
            E = correr(az, hz)
            fila.append(f"az {az:.0f}°: {E:.2f} MWh ({(E / BASE - 1) * 100:+.1f} %)")
        print(f"{nombre:14s} | " + " | ".join(fila))
    # aporte de cada sombra en el caso de diseño
    e.AZ = 60.0
    e.HORIZONTE = []
    e.FRAC_FILA_BAK = e.FRAC_FILA
    E_sin_arb = e.anual(e.GHI_MJ).E_ac.sum()
    e.FRAC_FILA = 0.0
    E_sin_nada = e.anual(e.GHI_MJ).E_ac.sum()
    print(f"Pérdida por condensadoras: {(1 - E_sin_arb / E_sin_nada) * 100:.2f} %")
    print(f"Pérdida por árboles +4 m: {(1 - BASE / E_sin_arb) * 100:.2f} %")
