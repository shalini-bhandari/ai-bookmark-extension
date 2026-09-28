from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")

db = client["ai_bookmark"]
bookmarks_collection = db["bookmarks"]

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
    result = bookmarks_collection.insert_one(bookmark_data)
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