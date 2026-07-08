from app.services.assistant import UNKNOWN_ANSWER, build_answer
from app.services.retriever import RetrievalResult


def test_build_answer_escalates_low_confidence():
    result = build_answer("What is the warranty?", [RetrievalResult("Refunds are available.", 0.03)])
    assert result["answer"] == UNKNOWN_ANSWER
    assert result["escalated"] is True


def test_build_answer_uses_relevant_evidence():
    result = build_answer(
        "How long does shipping take?",
        [RetrievalResult("Standard shipping takes 3 to 5 business days.", 0.55)],
    )
    assert "shipping" in result["answer"].lower()
    assert result["escalated"] is False

