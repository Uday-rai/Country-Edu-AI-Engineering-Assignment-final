from app.services.retriever import RetrievalResult


UNKNOWN_ANSWER = "I don't know"
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "does", "for",
    "from", "how", "i", "in", "is", "it", "my", "of", "on", "or", "the",
    "to", "what", "when", "where", "with", "you", "your"
}


def build_answer(question: str, results: list[RetrievalResult], threshold: float = 0.12) -> dict:
    if not results or results[0].score < threshold:
        return {
            "answer": UNKNOWN_ANSWER,
            "confidence": results[0].score if results else 0.0,
            "escalated": True,
            "sources": [],
            "reason": "No knowledge base chunk was relevant enough to answer safely.",
        }

    useful_results = [result for result in results if result.score >= threshold]
    evidence = " ".join(result.text for result in useful_results)
    answer = summarize_evidence(question, evidence)

    return {
        "answer": answer,
        "confidence": results[0].score,
        "escalated": False,
        "sources": [result.text[:180] for result in useful_results],
        "reason": "",
    }


def summarize_evidence(question: str, evidence: str) -> str:
    sentences = [sentence.strip() for sentence in evidence.replace("\n", " ").split(".") if sentence.strip()]
    question_terms = {
        term.strip("?:!,.;").lower()
        for term in question.split()
        if term.strip("?:!,.;").lower() not in STOPWORDS
    }

    ranked = sorted(
        sentences,
        key=lambda sentence: len(question_terms.intersection({
            term.strip("?:!,.;").lower()
            for term in sentence.split()
        })),
        reverse=True,
    )
    selected = [sentence for sentence in ranked[:2] if sentence]
    if not selected:
        return UNKNOWN_ANSWER
    response = ". ".join(selected)
    if not response.endswith("."):
        response += "."
    return response
