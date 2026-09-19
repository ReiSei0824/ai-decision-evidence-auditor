import argparse, json
from datetime import datetime, timezone
from pathlib import Path

REQ={'id','claim','impact','source_url','published_at','accessed_at','support','confidence'}
ALLOWED_IMPACT={'low','medium','high'}
ALLOWED_SUPPORT={'direct','partial','related','contradicted','missing','unverified'}

def parse_date(v):
    if not v: return None
    return datetime.fromisoformat(v.replace('Z','+00:00'))

def audit(rows):
    seen_id=set(); seen_url={}; results=[]
    now=datetime.now(timezone.utc)
    for i,row in enumerate(rows,1):
        missing=sorted(REQ-set(row))
        issues=[]
        if missing: issues.append('missing fields: '+', '.join(missing))
        cid=str(row.get('id',f'row-{i}'))
        if cid in seen_id: issues.append('duplicate id')
        seen_id.add(cid)
        impact=row.get('impact')
        support=row.get('support')
        if impact not in ALLOWED_IMPACT: issues.append('invalid impact')
        if support not in ALLOWED_SUPPORT: issues.append('invalid support')
        url=str(row.get('source_url','')).strip()
        if url:
            seen_url.setdefault(url,[]).append(cid)
        for key in ('published_at','accessed_at'):
            try:
                dt=parse_date(row.get(key))
                if dt and dt.astimezone(timezone.utc)>now: issues.append(f'{key} is in the future')
            except Exception: issues.append(f'invalid {key}')
        if impact=='high' and support not in {'direct','contradicted'}:
            issues.append('high-impact claim lacks direct evidence')
        if support in {'missing','contradicted'}: status='BLOCK'
        elif issues or support in {'partial','related','unverified'}: status='REVIEW'
        else: status='PASS'
        results.append({'id':cid,'claim':row.get('claim',''),'status':status,'issues':issues,'url':url})
    duplicate_urls={u:ids for u,ids in seen_url.items() if len(ids)>1}
    return results,duplicate_urls

def render(results,dupes):
    overall='PASS'
    if any(r['status']=='BLOCK' for r in results): overall='BLOCK'
    elif any(r['status']=='REVIEW' for r in results): overall='REVIEW'
    lines=['# Evidence-chain structural audit','',f'Overall: **{overall}**','',
           '| ID | Claim | Status | Issues |','|---|---|---|---|']
    for r in results:
        claim=str(r['claim']).replace('|','\\|')
        issues='; '.join(r['issues']) or 'none'
        lines.append(f"| {r['id']} | {claim} | {r['status']} | {issues} |")
    lines += ['','## Duplicate source URLs','']
    if dupes:
        lines += [f'- {u}: {", ".join(ids)}' for u,ids in dupes.items()]
    else: lines.append('- None')
    lines += ['','> This tool checks ledger structure and decision rules. It does not verify whether a web source is true or supports the claim.']
    return '\n'.join(lines)+'\n'

def main():
    p=argparse.ArgumentParser(); p.add_argument('input'); p.add_argument('--out',required=True); a=p.parse_args()
    rows=json.loads(Path(a.input).read_text(encoding='utf-8'))
    if not isinstance(rows,list): raise SystemExit('input must be a JSON list')
    results,dupes=audit(rows); Path(a.out).write_text(render(results,dupes),encoding='utf-8')
    print(json.dumps({'claims':len(results),'pass':sum(r['status']=='PASS' for r in results),'review':sum(r['status']=='REVIEW' for r in results),'block':sum(r['status']=='BLOCK' for r in results),'duplicate_urls':len(dupes)}))
    raise SystemExit(2 if any(r['status']=='BLOCK' for r in results) else 0)
if __name__=='__main__': main()
