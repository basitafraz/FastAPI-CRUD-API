from typing import Union, Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None
    


@app.get("/")
def get_all_posts():
    return {"Hello": "World"}

@app.get("/{id}")
def get_single_post():
    return {"Hello": "World"}



@app.post("/post")
def create_posts(post: Post):
    
    return {"data": post}

