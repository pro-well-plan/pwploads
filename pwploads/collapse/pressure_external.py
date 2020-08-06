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


def injection(tvd, tvd_perf, p_inj, rho_inj, tvd_influencedzone, rho_fluid, p_fric, rho_form, g):
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
