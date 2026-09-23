from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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
    return {
        "message": "Bookmark created successfully",
        "bookmark": bookmark
    }