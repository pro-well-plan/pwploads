import pwploads
from unittest import TestCase


def default_casing_with_trajectory():
    pipe = {'od': 8,
            'id': 7.2,
            'shoeDepth': 1500,
            'tocMd': 1000,
            'top': 500}
    df = {'pipe': {'tension': 1.1, 'compression': 1.1, 'burst': 1.1, 'collapse': 1.1, 'triaxial': 1.25},
          'connection': {'tension': 1.0, 'compression': 1.0}}

    casing = pwploads.Casing(pipe, factors=df)
    casing.add_trajectory(r'https://github.com/pro-well-plan/pwploads/raw/master/pwploads/tests/TrajectorySample.xlsx')

    return casing


class TestSettings(TestCase):
    def test_settings_none(self):
        casing = default_casing_with_trajectory()
        casing.run_loads(settings=None)

    def test_settings_dict(self):
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
        casing = default_casing_with_trajectory()
        casing.run_loads(settings)
