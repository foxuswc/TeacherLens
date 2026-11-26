import unittest
from teacherlens.core import ROOT, load, grade
from teacherlens.review import confirm_review, summarize
class ComponentReviewTests(unittest.TestCase):
    def setUp(self):
        d=load(ROOT/'data/demo.json')
        self.row=grade(d['task'],d['answers'][0],d['rubric'])
    def test_component_total(self):
        r=confirm_review(self.row,3,'教师确认','single',{'trait':2,'evidence':1},'评语')
        self.assertEqual(r['teacher_score'],3)
        self.assertEqual(r['comment'],'评语')
        self.assertFalse(r['rule_applied'])
    def test_bad_component(self):
        for parts in ({'trait':3,'evidence':0},{'trait':2},{'trait':2,'evidence':2}):
            with self.assertRaises(ValueError):
                confirm_review(self.row,3,'确认','single',parts)
    def test_confirmed_stats_only(self):
        r=confirm_review(self.row,3,'确认','single',{'trait':2,'evidence':1})
        s=summarize([self.row],[r])
        self.assertEqual(s['criteria_stats']['evidence']['mean'],1)
        self.assertEqual(s['changed'],1)
        self.assertEqual(summarize([self.row],[])['criteria_stats'],{})
    def test_legacy_record(self):
        r=confirm_review(self.row,4,'确认')
        self.assertNotIn('criterion_scores',r)
