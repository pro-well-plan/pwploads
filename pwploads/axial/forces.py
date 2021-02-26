from math import pi

from ..unit_converter import convert_unit


def air_weight(tvd, nominal_weight):
    """
    Calculate axial force due to pipe weight in air
    :param tvd: list - true vertical depth, m
    :param nominal_weight: weight per unit length, kg/m
    :return: axial force profile, kN
    """

    f_w = [nominal_weight * (tvd[-1] - x) / 1000 for x in tvd]

    return f_w


def buoyancy_force(tvd, od_csg, id_csg, tvd_fluid_ext, rho_fluid_ext, tvd_fluid_int, rho_fluid_int):
    """
    Calculate axial force due to buoyancy effect
    :param tvd: list - true vertical depth, m
    :param od_csg: pipe outer diameter, in
    :param id_csg: pipe inner diameter, in
    :param tvd_fluid_ext: list - reference tvd of fluid change outside, m
    :param rho_fluid_ext: list - downwards sorted fluids densities outside, sg
    :param tvd_fluid_int: list - reference tvd of fluid change inside, m
    :param rho_fluid_int: list - downwards sorted fluids densities inside, sg
    :return: axial force profile, kN
    """
    p_ext = pressure_profile(tvd, tvd_fluid_ext, rho_fluid_ext)
    p_int = pressure_profile(tvd, tvd_fluid_int, rho_fluid_int)

    area_total = (pi / 4) * od_csg ** 2
    area_total = convert_unit(area_total, unit_from="in2", unit_to="m2")

    area_int = (pi / 4) * id_csg ** 2
    area_int = convert_unit(area_int, unit_from="in2", unit_to="m2")

    f_bu = [area_total * x - area_int * y for x, y in zip(p_ext, p_int)]
    f_bu = [x/1000 for x in f_bu]       # N to kN

    return f_bu


def drag(trajectory, od_csg, id_csg, shoe_depth, nominal_weight, tvd_fluid, rho_fluid, sliding_fric=0.24,
         case='lowering', hole=10):
    """
    Calculate axial force due to drag effect
    :param trajectory: wellpath object
    :param od_csg: pipe outer diameter, in
    :param id_csg: pipe inner diameter, in
    :param shoe_depth: measured depth at shoe, m
    :param nominal_weight: weight per unit length, kg/m
    :param tvd_fluid: list - reference tvd of fluid change
    :param rho_fluid: list - downwards sorted fluids densities
    :param sliding_fric: sliding friction factor pipe - wellbore
    :param case: operational case "lowering", "static", "hoisting" or "all"
    :param hole: borehole size, in
    :return: axial force profile, kN
    """

    import torque_drag

    rhof = density_profile(trajectory.tvd, tvd_fluid, rho_fluid)

    area = (pi / 4) * (od_csg ** 2 - id_csg * 2)        # in2
    area = convert_unit(area, unit_from="in2", unit_to="m2")

    rho_pipe = convert_unit(nominal_weight/area, unit_from="kg/m3", unit_to="sg")    # kg/m3 to sg

    f_d = torque_drag.calc(trajectory,
                           dimensions={'od_pipe': od_csg,
                                       'id_pipe': id_csg,
                                       'od_annular': hole,
                                       'length_pipe': shoe_depth},
                           densities={'rhof': rhof, 'rhod': rho_pipe},
                           case=case,
                           fric=sliding_fric,
                           wob=0,
                           tbit=0).force[case]      # kN

    return f_d


def pressure_testing(tvd, whp, effective_diameter):
    """
    Calculate axial force due to pressure testing
    :param tvd: list - true vertical depth, m
    :param whp: wellhead pressure, bar
    :param effective_diameter: diameter, in
    :return: axial force profile, kN
    """

    whp = convert_unit(whp, unit_from="bar", unit_to="Pa")
    effective_diameter = convert_unit(effective_diameter, unit_from="in", unit_to="m")

    f_h = [(effective_diameter ** 2) * (pi/4) * whp] * len(tvd)
    f_h = [x / 1000 for x in f_h]  # N to kN

    return f_h


def pickup_force(tvd, od_csg, id_csg, tvd_toc, t_k, t_o, e, alpha):
    """
    Calculate axial force due to picking-up
    :param tvd: list - true vertical depth, m
    :param od_csg: pipe outer diameter, in
    :param id_csg: pipe inner diameter, in
    :param tvd_toc: tvd at top of cement, m
    :param t_k: max. wellhead temperature during production, °C
    :param t_o: mean ambient temperature, °C
    :param e: pipe Young's modulus, bar
    :param alpha: thermal expansion coefficient, 1/°C
    :return: axial force profile, kN
    """

    delta_t = [x - y for x, y in zip(t_k, t_o)]
    area = (pi/4) * (od_csg**2 - id_csg*2)
    area = convert_unit(area, unit_from="in2", unit_to="m2")
    e = convert_unit(e, unit_from="bar", unit_to="Pa")

    f_pu = [e * area * alpha * y for x, y in zip(tvd, delta_t) if x <= tvd_toc]
    f_pu += [0] * (len(tvd) - len(f_pu))
    f_pu = [x / 1000 for x in f_pu]  # N to kN

    return f_pu


def thermal_load(trajectory, od_csg, id_csg, t_w, temp, alpha, e):
    """
    Calculate axial force fue to thermal effect
    :param trajectory: wellpath object
    :param od_csg: pipe outer diameter, in
    :param id_csg: pipe inner diameter, in
    :param t_w: max. wellhead temperature, °C
    :param temp: dict with temp values (°C) at seabed and a target
    :param alpha: thermal expansion coefficient, 1/°C
    :param e: pipe Young's modulus, bar
    :return: axial force profile, kN
    """

    gradient = (temp['target']['temp'] - temp['seabed']['temp']) / (temp['target']['tvd'] - temp['seabed']['tvd'])
    t_o = [temp['seabed']['temp'] + gradient * (tvd - temp['seabed']['tvd']) for tvd in trajectory.tvd]
    t_k = [t_w + gradient * (tvd - temp['seabed']['tvd']) for tvd in trajectory.tvd]
    delta_t = [x - y for x, y in zip(t_k, t_o)]
    area = (pi / 4) * (od_csg ** 2 - id_csg * 2)
    area = convert_unit(area, unit_from="in2", unit_to="m2")
    e = convert_unit(e, unit_from="bar", unit_to="Pa")

    f_th = [- e * area * alpha * x for x in delta_t]
    f_th = [x / 1000 for x in f_th]  # N to kN

    return f_th


def ballooning(md, md_toc, od_csg, id_csg, rho_fluid_int, rho_fluid_ext, poisson=0.3):
    """
    Calculate axial force due to balloning
    :param md: list - measured depth, m
    :param md_toc: md at top of cement, m
    :param od_csg: pipe outer diameter, in
    :param id_csg: pipe inner diameter, in
    :param rho_fluid_int: fluid density in the casing string after installation
    :param rho_fluid_ext: density of annular fluid after installation
    :param poisson: Poisson’s ratio
    :return: axial force profile, kN
    """

    area_i = convert_unit(pi * (id_csg / 2) ** 2, unit_from='in2', unit_to='m2')
    area_o = convert_unit(pi * (od_csg / 2) ** 2, unit_from='in2', unit_to='m2')

    delta_rho_i = rho_fluid_ext - rho_fluid_int
    delta_rho_a = 0
    f_bl = [-2 * poisson * ((area_i * delta_rho_i * x - area_o * delta_rho_a * x) * 0.0981) for x in md if x >= md_toc]
    f_bl = [0] * (len(md) - len(f_bl)) + f_bl
    f_bl = [x / 1000 for x in f_bl]  # N to kN

    return f_bl


def shock_load(tvd, v_avg, od_csg, id_csg, nominal_weight, e, a=1.5):
    """
    Calculate axial force due to sudden stop during running
    :param tvd: list - true vertical depth, m
    :param v_avg: average running speed, m/s
    :param od_csg: pipe outer diameter, in
    :param id_csg: pipe inner diameter, in
    :param nominal_weight: weight per unit length, kg/m
    :param e: pipe Young's modulus, bar
    :param a: ratio of maximum running speed to average running speed
    :return: axial force profile, kN
    """

    area = (pi / 4) * (od_csg ** 2 - id_csg * 2)
    area = convert_unit(area, unit_from="in2", unit_to="m2")
    e = convert_unit(e, unit_from="bar", unit_to="Pa")

    rho_pipe = nominal_weight / area

    f_sh = [a * v_avg * area * (e * rho_pipe) ** 0.5] * len(tvd)
    f_sh = [x / 1000 for x in f_sh]  # N to kN

    return f_sh


def bending(od_csg, dls, dls_res, e):
    """
    Calculate axial force due to sudden stop during running
    :param od_csg: pipe outer diameter, in
    :param dls: dog leg severity, °/30m
    :param dls_res: resolution of dog leg severity, m
    :param e: pipe Young's modulus, bar
    :return: axial force profile, kN
    """

    e = convert_unit(e, unit_from="bar", unit_to="psi")

    f_be = [pi * e * (x/dls_res) * od_csg * 30.48 / 4.32e5 for x in dls]       # lbf
    f_be = [convert_unit(x, unit_from="lbf", unit_to="kN") for x in f_be]       # lbf to kN

    return f_be


def pressure_profile(tvd, tvd_fluid, rho_fluid):
    """
    Generate hydrostatic pressure profile
    :param tvd: list - true vertical depth, m
    :param tvd_fluid: list - reference tvd of fluid change, m
    :param rho_fluid: list - downwards sorted fluids densities, sg
    :return: pressure profile, Pa
    """
    g = 9.81        # gravity constant, [m/s2]
    rho_fluid = [convert_unit(x, unit_from="sg", unit_to="kg/m3") for x in rho_fluid]   # convert sg to kg/m3

    tvd_fluid.append(tvd[-1])

    p_prev = 0
    tvd_fluid_prev = 0
    rho_fluid = iter(rho_fluid)
    tvd_fluid = iter(tvd_fluid)
    rho_fluid_selected = next(rho_fluid)
    tvd_fluid_selected = next(tvd_fluid)

    pressure = []
    density = []
    for x in tvd:
        p = g * rho_fluid_selected * (x - tvd_fluid_prev) + p_prev
        density.append(rho_fluid_selected)

        if (x >= tvd_fluid_selected) and (tvd_fluid_selected != tvd[-1]):
            tvd_fluid_prev = tvd_fluid_selected
            tvd_fluid_selected = next(tvd_fluid)
            rho_fluid_selected = next(rho_fluid)
            p_prev = p
        pressure.append(p)

    return pressure


def density_profile(tvd, tvd_fluid, rho_fluid):
    """
    Generate a density profile from specific density values and depth of change
    :param tvd: list - true vertical depth, m
    :param tvd_fluid: list - reference tvd of fluid change, m
    :param rho_fluid: list - downwards sorted fluids densities, sg
    :return: density profile
    """

    tvd_fluid.append(tvd[-1])

    rho_fluid = iter(rho_fluid)
    tvd_fluid = iter(tvd_fluid)
    rho_fluid_selected = next(rho_fluid)
    tvd_fluid_selected = next(tvd_fluid)

    density = []
    for x in tvd:
        density.append(rho_fluid_selected)

        if (x >= tvd_fluid_selected) and (tvd_fluid_selected != tvd[-1]):
            tvd_fluid_selected = next(tvd_fluid)
            rho_fluid_selected = next(rho_fluid)

    return density
