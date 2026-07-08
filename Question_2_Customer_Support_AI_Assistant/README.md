# Customer Support Knowledge Base Assistant

I built this as a FastAPI service that lets you upload company docs and answer support questions against that knowledge base. If there isn't enough information to answer confidently, it returns `I don't know` and queues an escalation.

## Setup and Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8010
```

Open:

- Assistant UI: `http://127.0.0.1:8010/assistant`
- Swagger docs: `http://127.0.0.1:8010/docs`

SQLite is used by default — no database setup required. To run with PostgreSQL, use Docker:

```bash
docker-compose up --build
```

## Features

- PDF, DOCX and TXT knowledge base upload
- Document parsing and chunking
- Retrieval-based answer generation
- Conversation history by session
- Escalation for unanswered queries

## Main Endpoints

- `GET /health`
- `POST /documents/upload`
- `POST /chat`
- `GET /sessions/{session_id}/history`
- `GET /escalations`

## Sample Data

Use `sample_data/faq.txt` for a quick demo.

