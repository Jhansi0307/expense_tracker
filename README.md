# Expense Tracker API

Backend for a personal finance app using FastAPI, PostgreSQL, JWT, and Pandas.

## Run locally

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
