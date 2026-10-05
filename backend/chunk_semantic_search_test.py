from pymongo import MongoClient
from sklearn.metrics.pairwise import cosine_similarity

from embedding_service import generate_embedding


# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["ai_bookmark"]
bookmarks_collection = db["bookmarks"]

# Query
query = "Which HTTP method is used to create new data?"

print("\nQuery:")
print(query)

# Generate query embedding
query_embedding = generate_embedding(query)

print(
    "\nQuery embedding dimensions:",
    len(query_embedding)
)

# Get bookmarks containing chunks
bookmarks = list(
    bookmarks_collection.find({
        "chunks": {
            "$exists": True,
            "$ne": []
        }
    })
)

print(
    "\nBookmarks with chunks:",
    len(bookmarks)
)
results = []

# Compare query with every chunk
for bookmark in bookmarks:

    print(
        f"Processing: {bookmark['title']} "
        f"({len(bookmark['chunks'])} chunks)"
    )

    for chunk in bookmark["chunks"]:

        similarity = cosine_similarity(
            [query_embedding],
            [chunk["embedding"]]
        )[0][0]

        results.append({
            "title": bookmark["title"],
            "url": bookmark["url"],
            "chunk_index": chunk["index"],
            "text": chunk["text"],
            "similarity_score": float(similarity)
        })

print(
    "\nTotal chunk comparisons:",
    len(results)
)

# Sort by similarity
results.sort(
    key=lambda x: x["similarity_score"],
    reverse=True
)

print("\nTop matching chunks:")

for result in results[:5]:

    print("\n")

    print(
        "Title:",
        result["title"]
    )

    print(
        "Chunk:",
        result["chunk_index"]
    )

    print(
        "Similarity:",
        round(
            result["similarity_score"],
            4
        )
    )

    print(
        "Text:",
        result["text"]
    )