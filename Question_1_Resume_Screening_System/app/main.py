import logging
import os
import tempfile
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Candidate, JobDescription
from app.schemas import JobDescriptionCreate
from app.services.document_parser import extract_text
from app.services.export_service import candidates_to_csv
from app.services.extractor import extract_candidate_profile
from app.services.matcher import calculate_match, generate_interview_questions


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("resume-screening")

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Resume Screening and Candidate Ranking System",
    description="Upload resumes, extract profiles, rank candidates, filter shortlists, and export CSV results.",
    version="1.0.0",
)

app.mount("/dashboard", StaticFiles(directory="app/static", html=True), name="dashboard")


@app.get("/")
def root():
    return RedirectResponse(url="/dashboard/")


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def latest_job_description(db: Session) -> JobDescription:
    job = db.query(JobDescription).order_by(JobDescription.id.desc()).first()
    if not job:
        raise HTTPException(status_code=400, detail="Create a job description before uploading resumes.")
    return job


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/job-description")
def create_job_description(payload: JobDescriptionCreate, db: Session = Depends(get_db)):
    job = JobDescription(
        title=payload.title,
        description=payload.description,
        required_skills=",".join(payload.required_skills),
        preferred_skills=",".join(payload.preferred_skills),
        minimum_experience=payload.minimum_experience,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return {"id": job.id, "message": "Job description saved."}


@app.post("/resumes")
async def upload_resumes(files: list[UploadFile] = File(...), db: Session = Depends(get_db)):
    job = latest_job_description(db)
    saved_candidates = []

    for file in files:
        suffix = os.path.splitext(file.filename or "")[1].lower()
        if suffix not in {".pdf", ".docx"}:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.filename}")

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(await file.read())
                temp_path = temp_file.name

            text = extract_text(temp_path)
            profile = extract_candidate_profile(text)
            match = calculate_match(
                job.description,
                split_csv(job.required_skills),
                split_csv(job.preferred_skills),
                job.minimum_experience,
                profile,
            )
            candidate = Candidate(
                name=profile["name"],
                email=profile["email"],
                phone=profile["phone"],
                skills=",".join(profile["skills"]),
                education=profile["education"],
                experience_years=profile["experience_years"],
                certifications=",".join(profile["certifications"]),
                resume_text=profile["resume_text"],
                match_score=match["match_score"],
                matched_skills=",".join(match["matched_skills"]),
                missing_skills=",".join(match["missing_skills"]),
            )
            db.add(candidate)
            saved_candidates.append(candidate)
        except Exception as exc:
            logger.exception("Resume processing failed for %s", file.filename)
            raise HTTPException(status_code=500, detail=f"Could not process {file.filename}: {exc}") from exc
        finally:
            if "temp_path" in locals() and os.path.exists(temp_path):
                os.remove(temp_path)

    db.commit()
    return {"processed": len(saved_candidates), "message": "Resumes processed and ranked."}


@app.get("/candidates")
def list_candidates(db: Session = Depends(get_db)):
    candidates = db.query(Candidate).order_by(Candidate.match_score.desc()).all()
    return [
        {
            "id": candidate.id,
            "name": candidate.name,
            "email": candidate.email,
            "skills": split_csv(candidate.skills),
            "education": candidate.education,
            "experience_years": candidate.experience_years,
            "match_score": candidate.match_score,
            "matched_skills": split_csv(candidate.matched_skills),
            "missing_skills": split_csv(candidate.missing_skills),
        }
        for candidate in candidates
    ]


@app.get("/candidates/filter")
def filter_candidates(
    skill: str | None = None,
    education: str | None = None,
    min_experience: int = 0,
    db: Session = Depends(get_db),
):
    candidates = db.query(Candidate).filter(Candidate.experience_years >= min_experience).all()
    filtered = []
    for candidate in candidates:
        if skill and skill.lower() not in candidate.skills.lower():
            continue
        if education and education.lower() not in candidate.education.lower():
            continue
        filtered.append(candidate)
    return sorted(
        [{"id": c.id, "name": c.name, "email": c.email, "match_score": c.match_score} for c in filtered],
        key=lambda item: item["match_score"],
        reverse=True,
    )


@app.get("/export/shortlist")
def export_shortlist(min_score: float = 70, db: Session = Depends(get_db)):
    candidates = db.query(Candidate).filter(Candidate.match_score >= min_score).order_by(Candidate.match_score.desc()).all()
    output = candidates_to_csv(candidates)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=shortlisted_candidates.csv"},
    )


@app.get("/candidates/{candidate_id}/interview-questions")
def interview_questions(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found.")
    profile = {"skills": split_csv(candidate.skills), "resume_text": candidate.resume_text}
    return {"questions": generate_interview_questions(profile, split_csv(candidate.missing_skills))}
