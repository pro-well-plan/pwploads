from numpy import linspace
from math import pi


def vme(yield_s, area, int_diam, out_diam, design_factor=1.25):

    yield_s /= design_factor

    yield_s_new = yield_s * 1.1547

    xaxis_pos = linspace(0, yield_s_new, 300)
    xaxis_neg = linspace(- yield_s_new, 0, 300)[:-1]

    a_factor = ((pi * (out_diam/2)**2) + (pi * (int_diam/2)**2)) / area

    ellipse = [[x * area for x in xaxis_neg] + [x * area for x in xaxis_pos],
               [0.5 * (x + (4*yield_s**2 - 3*x**2)**0.5)/a_factor for x in xaxis_neg] +
               [0.5 * (x + (4*yield_s**2 - 3*x**2)**0.5)/a_factor for x in xaxis_pos],
               [0.5 * (x - (4*yield_s**2 - 3*x**2)**0.5)/a_factor for x in xaxis_neg] +
               [0.5 * (x - (4*yield_s**2 - 3*x**2)**0.5)/a_factor for x in xaxis_pos]]

    return ellipse
