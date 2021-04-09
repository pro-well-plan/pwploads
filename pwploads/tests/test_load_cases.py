from unittest import TestCase
import pwploads


pipe = {'od': 8,
        'id': 7.2,
        'shoeDepth': 1500,
        'tocMd': 1000,
        'weight': 100,
        'grade': 'X-80',
        'e': 29e6,
        'top': 500}
df = {'pipe': {'tension': 1.1, 'compression': 1.1, 'burst': 1.1, 'collapse': 1.1, 'triaxial': 1.25},
      'connection': {'tension': 1.0, 'compression': 1.0}}

casing = pwploads.Casing(pipe, factors=df)
casing.add_trajectory(r'https://github.com/pro-well-plan/pwploads/raw/master/pwploads/tests/TrajectorySample.xlsx')

settings = {'densities': {'mud': 1.7,
                          'cement': 1.8,
                          'cementDisplacingFluid': 1.3,
                          'gasKick': 0.5,
                          'completionFluid': 1.8,
                          'injectionFluid': 1.3},
            'tripping': {'slidingFriction': 0.24,
                         'speed': 0.3,
                         'maxSpeedRatio': 1.5},
            'production': {'resPressure': 4200,
                           'resTvd': 2000,
                           'fluidDensity': 0.8,
                           'packerFluidDensity': 1.3,
                           'packerTvd': 1450,
                           'perforationsTvd': 1600,
                           'poisson': 0.3,
                           'wellHeadTemp': 5},
            'forces': {'overpull': 0,
                       'preloading': 0},
            'testing': {'cementingPressure': 1500, 'testFluidDensity': 1.3, 'testPressure': 3000,
                        'pipeDiameter': 4},
            'injection': {'whp': 2000},
            'temp': {'seabed': {'tvd': 500, 'temp': 4},
                     'target': {'tvd': 1500, 'temp': 160}}
            }

casing.run_loads(settings)


class TestLoadCases(TestCase):
    def test_run_loads(self):
        cases = ['Overpull', 'Running', 'Green Cement Pressure Test', 'Cementing', 'Full Evacuation', 'Mud Drop',
                 'Displacement to gas', 'Production', 'Injection', 'Pressure Test', 'Gas kick']

        for case in [load['description'] for load in casing.loads]:
            self.assertTrue(case in cases)

    def test_safety_factors(self):
        for sf in casing.safety_factors.values():
            self.assertTrue(sf is not None)
            self.assertIsInstance(sf, dict)
            self.assertTrue(sf['safetyFactor'] < 10)

    def test_msgs(self):
        self.assertIsInstance(casing.msgs, dict)
        self.assertTrue(len(casing.msgs) == 0)
