import unittest
from data_pipeline.collect import normalize
class CatalogTests(unittest.TestCase):
    def product(self,**kwargs):return {"code":"12345","product_name":"TEST FIXTURE ONLY","quantity":"100 g","nutriments":{"proteins_100g":5},**kwargs}
    def test_unknown_not_zero(self):self.assertIsNone(normalize(self.product())["fat"])
    def test_zero_preserved(self):self.assertEqual(normalize(self.product(nutriments={"fat_100g":0}))["fat"],0)
    def test_nan_rejected(self):
        with self.assertRaises(ValueError):normalize(self.product(nutriments={"fat_100g":float("nan")}))
    def test_liquid_rejected(self):
        with self.assertRaises(ValueError):normalize(self.product(quantity="250 ml"))
    def test_missing_name(self):
        with self.assertRaises(ValueError):normalize(self.product(product_name=""))
    def test_no_measurements(self):
        with self.assertRaises(ValueError):normalize(self.product(nutriments={}))
    def test_provenance(self):self.assertEqual(normalize(self.product())["license"],"ODbL-1.0")
