from math import pi
from .unit_converter import convert_unit
from .collapse_calcs import calc_collapse_pressure
from .von_mises import vme
from .design_factors import api_limits
from .connections import get_conn_limits
from .utilities import *
from .prepare_cases import *
import well_profile as wp


class Casing(object):
    """
    Casing object.

    Arguments:
        pipe (dict): set the main pipe characteristics. 'od', 'id', 'shoeDepth', 'tocMd',  'top', 'casingClass',
                     'weight'(opt), 'grade'(opt), 'e'(opt)
        factors (dict): set define factors for pipe and connection.

    Attributes:
        od (num): outer diameter of the casing [in]
        id (num): inner diameter of the casing [in]
        thickness (str or None): outer diameter of the casing [in]
        dt (num): ratio --> outer diameter / thickness
        area (num): effective area [in^2]
        shoe (num): measured depth at shoe [m]
        ellipse (list): triaxial points [x, y+, y-]
        loads (list): list of loads that have been run
        nominal_weight (num): weight per unit length [kg/m]
        trajectory (obj): wellbore trajectory object
        api_lines (list): API limits coordinates [x, y]
        design_factor (dict): design factors used 'vme', 'api'
    """

    def __init__(self, pipe, conn_compression=0.6, conn_tension=0.6, factors=None):

        df = {'pipe': {'tension': 1.1, 'compression': 1.1, 'burst': 1.1, 'collapse': 1.1, 'triaxial': 1.25},
              'connection': {'tension': 1.0, 'compression': 1.0}}

        if type(factors) == dict:
            for key in factors.keys():
                for item in factors[key].keys():
                    df[key][item] = factors[key][item]

        self.od = pipe['od']
        self.id = pipe['id']
        self.area = (pi / 4) * (self.od ** 2 - self.id ** 2)
        self.thickness = (self.od - self.id) / 2
        self.dt = self.od / self.thickness
        self.toc_md = pipe['tocMd']
        self.shoe = pipe['shoeDepth']
        self.top = pipe['top']

        if 'casingClass' in pipe:
            self.pipe_class = pipe['casingClass']
        else:
            self.pipe_class = None

        if 'grade' in pipe:
            yield_s = float(pipe['grade'].split('-')[1]) * 1000
        else:
            yield_s = 80000

        if 'weight' in pipe:
            self.nominal_weight = pipe['weight']
        else:
            self.nominal_weight = 64

        if 'e' in pipe:
            self.e = pipe['e']
        else:
            self.e = 29e6

        self.limits = {'burst': 0.875 * 2 * yield_s * self.thickness / self.od,
                       'burstDF': 0.875 * 2 * yield_s * self.thickness / self.od / df['pipe']['burst'],
                       'collapse': - calc_collapse_pressure(self.dt, yield_s),
                       'collapseDF': - calc_collapse_pressure(self.dt, yield_s) / df['pipe']['collapse'],
                       'compression': - yield_s * self.area,
                       'compressionDF': - yield_s * self.area / df['pipe']['compression'],
                       'tension': yield_s * self.area,
                       'tensionDF': yield_s * self.area / df['pipe']['tension']}

        self.ellipse = vme(yield_s, self.area, self.id, self.od, df['pipe']['triaxial'])
        self.loads = []
        self.trajectory = None
        self.settings = None
        self.msgs = None
        self.safety_factors = None
        self.api_lines, self.collapse_curve = api_limits(self.dt, yield_s, self.limits, self.area,
                                                         df['pipe']['tension'],
                                                         df['pipe']['compression'],
                                                         df['pipe']['burst'],
                                                         df['pipe']['collapse'])
        self.conn_limits = get_conn_limits(self.limits, conn_compression, conn_tension,
                                           df['connection']['compression'],
                                           df['connection']['tension'])
        self.design_factor = {'vme': df['pipe']['triaxial'],
                              'api': {'compression': df['pipe']['compression'],
                                      'tension': df['pipe']['tension'],
                                      'burst': df['pipe']['burst'],
                                      'collapse': df['pipe']['collapse']}}

    def add_trajectory(self, survey):

        trajectory = wp.load(survey, equidistant=False)
        idx = [trajectory.trajectory.index(x) for x in trajectory.trajectory if self.top <= x['md'] <= self.shoe]
        trajectory.md = [x['md'] - self.top for x in trajectory.trajectory][idx[0]:idx[-1]+1]
        trajectory.tvd = [x['tvd'] - self.top for x in trajectory.trajectory][idx[0]:idx[-1]+1]
        trajectory.inclination = [x['inc'] for x in trajectory.trajectory][idx[0]:idx[-1]+1]
        trajectory.azimuth = [x['azi'] for x in trajectory.trajectory][idx[0]:idx[-1]+1]
        trajectory.dls = [x['dls'] for x in trajectory.trajectory][idx[0]:idx[-1]+1]
        self.trajectory = trajectory

    def plot(self, plot_type='plotly'):
        from .plot import create_plotly_figure, create_pyplot_figure
        if plot_type == 'plotly':
            fig = create_plotly_figure(self)
        else:
            fig = create_pyplot_figure(self)

        return fig
    
    def run_loads(self, settings=None):

        self.define_settings(settings)
        config = self.settings
        gen_msgs(self)

        gen_overpull(self, rho_fluid=[config['densities']['mud']], v_avg=config['tripping']['speed'],
                     fric=config['tripping']['slidingFriction'], a=config['tripping']['maxSpeedRatio'],
                     f_ov=int(config['forces']['overpull']))

        gen_running(self, rho_fluid=[config['densities']['mud']], v_avg=config['tripping']['speed'],
                    fric=config['tripping']['slidingFriction'], a=config['tripping']['maxSpeedRatio'])

        gen_green_cement(self, rho_fluid_int=config['densities']['cementDisplacingFluid'],
                         rho_cement=config['densities']['cement'], f_pre=config['forces']['preloading'],
                         p_test=config['testing']['cementingPressure'])

        gen_cementing(self, rho_cement=config['densities']['cement'],
                      rho_fluid=config['densities']['cementDisplacingFluid'],
                      f_pre=config['forces']['preloading'])

        if self.pipe_class in [None, 'Production']:
            gen_full_evacuation(self, rho_prod_fluid=config['production']['fluidDensity'],
                                rho_mud=config['densities']['mud'], md_toc=self.toc_md,
                                poisson=config['production']['poisson'],
                                f_setting=config['forces']['preloading'])

        gen_mud_drop(self, rho_mud=config['densities']['mud'], rho_mud_new=config['densities']['mudDropTo'])

        if 'Displacement to gas' not in self.msgs:
            gen_displacement_gas(self, p_res=config['production']['resPressure'],
                                 tvd_res=config['production']['resTvd'],
                                 rho_gas=config['densities']['gasKick'], rho_mud=config['densities']['mud'])

        if 'Production' not in self.msgs and self.pipe_class in [None, 'Production']:
            gen_production(self, p_res=config['production']['resPressure'],
                           rho_prod_fluid=config['production']['fluidDensity'],
                           rho_ann_fluid=config['densities']['completionFluid'],
                           rho_packerfluid=config['production']['packerFluidDensity'],
                           md_toc=self.toc_md,
                           tvd_packer=config['production']['packerTvd'],
                           tvd_perf=config['production']['perforationsTvd'],
                           poisson=config['production']['poisson'],
                           f_setting=config['forces']['preloading'])

        if 'Injection' not in self.msgs and self.pipe_class in [None, 'Production']:
            gen_injection(self, whp=config['injection']['whp'],
                          rho_injectionfluid=config['densities']['injectionFluid'],
                          rho_mud=config['densities']['mud'], temp=config['temp'],
                          t_k=config['production']['wellHeadTemp'],
                          poisson=config['production']['poisson'],
                          f_setting=config['forces']['preloading'])

        if 'Pressure Test' not in self.msgs:
            gen_pressure_test(self, whp=config['testing']['testPressure'],
                              effective_diameter=config['testing']['pipeDiameter'],
                              rho_testing_fluid=config['testing']['testFluidDensity'],
                              rho_mud=config['densities']['mud'])

        if 'Gas Kick' not in self.msgs:
            gen_gas_kick(self, p_res=config['production']['resPressure'], tvd_res=config['production']['resTvd'],
                         rho_gas=config['densities']['gasKick'], rho_mud=config['densities']['mud'],
                         vol_kick_initial=config['influx']['gasKickVolume'])

        define_max_loads(self.loads)
        define_min_df(self)
        define_safety_factors(self)

    def define_settings(self, settings):

        default = {'densities': {'mud': 1.5, 'cement': 1.9, 'cementDisplacingFluid': 1.6, 'gasKick': 0.5,
                                 'completionFluid': 1.8, 'injectionFluid': 1.3, 'mudDropTo': 1.1},
                   'tripping': {'slidingFriction': 0.24, 'speed': 0.3, 'maxSpeedRatio': 1.5},
                   'production': {'fluidDensity': 0.9, 'packerFluidDensity': 1.3, 'poisson': 0.3, 'wellHeadTemp': 5},
                   'forces': {'overpull': 0,
                              'preloading': 0},
                   'testing': {'cementingPressure': 1500},
                   'injection': {'whp': 2000, 'injectionFluid': 1.3},
                   'temp': {'seabed': {'tvd': 500, 'temp': 4},
                            'target': {'tvd': 1500, 'temp': 160}},
                   'influx': {'gasKickVolume': 20}}

        if type(settings) == dict:
            for key in settings.keys():
                for item in settings[key].keys():
                    default[key][item] = settings[key][item]

        self.settings = default
