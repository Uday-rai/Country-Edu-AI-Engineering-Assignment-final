import re


SKILL_LIBRARY = {
    "python", "fastapi", "flask", "django", "sql", "postgresql", "mysql",
    "machine learning", "deep learning", "nlp", "pandas", "numpy",
    "scikit-learn", "tensorflow", "pytorch", "docker", "aws", "git",
    "rest api", "linux", "data analysis", "excel", "power bi", "javascript"
}

EDUCATION_PATTERNS = [
    "b.tech", "bachelor", "bachelors", "be ", "m.tech", "master",
    "masters", "mca", "bca", "phd", "diploma"
]


def clean_list(values: list[str]) -> list[str]:
    return sorted({value.strip().lower() for value in values if value.strip()})


def extract_email(text: str) -> str | None:
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    return match.group(0) if match else None


def extract_phone(text: str) -> str | None:
    match = re.search(r"(\+?\d[\d\s\-()]{8,}\d)", text)
    return match.group(0).strip() if match else None


def extract_name(text: str) -> str | None:
    for line in text.splitlines()[:8]:
        cleaned = line.strip()
        if cleaned and not extract_email(cleaned) and len(cleaned.split()) <= 4:
            if not any(char.isdigit() for char in cleaned):
                return cleaned
    return None


def extract_skills(text: str) -> list[str]:
    lowered = text.lower()
    return clean_list([skill for skill in SKILL_LIBRARY if skill in lowered])


def extract_education(text: str) -> str:
    lines = []
    lowered_lines = text.lower().splitlines()
    for original, lowered in zip(text.splitlines(), lowered_lines):
        if any(pattern in lowered for pattern in EDUCATION_PATTERNS):
            lines.append(original.strip())
    return "; ".join(lines[:4])


def extract_experience_years(text: str) -> int:
    lowered = text.lower()
    matches = re.findall(r"(\d+)\+?\s*(?:years|year|yrs|yr)", lowered)
    numbers = [int(value) for value in matches]
    return max(numbers) if numbers else 0


def extract_certifications(text: str) -> list[str]:
    certifications = []
    for line in text.splitlines():
        lowered = line.lower()
        if "certified" in lowered or "certification" in lowered or "certificate" in lowered:
            certifications.append(line.strip())
    return certifications[:8]


def extract_candidate_profile(text: str) -> dict:
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience_years": extract_experience_years(text),
        "certifications": extract_certifications(text),
        "resume_text": text,
    }
