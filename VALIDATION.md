# V1 Validation Record — November 9, 2026

## User-reported Windows / PyCharm execution
- Four Streamlit modules visually reviewed in screenshots.
- CSV and JSON exports downloaded and reviewed.
- Synthetic dataset: 6 rows; 3 PASS; 3 REVIEW.
- Unit test command: `python -m unittest discover -s tests -v`
- Reported result: `Ran 8 tests in 0.075s` / `OK`.
- Test names: test_conversion, test_duplicate, test_hash, test_negative, test_retrieve, test_schema, test_url, test_valid.

## Scope and limits
Validation confirms the demonstrated educational workflow and reported unit tests; it is not an independent production audit. Synthetic records only; no real-world climate impact. Keyword retrieval is not generative RAG. Multi-agent orchestration and live UNFCCC ingestion are not implemented.

## Evidence
A four-screen validation montage is available in the final project archive. Screenshots are not included in this GitHub commit.
