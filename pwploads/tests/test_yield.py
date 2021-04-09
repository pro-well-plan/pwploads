from unittest import TestCase
import pwploads


def default_casing(grade, size):
    pipe = {'od': size['oDia'],
            'id': size['iDia'],
            'shoeDepth': 1500,
            'tocMd': 1000,
            'weight': 100,
            'grade': grade,
            'e': 29e6,
            'top': 500}
    df = {'pipe': {'tension': 1, 'compression': 1, 'burst': 1, 'collapse': 1, 'triaxial': 1},
          'connection': {'tension': 1.0, 'compression': 1.0}}

    casing = pwploads.Casing(pipe, factors=df)

    return casing


class TestCasing(TestCase):
    def test_different_yield(self):
        size = {'oDia': 8, 'iDia': 7.2}
        for yield_s in ['X-35', 'X-45', 'X-60', 'X-80', 'X-100', 'X-135']:
            pipe = default_casing(yield_s, size)
            fig = pipe.plot()
            fig.show()

    def test_different_size(self):
        yield_s = 'X-135'
        for size in [{'oDia': 4, 'iDia': 3}, {'oDia': 9, 'iDia': 8}, {'oDia': 15, 'iDia': 14}]:
            pipe = default_casing(yield_s, size)
            fig = pipe.plot()
            fig.show()

    def test_different_thickness(self):
        yield_s = 'X-135'
        for size in [{'oDia': 5, 'iDia': 4.8}, {'oDia': 5, 'iDia': 4.5}, {'oDia': 5, 'iDia': 3.5}]:
            pipe = default_casing(yield_s, size)
            fig = pipe.plot()
            fig.show()
