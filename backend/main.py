from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from sklearn.metrics.pairwise import cosine_similarity
from embedding_service import generate_embedding
from chunking_service import chunk_text
from semantic_search import semantic_search

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")

db = client["ai_bookmark"]
bookmarks_collection = db["bookmarks"]

bookmarks_collection.create_index("url", unique = True)

class Bookmark(BaseModel):
    title: str
    url: str
    content: str

@app.get("/")
def root():
    return {
          "message": "AI Bookmark API is running"
    }

@app.post("/bookmarks")
def create_bookmark(bookmark: Bookmark):
    full_text = bookmark.title + ". " + bookmark.content
    embedding = generate_embedding(full_text)

    chunks = chunk_text(full_text, chunk_size = 3, overlap = 1)

    # Generate embedding for every chunk
    chunk_documents = []

    for index, chunk in enumerate(chunks):
        chunk_embedding = generate_embedding(chunk)
        chunk_documents.append({
            "index": index,
            "text": chunk,
            "embedding": chunk_embedding
        })

    # Prepare MongoDB document
    bookmark_data = {
        "title": bookmark.title,
        "url": bookmark.url,
        "content": bookmark.content,
        "embedding": embedding,

        # Add chunk level embeddings
        "chunks": chunk_documents
    }
    result = bookmarks_collection.insert_one(bookmark_data)
    return {
        "message": "Bookmark created successfully",
        "_id": str(result.inserted_id),
        "chunks_created": len(chunk_documents)
    }

@app.delete("/bookmark/{bookmark_id}")
def delete_bookmark(bookmark_id: str) :
    try:
        object_id = ObjectId(bookmark_id)
    except Exception:
        raise HTTPException(
            status_code = 400,
            detail = "Invalid Bookmark ID"
        )

    result = bookmarks_collection.delete_one({
        "_id": object_id
    })
    if result.deleted_count == 0:
        raise HTTPException(
            status_code = 404,
            detail = "Bookmark not found"
        )
    return {
        "message": "Bookmark deleted successfully"
    }

@app.get("/bookmarks")
def get_bookmarks():
    bookmarks = list(bookmarks_collection.find())

    for bookmark in bookmarks:
        bookmark["_id"] = str(bookmark["_id"])

    return {
        "bookmarks": bookmarks
    }

@app.get("/bookmarks/search")
def search_bookmarks(query: str = Query(..., min_length = 1)):

    bookmarks = bookmarks_collection.find({
        "$or": [
            {
                "title": {
                    "$regex": query,  # perform pattern/text matching
                    "$options": "i"  # case-insensitive search
                }
            },
            {
                "content": {
                    "$regex": query,  # perform pattern/text matching
                    "$options": "i"  # case-insensitive search
                }
            }
        ]
    })

    results = list(bookmarks)
    for bookmark in results:
        bookmark["_id"] = str(bookmark["_id"])
    return {
        "query": query,
        "count" : len(results),
        "bookmarks": results
    }

@app.get("/bookmarks/semantic-search")
def semantic_search_bookmarks(query: str = Query(..., min_length = 1), top_k: int = 5):
    
    bookmarks = list(
        bookmarks_collection.find({
            "chunks": {
                "$exists": True
            }
        })
    )

    if not bookmarks:
        return {
            "query": query,
            "count": 0,
            "bookmarks": []
        }
    results = semantic_search(query, bookmarks, top_k)

    unique_bookmarks = {}

    for bookmark, score, chunk in results:
        bookmark_id = str(bookmark["_id"])
        if(bookmark_id not in unique_bookmarks or score > unique_bookmarks[bookmark_id]["similarity_score"]):
            unique_bookmarks[bookmark_id] = {
                "id": bookmark_id,
                "title": bookmark["title"],
                "url": bookmark["url"],
                "chunk_index": chunk["index"],
                "content": chunk["text"],
                "similarity_score": float(score)
            }

    response = list(unique_bookmarks.values())

    return {
        "query": str(query),
        "count": len(response),
        "bookmarks": response
    }

@app.get("/bookmarks/{bookmark_id}")
def get_bookmark(bookmark_id: str):

    try:
        object_id = ObjectId(bookmark_id)
    except Exception:
        raise HTTPException(
            status_code = 400,
            detail="Invaild bookmark ID"
        )
    bookmark = bookmarks_collection.find_one({
        "_id": object_id
    })
    if bookmark is None:
        raise HTTPException(
            status_code=404,
            detail="Bookmark not found"
        )
    bookmark["_id"] = str(bookmark["_id"])
    return {
        "bookmark": bookmark
    }