import pwploads
from unittest import TestCase


def default_casing():
    csg_od = 8
    csg_id = 7
    length = 1500

    casing = pwploads.Casing(csg_od, csg_id, length,
                             nominal_weight=100,
                             yield_s=80000,
                             df_burst=1.1,
                             df_collapse=1.1,
                             df_tension=1.3,
                             df_compression=1.3,
                             df_vme=1.25)

    return casing


class TestCasing(TestCase):
    def test_create_casing(self):

        casing = default_casing()
        self.assertIsInstance(casing, object, 'casing is not an object')
        self.assertEqual(casing.od, 8, 'outer diameter has been changed')
        self.assertEqual(casing.id, 7, 'inner diameter has been changed')
        self.assertIsInstance(casing.area, (float, int), 'area is not a number')
        self.assertTrue(casing.area < 20, 'the effective area is too high')
        self.assertIsInstance(casing.ellipse, list, 'triaxial ellipse is not a list')
        self.assertIsInstance(casing.csg_loads, list, 'loads is not a list')
        self.assertIsInstance(casing.nominal_weight, (float, int), 'weight is not a number')
        self.assertIsInstance(casing.api_lines, list, 'api_lines (limits) is not a list')
        self.assertIsInstance(casing.design_factor, dict, 'design_factor is not a dict')
        self.assertEqual(casing.design_factor['vme'], 1.25, 'df_vme is not corresponding')
