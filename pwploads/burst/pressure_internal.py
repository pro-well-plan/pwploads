from ..unit_converter import convert_unit
from math import pi
from numpy import array
g = 9.81        # gravity constant, [m/s2]


def fraction_of_bhp_at_wh(tvd, rho_mud, tvd_next_section, fraction=0.5):
    """
    Calculate internal pressure profile when a fraction of the bottom hole pressure (bhp) is at wellhead.
    :param tvd: list - true vertical depth, m
    :param rho_mud: mud density, sg
    :param tvd_next_section: tvd at bottom, m
    :param fraction: bhp fraction at wh
    :return: internal pressure profile, Pa
    """

    rho_mud = convert_unit(rho_mud, unit_from="sg", unit_to="kg/m3")
    bhp = g * rho_mud * tvd_next_section
    p_int = [fraction * bhp] * len(tvd)

    return p_int


def frac_shoe_gas_grad_above(tvd, frac_gradient, rho_fluid):
    """
    Calculate internal pressure profile when fracture pressure ar shoe with gas gradient above.
    :param tvd: list - true vertical depth, m
    :param frac_gradient: fracture gradient, bar/m
    :param rho_fluid: fluid density, sg
    :return: internal pressure profile, Pa
    """

    frac_gradient = convert_unit(frac_gradient, unit_from="bar", unit_to="Pa")      # from bar/m to Pa/m
    rho_fluid = convert_unit(rho_fluid, unit_from="sg", unit_to="kg/m3")
    tvd_frac = tvd[-1]
    p_frac = frac_gradient * tvd_frac
    p_int = [p_frac - g * rho_fluid * (tvd_frac - x) for x in tvd]

    return p_int


def gas_kick(tvd, rho_mud, p_res, tvd_res, vol_kick_initial, id_csg, od_dp):
    """
    Calculate internal pressure profile when circulating out of a kick using the driller’s method.
    :param tvd: list - true vertical depth, m
    :param rho_mud: mud density, sg
    :param p_res: reservoir pressure, bar
    :param tvd_res: tvd at reservoir, m
    :param vol_kick_initial: influx initial volume, m3
    :param id_csg: casing inner diameter, in
    :param od_dp: drill pipe outer diameter, in
    :return: internal pressure profile, Pa
    """

    p_res = convert_unit(p_res, unit_from="bar", unit_to="Pa")
    rho_mud = convert_unit(rho_mud, unit_from="sg", unit_to="kg/m3")

    rho_kick_initial = (p_res / (tvd_res * g))
    kick_intensity = abs(rho_kick_initial - rho_mud)

    bhp = g * (rho_mud + kick_intensity) * tvd_res    # bottom hole pressure [Pa]

    p = [g * rho_mud * x for x in tvd]      # hydrostatic pressure profile [Pa]

    vol_kick = [vol_kick_initial * (bhp / x) for x in p]  # * (temp/temp_kick) * (z/z_kick) [m3]
    rho_kick = [rho_kick_initial * (vol_kick_initial / x) for x in vol_kick]

    p_basekick = [bhp - g * rho_mud * (tvd_res - x) for x in tvd]      # [Pa]

    ir_csg = convert_unit(id_csg/2, unit_from="in", unit_to="m")
    or_dp = convert_unit(od_dp/2, unit_from="in", unit_to="m")

    h = [x / (pi * (ir_csg ** 2 - or_dp ** 2)) for x in vol_kick]       # influx height [m]
    tvd_topkick = array([x - y for x, y in zip(tvd, h)])
    tvd_topkick[tvd_topkick < 0] = 0

    p_topkick = [a - g * b * (c - d) for a, b, c, d in zip(p_basekick, rho_kick, tvd, tvd_topkick) if d >= 0]

    whp = [x - g * rho_mud * y for x, y in zip(p_topkick, tvd_topkick)]

    p_int = [max(whp) + ((bhp - max(whp)) / tvd_res) * x for x in tvd]

    return p_int


def displacement_to_gas(tvd, p_res, rho_gas, tvd_res):
    """
    Calculate internal pressure profile when the entire casing string is filled with gas.
    :param tvd: list - true vertical depth, m
    :param p_res: reservoir pressure, bar
    :param rho_gas: gas density, sg
    :param tvd_res: tvd at reservoir, m
    :return: internal pressure profile, Pa
    """

    p_res = convert_unit(p_res, unit_from="bar", unit_to="Pa")
    rho_gas = convert_unit(rho_gas, unit_from="sg", unit_to="kg/m3")

    p_int = [p_res - g * rho_gas * (tvd_res - x) for x in tvd]

    return p_int


def pressure_test(tvd, p_test, rho_mud):
    """
    Calculate internal pressure profile based on mud weight applied pressure at the wellhead.
    :param tvd: list - true vertical depth, m
    :param p_test: testing pressure, bar
    :param rho_mud: float - downwards sorted mud densities, sg
    :return: internal pressure profile, Pa
    """

    p_test = convert_unit(p_test, unit_from="bar", unit_to="Pa")

    rho_fluid = convert_unit(rho_mud, unit_from="sg", unit_to="kg/m3")  # convert sg to kg/m3

    return [g * rho_fluid * tvd + p_test for tvd in tvd]


def tubing_leak(tvd, p_res, rho_fluid, tvd_perf, rho_packerfluid, tvd_packer, rho_mud):
    """
    Calculate internal pressure profile when a shut-in pressure applied to the top of the production
    annulus due to a tubing leak near the wellhead.
    :param tvd: list - true vertical depth, m
    :param p_res: reservoir pressure, bar
    :param rho_fluid: fluid density, sg
    :param tvd_perf: tvd at perforations, m
    :param rho_packerfluid: packer fluid density, sg
    :param tvd_packer: tvd at packer, m
    :param rho_mud: mud density, sg
    :return: internal pressure profile, Pa
    """

    p_res = convert_unit(p_res, unit_from="bar", unit_to="Pa")
    rho_fluid = convert_unit(rho_fluid, unit_from="sg", unit_to="kg/m3")
    rho_packerfluid = convert_unit(rho_packerfluid, unit_from="sg", unit_to="kg/m3")

    whp = p_res - g * rho_fluid * tvd_perf      # wellhead pressure [Pa]

    p_int = [whp + g * rho_packerfluid * x for x in tvd if x <= tvd_packer] + \
            [p_res - g * rho_packerfluid * (tvd_perf - x) for x in tvd if (x > tvd_packer) and (x <= tvd_perf)] + \
            [p_res + g * rho_mud * (x - tvd_perf) for x in tvd if x > tvd_perf]

    return p_int


def tubing_leak_stimulation(tvd, whp, rho_packerfluid, rho_injectionfluid, tvd_packer=0):
    """

    :param tvd: list - true vertical depth, m
    :param whp: wellhead pressure, bar
    :param rho_packerfluid: packer fluid density, sg
    :param rho_injectionfluid: injection fluid density, sg
    :param tvd_packer: tvd at packer, m
    :return: internal pressure profile, Pa
    """

    whp = convert_unit(whp, unit_from="bar", unit_to="Pa")
    rho_injectionfluid = convert_unit(rho_injectionfluid, unit_from="sg", unit_to="kg/m3")
    rho_packerfluid = convert_unit(rho_packerfluid, unit_from="sg", unit_to="kg/m3")

    p_int = [whp + g * rho_packerfluid * x for x in tvd if x <= tvd_packer] + \
            [whp + g * rho_injectionfluid * x for x in tvd if x > tvd_packer]

    return p_int
