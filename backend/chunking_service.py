import re

def split_into_sentences(text: str) -> list[str]:

    return re.split(
        r'(?<=[.!?])\s+',
        text.strip()
    )

def chunk_text(
    text: str,
    chunk_size: int = 3,
    overlap: int = 1
) -> list[str]:
    sentences = split_into_sentences(text)
    chunks = []
    start = 0
    while start < len(sentences):
        end = start + chunk_size
        chunk = " ".join(sentences[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks