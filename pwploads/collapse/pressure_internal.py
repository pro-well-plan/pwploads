from ..unit_converter import convert_unit
g = 9.81        # gravity constant, [m/s2]


def inside_full(tvd, rho_fluid):

    rho_fluid = convert_unit(rho_fluid, unit_from="sg", unit_to="kg/m3")

    p_int = [g * rho_fluid * x for x in tvd]

    return p_int


def partial_evacuation(tvd, rho_mud, tvd_zone, p_zone):

    rho_mud = convert_unit(rho_mud, unit_from="sg", unit_to="kg/m3")
    tvd_mud_droplevel = tvd_zone - p_zone / (g * rho_mud)

    p_int = []
    for x in tvd:
        if x <= tvd_mud_droplevel:
            p_int.append(0)
        else:
            p_int = g * rho_mud * (x - tvd_mud_droplevel)

    return p_int


def full_evacuation(tvd):
    p_int = [0] * len(tvd)

    return p_int
