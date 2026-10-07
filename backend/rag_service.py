from semantic_search import semantic_search

def retrieve_context(query, bookmarks, top_k = 3):
    results = semantic_search(query, bookmarks, top_k)
    context_parts = []
    sources = []

    for bookmark, score, chunk in results:
        context_parts.append(
            f"Source: {bookmark['title']}\n"
            f"Content: {chunk['text']}"
        )

        sources.append({
            "title": bookmark["title"],
            "url": bookmark["url"],
            "chunk_index": chunk["index"],
            "similarity_score": float(score)
        })

    context = "\n\n".join(context_parts)

    return context, sources