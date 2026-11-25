"""Same-source, held-out fixture comparison. Not evidence of real AI efficacy."""
from .core import grade, metrics
from .calibration import calibrate

def benchmark(d):
    ids=[a['id'] for a in d['answers']]
    if len(ids)!=len(set(ids)) or set(ids)&{a['id'] for a in d['calibration']}:
        raise ValueError('评测样本重复或与校准集重叠')
    gold={a['id']:a['gold'] for a in d['answers']}
    clean=[{k:a[k] for k in ('id','text','ambiguous') if k in a} for a in d['answers']]
    r=calibrate(d['rubric'],{'equivalence':'accept','evidence':'required'},d['task']['id'])
    runs={mode:[grade(d['task'],a,r,mode,'demo') for a in clean] for mode in ('baseline','rubric','calibrated')}
    before={a['id']:a for a in runs['rubric']}
    changes=[]
    for a in runs['calibrated']:
        i=a['id']; old=before[i]['score']; new=a['score']; g=gold[i]
        label='改善' if old!=g and new==g else '退化' if old==g and new!=g else '仍有差异' if new!=g else '保持正确'
        changes.append({'id':i,'text':a['text'],'reference':g,'before':old,'after':new,'category':label,'review':a['needs_review']})
    return {'engine':'demo','notice':'人工构造样本与关键词引擎；不能推断真实模型准确率或实际提效。','calibration_count':len(d['calibration']),'test_count':len(clean),'metrics':{k:metrics(v,gold) for k,v in runs.items()},'changes':changes}
