import re


def chunk_text(text: str, max_words: int = 120, overlap: int = 25) -> list[str]:
    sections = split_into_sections(text)
    chunks: list[str] = []

    for section in sections:
        words = section.split()
        if len(words) <= max_words:
            chunks.append(section)
            continue

        step = max(max_words - overlap, 1)
        for start in range(0, len(words), step):
            chunk = " ".join(words[start:start + max_words]).strip()
            if chunk:
                chunks.append(chunk)
            if start + max_words >= len(words):
                break

    return chunks


def split_into_sections(text: str) -> list[str]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    blocks = [block.strip() for block in re.split(r"\n\s*\n+", normalized) if block.strip()]
    if not blocks:
        return []

    sections: list[str] = []
    pending_heading = ""

    for block in blocks:
        compact = re.sub(r"\s+", " ", block).strip()
        if compact.endswith(":") and len(compact.split()) <= 5:
            if pending_heading:
                sections.append(pending_heading.rstrip(":"))
            pending_heading = compact
            continue

        if pending_heading:
            sections.append(f"{pending_heading} {compact}")
            pending_heading = ""
        else:
            sections.append(compact)

    if pending_heading:
        sections.append(pending_heading.rstrip(":"))

    return sections
