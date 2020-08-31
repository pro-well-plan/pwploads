from . import axial, burst, collapse


def running(trajectory, nominal_weight, od_csg, id_csg, tvd_fluid, rho_fluid, v_avg, e, g,
            fric=0.24, a=1.5):

    axial_force = axial.running(trajectory, nominal_weight, od_csg, id_csg, tvd_fluid, rho_fluid, v_avg,
                                e, g, fric, a)

    pressure_differential = [0] * len(axial_force)

    return axial_force, pressure_differential


def overpull(trajectory, nominal_weight, od_csg, id_csg, tvd_fluid, rho_fluid, v_avg, e, g,
             fric=0.24, a=1.5, f_ov=0):

    axial_force = axial.pulling(trajectory, nominal_weight, od_csg, id_csg, tvd_fluid, rho_fluid, v_avg,
                                e, g, fric, a, f_ov)

    pressure_differential = [0] * len(axial_force)

    return axial_force, pressure_differential


# BURST CASES

def green_cement_pressure_test(tvd, nominal_weight, od_csg, id_csg, tvd_fluid_ext, rho_fluid_ext, tvd_fluid_int,
                               rho_fluid_int, g, p_test, rho_mud, rho_fluid=None, tvd_fluid=None, f_pre=0, f_h=0):

    axial_force = axial.green_cement(tvd, nominal_weight, od_csg, id_csg, tvd_fluid_ext, rho_fluid_ext, tvd_fluid_int,
                                     rho_fluid_int, g, f_pre, f_h)

    if (type(rho_fluid) == list) and (type(tvd_fluid) == list):
        pressure_differential = burst.pressure_test_morefluids(tvd, p_test, rho_mud, rho_fluid, tvd_fluid, g)
    else:
        pressure_differential = burst.pressure_test_onefluid(tvd, p_test, rho_mud, g)

    return axial_force, pressure_differential


def production_with_packer(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, tvd,
                           rho_fluid, rho_mud, p_res, tvd_perf, rho_packerfluid, tvd_packer, g, poisson=0.3,
                           f_setting=0):

    axial_force = axial.production(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a,
                                   poisson, f_setting)

    pressure_differential = burst.production_with_packer(tvd, rho_fluid, rho_mud, p_res, tvd_perf, rho_packerfluid,
                                                         tvd_packer, g)

    return axial_force, pressure_differential


def production_with_packer_depleted_zone(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a,
                                         tvd, rho_fluid, rho_mud, p_res, tvd_perf, rho_packerfluid, tvd_packer, g,
                                         tvd_zone, p_zone, poisson=0.3, f_setting=0):

    axial_force = axial.production(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a,
                                   poisson, f_setting)

    pressure_differential = burst.production_with_packer_and_depletedzone(tvd, rho_fluid, rho_mud, p_res, tvd_perf,
                                                                          rho_packerfluid, tvd_packer, g, tvd_zone,
                                                                          p_zone)

    return axial_force, pressure_differential


def production_without_packer(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, tvd, p_res,
                              rho_gas, tvd_res, rho_mud, g, poisson=0.3, f_setting=0):

    axial_force = axial.production(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a,
                                   poisson, f_setting)

    pressure_differential = burst.production_without_packer(tvd, p_res, rho_gas, tvd_res, rho_mud, g)

    return axial_force, pressure_differential


def production_without_packer_depleted_zone(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i,
                                            delta_p_a, tvd, p_res, rho_gas, tvd_res, tvd_zone, p_zone, rho_mud,
                                            g, poisson=0.3, f_setting=0):

    axial_force = axial.production(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a,
                                   poisson, f_setting)

    pressure_differential = burst.production_without_packer_and_depletedzone(tvd, p_res, rho_gas, tvd_res, tvd_zone,
                                                                             p_zone, rho_mud, g)

    return axial_force, pressure_differential


def stimulation(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, t_k, t_o, alpha, tvd,
                whp, rho_injectionfluid, rho_mud, rho_packerfluid, g, poisson=0.3, f_setting=0, tvd_packer=0):

    axial_force = axial.injection(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, t_k,
                                  t_o, alpha, poisson, f_setting)

    pressure_differential = burst.stimulation(tvd, whp, rho_injectionfluid, rho_mud, rho_packerfluid, g, tvd_packer)

    return axial_force, pressure_differential


def fluid_storage(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, t_k, t_o, alpha,
                  poisson, f_setting, tvd, tvd_frac, frac_gradient, g, rho_mud, rho_fluid=None, tvd_fluid=None):

    axial_force = axial.injection(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, t_k,
                                  t_o, alpha, poisson, f_setting)

    if (type(rho_fluid) == list) and (type(tvd_fluid) == list):
        pressure_differential = burst.fluid_storage_morefluids_behindcasing(tvd, tvd_frac, frac_gradient, rho_fluid,
                                                                            tvd_fluid, g)

    else:
        pressure_differential = burst.fluid_storage_onefluid_behindcasing(tvd, tvd_frac, rho_fluid, frac_gradient,
                                                                          rho_mud, g)

    return axial_force, pressure_differential


def fluid_storage_depleted_zone(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, t_k, t_o,
                                alpha, tvd, tvd_frac, frac_gradient, rho_fluid, tvd_zone, p_zone, rho_mud, g,
                                poisson=0.3, f_setting=0):

    axial_force = axial.injection(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, t_k,
                                  t_o, alpha, poisson, f_setting)

    pressure_differential = burst.fluid_storage_depletedzone(tvd, tvd_frac, frac_gradient, rho_fluid, tvd_zone, p_zone,
                                                             rho_mud, g)

    return axial_force, pressure_differential


# BURST CASES

def drilling_losses(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, t_k, t_o, alpha,
                    tvd, rho_mud, tvd_zone, g, p_zone, poisson=0.3, f_setting=0):

    axial_force = axial.injection(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, t_k,
                                  t_o, alpha, poisson, f_setting)

    pressure_differential = collapse.drilling_losses(tvd, rho_mud, tvd_zone, p_zone, g)

    return axial_force, pressure_differential


def plug_cementation(tvd, nominal_weight, od_csg, id_csg, tvd_fluid_ext, rho_fluid_ext, tvd_fluid_int, rho_fluid_int, g,
                     rho_mud, f_pre=0, rho_fluid=None, tvd_fluid=None):

    axial_force = axial.cementation(tvd, nominal_weight, od_csg, id_csg, tvd_fluid_ext, rho_fluid_ext, tvd_fluid_int,
                                    rho_fluid_int, g, f_pre)

    if (type(rho_fluid) == list) and (type(tvd_fluid) == list):
        pressure_differential = collapse.plug_cementation_morefluids_behindcasing(tvd, rho_fluid, tvd_fluid, g)

    else:
        pressure_differential = collapse.plug_cementation_onefluid_behindcasing(tvd, rho_fluid, rho_mud, g)

    return axial_force, pressure_differential


def drill_stem_test(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, tvd, rho_mud, g,
                    tvd_zone, p_zone, poisson=0.3, f_setting=0, evacuation="full"):

    axial_force = axial.production(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a,
                                   poisson, f_setting)

    pressure_differential = [0] * len(axial_force)

    if evacuation == "full":
        pressure_differential = collapse.drill_stem_test_fullevacuation(tvd, rho_mud, g)

    if evacuation == "partial":
        pressure_differential = collapse.drill_stem_test_partialevacuation(tvd, rho_mud, tvd_zone, p_zone, g)

    return axial_force, pressure_differential


def production_evacuation(tvd, rho_mud, g, md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a,
                          poisson=0.3, f_setting=0):

    axial_force = axial.production(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a,
                                   poisson, f_setting)

    pressure_differential = collapse.production_fullevacuation(tvd, rho_mud, g)

    return axial_force, pressure_differential


def injection_evacuation(tvd, tvd_perf, rho_inj, p_inj, tvd_influencedzone, rho_fluid, p_fric, rho_form, g, evacuation,
                         p_zone, rho_fluid_before_cementation, rho_fluid_above_packer, md, md_toc, od_csg, id_csg,
                         delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, t_k, t_o, alpha, poisson=0.3, f_setting=0):

    axial_force = axial.injection(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, t_k,
                                  t_o, alpha, poisson, f_setting)

    pressure_differential = [0] * len(axial_force)

    if evacuation == "full":
        pressure_differential = collapse.injection_fulllevacuation(tvd, tvd_perf, rho_inj, p_inj, tvd_influencedzone,
                                                                   rho_fluid, p_fric, rho_form, g)

    if evacuation == "partial":
        pressure_differential = collapse.injection_partialevacuation(tvd, tvd_perf, rho_inj, p_inj, p_zone,
                                                                     tvd_influencedzone, rho_fluid_before_cementation,
                                                                     p_fric, rho_form, rho_fluid_above_packer, g)

    return axial_force, pressure_differential
