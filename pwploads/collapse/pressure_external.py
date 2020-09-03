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

    tvd_fluid.append(tvd[-1])

    p_prev = 0
    tvd_fluid_prev = 0
    rho_fluid = iter(rho_fluid)
    tvd_fluid = iter(tvd_fluid)
    rho_fluid_selected = next(rho_fluid)
    tvd_fluid_selected = next(tvd_fluid)

    p_ext = []
    for x in tvd:
        rho_fluid_selected = convert_unit(rho_fluid_selected, unit_from="sg", unit_to="kg/m3")
        p = g * rho_fluid_selected * (x - tvd_fluid_prev) + p_prev

        if (x >= tvd_fluid_selected) and (tvd_fluid_selected != tvd[-1]):
            tvd_fluid_prev = tvd_fluid_selected
            tvd_fluid_selected = next(tvd_fluid)
            rho_fluid_selected = next(rho_fluid)
            p_prev = p
        p_ext.append(p)

    return p_ext


def injection(tvd, tvd_perf, p_inj, rho_inj, tvd_influencedzone, rho_fluid, p_fric, rho_form):
    p_ext = []
    for x in tvd:
        if x <= tvd_influencedzone:
            p_ext.append(rho_fluid * g * x)
        else:
            p_ext.append(p_inj + (rho_inj * g * tvd_perf) - p_fric - (rho_form * g * (tvd_perf - x)))

    return p_ext


def gas_migration(tvd, p_res, rho_mud, g):
    p_ext = [p_res + g * rho_mud * x for x in tvd]

    return p_ext
