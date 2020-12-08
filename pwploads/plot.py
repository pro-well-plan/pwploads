import matplotlib.pyplot as plt
import plotly.graph_objects as go
from numpy import array, interp


def create_pyplot_figure(self):

    fig, ax = plt.subplots()

    # Plotting VME
    ax.plot(array(self.ellipse[0]) / 1000, array(self.ellipse[1]) / 1000, 'r', label='Triaxial ' +
                                                                                     str(self.design_factor['vme']),
            linestyle='dashed')
    ax.plot(array(self.ellipse[0]) / 1000, array(self.ellipse[2]) / 1000, 'r', linestyle='dashed')

    # Plotting API limits
    ax.plot(array(self.api_lines[0]) / 1000, array(self.api_lines[1]) / 1000, 'k', label='API')

    # Plotting connections limits
    # for compression
    ax.plot([self.conn_limits[0]/1000]*2,
            [self.limits['collapse_df']/1000, self.limits['burst_df']/1000],
            '0.55',
            label='Connection', linestyle='dashed')

    # for tension
    ax.plot([self.conn_limits[1] / 1000] * 2,
            [self.limits['burst_df'] / 1000,
             interp(self.conn_limits[1], self.collapse_curve[0], self.collapse_curve[1]) / 1000],
            '0.55', linestyle='dashed')

    # Plotting Loads
    for x in self.csg_loads:
        ax.plot(array(x[1]) / 1000, array(x[2]) / 1000, label=x[0])

    ax.set_xlabel('Axial Force, klb-f')
    ax.set_ylabel('Pressure Difference, ksi')
    ax.ticklabel_format(style='plain')
    ax.legend(loc='lower right', fontsize='x-small')
    ax.grid()

    return fig


def create_plotly_figure(self):
    fig = go.Figure()

    # Plotting VME
    triaxial_x = array(self.ellipse[0] + self.ellipse[0][::-1])/1000
    triaxial_y = array(self.ellipse[1] + self.ellipse[2][::-1])/1000
    fig.add_trace(go.Scatter(x=triaxial_x, y=triaxial_y, line={'color': 'red', 'dash': 'dash'},
                             name='Triaxial ' + str(self.design_factor['vme'])))

    # Plotting API limits
    fig.add_trace(go.Scatter(x=array(self.api_lines[0]) / 1000, y=array(self.api_lines[1]) / 1000,
                             line={'color': 'black'}, name='API'))

    # Plotting connections limits
    # for compression
    fig.add_trace(go.Scatter(x=[self.conn_limits[0] / 1000] * 2,
                             y=[self.limits['collapse_df'] / 1000, self.limits['burst_df'] / 1000],
                             line={'color': 'gray', 'dash': 'dash'}, name='Connection', mode='lines'))
    # for tension
    fig.add_trace(go.Scatter(x=[self.conn_limits[1] / 1000] * 2,
                             y=[self.limits['burst_df'] / 1000,
                                interp(self.conn_limits[1], self.collapse_curve[0], self.collapse_curve[1]) / 1000],
                             line={'color': 'gray', 'dash': 'dash'}, name='Connection', mode='lines'))
    fig['data'][-1]['showlegend'] = False       # Hide last label (otherwise it'd show twice 'Connection')

    # Plotting Loads
    for x in self.csg_loads:
        fig.add_trace(go.Scatter(x=array(x[1]) / 1000, y=array(x[2]) / 1000, name=x[0]))

    fig.update_layout(
        xaxis_title='Axial Force, klb-f',
        yaxis_title='Pressure Difference, ksi')

    return fig
