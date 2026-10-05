from pymongo import MongoClient

from chunking_service import chunk_text
from embedding_service import generate_embedding

client = MongoClient("mongodb://localhost:27017")

db = client["ai_bookmark"]
bookmarks_collection = db["bookmarks"]

bookmarks = bookmarks_collection.find({
    "chunks": {
        "$exists": False
    }
})

for bookmark in bookmarks:
    title = bookmark.get("title", "")
    content = bookmark.get("content", "")

    print(f"\nProcessing: {title}")
    text = title + ". " + content

    chunks = chunk_text(text, chunk_size = 3, overlap = 1)
    chunk_documents = []

    for index, chunk in enumerate(chunks):
        embedding = generate_embedding(chunk)

        chunk_documents.append({
            "index": index,
            "text": chunk,
            "embedding": embedding
        })

        print(
            f"Chunk {index}: "
            f"{len(embedding)} dimensions"
        )

        bookmarks_collection.update_one(
        {
            "_id": bookmark["_id"]
        },
        {
            "$set": {
                "chunks": chunk_documents
            }
        }
    )

    print(
        f"Saved {len(chunk_documents)} chunks "
        f"for {title}"
    )
print("\nChunk migration completed.")