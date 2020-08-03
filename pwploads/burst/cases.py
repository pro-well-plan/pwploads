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


def pressure_test_onefluid(tvd, p_test, rho_mud, g):
    from .pressure_internal import pressure_test
    from .pressure_external import onefluid_behindcasing

    p_int = pressure_test(tvd, p_test, rho_mud, g)
    p_ext = onefluid_behindcasing(tvd, rho_mud, g)

    pressure_differential = p_int - p_ext

    return pressure_differential


def pressure_test_morefluids(tvd, p_test, rho_mud, rho_fluid, tvd_fluid, g):
    from .pressure_internal import pressure_test
    from .pressure_external import morefluids_behindcasing

    p_int = pressure_test(tvd, p_test, rho_mud, g)
    p_ext = morefluids_behindcasing(tvd, rho_fluid, tvd_fluid, g)

    pressure_differential = p_int - p_ext

    return pressure_differential


def production_with_packer(tvd, rho_fluid, rho_mud, p_res, tvd_perf, rho_packerfluid, tvd_packer, g):
    from .pressure_internal import tubing_leak
    from .pressure_external import onefluid_behindcasing

    p_int = tubing_leak(tvd, p_res, rho_fluid, tvd_perf, rho_packerfluid, tvd_packer, rho_mud, g)
    p_ext = onefluid_behindcasing(tvd, rho_mud, g)

    pressure_differential = p_int - p_ext

    return pressure_differential


def production_with_packer_and_depletedzone(tvd, rho_fluid, rho_mud, p_res, tvd_perf, rho_packerfluid, tvd_packer, g,
                                            tvd_zone, p_zone):
    from .pressure_internal import tubing_leak
    from .pressure_external import depleted_zone

    p_int = tubing_leak(tvd, p_res, rho_fluid, tvd_perf, rho_packerfluid, tvd_packer, rho_mud, g)
    p_ext = depleted_zone(tvd, tvd_zone, p_zone, rho_mud, g)

    pressure_differential = p_int - p_ext

    return pressure_differential


def production_without_packer(tvd, p_res, rho_gas, tvd_res, rho_mud, g):
    from .pressure_internal import displacement_to_gas
    from .pressure_external import onefluid_behindcasing

    p_int = displacement_to_gas(tvd, p_res, rho_gas, tvd_res, g)
    p_ext = onefluid_behindcasing(tvd, rho_mud, g)

    pressure_differential = p_int - p_ext

    return pressure_differential


def production_without_packer_and_depletedzone(tvd, p_res, rho_gas, tvd_res, tvd_zone, p_zone, rho_mud, g):
    from .pressure_internal import displacement_to_gas
    from .pressure_external import depleted_zone

    p_int = displacement_to_gas(tvd, p_res, rho_gas, tvd_res, g)
    p_ext = depleted_zone(tvd, tvd_zone, p_zone, rho_mud, g)

    pressure_differential = p_int - p_ext

    return pressure_differential


def stimulation(tvd, whp, rho_injectionfluid, rho_mud, rho_packerfluid, g, tvd_packer=0):
    from .pressure_internal import tubing_leak_stimulation
    from .pressure_external import onefluid_behindcasing

    p_int = tubing_leak_stimulation(tvd, whp, rho_packerfluid, rho_injectionfluid, g, tvd_packer)
    p_ext = onefluid_behindcasing(tvd, rho_mud, g)

    pressure_differential = p_int - p_ext

    return pressure_differential

