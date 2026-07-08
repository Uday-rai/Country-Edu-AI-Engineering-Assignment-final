from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def normalize_skill(skill: str) -> str:
    return skill.strip().lower()


def semantic_similarity(job_description: str, resume_text: str) -> float:
    if not job_description.strip() or not resume_text.strip():
        return 0.0
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform([job_description, resume_text])
    return float(cosine_similarity(matrix[0], matrix[1])[0][0])


def calculate_match(
    job_description: str,
    required_skills: list[str],
    preferred_skills: list[str],
    minimum_experience: int,
    candidate: dict,
) -> dict:
    candidate_skills = {normalize_skill(skill) for skill in candidate.get("skills", [])}
    required = {normalize_skill(skill) for skill in required_skills}
    preferred = {normalize_skill(skill) for skill in preferred_skills}

    matched_required = sorted(required.intersection(candidate_skills))
    matched_preferred = sorted(preferred.intersection(candidate_skills))
    missing_required = sorted(required.difference(candidate_skills))

    skill_score = len(matched_required) / len(required) if required else 0
    preferred_score = len(matched_preferred) / len(preferred) if preferred else 0
    experience_years = candidate.get("experience_years", 0)
    experience_score = min(experience_years / minimum_experience, 1) if minimum_experience else 1
    similarity_score = semantic_similarity(job_description, candidate.get("resume_text", ""))

    final_score = (
        skill_score * 45
        + similarity_score * 30
        + experience_score * 15
        + preferred_score * 10
    )

    return {
        "match_score": round(min(final_score, 100), 2),
        "matched_skills": sorted(set(matched_required + matched_preferred)),
        "missing_skills": missing_required,
    }


def generate_interview_questions(candidate: dict, missing_skills: list[str]) -> list[str]:
    skills = candidate.get("skills", [])[:5]
    questions = [
        f"Can you explain one project where you used {skill} in a real workflow?"
        for skill in skills
    ]
    for skill in missing_skills[:3]:
        questions.append(f"How would you approach learning and applying {skill} for this role?")
    questions.append("Tell us about a technical problem you solved and how you measured success.")
    return questions[:8]
