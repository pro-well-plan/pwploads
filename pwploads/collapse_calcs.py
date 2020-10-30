def calc_collapse_pressure(dt, yield_strength, axial_stress=None):

    y_p = yield_strength

    if axial_stress is not None:
        s_a = axial_stress
        y_pa = ((1 - 0.75 * (s_a / y_p) ** 2) ** 0.5 - 0.5 * s_a / y_p) * y_p
        y_p = y_pa

    if y_p != 0:
        a = 2.8762 + 0.10679 * 1e-5 * y_p + 0.21301 * 1e-10 * y_p ** 2 - 0.53132 * 1e-16 * y_p ** 3
        b = 0.026233 + 0.50609 * 1e-6 * y_p  # 0.0789
        c = -465.93 + 0.030867 * y_p - 0.10483 * 1e-7 * y_p ** 2 + 0.36989 * 1e-13 * y_p ** 3  # 2675
        f = (46.95 * 1e6 * ((3 * b / a) / (2 + b / a)) ** 3) / \
            (y_p * ((3 * b / a) / (2 + b / a) - (b / a)) * (1 - ((3 * b / a) / (2 + b / a))) ** 2)
        g = f * b / a

        dt_yp = (((a - 2) ** 2 + 8 * (b + c / y_p)) ** 0.5 + (a - 2)) / (2 * (b + c / y_p))
        dt_pt = y_p * (a - f) / (c + y_p * (b - g))
        dt_te = (2 + b / a) / (3 * b / a)

        if dt <= dt_yp:
            collapse_range = 'yield'
        elif dt_yp < dt < dt_pt:
            collapse_range = 'plastic'
        elif dt_pt < dt < dt_te:
            collapse_range = 'transition'
        else:
            collapse_range = 'elastic'

        pressure = p_collap(dt, y_p, collapse_range, a, b, c, f, g)
    else:
        pressure = 0

    return pressure


def p_collap(dt, y_p, c_range, a, b, c, f, g):
    if c_range == 'yield':
        p_collapse = 2 * y_p * (dt - 1) / dt**2
    elif c_range == 'plastic':
        p_collapse = y_p * ((a/dt) - b) - c
    elif c_range == 'transition':
        p_collapse = y_p * ((f/dt) - g)
    else:
        p_collapse = 46.96 * 1e6 / (dt * (dt-1)**2)

    return p_collapse
