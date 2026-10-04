import re


def split_into_sentences(text):

    sentences = re.split(
        r'(?<=[.!?])\s+',
        text.strip()
    )

    return sentences


def chunk_text(
    text,
    chunk_size=3,
    overlap=1
):

    sentences = split_into_sentences(text)

    chunks = []

    start = 0

    while start < len(sentences):

        end = start + chunk_size

        chunk = " ".join(
            sentences[start:end]
        )

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


text = """
Python is a programming language.
FastAPI is a Python web framework.
It can be used to build REST APIs.
Python is also popular in machine learning.
PyTorch and TensorFlow are popular machine learning libraries.
Python can also be used for automation.
"""


sentences = split_into_sentences(text)

print("Sentences:")

for sentence in sentences:
    print("-", sentence)


chunks = chunk_text(text)

print("\nChunks:")

for i, chunk in enumerate(chunks):

    print(f"\nChunk {i + 1}:")
    print(chunk)