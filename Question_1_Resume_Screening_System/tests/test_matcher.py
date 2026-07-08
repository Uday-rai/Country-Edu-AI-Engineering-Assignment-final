from app.services.matcher import calculate_match


def test_calculate_match_returns_score_and_missing_skills():
    candidate = {
        "skills": ["python", "fastapi", "sql"],
        "experience_years": 2,
        "resume_text": "Python FastAPI SQL NLP project experience",
    }
    result = calculate_match(
        "Python FastAPI NLP engineer with SQL experience",
        ["python", "fastapi", "nlp"],
        ["docker"],
        1,
        candidate,
    )
    assert result["match_score"] > 50
    assert "nlp" in result["missing_skills"]

