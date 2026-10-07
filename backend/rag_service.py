from semantic_search import semantic_search
from llm_service import generate_answer

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

def answer_question(query, bookmarks, top_k = 3):
    context, sources = retrieve_context(query, bookmarks, top_k)
    if not context:
        return {
            "answer": "I couldn't find relevant information in your saved bookmarks.",
            "sources": []
        }
    answer = generate_answer(query, context)

    return {
        "answer": answer,
        "sources": sources
    }