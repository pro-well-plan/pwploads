from .forces import *


def running(trajectory, nominal_weight, od_csg, id_csg, shoe_depth, tvd_fluid, rho_fluid, v_avg, e,
            fric=0.24, a=1.5):
    """
    Calculate axial load during running
    :param trajectory: wellpath object
    :param nominal_weight: weight per unit length, kg/m
    :param od_csg: pipe outer diameter, in
    :param id_csg: pipe inner diameter, in
    :param shoe_depth: measured depth at shoe, m
    :param tvd_fluid: list - reference tvd of fluid change
    :param rho_fluid: list - downwards sorted fluids densities
    :param v_avg: average running speed, m/s
    :param e: pipe Young's modulus, bar
    :param fric: sliding friction factor pipe - wellbore
    :param a: ratio of maximum running speed to average running speed
    :return: total axial force profile, kN
    """

    f_w = air_weight(trajectory.tvd, nominal_weight)
    f_bu = buoyancy_force(trajectory.tvd, od_csg, id_csg, tvd_fluid, rho_fluid, tvd_fluid, rho_fluid)
    f_sh = shock_load(trajectory.tvd, v_avg, od_csg, id_csg, nominal_weight, e, a)
    f_d = drag(trajectory, od_csg, id_csg, shoe_depth, nominal_weight, tvd_fluid, rho_fluid, fric)
    f_be = bending(od_csg, trajectory.dls, trajectory.dls_resolution, e)

    force = [x1 - x2 + x3 - x4 + x5 for x1, x2, x3, x4, x5 in zip(f_w, f_bu, f_sh, f_d, f_be)]

    return force


def pulling(trajectory, nominal_weight, od_csg, id_csg, shoe_depth, tvd_fluid, rho_fluid, v_avg, e,
            fric=0.24, a=1.5, f_ov=0):
    """
    Calculate axial load during pulling
    :param trajectory: wellpath object
    :param nominal_weight: weight per unit length, kg/m
    :param od_csg: pipe outer diameter, in
    :param id_csg: pipe inner diameter, in
    :param shoe_depth: measured depth at shoe, m
    :param tvd_fluid: list - reference tvd of fluid change
    :param rho_fluid: list - downwards sorted fluids densities
    :param v_avg: average running speed, m/s
    :param e: pipe Young's modulus, bar
    :param fric: sliding friction factor pipe - wellbore
    :param a: ratio of maximum running speed to average running speed
    :param f_ov: overpull force (often during freeing of stuck pipe), kN.
    :return: total axial force profile, kN
    """

    f_w = air_weight(trajectory.tvd, nominal_weight)
    f_bu = buoyancy_force(trajectory.tvd, od_csg, id_csg, tvd_fluid, rho_fluid, tvd_fluid, rho_fluid)
    f_sh = shock_load(trajectory.tvd, v_avg, od_csg, id_csg, nominal_weight, e, a)
    f_d = drag(trajectory, od_csg, id_csg, shoe_depth, nominal_weight, tvd_fluid, rho_fluid, fric, 'hoisting')
    f_be = bending(od_csg, trajectory.dls, trajectory.dls_resolution, e)

    force = [x1 - x2 + x3 + x4 + f_ov + x5 for x1, x2, x3, x4, x5 in zip(f_w, f_bu, f_sh, f_d, f_be)]

    return force


def fluid_filled(trajectory, tvd, nominal_weight, od_csg, id_csg, rho_fluid_ext, rho_fluid_int, e):
    """
    Calculate axial load when casing is filled with a specific fluid.
    :param trajectory: wellpath object
    :param tvd: list - true vertical depth, m
    :param nominal_weight: weight per unit length, kg/m
    :param od_csg: pipe outer diameter, in
    :param id_csg: pipe inner diameter, in
    :param rho_fluid_ext: list - downwards sorted fluids densities outside, sg
    :param rho_fluid_int: list - downwards sorted fluids densities inside, sg
    :param e: pipe Young's modulus, bar
    :return: total axial force profile, kN
    """

    f_w = air_weight(tvd, nominal_weight)
    f_bu = buoyancy_force(tvd, od_csg, id_csg, [], [rho_fluid_ext], [], [rho_fluid_int])
    f_be = bending(od_csg, trajectory.dls, trajectory.dls_resolution, e)

    force = [x1 - x2 + x3 for x1, x2, x3 in zip(f_w, f_bu, f_be)]

    return force


def cementation(trajectory, tvd, nominal_weight, od_csg, id_csg, rho_cement, rho_fluid, e, f_pre=0):
    """
    Calculate axial load during cementing
    :param trajectory: wellpath object
    :param tvd: list - true vertical depth, m
    :param nominal_weight: weight per unit length, kg/m
    :param od_csg: pipe outer diameter, in
    :param id_csg: pipe inner diameter, in
    :param rho_cement: cement density, sg
    :param rho_fluid: displacement fluid density, sg
    :param e: pipe Young's modulus, bar
    :param f_pre: pre-loading force applied to the casing string if necessary, kN
    :return: total axial force profile, kN
    """

    f_w = air_weight(tvd, nominal_weight)
    f_bu = buoyancy_force(tvd, od_csg, id_csg, [], [rho_cement], [], [rho_fluid])
    f_be = bending(od_csg, trajectory.dls, trajectory.dls_resolution, e)

    force = [x1 - x2 + f_pre + x3 for x1, x2, x3 in zip(f_w, f_bu, f_be)]

    return force


def green_cement(trajectory, tvd, nominal_weight, od_csg, id_csg, rho_cement, tvd_fluid_int, rho_fluid_int, e,
                 f_pre=0, f_h=0):
    """
    Calculate axial load during green cement pressure test
    :param trajectory: wellpath object
    :param tvd: list - true vertical depth, m
    :param nominal_weight: weight per unit length, kg/m
    :param od_csg: pipe outer diameter, in
    :param id_csg: pipe inner diameter, in
    :param rho_cement: cement density, sg
    :param tvd_fluid_int: list - reference tvd of fluid change inside, m
    :param rho_fluid_int: list - downwards sorted fluids densities inside, sg
    :param e: pipe Young's modulus, bar
    :param f_pre: pre-loading force applied to the casing string if necessary, kN
    :param f_h: pressure testing force, kN
    :return: total axial force profile, kN
    """

    f_w = air_weight(tvd, nominal_weight)
    f_bu = buoyancy_force(tvd, od_csg, id_csg, [], [rho_cement], tvd_fluid_int, rho_fluid_int)
    f_be = bending(od_csg, trajectory.dls, trajectory.dls_resolution, e)

    force = [x1 - x2 + f_h + f_pre + x3 for x1, x2, x3 in zip(f_w, f_bu, f_be)]

    return force


def production(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, poisson=0.3, f_setting=0):
    """
    Calculate axial load during production
    :param md: list - measured depth, m
    :param md_toc: md at top of cement, m
    :param od_csg: pipe outer diameter, in
    :param id_csg: pipe inner diameter, in
    :param delta_rho_i: density change of fluid in the casing string after installation
    :param delta_rho_a: density change of annular fluid after installation
    :param e: pipe Young's modulus, bar
    :param delta_p_i: pressure change of fluid in the casing string after installation
    :param delta_p_a: pressure change of annular fluid after installation
    :param poisson: Poisson’s ratio
    :param f_setting: hang off force of the casing string on slips or hangers, kN
    :return: total axial force profile, kN
    """

    # f_bl = ballooning(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, poisson)
    # f_be --> bending
    f_bl = [0] * len(md)  # while ballooning load is being checked

    force = [f_setting + x for x in f_bl]
    # + f_be

    return force


def injection(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, t_k, t_o, alpha,
              poisson=0.3, f_setting=0):
    """
    Calculate axial load during injection
    :param md: list - measured depth, m
    :param md_toc: md at top of cement, m
    :param od_csg: pipe outer diameter, in
    :param id_csg: pipe inner diameter, in
    :param delta_rho_i: density change of fluid in the casing string after installation
    :param delta_rho_a: density change of annular fluid after installation
    :param e: pipe Young's modulus, bar
    :param delta_p_i: pressure change of fluid in the casing string after installation
    :param delta_p_a: pressure change of annular fluid after installation
    :param t_k: max. wellhead temperature during production, °C
    :param t_o: mean ambient temperature, °C
    :param alpha: thermal expansion coefficient, 1/°C
    :param poisson: Poisson’s ratio
    :param f_setting: hang off force of the casing string on slips or hangers, kN
    :return: total axial force profile, kN
    """

    from .forces import thermal_load

    f_th = thermal_load(od_csg, id_csg, t_k, t_o, alpha, e)
    # f_bl = ballooning(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, poisson)
    f_bl = [0] * len(f_th)      # while ballooning load is being checked
    # f_be --> bending

    force = [f_setting + x1 + x2 for x1, x2 in zip(f_bl, f_th)]
    # + f_be

    return force
