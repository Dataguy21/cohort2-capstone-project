# Clinical Insights Assistant - Starter Project

This repository contains a starter scaffold for building a GenAI-powered Clinical Insights Assistant.

## What is included
- Synthetic dataset: `data/clinical_trial_data.csv`
- Source modules in `src/`
- Notebooks (python scripts) in `notebooks/`
- Streamlit demo app at `src/ui/streamlit_app.py`
- Basic pytest tests in `tests/`
- Dockerfile and requirements

## How to run locally (quick)
1. Create a venv and install requirements:
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
2. Start Streamlit (from the project root):
   streamlit run src/ui/streamlit_app.py
3. Run tests:
   pytest -q

## Notes
- LLM / GenAI components are placeholders. Integrate OpenAI/other SDK and add prompts and prompt management.
- Replace simple simulation logic with proper statistical / ML models for realistic scenarios.
