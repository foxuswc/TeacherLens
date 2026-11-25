"""Usage: python validate_scores.py rubric.json draft_scores.json; structural checks only."""
import json,sys
r=json.load(open(sys.argv[1],encoding='utf-8')); rows=json.load(open(sys.argv[2],encoding='utf-8')); limits={c['id']:c['max'] for c in r['criteria']}; errors=[]
for row in rows:
    scores={}
    for c in row['criteria']:
        cid=c['id']; s=c['score']; ev=c.get('evidence','')
        if cid not in limits or cid in scores or type(s) is not int or not 0<=s<=limits.get(cid,0) or (s and (not ev or ev not in row['text'])) or (ev and ev not in row['text']): errors.append([row['id'],cid,'invalid'])
        scores[cid]=s
    if set(scores)!=set(limits) or any(type(s) is not int for s in scores.values()) or row.get('score')!=sum(s for s in scores.values() if type(s) is int): errors.append([row['id'],'total','invalid'])
print(json.dumps({'errors':errors},ensure_ascii=False)); sys.exit(bool(errors))
