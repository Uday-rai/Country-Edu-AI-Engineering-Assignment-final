from sqlalchemy import Column, DateTime, Float, Integer, String, Text, func
from app.database import Base


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    required_skills = Column(Text, nullable=False, default="")
    preferred_skills = Column(Text, nullable=False, default="")
    minimum_experience = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    skills = Column(Text, nullable=False, default="")
    education = Column(Text, nullable=False, default="")
    experience_years = Column(Integer, default=0)
    certifications = Column(Text, nullable=False, default="")
    resume_text = Column(Text, nullable=False, default="")
    match_score = Column(Float, default=0)
    matched_skills = Column(Text, nullable=False, default="")
    missing_skills = Column(Text, nullable=False, default="")
    created_at = Column(DateTime, server_default=func.now())
