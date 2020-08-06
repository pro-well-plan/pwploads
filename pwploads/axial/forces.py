def air_weight(tvd, nominal_weight):
    f_w = [nominal_weight * (tvd[-1] - x) for x in tvd]

    return f_w


def buoyancy_force(tvd, od_csg, id_csg, tvd_fluid_ext, rho_fluid_ext, tvd_fluid_int, rho_fluid_int, g):
    from math import pi
    p_ext = pressure_profile(tvd, tvd_fluid_ext, rho_fluid_ext, g)
    p_int = pressure_profile(tvd, tvd_fluid_int, rho_fluid_int, g)

    area_total = (pi / 4) * od_csg ** 2
    area_int = (pi / 4) * id_csg ** 2

    f_bu = [area_total * x - area_int * y for x, y in zip(p_ext, p_int)]

    return f_bu


# def drag()


def pressure_testing(tvd, whp, effective_diameter):
    from math import pi
    f_h = [(effective_diameter ** 2) * (pi/4) * whp] * len(tvd)

    return f_h


def pickup_force(tvd, od_csg, id_csg, tvd_toc, t_k, t_o, e, alpha):
    from math import pi

    delta_t = [x - y for x, y in zip(t_k, t_o)]
    area = (pi/4) * (od_csg**2 - id_csg*2)

    f_pu = [e * area * alpha * y for x, y in zip(tvd, delta_t) if x <= tvd_toc]
    f_pu += [0] * (len(tvd) - len(f_pu))


def thermal_load(od_csg, id_csg, t_k, t_o, alpha, e):
    from math import pi

    delta_t = [x - y for x, y in zip(t_k, t_o)]
    area = (pi / 4) * (od_csg ** 2 - id_csg * 2)

    f_th = [- e * area * alpha * x for x in delta_t]

    return f_th


def ballooning(md, md_toc, od_csg, id_csg, delta_rho_i, delta_rho_a, e, delta_p_i, delta_p_a, poisson=0.3):
    from math import pi

    dia_rel = (od_csg/id_csg)**2
    delta_l = - poisson * (md_toc**2 / e) * ((delta_rho_i - dia_rel * delta_rho_a) / (dia_rel - 1)) -  \
        2 * poisson * (md_toc / e) * ((delta_p_i - dia_rel * delta_p_a) / (dia_rel - 1))

    area = (pi / 4) * (od_csg ** 2 - id_csg * 2)

    f_bl = [e * area * delta_l / md_toc for x in md if x <= md_toc]
    f_bl += [0] * (len(md) - len(f_bl))

    return f_bl


def pressure_profile(tvd, tvd_fluid, rho_fluid, g):
    tvd_fluid.append(tvd[-1])

    p_prev = 0
    tvd_fluid_prev = 0
    rho_fluid = iter(rho_fluid)
    tvd_fluid = iter(tvd_fluid)
    rho_fluid_selected = next(rho_fluid)
    tvd_fluid_selected = next(tvd_fluid)

    pressure = []
    for x in tvd:
        p = g * rho_fluid_selected * (x - tvd_fluid_prev) + p_prev

        if (x >= tvd_fluid_selected) and (tvd_fluid_selected != tvd[-1]):
            tvd_fluid_prev = tvd_fluid_selected
            tvd_fluid_selected = next(tvd_fluid)
            rho_fluid_selected = next(rho_fluid)
            p_prev = p
        pressure.append(p)

    return pressure
