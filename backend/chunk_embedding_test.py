from chunking_service import chunk_text
from embedding_service import generate_embedding

text = """
Python is a programming language.
FastAPI is a Python web framework.
It can be used to build REST APIs.
Python is also popular in machine learning.
PyTorch and TensorFlow are popular machine learning libraries.
Python can also be used for automation.
"""

chunks = chunk_text(text, chunk_size=3, overlap=1)

for i, chunk in enumerate(chunks):
    embedding = generate_embedding(chunk)
    print(f"Chunk {i + 1}:")
    print(chunk)

    print("Embedding dimensions:", len(embedding))

    print("First 5 values of the embedding:", embedding[:5])