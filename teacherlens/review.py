"""Summarize teacher-confirmed records without treating drafts as grades."""
from .core import record_review


def confirm_review(result, score, reason, scope='single', criterion_scores=None, comment=''):
    """Validate teacher-confirmed components independently of model drafts."""
    if not isinstance(comment,str) or len(comment)>1000:
        raise ValueError('教师评语格式无效')
    if not isinstance(reason,str) or len(reason)>1000:
        raise ValueError('确认依据格式无效')
    rec=record_review(result,score,reason,scope)
    if criterion_scores is not None:
        limits={q['id']:q['max'] for q in result['criteria']}
        if not isinstance(criterion_scores,dict) or set(criterion_scores)!=set(limits):
            raise ValueError('缺少或存在未知评分维度')
        if any(type(v) is not int or not 0<=v<=limits[k] for k,v in criterion_scores.items()):
            raise ValueError('分项评分越界')
        if sum(criterion_scores.values())!=score:
            raise ValueError('分项评分与总分不一致')
        rec['criterion_scores']=criterion_scores.copy()
    rec['comment']=comment
    return rec

def summarize(rows,reviews):
    if not isinstance(rows,list) or not isinstance(reviews,list) or len(rows)>100 or len(reviews)>100:
        raise ValueError('记录格式或数量无效')
    index={r['id']:r for r in rows}
    if len(index)!=len(rows): raise ValueError('样本ID重复')
    confirmed={}
    for rev in reviews:
        rid=rev['id']
        if rid not in index or rid in confirmed: raise ValueError('未知或重复复核记录')
        row=index[rid]
        if rev.get('rule_version')!=row['rule_version'] or rev.get('ai_score')!=row['score']:
            raise ValueError('复核记录与初评版本不一致')
        confirmed[rid]=confirm_review(row,rev['teacher_score'],rev['reason'],rev['scope'],rev.get('criterion_scores'),rev.get('comment',''))
    n=len(confirmed); changed=sum(x['ai_score']!=x['teacher_score'] or any(q['score']!=x.get('criterion_scores',{}).get(q['id'],q['score']) for q in index[x['id']].get('criteria',[])) for x in confirmed.values())
    buckets={}
    for r in confirmed.values():
        k=str(r['teacher_score']); buckets[k]=buckets.get(k,0)+1
    parts={}
    for rid,rec in confirmed.items():
        for q in index[rid].get('criteria',[]):
            if q['id'] not in rec.get('criterion_scores',{}): continue
            p=parts.setdefault(q['id'],{'name':q['name'],'max':q['max'],'sum':0,'count':0})
            p['sum']+=rec['criterion_scores'][q['id']]; p['count']+=1
    for p in parts.values(): p['mean']=p.pop('sum')/p['count']
    return {'criteria_stats':parts,'total':len(rows),'confirmed':n,'pending':len(rows)-n,'changed':changed,'change_rate':changed/n if n else None,'mean_confirmed':sum(x['teacher_score'] for x in confirmed.values())/n if n else None,'score_distribution':buckets,'candidate_rules':[x for x in confirmed.values() if x['scope']=='rule_candidate'],'technical_badcases':[x for x in confirmed.values() if x['scope']=='technical_badcase'],'notice':'仅统计模拟教师已确认记录，不代表真实学情；候选规则未生效。'}
