from math import pi
from .unit_converter import convert_unit
from .collapse_calcs import calc_collapse_pressure
from .von_mises import vme
from .design_factors import api_limits
from .connections import get_conn_limits
from .utilities import *
from .prepare_cases import *


class Casing(object):
    """
    Casing object.

    Arguments:
        pipe (dict): set the main pipe characteristics. 'od', 'id', 'shoeDepth', 'tocMd', 'weight'(opt), 'yield'(opt),
                     'e'(opt)
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

    def green_cement(self, tvd_fluid_int=None, rho_fluid_int=None, rho_cement=1.8, f_pre=0.0, p_test=0.0):
        gen_green_cement(self, tvd_fluid_int, rho_fluid_int, rho_cement, f_pre, p_test)

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

    def add_trajectory(self, wellbore):

        idx = [wellbore.trajectory.index(x) for x in wellbore.trajectory if self.top <= x['md'] <= self.shoe]
        wellbore.md = [x['md'] - self.top for x in wellbore.trajectory][idx[0]:idx[-1]+1]
        wellbore.tvd = [x['tvd'] - self.top for x in wellbore.trajectory][idx[0]:idx[-1]+1]
        wellbore.inclination = [x['inc'] for x in wellbore.trajectory][idx[0]:idx[-1]+1]
        wellbore.azimuth = [x['azi'] for x in wellbore.trajectory][idx[0]:idx[-1]+1]
        wellbore.dls = [x['dls'] for x in wellbore.trajectory][idx[0]:idx[-1]+1]
        self.trajectory = wellbore

    def plot(self, plot_type='plotly'):
        from .plot import create_plotly_figure, create_pyplot_figure
        if plot_type == 'plotly':
            fig = create_plotly_figure(self)
        else:
            fig = create_pyplot_figure(self)

        return fig
    
    def run_loads(self, settings=None):

        if self.settings is None:
            self.define_settings(settings)

        gen_msgs(self)

        self.overpull(rho_fluid=[settings['densities']['mud']], v_avg=settings['tripping']['speed'],
                      fric=settings['tripping']['slidingFriction'], a=settings['tripping']['maxSpeedRatio'],
                      f_ov=int(settings['forces']['overpull']))

        self.running(rho_fluid=[settings['densities']['mud']], v_avg=settings['tripping']['speed'],
                     fric=settings['tripping']['slidingFriction'], a=settings['tripping']['maxSpeedRatio'])

        self.green_cement(rho_fluid_int=[settings['densities']['cementDisplacingFluid']],
                          rho_cement=settings['densities']['cement'], f_pre=settings['forces']['preloading'],
                          p_test=settings['testing']['cementingPressure'])

        self.cementing(rho_cement=settings['densities']['cement'],
                       rho_fluid=settings['densities']['cementDisplacingFluid'],
                       f_pre=settings['forces']['preloading'])

        if 'Displacement to gas' not in self.msgs:
            self.displacement_gas(p_res=settings['production']['resPressure'], tvd_res=settings['production']['resTvd'],
                                  rho_gas=settings['densities']['gasKick'], rho_mud=settings['densities']['mud'])

        if 'Production' not in self.msgs:
            self.production(p_res=settings['production']['resPressure'],
                            rho_prod_fluid=settings['production']['fluidDensity'],
                            rho_ann_fluid=settings['densities']['completionFluid'],
                            rho_packerfluid=settings['production']['packerFluidDensity'],
                            md_toc=self.toc_md,
                            tvd_packer=settings['production']['packerTvd'],
                            tvd_perf=settings['production']['perforationsTvd'],
                            poisson=settings['production']['poisson'],
                            f_setting=settings['forces']['preloading'])

        if 'Injection' not in self.msgs:
            self.injection(whp=settings['injection']['whp'], rho_injectionfluid=settings['densities']['injectionFluid'],
                           rho_mud=settings['densities']['mud'], temp=settings['temp'],
                           t_k=settings['production']['wellHeadTemp'],
                           poisson=settings['production']['poisson'],
                           f_setting=settings['forces']['preloading'])

        define_max_loads(self.loads)
        define_min_df(self)
        define_safety_factors(self)

    def define_settings(self, settings):

        default = {'densities': {'mud': 1.2, 'cement': 1.8, 'cementDisplacingFluid': 1.3, 'gasKick': 0.5,
                                 'completionFluid': 1.8},
                   'tripping': {'slidingFriction': 0.24, 'speed': 0.3, 'maxSpeedRatio': 1.5},
                   'production': {'fluidDensity': 1.7, 'packerFluidDensity': 1.3, 'poisson': 0.3, 'wellHeadTemp': 10},
                   'forces': {'overpull': 0,
                              'preloading': 0},
                   'testing': {'cementingPressure': 4472.65},
                   'injection': {'whp': 2000, 'injectionFluid': 1.3},
                   'temp': {'seabed': {'tvd': 500, 'temp': 4},
                            'target': {'tvd': 1500, 'temp': 160}}}

        if type(settings) == dict:
            for key in settings.keys():
                for item in settings[key].keys():
                    default[key][item] = settings[key][item]

        self.settings = default
