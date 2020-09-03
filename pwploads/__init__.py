class Casing(object):

    def __init__(self, od_csg, id_csg, shoe_depth, yield_s=80000, strength_burst=7000, nominal_weight=64):
        from .von_mises import triaxial
        # DEPTH
        self.od = od_csg
        self.id = id_csg
        self.shoe_depth = shoe_depth
        self.ellipse = triaxial(yield_s, strength_burst, self.od, self.id)
        self.csg_loads = []
        self.nominal_weight = nominal_weight
        self.trajectory = None

    def running(self, tvd_fluid=[], rho_fluid=[10], v_avg=0.3, e=32e6, fric=0.24, a=1.5):

        from .load_cases import running

        axial_force, pressure_differential = running(self.trajectory, self.nominal_weight, self.od, self.id,
                                                     tvd_fluid, rho_fluid, v_avg, e, fric, a)

        self.csg_loads.append(
            ["Running", axial_force, pressure_differential]
        )

    def overpull(self, tvd_fluid=[], rho_fluid=[10], v_avg=0.3, e=32e6, fric=0.24, a=1.5, f_ov=0):

        from .load_cases import overpull

        axial_force, pressure_differential = overpull(self.trajectory, self.nominal_weight, self.od, self.id,
                                                      tvd_fluid, rho_fluid, v_avg, e, fric, a, f_ov)

        self.csg_loads.append(
            ["Overpull", axial_force, pressure_differential]
        )

    def add_trajectory(self, trajectory):

        trajectory.tvd = [x for x in trajectory.tvd if x <= self.shoe_depth]
        trajectory.md = trajectory.md[:len(trajectory.tvd)]
        trajectory.zstep = len(trajectory.tvd)
        trajectory.inclination = trajectory.inclination[:len(trajectory.tvd)]

        self.trajectory = trajectory

    def plot(self):
        import matplotlib.pyplot as plt

        plt.plot(self.ellipse[0], self.ellipse[1], 'k', label='Triaxial')
        plt.plot(self.ellipse[0], self.ellipse[2], 'k')

        for x in self.csg_loads:
            plt.plot(x[1], x[2], label=x[0])

        plt.xlabel('Axial Force, lb-f')
        plt.ylabel('Pressure Difference, psi')
        plt.ticklabel_format(style='plain')
        plt.legend()
        plt.grid()
        plt.show()
