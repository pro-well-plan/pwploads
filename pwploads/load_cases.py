from . import axial, burst, collapse


def running(trajectory, nominal_weight, od_csg, id_csg, shoe_depth, tvd_fluid, rho_fluid, v_avg, e,
            fric=0.24, a=1.5):
    """
    Load case: Running in hole
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
    :return: total axial force profile [kN] and pressure difference [psi]
    """

    axial_force = axial.running(trajectory, nominal_weight, od_csg, id_csg, shoe_depth, tvd_fluid, rho_fluid, v_avg,
                                e, fric, a)

    pressure_differential = [0] * len(axial_force)

    return axial_force, pressure_differential


def overpull(trajectory, nominal_weight, od_csg, id_csg, shoe_depth, tvd_fluid, rho_fluid, v_avg, e,
             fric=0.24, a=1.5, f_ov=0):
    """
    Load case: Overpull
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
    :return: total axial force profile [kN] and pressure difference [psi]
    """

    axial_force = axial.pulling(trajectory, nominal_weight, od_csg, id_csg, shoe_depth, tvd_fluid, rho_fluid, v_avg,
                                e, fric, a, f_ov)

    pressure_differential = [0] * len(axial_force)

    return axial_force, pressure_differential


def green_cement_pressure_test(trajectory, tvd, nominal_weight, od_csg, id_csg, rho_cement, tvd_fluid_int,
                               rho_fluid_int, p_test, e, f_h, f_pre=0):
    """
    Load case: Green Cement
    :param trajectory: wellpath object
    :param tvd: list - true vertical depth, m
    :param nominal_weight: weight per unit length, kg/m
    :param od_csg: pipe outer diameter, in
    :param id_csg: pipe inner diameter, in
    :param rho_cement: cement density, sg
    :param tvd_fluid_int: list - reference tvd of fluid change inside, m
    :param rho_fluid_int: list - downwards sorted fluids densities inside, sg
    :param p_test: testing pressure, bar
    :param e: pipe Young's modulus, bar
    :param f_h: pressure testing force, kN
    :param f_pre: pre-loading force applied to the casing string if necessary, kN
    :return: total axial force profile [kN] and pressure difference [psi]
    """

    axial_force = axial.green_cement(trajectory, tvd, nominal_weight, od_csg, id_csg, rho_cement, tvd_fluid_int,
                                     rho_fluid_int, e, f_pre, f_h)

    pressure_differential = burst.pressure_test_onefluid(tvd, p_test, rho_fluid_int, tvd_fluid_int, rho_cement)

    return axial_force, pressure_differential


def cementing(trajectory, nominal_weight, od_csg, id_csg, rho_cement, rho_fluid, e, f_pre=0):
    """
    Load case: Cementing
    :param trajectory: wellpath object
    :param nominal_weight: weight per unit length, kg/m
    :param od_csg: pipe outer diameter, in
    :param id_csg: pipe inner diameter, in
    :param rho_cement: cement density, sg
    :param rho_fluid: displacement fluid density, sg
    :param e: pipe Young's modulus, bar
    :param f_pre: pre-loading force applied to the casing string if necessary, kN
    :return: total axial force profile [kN] and pressure difference [psi]
    """

    tvd = trajectory.tvd
    axial_force = axial.cementation(trajectory, tvd, nominal_weight, od_csg, id_csg, rho_cement, rho_fluid, e, f_pre)

    pressure_differential = collapse.plug_cementation_onefluid_behindcasing(tvd, rho_fluid, rho_cement)

    return axial_force, pressure_differential


def gas_filled(trajectory, nominal_weight, od_csg, id_csg, rho_mud, rho_gas, p_res, tvd_res, e):
    """
    Load case: Displacement to gas
    :param trajectory: wellpath object
    :param nominal_weight: weight per unit length, kg/m
    :param od_csg: pipe outer diameter, in
    :param id_csg: pipe inner diameter, in
    :param rho_mud: mud density, sg
    :param rho_gas: gas density, sg
    :param p_res: reservoir pressure, bar
    :param tvd_res: tvd at reservoir, m
    :param e: pipe Young's modulus, bar
    :return: total axial force profile [kN] and pressure difference [psi]
    """

    tvd = trajectory.tvd
    axial_force = axial.fluid_filled(trajectory, tvd, nominal_weight, od_csg, id_csg, rho_mud, rho_gas, e)

    pressure_differential = burst.gas_filled(tvd, p_res, rho_gas, tvd_res, rho_mud)

    return axial_force, pressure_differential


def production_with_packer(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, tvd,
                           rho_fluid, rho_mud, p_res, tvd_perf, rho_packerfluid, tvd_packer, poisson=0.3,
                           f_setting=0):

    axial_force = axial.production(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a,
                                   poisson, f_setting)

    pressure_differential = burst.production_with_packer(tvd, rho_fluid, rho_mud, p_res, tvd_perf, rho_packerfluid,
                                                         tvd_packer)

    return axial_force, pressure_differential


def production_with_packer_depleted_zone(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a,
                                         tvd, rho_fluid, rho_mud, p_res, tvd_perf, rho_packerfluid, tvd_packer,
                                         tvd_zone, p_zone, poisson=0.3, f_setting=0):

    axial_force = axial.production(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a,
                                   poisson, f_setting)

    pressure_differential = burst.production_with_packer_and_depletedzone(tvd, rho_fluid, rho_mud, p_res, tvd_perf,
                                                                          rho_packerfluid, tvd_packer, tvd_zone,
                                                                          p_zone)

    return axial_force, pressure_differential


"""def production_without_packer(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, tvd, 
                            p_res, rho_gas, tvd_res, rho_mud, poisson=0.3, f_setting=0):

    axial_force = axial.production(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a,
                                   poisson, f_setting)

    pressure_differential = burst.production_without_packer(tvd, p_res, rho_gas, tvd_res, rho_mud)

    return axial_force, pressure_differential"""


def production_without_packer_depleted_zone(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i,
                                            delta_p_a, tvd, p_res, rho_gas, tvd_res, tvd_zone, p_zone, rho_mud,
                                            poisson=0.3, f_setting=0):

    axial_force = axial.production(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a,
                                   poisson, f_setting)

    pressure_differential = burst.production_without_packer_and_depletedzone(tvd, p_res, rho_gas, tvd_res, tvd_zone,
                                                                             p_zone, rho_mud)

    return axial_force, pressure_differential


def stimulation(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, t_k, t_o, alpha, tvd,
                whp, rho_injectionfluid, rho_mud, rho_packerfluid, poisson=0.3, f_setting=0, tvd_packer=0):

    axial_force = axial.injection(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, t_k,
                                  t_o, alpha, poisson, f_setting)

    pressure_differential = burst.stimulation(tvd, whp, rho_injectionfluid, rho_mud, rho_packerfluid, tvd_packer)

    return axial_force, pressure_differential


def fluid_storage(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, t_k, t_o, alpha,
                  poisson, f_setting, tvd, frac_gradient, rho_mud, rho_fluid=None, tvd_fluid=None):

    axial_force = axial.injection(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, t_k,
                                  t_o, alpha, poisson, f_setting)

    if (type(rho_fluid) == list) and (type(tvd_fluid) == list):
        pressure_differential = burst.fluid_storage_morefluids_behindcasing(tvd, frac_gradient, rho_fluid, tvd_fluid)

    else:
        pressure_differential = burst.fluid_storage_onefluid_behindcasing(tvd, rho_fluid, frac_gradient, rho_mud)

    return axial_force, pressure_differential


def fluid_storage_depleted_zone(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, t_k, t_o,
                                alpha, tvd, frac_gradient, rho_fluid, tvd_zone, p_zone, rho_mud,
                                poisson=0.3, f_setting=0):

    axial_force = axial.injection(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, t_k,
                                  t_o, alpha, poisson, f_setting)

    pressure_differential = burst.fluid_storage_depletedzone(tvd, frac_gradient, rho_fluid, tvd_zone, p_zone, rho_mud)

    return axial_force, pressure_differential


def drilling_losses(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, t_k, t_o, alpha,
                    tvd, rho_mud, tvd_zone, p_zone, poisson=0.3, f_setting=0):

    axial_force = axial.injection(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, t_k,
                                  t_o, alpha, poisson, f_setting)

    pressure_differential = collapse.drilling_losses(tvd, rho_mud, tvd_zone, p_zone)

    return axial_force, pressure_differential


def plug_cementation(tvd, nominal_weight, od_csg, id_csg, tvd_fluid_ext, rho_fluid_ext, tvd_fluid_int, rho_fluid_int,
                     rho_mud, f_pre=0, rho_fluid=None, tvd_fluid=None):

    axial_force = axial.cementation(tvd, nominal_weight, od_csg, id_csg, tvd_fluid_ext, rho_fluid_ext, tvd_fluid_int,
                                    rho_fluid_int, f_pre)

    if (type(rho_fluid) == list) and (type(tvd_fluid) == list):
        pressure_differential = collapse.plug_cementation_morefluids_behindcasing(tvd, rho_fluid, tvd_fluid)

    else:
        pressure_differential = collapse.plug_cementation_onefluid_behindcasing(tvd, rho_fluid, rho_mud)

    return axial_force, pressure_differential


def drill_stem_test(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, tvd, rho_mud,
                    tvd_zone, p_zone, poisson=0.3, f_setting=0, evacuation="full"):

    axial_force = axial.production(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a,
                                   poisson, f_setting)

    pressure_differential = [0] * len(axial_force)

    if evacuation == "full":
        pressure_differential = collapse.drill_stem_test_fullevacuation(tvd, rho_mud)

    if evacuation == "partial":
        pressure_differential = collapse.drill_stem_test_partialevacuation(tvd, rho_mud, tvd_zone, p_zone)

    return axial_force, pressure_differential


def production_evacuation(tvd, rho_mud, md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a,
                          poisson=0.3, f_setting=0):

    axial_force = axial.production(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a,
                                   poisson, f_setting)

    pressure_differential = collapse.production_fullevacuation(tvd, rho_mud)

    return axial_force, pressure_differential


def injection_evacuation(tvd, tvd_perf, rho_inj, p_inj, tvd_influencedzone, rho_fluid, p_fric, rho_form, evacuation,
                         p_zone, rho_fluid_before_cementation, rho_fluid_above_packer, md, md_toc, od_csg, id_csg,
                         delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, t_k, t_o, alpha, poisson=0.3, f_setting=0):

    axial_force = axial.injection(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, t_k,
                                  t_o, alpha, poisson, f_setting)

    pressure_differential = [0] * len(axial_force)

    if evacuation == "full":
        pressure_differential = collapse.injection_fulllevacuation(tvd, tvd_perf, rho_inj, p_inj, tvd_influencedzone,
                                                                   rho_fluid, p_fric, rho_form)

    if evacuation == "partial":
        pressure_differential = collapse.injection_partialevacuation(tvd, tvd_perf, rho_inj, p_inj, p_zone,
                                                                     tvd_influencedzone, rho_fluid_before_cementation,
                                                                     p_fric, rho_form, rho_fluid_above_packer)

    return axial_force, pressure_differential
