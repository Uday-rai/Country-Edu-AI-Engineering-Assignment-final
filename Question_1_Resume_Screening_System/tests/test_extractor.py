from app.services.extractor import extract_candidate_profile


def test_extract_candidate_profile():
    text = """
    Uday Sharma
    uday@example.com
    +91 9876543210
    Skills: Python, FastAPI, SQL, Docker
    Education: B.Tech in Computer Science
    2 years of experience
    Certified Machine Learning Foundations
    """
    profile = extract_candidate_profile(text)
    assert profile["email"] == "uday@example.com"
    assert "python" in profile["skills"]
    assert profile["experience_years"] == 2
    assert profile["certifications"]

