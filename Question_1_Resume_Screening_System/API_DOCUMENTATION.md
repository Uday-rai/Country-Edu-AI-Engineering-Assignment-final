# API Documentation

Base URL:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## Create Job Description

```http
POST /job-description
```

```json
{
  "title": "AI Engineer Intern",
  "description": "Python, NLP, FastAPI, SQL and Docker role.",
  "required_skills": ["python", "fastapi", "nlp", "sql"],
  "preferred_skills": ["docker", "postgresql", "scikit-learn"],
  "minimum_experience": 1
}
```

## Upload Resumes

```http
POST /resumes
```

Form field:

```text
files = one or more PDF/DOCX files
```

## View Candidates

```http
GET /candidates
```

## Filter Candidates

```http
GET /candidates/filter?skill=python&min_experience=1
```

## Export Shortlist

```http
GET /export/shortlist?min_score=70
```

## Interview Questions

```http
GET /candidates/1/interview-questions
```

