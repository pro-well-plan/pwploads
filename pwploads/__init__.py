from math import pi
from .unit_converter import convert_unit
from .collapse_calcs import calc_collapse_pressure


class Casing(object):

    def __init__(self, od_csg, id_csg, shoe_depth, nominal_weight=64, yield_s=80000, df_tension=1.1,
                 df_compression=1.1, df_burst=1.1, df_collapse=1.1, df_vme=1.25):
        from .von_mises import vme
        from .design_factors import api_limits

        self.od = od_csg
        self.id = id_csg
        self.thickness = (self.od - self.id) / 2
        self.dt = self.od / self.thickness
        p_burst = 0.875 * 2 * yield_s * self.thickness / self.od
        p_collapse = calc_collapse_pressure(self.dt, yield_s)
        self.area = (pi / 4) * (self.od ** 2 - self.id ** 2)
        self.shoe_depth = shoe_depth
        self.ellipse = vme(yield_s, self.area, self.id, self.od, df_vme)
        self.csg_loads = []
        self.nominal_weight = nominal_weight
        self.trajectory = None
        self.api_lines = api_limits(self.dt, yield_s, p_burst, p_collapse, self.area, df_tension,
                                    df_compression, df_burst, df_collapse)
        self.design_factor = {'vme': df_vme,
                              'api_compression': df_compression,
                              'api_tension': df_tension,
                              'api_burst': df_burst,
                              'api_collapse': df_collapse}

    def running(self, tvd_fluid=None, rho_fluid=None, v_avg=0.3, e=32e6, fric=0.24, a=1.5):
        """
        Run load case: Running in hole
        :param tvd_fluid: list - reference tvd of fluid change
        :param rho_fluid: list - downwards sorted fluids densities
        :param v_avg: average running speed, m/s
        :param e: pipe Young's modulus, bar
        :param fric: sliding friction factor pipe - wellbore
        :param a: ratio of maximum running speed to average running speed
        :return: add results in csg_loads as [load case name, axial_force, pressure_differential]
        """

        from .load_cases import running

        if tvd_fluid is None:
            tvd_fluid = []
        if rho_fluid is None:
            rho_fluid = [1.2]

        axial_force, pressure_differential = running(self.trajectory, self.nominal_weight, self.od, self.id,
                                                     self.shoe_depth, tvd_fluid, rho_fluid, v_avg, e, fric, a)

        axial_force = [x * 1000 / 4.448 for x in axial_force]   # kN to lbf

        self.csg_loads.append(
            ["Running", axial_force, pressure_differential]
        )

    def overpull(self, tvd_fluid=None, rho_fluid=None, v_avg=0.3, e=32e6, fric=0.24, a=1.5, f_ov=0):
        """
        Run load case: Overpull
        :param tvd_fluid: list - reference tvd of fluid change
        :param rho_fluid: list - downwards sorted fluids densities
        :param v_avg: average running speed, m/s
        :param e: pipe Young's modulus, bar
        :param fric: sliding friction factor pipe - wellbore
        :param a: ratio of maximum running speed to average running speed
        :param f_ov: overpull force (often during freeing of stuck pipe), kN.
        :return: add results in csg_loads as [load case name, axial_force, pressure_differential]
        """

        from .load_cases import overpull

        if tvd_fluid is None:
            tvd_fluid = []
        if rho_fluid is None:
            rho_fluid = [1.2]

        axial_force, pressure_differential = overpull(self.trajectory, self.nominal_weight, self.od, self.id,
                                                      self.shoe_depth, tvd_fluid, rho_fluid, v_avg, e, fric, a, f_ov)

        axial_force = [x * 1000 / 4.448 for x in axial_force]  # kN to lbf

        self.csg_loads.append(
            ["Overpull", axial_force, pressure_differential]
        )

    def green_cement(self, tvd_fluid_int=None, rho_fluid_int=None, tvd_fluid_ext=None, rho_fluid_ext=None,
                     f_pre=0, f_h=0):
        """
        Run load case: Green Cement Pressure test
        :param tvd_fluid_ext: list - reference tvd of fluid change outside, m
        :param rho_fluid_ext: list - downwards sorted fluids densities outside, sg
        :param tvd_fluid_int: list - reference tvd of fluid change inside, m
        :param rho_fluid_int: list - downwards sorted fluids densities inside, sg
        :param f_pre: pre-loading force applied to the casing string if necessary, kN
        :param f_h: pressure testing force, kN
        :return: add results in csg_loads as [load case name, axial_force, pressure_differential]
        """

        from .load_cases import green_cement_pressure_test

        if tvd_fluid_ext is None:
            tvd_fluid_ext = []
        if rho_fluid_ext is None:
            rho_fluid_ext = [1.2]
        if tvd_fluid_int is None:
            tvd_fluid_int = []
        if rho_fluid_int is None:
            rho_fluid_int = [1.2]

        tvd = self.trajectory.tvd
        f_test = convert_unit(f_h, unit_from="kN", unit_to="lbf")
        p_test = convert_unit(f_test / self.area, unit_from="psi", unit_to="bar")

        axial_force, pressure_differential = green_cement_pressure_test(tvd, self.nominal_weight, self.od, self.id,
                                                                        tvd_fluid_ext, rho_fluid_ext, tvd_fluid_int,
                                                                        rho_fluid_int, p_test, f_pre, f_h)

        pressure_differential = convert_unit(pressure_differential, unit_from="Pa", unit_to="psi")

        axial_force = [x * 1000 / 4.448 for x in axial_force]  # kN to lbf

        self.csg_loads.append(
            ["Green Cement", axial_force, pressure_differential]
        )

    def add_trajectory(self, trajectory):

        trajectory.tvd = [x for x in trajectory.tvd if x <= self.shoe_depth]
        trajectory.md = trajectory.md[:len(trajectory.tvd)]
        trajectory.zstep = len(trajectory.tvd)
        trajectory.inclination = trajectory.inclination[:len(trajectory.tvd)]

        self.trajectory = trajectory

    def plot(self, plot_type='plotly'):
        from .plot import create_plotly_figure, create_pyplot_figure
        if plot_type == 'plotly':
            fig = create_plotly_figure(self)
        else:
            fig = create_pyplot_figure(self)

        return fig
