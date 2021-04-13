import plotly.graph_objects as go
from numpy import array, interp


def vme_plot(csg):
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


def pressure_plot(csg):
    fig = go.Figure()

    # Plotting Loads
    for load in csg.loads:
        fig.add_trace(go.Scatter(x=array(load['diffPressure']) / 1000, y=csg.trajectory.tvd,
                                 name=load['description']))

    # Add Burst and Collapse limits
    fig.add_trace(go.Scatter(x=[csg.limits['burstDF']/1000]*len(csg.trajectory.tvd), y=csg.trajectory.tvd,
                             name='Burst limit ' + str(csg.design_factor['api']['burst'])))
    fig.add_trace(go.Scatter(x=[csg.limits['collapseDF']/1000]*len(csg.trajectory.tvd), y=csg.trajectory.tvd,
                             name='Collapse limit ' + str(csg.design_factor['api']['collapse'])))

    fig.update_layout(
        yaxis_title='Depth, m',
        xaxis_title='Pressure Difference, ksi')
    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(range=[(csg.limits['collapseDF']/1000)-1, (csg.limits['burstDF']/1000)+1])

    return fig


def burst_plot(csg, max_limit=10):
    fig = go.Figure()

    # Plotting Loads
    for load in csg.loads:
        sf = []
        for x in load['diffPressure']:
            if x > 0:
                sf.append(csg.limits['burst']/x)
                if sf[-1] > max_limit:
                    sf[-1] = max_limit
            else:
                sf.append(max_limit)
        fig.add_trace(go.Scatter(x=sf,
                                 y=csg.trajectory.tvd,
                                 name=load['description']))

    # Add Burst SF Limit
    fig.add_trace(go.Scatter(x=[csg.limits['burst']/csg.limits['burstDF']] * len(csg.trajectory.tvd),
                             y=csg.trajectory.tvd,
                             name='Burst SF ' + str(csg.design_factor['api']['burst'])))

    fig.update_layout(
        yaxis_title='Depth, m',
        xaxis_title='Burst Safety Factor')
    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(range=[0, max_limit])

    return fig


def collapse_plot(csg, max_limit=10):
    fig = go.Figure()

    # Plotting Loads
    for load in csg.loads:
        sf = []
        for x in load['diffPressure']:
            if x < 0:
                sf.append(csg.limits['collapse']/x)
                if sf[-1] > max_limit:
                    sf[-1] = max_limit
            else:
                sf.append(max_limit)
        fig.add_trace(go.Scatter(x=sf,
                                 y=csg.trajectory.tvd,
                                 name=load['description']))

    # Add Collapse SF Limit
    fig.add_trace(go.Scatter(x=[csg.limits['collapse']/csg.limits['collapseDF']] * len(csg.trajectory.tvd),
                             y=csg.trajectory.tvd,
                             name='Collapse SF ' + str(csg.design_factor['api']['collapse'])))

    fig.update_layout(
        yaxis_title='Depth, m',
        xaxis_title='Collapse Safety Factor')
    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(range=[0, max_limit])

    return fig


def axial_plot(csg, max_limit=50):
    fig = go.Figure()

    # Plotting Loads
    for load in csg.loads:
        sf = []
        for x in load['axialForce']:
            if x > 0:
                sf.append(csg.limits['tension']/x)
                if sf[-1] > max_limit:
                    sf[-1] = max_limit
            else:
                sf.append(max_limit)
        fig.add_trace(go.Scatter(x=sf,
                                 y=csg.trajectory.tvd,
                                 name=load['description']))

    # Add Burst SF Limit
    fig.add_trace(go.Scatter(x=[csg.limits['tension']/csg.limits['tensionDF']] * len(csg.trajectory.tvd),
                             y=csg.trajectory.tvd,
                             name='Axial SF ' + str(csg.design_factor['api']['tension'])))

    fig.update_layout(
        yaxis_title='Depth, m',
        xaxis_title='Axial Safety Factor')
    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(range=[0, max_limit])

    return fig
