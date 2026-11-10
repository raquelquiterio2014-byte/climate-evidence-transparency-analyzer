"""Deterministic, offline climate evidence quality checks."""
from __future__ import annotations
import hashlib
import re
from datetime import datetime, timezone
import pandas as pd

REQUIRED = ['country','year','sector','gas','value','unit','source_url']
VALID_UNITS = {'tCO2e','ktCO2e','MtCO2e'}

def normalize(df: pd.DataFrame) -> pd.DataFrame:
    missing = set(REQUIRED)-set(df.columns)
    if missing: raise ValueError('Missing columns: '+', '.join(sorted(missing)))
    out=df.copy()
    out['year']=pd.to_numeric(out['year'],errors='coerce')
    out['value']=pd.to_numeric(out['value'],errors='coerce')
    for col in ['country','sector','gas','unit','source_url']:
        out[col]=out[col].fillna('').astype(str).str.strip()
    return out

def audit(df: pd.DataFrame) -> pd.DataFrame:
    df=normalize(df)
    findings=[]
    now=datetime.now(timezone.utc).year
    for i,row in df.iterrows():
        issues=[]
        if pd.isna(row['year']) or row['year']<1990 or row['year']>now: issues.append('Invalid or future year')
        if pd.isna(row['value']): issues.append('Missing/non-numeric value')
        elif row['value']<0: issues.append('Negative value: verify whether removals are intended')
        if row['unit'] not in VALID_UNITS: issues.append('Unsupported unit')
        if not row['source_url'].startswith(('https://','http://')): issues.append('Missing source URL')
        if not row['country'] or not row['sector'] or not row['gas']: issues.append('Missing identifying field')
        findings.append({'row':int(i)+1,'severity':'REVIEW' if issues else 'PASS','finding':'; '.join(issues) or 'Basic checks passed'})
    dup=df.duplicated(subset=['country','year','sector','gas'],keep=False)
    for i,flag in enumerate(dup):
        if flag:
            findings[i]['severity']='REVIEW'
            findings[i]['finding'] += '; Duplicate country/year/sector/gas key'
    return pd.DataFrame(findings)

def to_tonnes(df: pd.DataFrame) -> pd.DataFrame:
    df=normalize(df)
    multipliers={'tCO2e':1,'ktCO2e':1_000,'MtCO2e':1_000_000}
    df['tonnes_co2e']=df.apply(lambda r: r['value']*multipliers[r['unit']] if r['unit'] in multipliers and pd.notna(r['value']) else float('nan'),axis=1)
    return df

def retrieve(query: str, documents: list[dict], limit: int=5) -> list[dict]:
    """Transparent keyword retrieval, not LLM-based RAG."""
    words=set(re.findall(r'[a-z0-9]{3,}',query.lower()))
    scored=[]
    for d in documents:
        content=d.get('text','')
        tokens=set(re.findall(r'[a-z0-9]{3,}',content.lower()))
        score=len(words & tokens)
        if score: scored.append({'title':d.get('title','Untitled'),'source':d.get('source',''), 'score':score,'excerpt':content[:600]})
    return sorted(scored,key=lambda d:-d['score'])[:limit]

def file_sha256(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()
