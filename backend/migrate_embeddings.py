from pymongo import MongoClient
from embedding_service import generate_embedding

client = MongoClient("mongodb://localhost:27017/")
db = client["ai_bookmark"]
bookmarks_collection = db["bookmarks"]

bookmarks = bookmarks_collection.find({
    "embedding": {
        "$exists": False
    }
})

for bookmark in bookmarks:

    text = (
        bookmark.get("title", "")
        + "\n"
        + bookmark.get("content", "")
    )
    print (f"Generating embedding for bookmark: {bookmark.get('title', '')}")
    embedding = generate_embedding(text)
    bookmarks_collection.update_one(
        {"_id": bookmark["_id"]},
        {"$set": {"embedding": embedding}}
    )

    print(
        f"Saved embedding with "
        f"{len(embedding)} dimensions"
    )


print("Embedding migration completed.")