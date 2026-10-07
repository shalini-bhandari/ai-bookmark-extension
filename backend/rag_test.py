from pymongo import MongoClient

from rag_service import retrieve_context


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


context, sources = retrieve_context(
    question,
    bookmarks,
    top_k=3
)


print("\nCONTEXT:")
print(context)

print("\nSOURCES:")
print(sources)