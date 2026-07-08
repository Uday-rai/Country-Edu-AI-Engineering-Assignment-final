from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class RetrievalResult:
    text: str
    score: float


def retrieve_relevant_chunks(question: str, chunks: list[str], top_k: int = 3) -> list[RetrievalResult]:
    if not question.strip() or not chunks:
        return []

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform([question] + chunks)
    scores = cosine_similarity(matrix[0], matrix[1:])[0]
    ranked = sorted(zip(chunks, scores), key=lambda item: item[1], reverse=True)
    return [RetrievalResult(text=text, score=round(float(score), 4)) for text, score in ranked[:top_k]]
