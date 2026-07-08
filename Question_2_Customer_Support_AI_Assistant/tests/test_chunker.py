from app.services.chunker import chunk_text


def test_chunk_text_splits_long_text():
    text = " ".join(["word"] * 250)
    chunks = chunk_text(text, max_words=100, overlap=20)
    assert len(chunks) == 3
    assert all(chunk for chunk in chunks)


def test_chunk_text_keeps_faq_sections_separate():
    text = """
    Shipping:
    Standard shipping takes 3 to 5 business days.

    Password Reset:
    Customers can reset their password from the login page.
    """
    chunks = chunk_text(text)
    assert len(chunks) == 2
    assert "Shipping:" in chunks[0]
    assert "Password Reset:" in chunks[1]

