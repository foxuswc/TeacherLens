"""Task-scoped calibration; no automatic profile update."""
import copy, hashlib, json
from .core import validate_rubric

def calibrate(rubric, decisions, task_id):
    validate_rubric(rubric)
    if task_id != 'R001':
        raise ValueError('当前校准模板仅适用于 R001')
    if not isinstance(decisions,dict) or set(decisions) != {'equivalence','evidence'}:
        raise ValueError('请完成两个边界判断')
    if decisions['equivalence'] not in ('accept','review') or decisions['evidence'] not in ('required','review'):
        raise ValueError('未知校准选项')
    r=copy.deepcopy(rubric)
    r['confirmed_rules']=[x for x in r.get('confirmed_rules',[]) if x.get('id')=='R01'] if decisions['equivalence']=='accept' else []
    r['force_review']='review' in decisions.values()
    r['calibration']={'task_id':task_id,'decisions':decisions.copy(),'scope':'current_task','source':'demo_user_choice','profile_updated':False}
    digest=hashlib.sha256(json.dumps(decisions,sort_keys=True).encode()).hexdigest()[:8]
    r['version']='v0.3-R001-'+digest
    return r
