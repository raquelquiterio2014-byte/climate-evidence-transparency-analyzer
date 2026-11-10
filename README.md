# COP31 AI Solutions Lab — Day 1
## Climate Evidence & Transparency Analyzer · V1.0 Educational Prototype

**Independent educational project, not affiliated with UNFCCC or COP31.** All bundled emissions records are **synthetic**. No real-world emissions or impact conclusions are drawn.

### Features implemented
- Streamlit English-language dashboard and CSV uploader
- Deterministic emissions data quality audit (required columns, year, values, units, provenance URLs, duplicates)
- CO₂e unit conversion (t, kt, Mt), without assuming methodological comparability
- Transparent keyword retrieval over a small curated **reference-description** collection (not full-document RAG)
- Downloadable CSV findings, JSON summary and SHA-256 input fingerprint
- Eight automated unit tests

### Windows / PyCharm setup
1. Install Python 3.11 or 3.12.
2. Open this repository folder in PyCharm.
3. Open the terminal and run:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m streamlit run app.py
```

Open the local address shown in the terminal, usually `http://localhost:8501`.

### Input CSV schema
`country,year,sector,gas,value,unit,source_url`

Accepted units: `tCO2e`, `ktCO2e`, `MtCO2e`. The tool does not calculate gas-specific global warming potentials; the user must supply already harmonized CO₂e values. Negative values are flagged for review because removals may be legitimate. Duplicate keys are flagged, not silently discarded. The application does not verify source URLs or authenticate their contents.

### Modules
1. **Overview** — preview and basic charts.
2. **Emissions Quality Audit** — row-level quality findings and unit conversion.
3. **Evidence Search** — transparent keyword matching over curated reference descriptions.
4. **Export & Methodology** — audit exports and roadmap.

### Architecture
Implemented: **CSV ingestion → deterministic validator → keyword retriever → report export**.

Planned, **not implemented**: document/PDF ingestion, embedding-based RAG, specialized LLM agents, automated official UNFCCC ingestion, reviewer approval UI, immutable audit database, climate impact evaluation.

### Candidate authoritative sources
- [UNFCCC GHG Data Interface FAQ](https://unfccc.int/process-and-meetings/transparency-and-reporting/reporting-and-review/transparency-data-and-tools/greenhouse-gas-data/frequently-asked-questions)
- [UNFCCC Transparency and Reporting](https://unfccc.int/process-and-meetings/transparency-and-reporting)
- [IPCC 2006 Guidelines](https://www.ipcc-nggip.iges.or.jp/public/2006gl/)

### Validation evidence
- [V1 validation record](VALIDATION.md)
- User-reported local Windows test run: 8 tests, 0 failures (`Ran 8 tests in 0.075s`).

### Research integrity
- Bundled source descriptions are summaries for educational search, not the full text of the referenced documents.
- No automated official downloads, LLM API calls or paid services.
- All charts from bundled data are demonstrations, not real climate metrics.
- Human experts must verify units, GWP basis, boundaries, sector classifications, and reporting context before interpreting real data.
- No COP31 event findings or speaker claims are encoded into this project.
