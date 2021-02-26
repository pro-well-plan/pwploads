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
    f_be = bending(od_csg, trajectory.dls, trajectory.info['dlsResolution'], e)

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
    f_be = bending(od_csg, trajectory.dls, trajectory.info['dlsResolution'], e)

    force = [x1 - x2 + x3 + x4 + f_ov + x5 for x1, x2, x3, x4, x5 in zip(f_w, f_bu, f_sh, f_d, f_be)]

    return force


def fluid_filled(trajectory, nominal_weight, od_csg, id_csg, rho_fluid_ext, rho_fluid_int, e):
    """
    Calculate axial load when casing is filled with a specific fluid.
    :param trajectory: wellpath object
    :param nominal_weight: weight per unit length, kg/m
    :param od_csg: pipe outer diameter, in
    :param id_csg: pipe inner diameter, in
    :param rho_fluid_ext: list - downwards sorted fluids densities outside, sg
    :param rho_fluid_int: list - downwards sorted fluids densities inside, sg
    :param e: pipe Young's modulus, bar
    :return: total axial force profile, kN
    """

    f_w = air_weight(trajectory.tvd, nominal_weight)
    f_bu = buoyancy_force(trajectory.tvd, od_csg, id_csg, [], [rho_fluid_ext], [], [rho_fluid_int])
    f_be = bending(od_csg, trajectory.dls, trajectory.info['dlsResolution'], e)

    force = [x1 - x2 + x3 for x1, x2, x3 in zip(f_w, f_bu, f_be)]

    return force


def cementation(trajectory, nominal_weight, od_csg, id_csg, rho_cement, rho_fluid, e, f_pre=0):
    """
    Calculate axial load during cementing
    :param trajectory: wellpath object
    :param nominal_weight: weight per unit length, kg/m
    :param od_csg: pipe outer diameter, in
    :param id_csg: pipe inner diameter, in
    :param rho_cement: cement density, sg
    :param rho_fluid: displacement fluid density, sg
    :param e: pipe Young's modulus, bar
    :param f_pre: pre-loading force applied to the casing string if necessary, kN
    :return: total axial force profile, kN
    """

    f_w = air_weight(trajectory.tvd, nominal_weight)
    f_bu = buoyancy_force(trajectory.tvd, od_csg, id_csg, [], [rho_cement], [], [rho_fluid])
    f_be = bending(od_csg, trajectory.dls, trajectory.info['dlsResolution'], e)

    force = [x1 - x2 + f_pre + x3 for x1, x2, x3 in zip(f_w, f_bu, f_be)]

    return force


def green_cement(trajectory, nominal_weight, od_csg, id_csg, rho_cement, rho_fluid_int, e, f_pre=0, f_h=0):
    """
    Calculate axial load during green cement pressure test
    :param trajectory: wellpath object
    :param nominal_weight: weight per unit length, kg/m
    :param od_csg: pipe outer diameter, in
    :param id_csg: pipe inner diameter, in
    :param rho_cement: cement density, sg
    :param rho_fluid_int: inside fluid density, sg
    :param e: pipe Young's modulus, bar
    :param f_pre: pre-loading force applied to the casing string if necessary, kN
    :param f_h: pressure testing force, kN
    :return: total axial force profile, kN
    """

    f_w = air_weight(trajectory.tvd, nominal_weight)
    f_bu = buoyancy_force(trajectory.tvd, od_csg, id_csg, [], [rho_cement], [], [rho_fluid_int])
    f_be = bending(od_csg, trajectory.dls, trajectory.info['dlsResolution'], e)

    force = [x1 - x2 + f_h + f_pre + x3 for x1, x2, x3 in zip(f_w, f_bu, f_be)]

    return force


def production(trajectory, md_toc, od_csg, id_csg, rho_fluid_int, rho_fluid_ext, e, poisson=0.3, f_setting=0):
    """
    Calculate axial load during production
    :param trajectory: wellpath object
    :param md_toc: md at top of cement, m
    :param od_csg: pipe outer diameter, in
    :param id_csg: pipe inner diameter, in
    :param rho_fluid_int: fluid density in the casing string after installation
    :param rho_fluid_ext: density of annular fluid after installation
    :param e: pipe Young's modulus, bar
    :param poisson: Poisson’s ratio
    :param f_setting: hang off force of the casing string on slips or hangers, kN
    :return: total axial force profile, kN
    """

    f_bl = ballooning(trajectory.md, md_toc, od_csg, id_csg, rho_fluid_int, rho_fluid_ext, poisson)
    f_be = bending(od_csg, trajectory.dls, trajectory.info['dlsResolution'], e)

    force = [f_setting + x1 + x2 for x1, x2 in zip(f_bl, f_be)]

    return force


def injection(trajectory, md_toc, od_csg, id_csg, rho_fluid_int, rho_fluid_ext, e, t_k, temp, alpha=17e-6, poisson=0.3,
              f_setting=0):
    """
    Calculate axial load during injection
    :param trajectory: wellpath object
    :param md_toc: md at top of cement, m
    :param od_csg: pipe outer diameter, in
    :param id_csg: pipe inner diameter, in
    :param rho_fluid_int: fluid density in the casing string after installation
    :param rho_fluid_ext: density of annular fluid after installation
    :param e: pipe Young's modulus, bar
    :param t_k: max. wellhead temperature during production, °C
    :param temp: dict with temp values (°C) at seabed and a target
    :param alpha: thermal expansion coefficient, 1/°C
    :param poisson: Poisson’s ratio
    :param f_setting: hang off force of the casing string on slips or hangers, kN
    :return: total axial force profile, kN
    """

    from .forces import thermal_load

    f_th = thermal_load(trajectory, od_csg, id_csg, t_k, temp, alpha, e)
    f_bl = ballooning(trajectory.md, md_toc, od_csg, id_csg, rho_fluid_int, rho_fluid_ext, poisson)
    f_be = bending(od_csg, trajectory.dls, trajectory.info['dlsResolution'], e)

    force = [f_setting + x1 + x2 + x3 for x1, x2, x3 in zip(f_bl, f_th, f_be)]

    return force


def pressure_test(trajectory, whp, effective_diameter, od_csg,  e):
    """
    Calculate axial load during green cement pressure test
    :param trajectory: wellpath object
    :param whp: wellhead pressure, bar
    :param od_csg: pipe outer diameter, in
    :param effective_diameter: pipe inner diameter, in
    :param e: pipe Young's modulus, bar
    :return: total axial force profile, kN
    """

    f_be = bending(od_csg, trajectory.dls, trajectory.info['dlsResolution'], e)
    f_h = pressure_testing(trajectory.tvd, whp, effective_diameter)

    force = [x1 + x2 for x1, x2 in zip(f_h, f_be)]

    return force
