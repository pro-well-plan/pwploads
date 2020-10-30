from numpy import array, linspace


def triaxial(yield_s, strength_burst, area):

    yield_s_new = yield_s * 1.1547

    xaxis_pos = [(x / yield_s) for x in array(linspace(0, yield_s_new, 1000))]
    xaxis_neg = [((-x) / yield_s) for x in array(linspace(0, yield_s_new, 1000))][::-1]

    ellipse = [[x * yield_s * area for x in xaxis_neg] + [x * yield_s * area for x in xaxis_pos],
               [((1 - ((3 / 4) * x ** 2)) ** 0.5 + (1 / 2) * x) * strength_burst for x in xaxis_neg] +
               [((1 - ((3 / 4) * x ** 2)) ** 0.5 + (1 / 2) * x) * strength_burst for x in xaxis_pos],
               [(-(1 - ((3 / 4) * x ** 2)) ** 0.5 + (1 / 2) * x) * strength_burst for x in xaxis_neg] +
               [(-(1 - ((3 / 4) * x ** 2)) ** 0.5 + (1 / 2) * x) * strength_burst for x in xaxis_pos]]

    return ellipse
