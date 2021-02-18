import pwploads
from unittest import TestCase


def default_casing():
    pipe = {'od': 8,
            'id': 7.2,
            'shoeDepth': 1500,
            'tocMd': 1000}

    casing = pwploads.Casing(pipe)

    return casing


class TestCasing(TestCase):
    def test_create_casing(self):

        casing = default_casing()
        self.assertIsInstance(casing, object, 'casing is not an object')
        self.assertEqual(casing.od, 8, 'outer diameter has been changed')
        self.assertEqual(casing.id, 7.2, 'inner diameter has been changed')
        self.assertIsInstance(casing.area, (float, int), 'area is not a number')
        self.assertTrue(casing.area < 20, 'the effective area is too high')
        self.assertIsInstance(casing.ellipse, list, 'triaxial ellipse is not a list')
        self.assertIsInstance(casing.csg_loads, list, 'loads is not a list')
        self.assertIsInstance(casing.nominal_weight, (float, int), 'weight is not a number')
        self.assertIsInstance(casing.api_lines, list, 'api_lines (limits) is not a list')
        self.assertIsInstance(casing.design_factor, dict, 'design_factor is not a dict')
        self.assertEqual(casing.design_factor['vme'], 1.25, 'df_vme is not corresponding')
