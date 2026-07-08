# AI Enginering Submission

Two FastAPI services: a resume screening system and a customer support assistant.

No database setup needed — both use SQLite and create it automatically on first run.

---

## Question 1 — Resume Screening System

Run these three commands from the `Uday/` folder:

```bash
cd Question_1_Resume_Screening_System
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open **http://127.0.0.1:8000/dashboard/?v=3** in the browser.

Swagger docs: http://127.0.0.1:8000/docs

---

## Question 2 — Customer Support Assistant

Open a **new terminal** from the `Uday/` folder, then:

```bash
cd Question_2_Customer_Support_AI_Assistant
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8010
```

Open **http://127.0.0.1:8010/assistant** in the browser.

Swagger docs: http://127.0.0.1:8010/docs