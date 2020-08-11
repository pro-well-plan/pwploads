def running(tvd, nominal_weight, od_csg, id_csg, tvd_fluid_ext, rho_fluid_ext, tvd_fluid_int, rho_fluid_int, v_avg,
            rho_csg, e, g, a=1.5):
    from .forces import air_weight, buoyancy_force, shock_load

    f_w = air_weight(tvd, nominal_weight)
    f_bu = buoyancy_force(tvd, od_csg, id_csg, tvd_fluid_ext, rho_fluid_ext, tvd_fluid_int, rho_fluid_int, g)
    f_sh = shock_load(v_avg, od_csg, id_csg, rho_csg, e, a)
    # f_d --> drag
    # f_be --> bending

    force = [x1 - x2 + x3 for x1, x2, x3 in zip(f_w, f_bu, f_sh)]
    # - f_d + f_be

    return force


def pulling(tvd, nominal_weight, od_csg, id_csg, tvd_fluid_ext, rho_fluid_ext, tvd_fluid_int, rho_fluid_int, v_avg,
            rho_csg, e, g, a=1.5, f_ov=0):
    from .forces import air_weight, buoyancy_force, shock_load

    f_w = air_weight(tvd, nominal_weight)
    f_bu = buoyancy_force(tvd, od_csg, id_csg, tvd_fluid_ext, rho_fluid_ext, tvd_fluid_int, rho_fluid_int, g)
    f_sh = shock_load(v_avg, od_csg, id_csg, rho_csg, e, a)
    # f_d --> drag
    # f_be --> bending

    force = [x1 - x2 + x3 + f_ov for x1, x2, x3 in zip(f_w, f_bu, f_sh)]
    # + f_d + f_be

    return force


def cementation(tvd, nominal_weight, od_csg, id_csg, tvd_fluid_ext, rho_fluid_ext, tvd_fluid_int, rho_fluid_int, g,
                f_pre=0):
    from .forces import air_weight, buoyancy_force

    f_w = air_weight(tvd, nominal_weight)
    f_bu = buoyancy_force(tvd, od_csg, id_csg, tvd_fluid_ext, rho_fluid_ext, tvd_fluid_int, rho_fluid_int, g)
    # f_be --> bending

    force = [x1 - x2 + f_pre for x1, x2 in zip(f_w, f_bu)]
    # + f_be

    return force


def green_cement(tvd, nominal_weight, od_csg, id_csg, tvd_fluid_ext, rho_fluid_ext, tvd_fluid_int, rho_fluid_int, g,
                 f_pre=0, f_h=0):
    from .forces import air_weight, buoyancy_force

    f_w = air_weight(tvd, nominal_weight)
    f_bu = buoyancy_force(tvd, od_csg, id_csg, tvd_fluid_ext, rho_fluid_ext, tvd_fluid_int, rho_fluid_int, g)
    # f_be --> bending

    force = [x1 - x2 + f_h + f_pre for x1, x2 in zip(f_w, f_bu)]
    # + f_be

    return force


def production(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, poisson=0.3, f_setting=0):
    from .forces import ballooning

    f_bl = ballooning(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, poisson)
    # f_be --> bending

    force = [f_setting + x for x in f_bl]
    # + f_be

    return force


def injection(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, t_k, t_o, alpha,
              poisson=0.3, f_setting=0):
    from .forces import ballooning, thermal_load

    f_bl = ballooning(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, poisson)
    f_th = thermal_load(od_csg, id_csg, t_k, t_o, alpha, e)
    # f_be --> bending

    force = [f_setting + x1 + x2 for x1, x2 in zip(f_bl, f_th)]
    # + f_be

    return force
