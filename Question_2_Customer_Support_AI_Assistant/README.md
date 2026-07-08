# Customer Support Knowledge Base Assistant

I built this as a FastAPI service that lets you upload company documents and ask support questions against them. If the knowledge base doesn't have enough to answer confidently, it returns a clear "I don't know" and queues the query for escalation.

## Run

```bash
python -m pip install -r requirements.txt
python run.py
```

The script picks a free port automatically and prints the URL to open.

SQLite is the default — no database setup needed. To run with PostgreSQL instead:

```bash
docker-compose up --build
```

## How It Works

Upload one or more documents (PDF, DOCX, or TXT) and the service chunks and indexes them. When a question comes in, it retrieves the most relevant chunks and builds an answer. Conversation history is tracked per session, so follow-up questions have context. Anything the system can't answer confidently gets logged as an escalation.

## Endpoints

| Method | Path | What It Does |
|---|---|---|
| GET | `/health` | Service health check |
| POST | `/documents/upload` | Upload PDF, DOCX, or TXT files |
| POST | `/chat` | Ask a question against the knowledge base |
| GET | `/sessions/{session_id}/history` | View conversation history for a session |
| GET | `/escalations` | List queries that couldn't be answered |

## Sample Data

`sample_data/faq.txt` has a sample knowledge base ready to upload for a quick demo.
