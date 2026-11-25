import unittest
from teacherlens.core import ROOT,load
from teacherlens.evaluation import benchmark
class BenchmarkTests(unittest.TestCase):
    def test_fixture_comparison(self):
        r=benchmark(load(ROOT/'data/demo.json'))
        self.assertEqual(r['test_count'],12); self.assertEqual(r['calibration_count'],2)
        self.assertEqual(len(r['changes']),12)
        self.assertTrue(any(x['category']=='改善' for x in r['changes']))
        self.assertTrue(any(x['id']=='S06' and x['category']=='仍有差异' for x in r['changes']))
    def test_leakage_guard(self):
        d=load(ROOT/'data/demo.json');d['calibration'][0]['id']=d['answers'][0]['id']
        with self.assertRaises(ValueError): benchmark(d)
