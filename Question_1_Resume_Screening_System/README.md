# Resume Screening and Candidate Ranking System

I built this to automate the manual part of resume screening — upload a stack of PDFs or DOCXs and the system pulls out each candidate's info, scores them against a job description, and ranks the results. From there you can filter by skill or experience level, generate interview questions for a specific candidate, or export the shortlist to CSV.

## Run

```bash
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Dashboard: **http://127.0.0.1:8000/dashboard/?v=3**

Swagger docs: http://127.0.0.1:8000/docs

SQLite is the default — no database setup needed. To run with PostgreSQL instead:

```bash
docker-compose up --build
```

## How It Works

Post a job description first, then upload resumes. It parses each file, pulls out skills, education, experience, and contact info, then scores everything against the JD. I ended up weighting skills matching the heaviest — it's usually the clearest signal. Semantic similarity to the description and years of experience fill in the rest, with a small bump for preferred skills on top of the required ones.

Ranked results come back through `/candidates`. Filter by a specific skill or minimum experience using `/candidates/filter`, or pull anyone above a score threshold as a CSV export. There's also an interview-questions endpoint that generates role-specific questions for whichever candidate you're reviewing.

## Endpoints

| Method | Path | What It Does |
|---|---|---|
| GET | `/health` | Service health check |
| POST | `/job-description` | Set the active job description |
| POST | `/resumes` | Upload one or more PDF/DOCX files |
| GET | `/candidates` | List all ranked candidates |
| GET | `/candidates/filter` | Filter by `skill` and/or `min_experience` |
| GET | `/export/shortlist` | Download CSV above a score threshold |
| GET | `/candidates/{id}/interview-questions` | Role-specific questions based on the candidate's profile |

## Sample Data

Sample resumes are in `sample_data/`.