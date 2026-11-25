import unittest
from teacherlens.core import ROOT,load,grade,record_review
from teacherlens.review import summarize
class ReviewTests(unittest.TestCase):
    def setUp(self):
        d=load(ROOT/'data/demo.json')
        self.rows=[grade(d['task'],a,d['rubric']) for a in d['answers'][:2]]
    def test_drafts_excluded(self):
        x=summarize(self.rows,[]); self.assertIsNone(x['mean_confirmed']); self.assertEqual(x['pending'],2)
    def test_confirmed_only(self):
        r=record_review(self.rows[0],3,'模拟修改','rule_candidate')
        x=summarize(self.rows,[r]); self.assertEqual(x['mean_confirmed'],3); self.assertEqual(x['changed'],1); self.assertFalse(x['candidate_rules'][0]['rule_applied'])
    def test_stale(self):
        r=record_review(self.rows[0],3,'模拟修改'); r['rule_version']='old'
        with self.assertRaises(ValueError): summarize(self.rows,[r])
    def test_duplicate(self):
        r=record_review(self.rows[0],3,'模拟修改')
        with self.assertRaises(ValueError): summarize(self.rows,[r,r])
