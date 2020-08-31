def running(trajectory, nominal_weight, od_csg, id_csg, tvd_fluid, rho_fluid, v_avg, e, g,
            fric=0.24, a=1.5):
    from .forces import air_weight, buoyancy_force, shock_load, drag

    f_w = air_weight(trajectory.tvd, nominal_weight)
    f_bu = buoyancy_force(trajectory.tvd, od_csg, id_csg, tvd_fluid, rho_fluid, tvd_fluid, rho_fluid, g)
    f_sh = shock_load(trajectory.tvd, v_avg, od_csg, id_csg, nominal_weight, e, a)
    f_d = drag(trajectory, od_csg, id_csg, nominal_weight, tvd_fluid, rho_fluid, fric)
    # f_be --> bending

    force = [x1 - x2 + x3 - x4 for x1, x2, x3, x4 in zip(f_w, f_bu, f_sh, f_d)]
    # + f_be
    return force


def pulling(trajectory, nominal_weight, od_csg, id_csg, tvd_fluid, rho_fluid, v_avg, e, g,
            fric=0.24, a=1.5, f_ov=0):
    from .forces import air_weight, buoyancy_force, shock_load, drag

    f_w = air_weight(trajectory.tvd, nominal_weight)
    f_bu = buoyancy_force(trajectory.tvd, od_csg, id_csg, tvd_fluid, rho_fluid, tvd_fluid, rho_fluid, g)
    f_sh = shock_load(trajectory.tvd, v_avg, od_csg, id_csg, nominal_weight, e, a)
    f_d = drag(trajectory, od_csg, id_csg, nominal_weight, tvd_fluid, rho_fluid, fric, 'hoisting')
    # f_be --> bending

    force = [x1 - x2 + x3 + x4 + f_ov for x1, x2, x3, x4 in zip(f_w, f_bu, f_sh, f_d)]
    # + f_be

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
    #from .forces import ballooning

    # f_bl = ballooning(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, poisson)
    # f_be --> bending
    f_bl = [0] * len(md)  # while ballooning load is being checked

    force = [f_setting + x for x in f_bl]
    # + f_be

    return force


def injection(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, t_k, t_o, alpha,
              poisson=0.3, f_setting=0):
    from .forces import thermal_load

    f_th = thermal_load(od_csg, id_csg, t_k, t_o, alpha, e)
    # f_bl = ballooning(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, poisson)
    f_bl = [0] * len(f_th)      # while ballooning load is being checked
    # f_be --> bending

    force = [f_setting + x1 + x2 for x1, x2 in zip(f_bl, f_th)]
    # + f_be

    return force
