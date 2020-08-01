def fraction_of_bhp_at_wh(tvd, rho_mud, tvd_next_section, fraction=0.5, g):
    bhp = g * rho_mud * tvd_next_section
    p_int = [fraction * bhp] * len(tvd)

    return p_int


def frac_shoe_gas_grad_above(tvd, frac_gradient, tvd_frac, rho_fluid, g):
    p_frac = frac_gradient * tvd_frac
    p_int = [p_frac - g * rho_fluid * (tvd_frac - x) for x in tvd]

    return p_int


def gas_kick(tvd, rho_mud, kick_intensity, tvd_kick, vol_kick_initial, rho_kick_initial, id_csg, od_dp, g):
    from math import pi

    bhp = g * (rho_mud + kick_intensity) * tvd_kick

    p = [g * rho_mud * x for x in tvd]

    vol_kick = [vol_kick_initial * (bhp / x) for x in p]  # * (temp/temp_kick) * (z/z_kick)
    rho_kick = [rho_kick_initial * (vol_kick_initial / x) for x in vol_kick]

    p_basekick = [bhp - g * rho_mud * (tvd_kick - x) for x in tvd]

    ir_csg = (id_csg / 2) / 12
    or_dp = (od_dp / 2) / 12
    h = [x / (pi * (ir_csg ** 2 - or_dp ** 2)) for x in vol_kick]
    tvd_topkick = np.array([x - y for x, y in zip(tvd, h)])
    tvd_topkick[tvd_topkick < 0] = 0

    p_topkick = [a - g * b * (c - d) for a, b, c, d in zip(p_basekick, rho_kick, tvd, tvd_topkick) if d >= 0]

    whp = [x - g * rho_mud * y for x, y in zip(p_topkick, tvd_topkick)]

    p_int = [max(whp) + ((bhp - max(whp)) / (tvd_kick)) * x for x in tvd]

    return p_int


def displacement_to_gas(tvd, p_res, rho_gas, tvd_res, g):
    p_int = [p_res - g * rho_gas * (tvd_res - x) for x in tvd]

    return p_int


def pressure_test(tvd, p_test, rho_mud, g):
    p_int = [p_test + g * rho_mud * x for x in tvd]

    return p_int


def tubing_leak(tvd, p_res, rho_fluid, tvd_perf, rho_packerfluid, tvd_packer, rho_mud, g):
    whp = p_res - g * rho_fluid * tvd_perf
    p_int = [whp + g * rho_packerfluid * x for x in tvd if x <= tvd_packer] + \
            [p_res - g * rho_packerfluid * (tvd_perf - x) for x in tvd if (x > tvd_packer) and (x <= tvd_perf)] + \
            [p_res + g * rho_mud * (x - tvd_perf) for x in tvd if x > tvd_perf]

    return p_int


def tubing_leak_stimulation(tvd, whp, rho_packerfluid, rho_injectionfluid, tvd_packer=0):
    p_int = [whp + g * rho_packerfluid * x for x in tvd if x <= tvd_packer] + \
            [whp + g * rho_injectionfluid * x for x in tvd if x > tvd_packer]

    return p_int



