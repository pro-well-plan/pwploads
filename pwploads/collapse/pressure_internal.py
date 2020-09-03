g = 9.81        # gravity constant, [m/s2]


def inside_full(tvd, rho_fluid):
    p_int = [g * rho_fluid * x for x in tvd]

    return p_int


def partial_evacuation(tvd, rho_mud, tvd_zone, p_zone):
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
