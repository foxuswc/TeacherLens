import unittest
from unittest.mock import patch
from teacherlens.core import ROOT,load,grade,metrics,record_review
class CoreTests(unittest.TestCase):
    def setUp(self): self.d=load(ROOT/'data/demo.json'); self.a=self.d['answers'][0]; self.r=self.d['rubric']
    def test_total(self):
        x=grade(self.d['task'],self.a,self.r); self.assertEqual(x['score'],4); self.assertEqual(x['status'],'draft')
    def test_calibration(self):
        a=self.d['answers'][2]; self.assertEqual(grade(self.d['task'],a,self.r,'rubric')['score'],2); self.assertEqual(grade(self.d['task'],a,self.r)['score'],4)
    def test_missing_evidence(self):
        with patch('teacherlens.core.model_grade',return_value={'criteria':[{'id':'trait','score':2,'evidence':'fake'}],'needs_review':False}):
            r=grade(self.d['task'],self.a,self.r,engine='llm'); self.assertIsNone(r['score']); self.assertTrue(r['needs_review'])
    def test_review(self):
        x=grade(self.d['task'],self.a,self.r); self.assertFalse(record_review(x,3,'示例','rule_candidate')['rule_applied']); self.assertRaises(ValueError,record_review,x,5,'错误')
    def test_metrics(self):
        self.assertEqual(metrics([{'id':'a','score':None,'needs_review':True}],{'a':2})['coverage'],0)
    def test_no_calibration_leak(self): self.assertFalse({x['id'] for x in self.d['calibration']} & {x['id'] for x in self.d['answers']})
if __name__=='__main__': unittest.main()
