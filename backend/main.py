from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from embedding_service import generate_embedding
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
    bookmark_data = bookmark.model_dump()

    text = (
        bookmark_data["title"] + "\n" + bookmark_data["content"]
    )
    embedding = generate_embedding(text)
    bookmark_data["embedding"] = embedding

    try:
        result = bookmarks_collection.insert_one(bookmark_data)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail="Bookmark with this URL already exists"
        )
    return {
        "message": "Bookmark created successfully",
        "id": str(result.inserted_id),
        "bookmark": {
            "title": bookmark_data["title"],
            "url": bookmark_data["url"],
            "content": bookmark_data["content"]
        }
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
    bookmarks = list(bookmarks_collection.find({
        "embedding": {
            "$exists": True
        }
    }))
    if not bookmarks:
        return {
            "query": query,
            "count": 0,
            "bookmarks": []
        }
    results = semantic_search(query, bookmarks, top_k)

    response = []

    for bookmark, score in results:
        bookmark["_id"] = str(bookmark["_id"])
        response.append({
            "id": bookmark["_id"],
            "title": bookmark["title"],
            "url": bookmark["url"],
            "content": bookmark["content"],
            "similarity_score": float(score)
        })

    return {
        "query": query,
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