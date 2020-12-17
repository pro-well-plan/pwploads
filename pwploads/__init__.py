from math import pi
from .unit_converter import convert_unit
from .collapse_calcs import calc_collapse_pressure
from .von_mises import vme
from .design_factors import api_limits
from .connections import get_conn_limits


class Casing(object):
    """
    Casing object.

    Arguments:
        od_csg (outer diameter, float or int): casing outer diameter [in].
        id_csg (inner diameter, float or int): casing inner diameter [in].
        shoe_depth (depth at shoe, float or int): measured depth at shoe [m].

    Keyword Arguments:
        nominal_weight (nominal weight, float or int): weight per unit length [kg/m].
        yield_s (yield strength, int): pipe's yield strength [psi].
        df_tension (design factor - tension, float): API design factor for tension.
        df_compression (design factor - compression, float): API design factor for compression.
        df_burst (design factor - burst, float): API design factor for burst.
        df_collapse (design factor - collapse, float): API design factor for collapse.
        df_vme (design factor - Von Mises, float): design factor for triaxial.

    Attributes:
        od (float): outer diameter of the casing [in]
        id (float): inner diameter of the casing [in]
        thickness (str or None): outer diameter of the casing [in]
        dt (float): ratio --> outer diameter / thickness
        area (float): effective area [in^2]
        shoe_depth (float or int): measured depth at shoe [m]
        ellipse (list): triaxial points [x, y+, y-]
        csg_loads (list): list of loads that have been run
        nominal_weight (float or int): weight per unit length [kg/m]
        trajectory (obj): wellbore trajectory object
        api_lines (list): API limits coordinates [x, y]
        design_factor (dict): design factors used 'vme', 'api_compression', 'api_tension', 'api_burst', 'api_collapse'
    """

    def __init__(self, od_csg, id_csg, shoe_depth, nominal_weight=64, yield_s=80000, df_tension=1.1,
                 df_compression=1.1, df_burst=1.1, df_collapse=1.1, df_vme=1.25, conn_compression=0.6,
                 conn_tension=0.6, df_conn_compression=1.0, df_conn_tension=1.0):

        self.od = od_csg
        self.id = id_csg
        self.area = (pi / 4) * (self.od ** 2 - self.id ** 2)
        self.thickness = (self.od - self.id) / 2
        self.dt = self.od / self.thickness
        self.limits = {'burst': 0.875 * 2 * yield_s * self.thickness / self.od,
                       'burst_df': 0.875 * 2 * yield_s * self.thickness / self.od / df_burst,
                       'collapse': - calc_collapse_pressure(self.dt, yield_s),
                       'collapse_df': - calc_collapse_pressure(self.dt, yield_s) / df_collapse,
                       'compression': - yield_s * self.area,
                       'compression_df': - yield_s * self.area / df_compression,
                       'tension': yield_s * self.area,
                       'tension_df': yield_s * self.area / df_tension}

        self.shoe_depth = shoe_depth
        self.ellipse = vme(yield_s, self.area, self.id, self.od, df_vme)
        self.csg_loads = []
        self.nominal_weight = nominal_weight
        self.trajectory = None
        self.api_lines, self.collapse_curve = api_limits(self.dt, yield_s, self.limits, self.area, df_tension,
                                                         df_compression, df_burst, df_collapse)
        self.conn_limits = get_conn_limits(self.limits, conn_compression, conn_tension,
                                           df_conn_compression, df_conn_tension)
        self.design_factor = {'vme': df_vme,
                              'api_compression': df_compression,
                              'api_tension': df_tension,
                              'api_burst': df_burst,
                              'api_collapse': df_collapse}

    def running(self, tvd_fluid=None, rho_fluid=None, v_avg=0.3, e=29e6, fric=0.24, a=1.5):
        """
        Run load case: Running in hole

        Keyword Arguments:
            tvd_fluid (list or None): reference tvd of fluid change
            rho_fluid (list or None): downwards sorted fluids densities
            v_avg (float): average running speed, m/s
            e (int): pipe Young's modulus, psi
            fric (float): sliding friction factor pipe - wellbore
            a (float): ratio of maximum running speed to average running speed

        Returns:
            None. It adds the load case results in csg_loads as [load case name, axial_force, pressure_differential]
        """

        from .load_cases import running

        if tvd_fluid is None:
            tvd_fluid = []
        if rho_fluid is None:
            rho_fluid = [1.2]

        e = convert_unit(e, unit_from='psi', unit_to='bar')

        axial_force, pressure_differential = running(self.trajectory, self.nominal_weight, self.od, self.id,
                                                     self.shoe_depth, tvd_fluid, rho_fluid, v_avg, e, fric, a)

        axial_force = [x * 1000 / 4.448 for x in axial_force]   # kN to lbf

        self.csg_loads.append(
            ["Running", axial_force, pressure_differential]
        )

    def overpull(self, tvd_fluid=None, rho_fluid=None, v_avg=0.3, e=29e6, fric=0.24, a=1.5, f_ov=0):
        """
        Run load case: Overpull

        Keyword Arguments:
            tvd_fluid (list or None): reference tvd of fluid change
            rho_fluid (list or None): downwards sorted fluids densities
            v_avg (float): average running speed, m/s
            e (int): pipe Young's modulus, psi
            fric (float): sliding friction factor pipe - wellbore
            a (float): ratio of maximum running speed to average running speed
            f_ov (int or float): overpull force (often during freeing of stuck pipe), kN.

        Returns:
            None. It adds the load case results in csg_loads as [load case name, axial_force, pressure_differential]
        """

        from .load_cases import overpull

        if tvd_fluid is None:
            tvd_fluid = []
        if rho_fluid is None:
            rho_fluid = [1.2]

        e = convert_unit(e, unit_from='psi', unit_to='bar')

        axial_force, pressure_differential = overpull(self.trajectory, self.nominal_weight, self.od, self.id,
                                                      self.shoe_depth, tvd_fluid, rho_fluid, v_avg, e, fric, a, f_ov)

        axial_force = [x * 1000 / 4.448 for x in axial_force]  # kN to lbf

        self.csg_loads.append(
            ["Overpull", axial_force, pressure_differential]
        )

    def green_cement(self, tvd_fluid_int=None, rho_fluid_int=None, rho_cement=1.8, e=29e6, f_pre=0, p_test=0):
        """
        Run load case: Green Cement Pressure test

        Keyword Arguments:
            rho_cement (float): cement density, sg
            e (int): pipe Young's modulus, psi
            tvd_fluid_int (list or None): reference tvd of fluid change inside, m
            rho_fluid_int (list or None): downwards sorted fluids densities inside, sg
            f_pre (int or float): pre-loading force applied to the casing string if necessary, kN
            p_test (int or float): testing pressure, psi

        Returns:
            None. It adds the load case results in csg_loads as [load case name, axial_force, pressure_differential]
        """

        from .load_cases import green_cement_pressure_test

        if tvd_fluid_int is None:
            tvd_fluid_int = []
        if rho_fluid_int is None:
            rho_fluid_int = [1.2]

        tvd = self.trajectory.tvd
        f_test = convert_unit(p_test * self.area, unit_from="lbf", unit_to="kN")
        p_test = convert_unit(p_test, unit_from="psi", unit_to="bar")
        e = convert_unit(e, unit_from='psi', unit_to='bar')

        axial_force, pressure_differential = green_cement_pressure_test(self.trajectory, tvd, self.nominal_weight,
                                                                        self.od, self.id, rho_cement, tvd_fluid_int,
                                                                        rho_fluid_int, p_test, e, f_test, f_pre)

        pressure_differential = convert_unit(pressure_differential, unit_from="Pa", unit_to="psi")

        axial_force = [x * 1000 / 4.448 for x in axial_force]  # kN to lbf

        self.csg_loads.append(
            ["Green Cement", axial_force, pressure_differential]
        )

    def cementing(self, rho_cement=1.8, rho_fluid=1.3, e=29e6, f_pre=0):
        """
        Run load case: Cementing

        Keyword Arguments:
            rho_cement (float): cement density, sg
            rho_fluid (float): displacement fluid density, sg
            e (int): pipe Young's modulus, psi
            f_pre (int or float): pre-loading force applied to the casing string if necessary, kN

        Returns:
            None. It adds the load case results in csg_loads as [load case name, axial_force, pressure_differential]
        """

        from .load_cases import cementing

        e = convert_unit(e, unit_from='psi', unit_to='bar')

        axial_force, pressure_differential = cementing(self.trajectory, self.nominal_weight, self.od, self.id,
                                                       rho_cement, rho_fluid, e, f_pre)

        pressure_differential = convert_unit(pressure_differential, unit_from="Pa", unit_to="psi")

        axial_force = [x * 1000 / 4.448 for x in axial_force]  # kN to lbf

        self.csg_loads.append(
            ["Cementing", axial_force, pressure_differential]
        )

    def displacement_gas(self, p_res, tvd_res, rho_gas=0.5, rho_mud=1.4, e=29e6):
        """
        Run load case: Displacement to gas

        Keyword Arguments:
            :param p_res: reservoir pressure, psi
            :param tvd_res: tvd at reservoir, m
            rho_gas (float): gas density, sg
            rho_mud (float): mud density, sg
            e (int): pipe Young's modulus, psi

        Returns:
            None. It adds the load case results in csg_loads as [load case name, axial_force, pressure_differential]
        """

        from .load_cases import gas_filled

        p_res = convert_unit(p_res, unit_from='psi', unit_to='bar')
        e = convert_unit(e, unit_from='psi', unit_to='bar')

        axial_force, pressure_differential = gas_filled(self.trajectory, self.nominal_weight, self.od, self.id,
                                                        rho_mud, rho_gas, p_res, tvd_res, e)

        pressure_differential = convert_unit(pressure_differential, unit_from="Pa", unit_to="psi")

        axial_force = [x * 1000 / 4.448 for x in axial_force]  # kN to lbf

        self.csg_loads.append(
            ["Displacement to gas", axial_force, pressure_differential]
        )

    def add_trajectory(self, trajectory):

        trajectory.md = [x for x in trajectory.md if x <= self.shoe_depth]
        trajectory.cells_no = len(trajectory.md)
        trajectory.tvd = trajectory.tvd[:trajectory.cells_no]
        trajectory.inclination = trajectory.inclination[:trajectory.cells_no]

        self.trajectory = trajectory

    def plot(self, plot_type='plotly'):
        from .plot import create_plotly_figure, create_pyplot_figure
        if plot_type == 'plotly':
            fig = create_plotly_figure(self)
        else:
            fig = create_pyplot_figure(self)

        return fig
