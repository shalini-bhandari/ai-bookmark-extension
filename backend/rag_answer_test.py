from pymongo import MongoClient

from rag_service import answer_question


client = MongoClient("mongodb://localhost:27017/")

db = client["ai_bookmark"]

bookmarks_collection = db["bookmarks"]


bookmarks = list(
    bookmarks_collection.find({
        "chunks": {
            "$exists": True,
            "$ne": []
        }
    })
)

question = "Which HTTP method is used to create new data?"

result = answer_question(
    question,
    bookmarks,
    top_k=3
)

print("\nANSWER:")
print(result["answer"])

print("\nSOURCES:")
for source in result["sources"]:
    print(
        f"{source['title']}:"
        f"chunk {source['chunk_index']}:"
        f"score {source['similarity_score']:.4f}"
    )