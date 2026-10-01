from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_search(query: str, bookmarks: list, top_k: int = 5):
    query_embedding = model.encode([query])
    document_embeddings = [bookmark['embedding'] for bookmark in bookmarks]

    similarities = cosine_similarity(query_embedding, document_embeddings)[0]

    results = list(zip(bookmarks, similarities))
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_k]