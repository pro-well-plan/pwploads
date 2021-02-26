def drilling_influx_1(tvd, rho_fluid, rho_mud, frac_gradient):
    """
    Calculate differential pressure profile with influx during drilling case 1 (fracture pressure at
    shoe and gas gradient above - one fluid behind the casing)
    :param tvd: list - true vertical depth, m
    :param rho_fluid: rho_fluid: fluid density, sg
    :param rho_mud: mud density, sg
    :param frac_gradient: fracture gradient, bar/m
    :return: differential pressure profile, Pa
    """

    from .pressure_internal import frac_shoe_gas_grad_above
    from .pressure_external import onefluid_behindcasing

    p_int = frac_shoe_gas_grad_above(tvd, frac_gradient, rho_fluid)
    p_ext = onefluid_behindcasing(tvd, rho_mud)

    pressure_differential = p_int - p_ext

    return pressure_differential


def drilling_influx_2(tvd, rho_mud, tvd_next_section, fraction=0.5):
    """
    Calculate differential pressure profile with influx during drilling case 2 (fraction of bhp at wh -
    one fluid behind the casing)
    :param tvd: list - true vertical depth, m
    :param rho_mud: mud density, sg
    :param tvd_next_section: tvd at bottom, m
    :param fraction: bhp fraction at wh
    :return: differential pressure profile, Pa
    """

    from .pressure_internal import fraction_of_bhp_at_wh
    from .pressure_external import onefluid_behindcasing

    p_int = fraction_of_bhp_at_wh(tvd, rho_mud, tvd_next_section, fraction)
    p_ext = onefluid_behindcasing(tvd, rho_mud)

    pressure_differential = p_int - p_ext

    return pressure_differential


def drilling_influx_3(tvd, rho_mud, id_csg, od_dp, p_res, tvd_res, vol_kick_initial):
    """
    Calculate differential pressure profile with influx during drilling case 3 (gas kick profile -
    one fluid behind the casing)
    :param tvd: list - true vertical depth, m
    :param rho_mud: mud density, sg
    :param id_csg: casing inner diameter, in
    :param od_dp: drill pipe outer diameter, in
    :param p_res: reservoir pressure, bar
    :param tvd_res: tvd at reservoir, m
    :param vol_kick_initial: influx initial volume, m3
    :return: differential pressure profile, Pa
    """

    from .pressure_internal import gas_kick
    from .pressure_external import onefluid_behindcasing

    p_int = gas_kick(tvd, rho_mud, p_res, tvd_res, vol_kick_initial, id_csg, od_dp)
    p_ext = onefluid_behindcasing(tvd, rho_mud)

    pressure_differential = [x - y for x, y in zip(p_int, p_ext)]

    return pressure_differential


def pressure_test_onefluid(tvd, p_test, rho_fluid_int, rho_fluid_ext):
    """
    Calculate differential pressure profile during pressure testing with one fluid behind the casing.
    :param tvd: list - true vertical depth, m
    :param p_test: testing pressure, bar
    :param rho_fluid_int: float - internal fluid density, sg
    :param rho_fluid_ext: float - external fluid density, sg
    :return: differential pressure profile, Pa
    """

    from .pressure_internal import pressure_test
    from .pressure_external import onefluid_behindcasing

    p_int = pressure_test(tvd, p_test, rho_fluid_int)
    p_ext = onefluid_behindcasing(tvd, rho_fluid_ext)

    pressure_differential = [x - y for x, y in zip(p_int, p_ext)]

    return pressure_differential


def pressure_test_morefluids(tvd, p_test, rho_mud, rho_fluid, tvd_fluid):
    """
    Calculate differential pressure profile during pressure testing with more than one fluid behind the casing.
    :param tvd: list - true vertical depth, m
    :param p_test: testing pressure, bar
    :param rho_mud: list - downwards sorted mud densities, sg
    :param rho_fluid: list - downwards sorted fluids densities, sg
    :param tvd_fluid: list - reference tvd of fluid change, m
    :return: differential pressure profile, Pa
    """

    from .pressure_internal import pressure_test
    from .pressure_external import morefluids_behindcasing

    p_int = pressure_test(tvd, p_test, rho_mud)
    p_ext = morefluids_behindcasing(tvd, rho_fluid, tvd_fluid)

    pressure_differential = [x - y for x, y in zip(p_int, p_ext)]

    return pressure_differential


def production_with_packer(tvd, rho_fluid, rho_mud, p_res, tvd_perf, rho_packerfluid, tvd_packer):
    """
    Calculate differential pressure profile during production with packer.
    :param tvd: list - true vertical depth, m
    :param rho_fluid: fluid density, sg
    :param rho_mud: mud density, sg
    :param p_res: reservoir pressure, bar
    :param tvd_perf: tvd at perforations, m
    :param rho_packerfluid: packer fluid density, sg
    :param tvd_packer: tvd at packer, m
    :return: differential pressure profile, Pa
    """

    from .pressure_internal import tubing_leak
    from .pressure_external import onefluid_behindcasing

    p_int = tubing_leak(tvd, p_res, rho_fluid, tvd_perf, rho_packerfluid, tvd_packer, rho_mud)
    p_ext = onefluid_behindcasing(tvd, rho_mud)

    pressure_differential = [x - y for x, y in zip(p_int, p_ext)]

    return pressure_differential


def production_with_packer_and_depletedzone(tvd, rho_fluid, rho_mud, p_res, tvd_perf, rho_packerfluid, tvd_packer,
                                            tvd_zone, p_zone):
    """
    Calculate differential pressure profile during production with packer and a depleted zone.
    :param tvd: list - true vertical depth, m
    :param rho_fluid: fluid density, sg
    :param rho_mud: mud density, sg
    :param p_res: reservoir pressure, bar
    :param tvd_perf: tvd at perforations, m
    :param rho_packerfluid: packer fluid density, sg
    :param tvd_packer: tvd at packer, m
    :param tvd_zone: tvd at depleted zone, m
    :param p_zone: pressure at depleted zone, bar
    :return: differential pressure profile, Pa
    """

    from .pressure_internal import tubing_leak
    from .pressure_external import depleted_zone

    p_int = tubing_leak(tvd, p_res, rho_fluid, tvd_perf, rho_packerfluid, tvd_packer, rho_mud)
    p_ext = depleted_zone(tvd, tvd_zone, p_zone, rho_mud)

    pressure_differential = p_int - p_ext

    return pressure_differential


def gas_filled(tvd, p_res, rho_gas, tvd_res, rho_mud):
    """
    Calculate differential pressure profile when the entire casing string is filled with gas.
    :param tvd: list - true vertical depth, m
    :param p_res: reservoir pressure, bar
    :param rho_gas: gas density, sg
    :param tvd_res: tvd at reservoir, m
    :param rho_mud: mud density, sg
    :return: differential pressure profile, Pa
    """

    from .pressure_internal import displacement_to_gas
    from .pressure_external import onefluid_behindcasing

    p_int = displacement_to_gas(tvd, p_res, rho_gas, tvd_res)
    p_ext = onefluid_behindcasing(tvd, rho_mud)

    pressure_differential = [x - y for x, y in zip(p_int, p_ext)]

    return pressure_differential


def production_without_packer_and_depletedzone(tvd, p_res, rho_gas, tvd_res, tvd_zone, p_zone, rho_mud):
    """
    Calculate differential pressure profile during production with depleted zone and without packer.
    :param tvd: list - true vertical depth, m
    :param p_res: reservoir pressure, bar
    :param rho_gas: gas density, sg
    :param tvd_res: tvd at reservoir, m
    :param tvd_zone: tvd at depleted zone, m
    :param p_zone: pressure at depleted zone, bar
    :param rho_mud: mud density, sg
    :return: differential pressure profile, Pa
    """

    from .pressure_internal import displacement_to_gas
    from .pressure_external import depleted_zone

    p_int = displacement_to_gas(tvd, p_res, rho_gas, tvd_res)
    p_ext = depleted_zone(tvd, tvd_zone, p_zone, rho_mud)

    pressure_differential = p_int - p_ext

    return pressure_differential


def stimulation(tvd, whp, rho_injectionfluid, rho_mud, rho_packerfluid, tvd_packer=0):
    """
    Calculate differential pressure profile during stimulation.
    :param tvd: list - true vertical depth, m
    :param whp: wellhead pressure, bar
    :param rho_injectionfluid: injection fluid density, sg
    :param rho_mud: mud density, sg
    :param rho_packerfluid: packer fluid density, sg
    :param tvd_packer: tvd at packer, m
    :return: differential pressure profile, Pa
    """

    from .pressure_internal import tubing_leak_stimulation
    from .pressure_external import onefluid_behindcasing

    p_int = tubing_leak_stimulation(tvd, whp, rho_packerfluid, rho_injectionfluid, tvd_packer)
    p_ext = onefluid_behindcasing(tvd, rho_mud)

    pressure_differential = [x - y for x, y in zip(p_int, p_ext)]

    return pressure_differential


def fluid_storage_onefluid_behindcasing(tvd, rho_fluid, frac_gradient, rho_mud):
    """
    Calculate differential pressure profile during fluid storage with one fluid behind the casing.
    :param tvd: list - true vertical depth, m
    :param rho_fluid: fluid density, sg
    :param frac_gradient: fracture gradient, bar/m
    :param rho_mud: mud density, sg
    :return: differential pressure profile, Pa
    """

    from .pressure_internal import frac_shoe_gas_grad_above
    from .pressure_external import onefluid_behindcasing

    p_int = frac_shoe_gas_grad_above(tvd, frac_gradient, rho_fluid)
    p_ext = onefluid_behindcasing(tvd, rho_mud)

    pressure_differential = p_int - p_ext

    return pressure_differential


def fluid_storage_morefluids_behindcasing(tvd, frac_gradient, rho_fluid, tvd_fluid):
    """
    Calculate differential pressure profile during fluid storage with more than one fluid behind the casing.
    :param tvd: list - true vertical depth, m
    :param rho_fluid: fluid density, sg
    :param frac_gradient: fracture gradient, bar/m
    :param rho_fluid: list - downwards sorted fluids densities, sg
    :param tvd_fluid: list - reference tvd of fluid change, m
    :return: differential pressure profile, Pa
    """

    from .pressure_internal import frac_shoe_gas_grad_above
    from .pressure_external import morefluids_behindcasing

    p_int = frac_shoe_gas_grad_above(tvd, frac_gradient, rho_fluid)
    p_ext = morefluids_behindcasing(tvd, rho_fluid, tvd_fluid)

    pressure_differential = p_int - p_ext

    return pressure_differential


def fluid_storage_depletedzone(tvd, frac_gradient, rho_fluid, tvd_zone, p_zone, rho_mud):
    """
    Calculate differential pressure profile during fluid storage with depleted zone.
    :param tvd: list - true vertical depth, m
    :param frac_gradient: fracture gradient, bar/m
    :param rho_fluid: fluid density, sg
    :param tvd_zone: tvd at depleted zone, m
    :param p_zone: pressure at depleted zone, bar
    :param rho_mud: mud density, sg
    :return: differential pressure profile, Pa
    """

    from .pressure_internal import frac_shoe_gas_grad_above
    from .pressure_external import depleted_zone

    p_int = frac_shoe_gas_grad_above(tvd, frac_gradient, rho_fluid)
    p_ext = depleted_zone(tvd, tvd_zone, p_zone, rho_mud)

    pressure_differential = p_int - p_ext

    return pressure_differential
