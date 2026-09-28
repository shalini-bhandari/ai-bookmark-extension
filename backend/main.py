from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

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
        "bookmark": bookmark
    }

@app.get("/bookmarks")
def get_bookmarks():
    bookmarks = list(bookmarks_collection.find())

    for bookmark in bookmarks:
        bookmark["_id"] = str(bookmark["_id"])

    return {
        "bookmarks": bookmarks
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