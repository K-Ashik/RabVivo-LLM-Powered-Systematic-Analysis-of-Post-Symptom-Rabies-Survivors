# RABV Survivor Analysis with LLM

## Project Overview
This project analyzes published clinical and immunological data on rare post-symptom rabies survivors using LLM-powered text synthesis and knowledge graph construction.

![Screenshot 2026-03-27 at 10 56 27](https://github.com/user-attachments/assets/e28c66b9-57ca-4bd4-9f6a-8f0ca92c2f61)


## Goal
Understand why the ~6 known post-symptom rabies survivors survived when post-symptom rabies is otherwise ~100% fatal.

## Research Question
What genetic, immunological, and viral factors distinguish survivors from fatal cases?

## Tech Stack
- **Data Collection:** PubMed API
- **LLM:** Groq Cloud (LLaMA)
- **Processing:** Python, pandas, spaCy
- **Dashboard:** Streamlit
- **Development:** structured loop pipeline

## Project Phases
1. Data Collection (PubMed abstracts & case reports)
2. LLM Entity & Relation Extraction
3. Data Synthesis & Analysis
4. Hypothesis Generation
5. Dashboard & Visualization
<img width="1536" height="1024" alt="RabVivo" src="https://github.com/user-attachments/assets/23872e10-ddb4-4e3a-a0ed-930fa8e95151" />

## Setup
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt

```

## Usage
Dashboard: streamlit run dashboard/app.py
