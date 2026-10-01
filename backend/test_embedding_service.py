from embedding_service import generate_embedding

text = "I want to learn Python"

embedding = generate_embedding(text)

print("Number of dimensions:", len(embedding))
print("First 10 values:", embedding[:10])