import argparse, csv, json, sys
from pathlib import Path
from .core import ROOT, load, dump, grade, metrics

def main():
    p=argparse.ArgumentParser(description='TeacherLens evaluation runner')
    p.add_argument('--data',default=str(ROOT/'data/demo.json')); p.add_argument('--engine',choices=['demo','llm'],default='demo'); p.add_argument('--out',default='outputs'); args=p.parse_args()
    d=load(args.data); out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    gold={a['id']:a['gold'] for a in d['answers'] if 'gold' in a}; summary={}; allrows={}
    for mode in ('baseline','rubric','calibrated'):
        rows=[grade(d['task'], {'id':a['id'],'text':a['text'],'ambiguous':a.get('ambiguous',False)}, d['rubric'],mode,args.engine) for a in d['answers']]
        allrows[mode]=rows; summary[mode]=metrics(rows,gold)
        dump(out/f'{mode}.json',rows)
    with (out/'badcases.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f); w.writerow(['id','reference_score','baseline','rubric','calibrated','review','flags'])
        for a,b,c in zip(*allrows.values()):
            if c['score'] != gold.get(c['id']) or c['needs_review']:
                w.writerow([c['id'],gold.get(c['id']),a['score'],b['score'],c['score'],c['needs_review'],'; '.join(c['flags'])])
    report={'notice':d.get('notice'),'engine':args.engine,'rule_version':d['rubric']['version'],'metrics':summary}
    dump(out/'summary.json',report); print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
