from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

texts = [
    "I love Python programming.",
    "Python is my favorite programming language.",
    "I went hiking in the mountains.",
    "How do I learn Python?"
]

embeddings = model.encode(texts)

similarity_matrix = cosine_similarity(embeddings)

print("Cosine similarity matrix:")
print(similarity_matrix)

for i in range(len(texts)):
    for j in range(i + 1, len(texts)):
        print(
            f"\nSimilarity:"
            f"\n Text 1: {texts[i]}"
            f"\n Text 2: {texts[j]}"
            f"\n Score: {similarity_matrix[i][j]:.4f}"
        )