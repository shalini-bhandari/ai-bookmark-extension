from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_search(query, documents):
    query_embedding = model.encode([query])
    document_embeddings = model.encode(documents)

    similarities = cosine_similarity(query_embedding, document_embeddings)[0]

    results = list(zip(documents, similarities))
    results.sort(key=lambda x: x[1], reverse=True)
    return results

documents = [
    "I love Python programming.",
    "Python is my favorite programming language.",
    "I went hiking in the mountains.",
    "Docker containers allow applications to run in isolated environments.",
    "Machine learning models can learn patterns from data."
]

query = "I want to learn Python"

results = semantic_search(query, documents)

print("\nQuery:", query)
print("\nResults:")

for document, score in results:
    print(
        f"{score:.4f}  →  {document}"
    )