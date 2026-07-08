from pydantic import BaseModel


class JobDescriptionCreate(BaseModel):
    title: str
    description: str
    required_skills: list[str]
    preferred_skills: list[str] = []
    minimum_experience: int = 0


class CandidateResponse(BaseModel):
    id: int
    name: str | None
    email: str | None
    phone: str | None
    skills: list[str]
    education: str
    experience_years: int
    certifications: list[str]
    match_score: float
    matched_skills: list[str]
    missing_skills: list[str]

    class Config:
        from_attributes = True
