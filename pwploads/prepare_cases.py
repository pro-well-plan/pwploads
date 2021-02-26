from .unit_converter import convert_unit


def gen_running(csg, tvd_fluid=None, rho_fluid=None, v_avg=0.3, fric=0.24, a=1.5):
    """
    Run load case: Running in hole

    Arguments:
        csg: casing obj
        tvd_fluid (list or None): reference tvd of fluid change
        rho_fluid (list or None): downwards sorted fluids densities
        v_avg (num): average running speed, m/s
        fric (num): sliding friction factor pipe - wellbore
        a (num): ratio of maximum running speed to average running speed

    Returns:
        None. It adds the load case results in loads as [load case name, axial_force, pressure_differential]
    """

    from .load_cases import running

    if tvd_fluid is None:
        tvd_fluid = []
    if rho_fluid is None:
        rho_fluid = [1.2]

    e = convert_unit(csg.e, unit_from='psi', unit_to='bar')

    axial_force, pressure_differential = running(csg.trajectory, csg.nominal_weight, csg.od, csg.id,
                                                 csg.shoe, tvd_fluid, rho_fluid, v_avg, e, fric, a)

    axial_force = [x * 1000 / 4.448 for x in axial_force]  # kN to lbf

    csg.loads.append({'description': 'Running', 'axialForce': axial_force,
                      'diffPressure': pressure_differential})


def gen_overpull(csg, tvd_fluid=None, rho_fluid=None, v_avg=0.3, fric=0.24, a=1.5, f_ov=0.0):
    """
    Run load case: Overpull

    Arguments:
        csg: casing obj
        tvd_fluid (list or None): reference tvd of fluid change
        rho_fluid (list or None): downwards sorted fluids densities
        v_avg (num): average running speed, m/s
        fric (num): sliding friction factor pipe - wellbore
        a (num): ratio of maximum running speed to average running speed
        f_ov (int or num): overpull force (often during freeing of stuck pipe), kN.

    Returns:
        None. It adds the load case results in loads as [load case name, axial_force, pressure_differential]
    """

    from .load_cases import overpull

    if tvd_fluid is None:
        tvd_fluid = []
    if rho_fluid is None:
        rho_fluid = [1.2]

    e = convert_unit(csg.e, unit_from='psi', unit_to='bar')

    axial_force, pressure_differential = overpull(csg.trajectory, csg.nominal_weight, csg.od, csg.id,
                                                  csg.shoe, tvd_fluid, rho_fluid, v_avg, e, fric, a, f_ov)

    axial_force = [x * 1000 / 4.448 for x in axial_force]  # kN to lbf

    csg.loads.append({'description': 'Overpull', 'axialForce': axial_force,
                      'diffPressure': pressure_differential})


def gen_green_cement(csg, rho_fluid_int=1.2, rho_cement=1.8, f_pre=0.0, p_test=0.0):
    """
    Run load case: Green Cement Pressure test

    Arguments:
        csg: casing obj
        rho_cement (num): cement density, sg
        rho_fluid_int (num): inside fluid density, sg
        f_pre (num): pre-loading force applied to the casing string if necessary, kN
        p_test (num): testing pressure, psi

    Returns:
        None. It adds the load case results in loads as [load case name, axial_force, pressure_differential]
    """

    from .load_cases import green_cement_pressure_test

    f_test = convert_unit(p_test * csg.area, unit_from="lbf", unit_to="kN")
    p_test = convert_unit(p_test, unit_from="psi", unit_to="bar")
    e = convert_unit(csg.e, unit_from='psi', unit_to='bar')

    axial_force, pressure_differential = green_cement_pressure_test(csg.trajectory, csg.nominal_weight,
                                                                    csg.od, csg.id, rho_cement, rho_fluid_int,
                                                                    p_test, e, f_test, f_pre)

    pressure_differential = convert_unit(pressure_differential, unit_from="Pa", unit_to="psi")

    axial_force = [x * 1000 / 4.448 for x in axial_force]  # kN to lbf

    csg.loads.append({'description': 'Green Cement Pressure Test', 'axialForce': axial_force,
                      'diffPressure': pressure_differential})


def gen_cementing(csg, rho_cement=1.8, rho_fluid=1.3, f_pre=0.0):
    """
    Run load case: Cementing

    Arguments:
        csg: casing obj
        rho_cement (num): cement density, sg
        rho_fluid (num): displacement fluid density, sg
        f_pre (int or num): pre-loading force applied to the casing string if necessary, kN

    Returns:
        None. It adds the load case results in loads as [load case name, axial_force, pressure_differential]
    """

    from .load_cases import cementing

    e = convert_unit(csg.e, unit_from='psi', unit_to='bar')

    axial_force, pressure_differential = cementing(csg.trajectory, csg.nominal_weight, csg.od, csg.id,
                                                   rho_cement, rho_fluid, e, f_pre)

    pressure_differential = convert_unit(pressure_differential, unit_from="Pa", unit_to="psi")

    axial_force = [x * 1000 / 4.448 for x in axial_force]  # kN to lbf

    csg.loads.append({'description': 'Cementing', 'axialForce': axial_force,
                      'diffPressure': pressure_differential})


def gen_displacement_gas(csg, p_res, tvd_res, rho_gas=0.5, rho_mud=1.4):
    """
    Run load case: Displacement to gas

    Arguments:
        csg: casing obj
        p_res (num): reservoir pressure, psi
        tvd_res (num): tvd at reservoir, m
        rho_gas (num): gas density, sg
        rho_mud (num): mud density, sg

    Returns:
        None. It adds the load case results in loads as [load case name, axial_force, pressure_differential]
    """

    from .load_cases import gas_filled

    p_res = convert_unit(p_res, unit_from='psi', unit_to='bar')
    e = convert_unit(csg.e, unit_from='psi', unit_to='bar')

    axial_force, pressure_differential = gas_filled(csg.trajectory, csg.nominal_weight, csg.od, csg.id,
                                                    rho_mud, rho_gas, p_res, tvd_res, e)

    pressure_differential = convert_unit(pressure_differential, unit_from="Pa", unit_to="psi")

    axial_force = [x * 1000 / 4.448 for x in axial_force]  # kN to lbf

    csg.loads.append({'description': 'Displacement to gas', 'axialForce': axial_force,
                      'diffPressure': pressure_differential})


def gen_production(csg, p_res, rho_prod_fluid, rho_ann_fluid, rho_packerfluid, md_toc, tvd_packer, tvd_perf,
                   poisson=0.3, f_setting=0.0):
    from .load_cases import production_with_packer

    p_res = convert_unit(p_res, unit_from='psi', unit_to='bar')
    e = convert_unit(csg.e, unit_from='psi', unit_to='bar')

    axial_force, pressure_differential = production_with_packer(csg.trajectory, md_toc, csg.od, csg.id,
                                                                rho_prod_fluid, rho_ann_fluid, e, p_res, tvd_perf,
                                                                rho_packerfluid, tvd_packer, poisson, f_setting)

    pressure_differential = convert_unit(pressure_differential, unit_from="Pa", unit_to="psi")

    axial_force = [x * 1000 / 4.448 for x in axial_force]  # kN to lbf

    csg.loads.append({'description': 'Production', 'axialForce': axial_force,
                      'diffPressure': pressure_differential})


def gen_injection(csg, whp, rho_injectionfluid, rho_mud, temp, t_k, alpha=17e-6, poisson=0.3, f_setting=0):
    from .load_cases import stimulation

    whp = convert_unit(whp, unit_from='psi', unit_to='bar')
    e = convert_unit(csg.e, unit_from='psi', unit_to='bar')

    axial_force, pressure_differential = stimulation(csg.trajectory, csg.toc_md, csg.od, csg.id, e,
                                                     whp, rho_injectionfluid, rho_mud, rho_mud, temp, t_k,
                                                     alpha=alpha, poisson=poisson, f_setting=f_setting)

    pressure_differential = convert_unit(pressure_differential, unit_from="Pa", unit_to="psi")

    axial_force = [x * 1000 / 4.448 for x in axial_force]  # kN to lbf

    csg.loads.append({'description': 'Injection', 'axialForce': axial_force,
                      'diffPressure': pressure_differential})


def gen_full_evacuation(csg, rho_prod_fluid, rho_mud, md_toc, poisson=0.3, f_setting=0.0):
    from .load_cases import production_evacuation

    e = convert_unit(csg.e, unit_from='psi', unit_to='bar')

    axial_force, pressure_differential = production_evacuation(csg.trajectory, csg.od, csg.id, md_toc, rho_prod_fluid,
                                                               rho_mud, e, poisson, f_setting)

    pressure_differential = convert_unit(pressure_differential, unit_from="Pa", unit_to="psi")

    axial_force = [x * 1000 / 4.448 for x in axial_force]  # kN to lbf

    csg.loads.append({'description': 'Full Evacuation', 'axialForce': axial_force,
                      'diffPressure': pressure_differential})


def gen_pressure_test(csg, whp, effective_diameter, rho_testing_fluid, rho_mud):
    from .load_cases import pressure_test

    whp = convert_unit(whp, unit_from='psi', unit_to='bar')
    e = convert_unit(csg.e, unit_from='psi', unit_to='bar')

    axial_force, pressure_differential = pressure_test(csg.trajectory, whp, csg.od, e, effective_diameter,
                                                       rho_testing_fluid, rho_mud)

    pressure_differential = convert_unit(pressure_differential, unit_from="Pa", unit_to="psi")

    axial_force = [x * 1000 / 4.448 for x in axial_force]  # kN to lbf

    csg.loads.append({'description': 'Pressure Test', 'axialForce': axial_force,
                      'diffPressure': pressure_differential})


def gen_gas_kick(csg, p_res, tvd_res, rho_gas=0.5, rho_mud=1.4, vol_kick_initial=0.05):
    """
    Run load case: Gas Kick

    Arguments:
        csg: casing obj
        p_res (num): reservoir pressure, psi
        tvd_res (num): tvd at reservoir, m
        rho_gas (num): gas density, sg
        rho_mud (num): mud density, sg
        vol_kick_initial (num): influx initial volume, m3

    Returns:
        None. It adds the load case results in loads as [load case name, axial_force, pressure_differential]
    """

    from .load_cases import gas_kick

    p_res = convert_unit(p_res, unit_from='psi', unit_to='bar')
    e = convert_unit(csg.e, unit_from='psi', unit_to='bar')

    axial_force, pressure_differential = gas_kick(csg.trajectory, csg.nominal_weight, csg.od, csg.id, rho_mud, rho_gas,
                                                  p_res, tvd_res, e, vol_kick_initial)

    pressure_differential = convert_unit(pressure_differential, unit_from="Pa", unit_to="psi")

    axial_force = [x * 1000 / 4.448 for x in axial_force]  # kN to lbf

    csg.loads.append({'description': 'Gas kick', 'axialForce': axial_force,
                      'diffPressure': pressure_differential})


def gen_mud_drop(csg, rho_mud=1.4, rho_mud_new=1.1):
    """
    Run load case: Mud Drop

    Arguments:
        csg: casing obj
        rho_mud (num): mud density, sg
        rho_mud_new (num): new mud density, sg

    Returns:
        None. It adds the load case results in loads as [load case name, axial_force, pressure_differential]
    """

    from .load_cases import mud_drop

    e = convert_unit(csg.e, unit_from='psi', unit_to='bar')

    axial_force, pressure_differential = mud_drop(csg.trajectory, csg.nominal_weight, csg.od, csg.id, rho_mud,
                                                  rho_mud_new, e)

    pressure_differential = convert_unit(pressure_differential, unit_from="Pa", unit_to="psi")

    axial_force = [x * 1000 / 4.448 for x in axial_force]  # kN to lbf

    csg.loads.append({'description': 'Mud Drop', 'axialForce': axial_force,
                      'diffPressure': pressure_differential})
