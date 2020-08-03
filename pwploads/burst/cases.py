def drilling_influx_1(tvd, rho_fluid, rho_mud, tvd_frac, frac_gradient, g):
    from .pressure_internal import frac_shoe_gas_grad_above
    from .pressure_external import onefluid_behindcasing

    p_int = frac_shoe_gas_grad_above(tvd, frac_gradient, tvd_frac, rho_fluid, g)
    p_ext = onefluid_behindcasing(tvd, rho_mud, g)

    pressure_differential = p_int - p_ext

    return pressure_differential


def drilling_influx_2(tvd, rho_mud, tvd_next_section, g, fraction=0.5):
    from .pressure_internal import fraction_of_bhp_at_wh
    from .pressure_external import onefluid_behindcasing

    p_int = fraction_of_bhp_at_wh(tvd, rho_mud, tvd_next_section, g, fraction)
    p_ext = onefluid_behindcasing(tvd, rho_mud, g)

    pressure_differential = p_int - p_ext

    return pressure_differential


def drilling_influx_3(tvd, rho_mud, id_csg, od_dp, tvd_kick, kick_intensity, rho_kick_initial, vol_kick_initial, g):
    from .pressure_internal import gas_kick
    from .pressure_external import onefluid_behindcasing

    p_int = gas_kick(tvd, rho_mud, kick_intensity, tvd_kick, vol_kick_initial, rho_kick_initial, id_csg, od_dp, g)
    p_ext = onefluid_behindcasing(tvd, rho_mud, g)

    pressure_differential = p_int - p_ext

    return pressure_differential
