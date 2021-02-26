import matplotlib.pyplot as plt
import plotly.graph_objects as go
from numpy import array, interp


def create_pyplot_figure(csg):

    fig, ax = plt.subplots()

    # Plotting VME
    ax.plot(csg.ellipse[0], csg.ellipse[1], 'r', label='Triaxial ' + str(csg.design_factor['vme']),
            linestyle='dashed')
    ax.plot(csg.ellipse[0], csg.ellipse[2], 'r', linestyle='dashed')

    # Plotting API limits
    ax.plot(csg.api_lines[0], csg.api_lines[1], 'k', label='API')

    # Plotting connections limits
    # for compression
    ax.plot([csg.conn_limits[0]/1000]*2,
            [csg.limits['collapseDF']/1000, csg.limits['burstDF']/1000],
            '0.55',
            label='Connection', linestyle='dashed')

    # for tension
    ax.plot([csg.conn_limits[1] / 1000] * 2,
            [csg.limits['burstDF'] / 1000,
             interp(csg.conn_limits[1], csg.collapse_curve[0], csg.collapse_curve[1]) / 1000],
            '0.55', linestyle='dashed')

    # Plotting Loads
    for load in csg.loads:
        ax.plot(array(load['axialForce']) / 1000, array(load['diffPressure']) / 1000, label=load['description'])

    ax.set_xlabel('Axial Force, klb-f')
    ax.set_ylabel('Pressure Difference, ksi')
    ax.ticklabel_format(style='plain')
    ax.legend(loc='lower right', fontsize='x-small')
    ax.grid()

    return fig


def create_plotly_figure(csg):
    fig = go.Figure()

    # Plotting VME
    triaxial_x = csg.ellipse[0] + csg.ellipse[0][::-1]
    triaxial_y = csg.ellipse[1] + csg.ellipse[2][::-1]
    fig.add_trace(go.Scatter(x=triaxial_x, y=triaxial_y, line={'color': 'red', 'dash': 'dash'},
                             name='Triaxial ' + str(csg.design_factor['vme'])))

    # Plotting API limits
    fig.add_trace(go.Scatter(x=array(csg.api_lines[0]) / 1000, y=array(csg.api_lines[1]) / 1000,
                             line={'color': 'black'}, name='API'))

    # Plotting connections limits
    fig.add_trace(go.Scatter(x=[csg.conn_limits[0] / 1000] * 2 + [None] + [csg.conn_limits[1] / 1000] * 2,
                             y=[csg.limits['collapseDF'] / 1000, csg.limits['burstDF'] / 1000] + [None] +
                               [csg.limits['burstDF'] / 1000,
                                interp(csg.conn_limits[1], csg.collapse_curve[0], csg.collapse_curve[1]) / 1000],
                             line={'color': 'gray', 'dash': 'dash'}, name='Connection', mode='lines'))

    # Plotting Loads
    for load in csg.loads:
        fig.add_trace(go.Scatter(x=array(load['axialForce']) / 1000, y=array(load['diffPressure']) / 1000,
                                 name=load['description']))

    fig.update_layout(
        xaxis_title='Axial Force, kips',
        yaxis_title='Pressure Difference, ksi')

    return fig
