import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from embedding_service import generate_embedding


def semantic_search(query, bookmarks, top_k=5):

    query_embedding = generate_embedding(query)
    query_embedding = np.asarray(query_embedding)
    query_embedding = query_embedding.reshape(1, -1)

    results = []

    for bookmark in bookmarks:

        for chunk in bookmark["chunks"]:

            # Convert chunk embedding to NumPy array
            chunk_embedding = np.asarray(
                chunk["embedding"]
            )
            chunk_embedding = chunk_embedding.reshape(1, -1)

            similarity = cosine_similarity(
                query_embedding,
                chunk_embedding
            )[0][0]

            results.append(
                (
                    bookmark,
                    float(similarity),
                    chunk
                )
            )

    # Highest similarity first
    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return results[:top_k]