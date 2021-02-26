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
                     'weight'(opt), 'yield'(opt), 'e'(opt)
        factors (dict): set define factors for pipe and connection.

    Attributes:
        od (float): outer diameter of the casing [in]
        id (float): inner diameter of the casing [in]
        thickness (str or None): outer diameter of the casing [in]
        dt (float): ratio --> outer diameter / thickness
        area (float): effective area [in^2]
        shoe (float or int): measured depth at shoe [m]
        ellipse (list): triaxial points [x, y+, y-]
        loads (list): list of loads that have been run
        nominal_weight (float or int): weight per unit length [kg/m]
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
        self.pipe_class = pipe['casingClass']

        if 'casingClass' in pipe:
            self.pipe_class = pipe['casingClass']
        else:
            self.pipe_class = None

        if 'yield' in pipe:
            yield_s = pipe['yield']
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

    def running(self, tvd_fluid=None, rho_fluid=None, v_avg=0.3, fric=0.24, a=1.5):
        gen_running(self, tvd_fluid, rho_fluid, v_avg, fric, a)

    def overpull(self, tvd_fluid=None, rho_fluid=None, v_avg=0.3, fric=0.24, a=1.5, f_ov=0.0):
        gen_overpull(self, tvd_fluid, rho_fluid, v_avg, fric, a, f_ov)

    def green_cement(self, rho_fluid_int=1.2, rho_cement=1.8, f_pre=0.0, p_test=0.0):
        gen_green_cement(self, rho_fluid_int, rho_cement, f_pre, p_test)

    def cementing(self, rho_cement=1.8, rho_fluid=1.3, f_pre=0.0):
        gen_cementing(self, rho_cement, rho_fluid, f_pre)

    def displacement_gas(self, p_res, tvd_res, rho_gas=0.5, rho_mud=1.4):
        gen_displacement_gas(self, p_res, tvd_res, rho_gas, rho_mud)

    def production(self, p_res, rho_prod_fluid, rho_ann_fluid, rho_packerfluid, md_toc, tvd_packer, tvd_perf,
                   poisson=0.3, f_setting=0.0):
        gen_production(self, p_res, rho_prod_fluid, rho_ann_fluid, rho_packerfluid, md_toc, tvd_packer, tvd_perf,
                       poisson, f_setting)

    def injection(self, whp, rho_injectionfluid, rho_mud, temp, t_k, alpha=17e-6, poisson=0.3, f_setting=0):
        gen_injection(self, whp, rho_injectionfluid, rho_mud, temp, t_k, alpha, poisson, f_setting)

    def full_evacuation(self, rho_prod_fluid, rho_mud, md_toc, poisson=0.3, f_setting=0.0):
        gen_full_evacuation(self, rho_prod_fluid, rho_mud, md_toc, poisson, f_setting)

    def pressure_test(self, whp, effective_diameter, rho_testing_fluid, rho_mud):
        gen_pressure_test(self, whp, effective_diameter, rho_testing_fluid, rho_mud)

    def gas_kick(self, p_res, tvd_res, rho_gas=0.5, rho_mud=1.4, vol_kick_initial=20):
        gen_gas_kick(self, p_res, tvd_res, rho_gas, rho_mud, vol_kick_initial)

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

        self.overpull(rho_fluid=[config['densities']['mud']], v_avg=config['tripping']['speed'],
                      fric=config['tripping']['slidingFriction'], a=config['tripping']['maxSpeedRatio'],
                      f_ov=int(config['forces']['overpull']))

        self.running(rho_fluid=[config['densities']['mud']], v_avg=config['tripping']['speed'],
                     fric=config['tripping']['slidingFriction'], a=config['tripping']['maxSpeedRatio'])

        self.green_cement(rho_fluid_int=config['densities']['cementDisplacingFluid'],
                          rho_cement=config['densities']['cement'], f_pre=config['forces']['preloading'],
                          p_test=config['testing']['cementingPressure'])

        self.cementing(rho_cement=config['densities']['cement'],
                       rho_fluid=config['densities']['cementDisplacingFluid'],
                       f_pre=config['forces']['preloading'])

        self.full_evacuation(rho_prod_fluid=config['production']['fluidDensity'],
                             rho_mud=config['densities']['mud'], md_toc=self.toc_md,
                             poisson=config['production']['poisson'],
                             f_setting=config['forces']['preloading'])

        if 'Displacement to gas' not in self.msgs:
            self.displacement_gas(p_res=config['production']['resPressure'], tvd_res=config['production']['resTvd'],
                                  rho_gas=config['densities']['gasKick'], rho_mud=config['densities']['mud'])

        if 'Production' not in self.msgs:
            self.production(p_res=config['production']['resPressure'],
                            rho_prod_fluid=config['production']['fluidDensity'],
                            rho_ann_fluid=config['densities']['completionFluid'],
                            rho_packerfluid=config['production']['packerFluidDensity'],
                            md_toc=self.toc_md,
                            tvd_packer=config['production']['packerTvd'],
                            tvd_perf=config['production']['perforationsTvd'],
                            poisson=config['production']['poisson'],
                            f_setting=config['forces']['preloading'])

        if 'Injection' not in self.msgs:
            self.injection(whp=config['injection']['whp'], rho_injectionfluid=config['densities']['injectionFluid'],
                           rho_mud=config['densities']['mud'], temp=config['temp'],
                           t_k=config['production']['wellHeadTemp'],
                           poisson=config['production']['poisson'],
                           f_setting=config['forces']['preloading'])

        if 'Pressure Test' not in self.msgs:
            self.pressure_test(whp=config['testing']['testPressure'],
                               effective_diameter=config['testing']['pipeDiameter'],
                               rho_testing_fluid=config['testing']['testFluidDensity'],
                               rho_mud=config['densities']['mud'])

        if 'Gas Kick' not in self.msgs:
            self.gas_kick(p_res=config['production']['resPressure'], tvd_res=config['production']['resTvd'],
                          rho_gas=config['densities']['gasKick'], rho_mud=config['densities']['mud'],
                          vol_kick_initial=config['influx']['gasKickVolume'])

        define_max_loads(self.loads)
        define_min_df(self)
        define_safety_factors(self)

    def define_settings(self, settings):

        default = {'densities': {'mud': 1.2, 'cement': 1.8, 'cementDisplacingFluid': 1.3, 'gasKick': 0.5,
                                 'completionFluid': 1.8, 'injectionFluid': 1.3},
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
