def onefluid_behindcasing(tvd, rho_mud, g):
    p_ext = [g * rho_mud * x for x in tvd]

    return p_ext


def morefluids_behindcasing(tvd, rho_fluid, tvd_fluid, g):
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


def depleted_zone(tvd, tvd_zone, p_zone, rho_mud, g):
    tvd_mud_droplevel = tvd_zone - p_zone / (g * rho_mud)

    p_ext = []
    for x in tvd:
        if x <= tvd_mud_droplevel:
            p_ext.append(0)
        else:
            p_ext = g * rho_mud * (x - tvd_mud_droplevel)

    return p_ext

