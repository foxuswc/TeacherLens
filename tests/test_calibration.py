import unittest
from teacherlens.core import ROOT,load,grade
from teacherlens.calibration import calibrate
class CalibrationTests(unittest.TestCase):
    def setUp(self): self.d=load(ROOT/'data/demo.json')
    def test_task_scope(self):
        r=calibrate(self.d['rubric'],{'equivalence':'accept','evidence':'required'},'R001')
        self.assertFalse(r['calibration']['profile_updated']); self.assertEqual(r['calibration']['scope'],'current_task')
        self.assertEqual(grade(self.d['task'],self.d['answers'][2],r)['score'],4)
    def test_uncertain(self):
        r=calibrate(self.d['rubric'],{'equivalence':'review','evidence':'required'},'R001')
        self.assertFalse(r['confirmed_rules']); self.assertTrue(grade(self.d['task'],self.d['answers'][0],r)['needs_review'])
    def test_reject_scope(self):
        with self.assertRaises(ValueError): calibrate(self.d['rubric'],{'equivalence':'accept','evidence':'required'},'OTHER')
    def test_incomplete(self):
        with self.assertRaises(ValueError): calibrate(self.d['rubric'],{},'R001')
