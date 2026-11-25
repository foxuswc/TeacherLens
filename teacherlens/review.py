"""Summarize teacher-confirmed records without treating drafts as grades."""
from .core import record_review

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
        confirmed[rid]=record_review(row,rev['teacher_score'],rev['reason'],rev['scope'])
    n=len(confirmed); changed=sum(x['ai_score']!=x['teacher_score'] for x in confirmed.values())
    buckets={}
    for r in confirmed.values():
        k=str(r['teacher_score']); buckets[k]=buckets.get(k,0)+1
    return {'total':len(rows),'confirmed':n,'pending':len(rows)-n,'changed':changed,'change_rate':changed/n if n else None,'mean_confirmed':sum(x['teacher_score'] for x in confirmed.values())/n if n else None,'score_distribution':buckets,'candidate_rules':[x for x in confirmed.values() if x['scope']=='rule_candidate'],'technical_badcases':[x for x in confirmed.values() if x['scope']=='technical_badcase'],'notice':'仅统计模拟教师已确认记录，不代表真实学情；候选规则未生效。'}
