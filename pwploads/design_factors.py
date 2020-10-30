from numpy import linspace
from .collapse_calcs import calc_collapse_pressure


def api_limits(dt, yield_strength, p_burst, p_collapse, area, df_tension=1.3, df_compression=1.3, df_burst=1.1,
               df_collapse=1.1):

    # Defining respective limits according with design factors
    burst_limit = p_burst / df_burst
    collapse_limit = - p_collapse / df_collapse
    tension_limit = yield_strength * area / df_tension
    compression_limit = - yield_strength * area / df_compression

    # Zone with collapse and tension
    axial_force = linspace(0, tension_limit, 20)
    axial_stress = [x/area for x in axial_force]
    diff_pressure = [- calc_collapse_pressure(dt, yield_strength, x) / df_collapse for x in axial_stress]
    collapse_tens_line = [axial_force, diff_pressure]

    # Generating lines [x_list, y_list]
    burst_line = [[compression_limit, tension_limit], [burst_limit, burst_limit]]
    compression_line = [[compression_limit, compression_limit], [collapse_limit, burst_limit]]
    collapse_comp_line = [compression_limit, 0], [collapse_limit, collapse_limit]
    tension_line = [tension_limit, tension_limit], [burst_limit, collapse_tens_line[1][-1]]

    df_lines = [burst_line, compression_line, collapse_comp_line, collapse_tens_line, tension_line]

    return df_lines
