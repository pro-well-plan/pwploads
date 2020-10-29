from ..unit_converter import convert_unit
g = 9.81        # gravity constant, [m/s2]


def onefluid_behindcasing(tvd, rho_mud):
    """
    Calculate external pressure profile with one fluid behind casing.
    :param tvd: list - true vertical depth, m
    :param rho_mud: mud density, sg
    :return: internal pressure profile, Pa
    """

    rho_mud = convert_unit(rho_mud, unit_from="sg", unit_to="kg/m3")

    p_ext = [g * rho_mud * x for x in tvd]

    return p_ext


def morefluids_behindcasing(tvd, rho_fluid, tvd_fluid):
    """
    Calculate external pressure profile with more than one fluid behind casing.
    :param tvd: list - true vertical depth, m
    :param rho_fluid: list - downwards sorted fluids densities, sg
    :param tvd_fluid: list - reference tvd of fluid change, m
    :return: internal pressure profile, Pa
    """
    rho_fluid = [convert_unit(x, unit_from="sg", unit_to="kg/m3") for x in rho_fluid]  # convert sg to kg/m3

    tvd_fluid.append(tvd[-1])

    p_prev = 0
    tvd_fluid_prev = 0
    rho_fluid = iter(rho_fluid)
    tvd_fluid = iter(tvd_fluid)
    rho_fluid_selected = next(rho_fluid)
    tvd_fluid_selected = next(tvd_fluid)

    p_ext = []
    for x in tvd:
        p = g * rho_fluid_selected * (x - tvd_fluid_prev) + p_prev

        if (x >= tvd_fluid_selected) and (tvd_fluid_selected != tvd[-1]):
            tvd_fluid_prev = tvd_fluid_selected
            tvd_fluid_selected = next(tvd_fluid)
            rho_fluid_selected = next(rho_fluid)
            p_prev = p
        p_ext.append(p)
    return p_ext


def depleted_zone(tvd, tvd_zone, p_zone, rho_mud):
    """
    Calculate external pressure profile with a depleted zone.
    :param tvd: list - true vertical depth, m
    :param tvd_zone: tvd at depleted zone, m
    :param p_zone: pressure at depleted zone, bar
    :param rho_mud: mud density, sg
    :return: internal pressure profile, Pa
    """

    p_zone = convert_unit(p_zone, unit_from="bar", unit_to="Pa")
    rho_mud = convert_unit(rho_mud, unit_from="sg", unit_to="kg/m3")

    tvd_mud_droplevel = tvd_zone - p_zone / (g * rho_mud)

    p_ext = []
    for x in tvd:
        if x <= tvd_mud_droplevel:
            p_ext.append(0)
        else:
            p_ext = g * rho_mud * (x - tvd_mud_droplevel)

    return p_ext
