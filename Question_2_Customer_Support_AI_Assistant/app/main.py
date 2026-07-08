import logging
import os
import tempfile
from pathlib import Path
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import ChatMessage, Document, Escalation, KnowledgeChunk
from app.schemas import ChatRequest, ChatResponse
from app.services.assistant import build_answer
from app.services.chunker import chunk_text
from app.services.parser import parse_document
from app.services.retriever import retrieve_relevant_chunks


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("support-assistant")

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Intelligent Customer Support AI Assistant",
    description="Upload knowledge base files and answer customer questions with grounded retrieval.",
    version="1.0.0",
)

app.mount("/assistant", StaticFiles(directory="app/static", html=True), name="assistant")


@app.on_event("startup")
def seed_knowledge_base():
    db = next(get_db())
    try:
        if db.query(KnowledgeChunk).count() == 0:
            faq_path = Path(__file__).resolve().parents[1] / "sample_data" / "faq.txt"
            if faq_path.exists():
                text = faq_path.read_text(encoding="utf-8")
                chunks = chunk_text(text)
                doc = Document(filename="faq.txt", content=text)
                db.add(doc)
                db.flush()
                for chunk in chunks:
                    db.add(KnowledgeChunk(document_id=doc.id, chunk_text=chunk))
                db.commit()
                logger.info("Seeded knowledge base with %d chunks from faq.txt", len(chunks))
    finally:
        db.close()


@app.get("/")
def root():
    return RedirectResponse(url="/assistant/")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    suffix = os.path.splitext(file.filename or "")[1].lower()
    if suffix not in {".pdf", ".docx", ".txt"}:
        raise HTTPException(status_code=400, detail="Only PDF, DOCX, and TXT files are supported.")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(await file.read())
            temp_path = temp_file.name

        content = parse_document(temp_path)
        chunks = chunk_text(content)
        if not chunks:
            raise HTTPException(status_code=400, detail="The document did not contain readable text.")

        document = Document(filename=file.filename or "uploaded_document", content=content)
        db.add(document)
        db.flush()

        for chunk in chunks:
            db.add(KnowledgeChunk(document_id=document.id, chunk_text=chunk))

        db.commit()
        return {"document_id": document.id, "chunks_indexed": len(chunks)}
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Document upload failed")
        raise HTTPException(status_code=500, detail=f"Could not process document: {exc}") from exc
    finally:
        if "temp_path" in locals() and os.path.exists(temp_path):
            os.remove(temp_path)


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    chunks = [row.chunk_text for row in db.query(KnowledgeChunk).all()]
    results = retrieve_relevant_chunks(payload.question, chunks)
    answer = build_answer(payload.question, results)

    db.add(ChatMessage(session_id=payload.session_id, role="user", message=payload.question))
    db.add(ChatMessage(session_id=payload.session_id, role="assistant", message=answer["answer"]))

    if answer["escalated"]:
        db.add(
            Escalation(
                session_id=payload.session_id,
                question=payload.question,
                reason=answer["reason"],
            )
        )

    db.commit()
    return ChatResponse(
        session_id=payload.session_id,
        answer=answer["answer"],
        confidence=round(float(answer["confidence"]), 4),
        escalated=answer["escalated"],
        sources=answer["sources"],
    )


@app.get("/sessions/{session_id}/history")
def session_history(session_id: str, db: Session = Depends(get_db)):
    messages = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.id.asc()).all()
    return [{"role": message.role, "message": message.message, "created_at": message.created_at} for message in messages]


@app.get("/escalations")
def list_escalations(db: Session = Depends(get_db)):
    escalations = db.query(Escalation).order_by(Escalation.id.desc()).all()
    return [
        {
            "id": item.id,
            "session_id": item.session_id,
            "question": item.question,
            "reason": item.reason,
            "status": item.status,
        }
        for item in escalations
    ]
