from pathlib import Path
import json
import pandas as pd
import streamlit as st
from engine import audit, normalize, retrieve, to_tonnes, file_sha256

ROOT=Path(__file__).parent
st.set_page_config(page_title='COP31 | Climate Evidence Analyzer',page_icon='🌍',layout='wide')
st.markdown('''<style>.stApp{background:#081b25;color:#edf8f6} [data-testid="stSidebar"]{background:#102b34} h1,h2,h3{color:#7ce5c2!important} .stMetric{background:#15323b;padding:14px;border-radius:12px}</style>''',unsafe_allow_html=True)
st.title('🌍 COP31 AI Solutions Lab')
st.subheader('Day 1 · Climate Evidence & Transparency Analyzer')
st.caption('Educational software prototype · Independent of UNFCCC · Synthetic demo data · Human review required')

page=st.sidebar.radio('Modules',['Overview','Emissions Quality Audit','Evidence Search','Export & Methodology'])
source=st.sidebar.file_uploader('Upload emissions CSV',type=['csv'])
if source is not None:
    raw=source.getvalue()
    try: df=normalize(pd.read_csv(source))
    except Exception as exc: st.error(f'Invalid CSV: {exc}'); st.stop()
    label='User-provided data'
else:
    raw=(ROOT/'data'/'synthetic_emissions.csv').read_bytes()
    df=normalize(pd.read_csv(ROOT/'data'/'synthetic_emissions.csv'))
    label='SYNTHETIC demonstration data — not actual national inventories'
checks=audit(df)
normalized=to_tonnes(df)

if page=='Overview':
    st.info(label)
    a,b,c=st.columns(3)
    a.metric('Records',len(df)); b.metric('Flagged for review',int((checks.severity=='REVIEW').sum())); c.metric('Countries',df.country.nunique())
    st.markdown('### Dataset preview')
    st.dataframe(df,use_container_width=True)
    st.markdown('### Emissions by year (reported figures, not verified)')
    valid=normalized.dropna(subset=['year','tonnes_co2e'])
    valid=valid[valid.tonnes_co2e>=0]
    if not valid.empty: st.bar_chart(valid.groupby('year').tonnes_co2e.sum())
    st.warning('Do not interpret the demonstration chart as actual emissions or cross-country comparability. Mixed gases and accounting boundaries require expert verification.')
elif page=='Emissions Quality Audit':
    st.info('Rule-based validation: schema, units, year, negative/missing values, source URLs, duplicate keys. No AI-generated findings.')
    st.dataframe(checks,use_container_width=True)
    st.markdown('### Unit conversion to tonnes CO₂e')
    st.dataframe(normalized[['country','year','sector','gas','value','unit','tonnes_co2e']],use_container_width=True)
    st.warning('Unit conversion does not verify whether CO₂e figures use compatible GWP metrics or reporting boundaries.')
elif page=='Evidence Search':
    st.info('Keyword evidence retrieval, not generative RAG. Results are source-linked excerpts, not verified conclusions.')
    docs=json.loads((ROOT/'data'/'evidence.json').read_text(encoding='utf-8'))
    st.markdown('### Curated reference links')
    for d in docs: st.markdown(f"- [{d['title']}]({d['source']})")
    q=st.text_input('Search for a topic',value='transparency emissions reporting')
    for result in retrieve(q,docs):
        with st.expander(f"{result['title']} · keyword score {result['score']}"):
            st.write(result['excerpt']); st.markdown(f"[Open source]({result['source']})")
    st.caption('The bundled descriptions are educational summaries, not full official documents. Open original links for authoritative evidence.')
else:
    st.markdown('### Export reproducible results')
    st.code(f'SHA-256 input: {file_sha256(raw)}')
    st.download_button('Download audit CSV',checks.to_csv(index=False).encode(),file_name='audit_results.csv',mime='text/csv')
    report={'project':'COP31 Day 1 Climate Evidence Analyzer','data_status':label,'sha256':file_sha256(raw),'records':len(df),'review_count':int((checks.severity=='REVIEW').sum()),'limitations':['Educational prototype','Rule-based checks only','No official endorsement','No real-world climate impact validated']}
    st.download_button('Download audit summary JSON',json.dumps(report,indent=2).encode(),file_name='audit_summary.json',mime='application/json')
    st.markdown('### Agent architecture roadmap')
    st.markdown('**Ingestion → Schema Validator → Evidence Retriever → Consistency Critic → Human Approval → Reporter**')
    st.markdown('The current version implements deterministic ingestion, validation, keyword retrieval and reporting. LLM agents, live UNFCCC integrations and human approval workflows are **planned, not implemented**.')
    st.markdown('### Validation')
    st.code('python -m unittest discover -s tests -v',language='bash')
