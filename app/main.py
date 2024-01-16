from typing import Union, Optional
from fastapi import FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None
    
my_posts = [
  {
    "id": 1,
    "title": "First Object",
    "content": "This is the content of the first object.",
  },
  {
    "id": 2,
    "title": "Second Object",
    "content": "This is the content of the second object."
  },
]


@app.get("/")
def get_all_posts():
    return {"Hello": my_posts}

@app.get("/{id}")
def get_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            return {"data": post}
    
    # Raise an HTTP 404 exception if the loop completes without finding a matching post
    raise HTTPException(status_code=404, detail=f"Post with Id :{id} not found")

@app.post("/create", status_code= status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0,100000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.put("/update/{id}", status_code= status.HTTP_200_OK)
def update_post(post_id: int, updated_post: Post):
    # Find the post with the given post_id in my_posts
    for post in my_posts:
        if post["id"] == id:
            # Update the post with the new data from updated_post
            post.update(updated_post.dict())
            return {"message": f"Post with ID {post_id} has been updated.", "data": post}
    
    # If the post with the given post_id is not found, return an error
    raise HTTPException(status_code=404, detail=f"Post with Id :{id} not found")


@app.delete("/delete/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    for post in my_posts:
       if post["id"] == id:
           my_posts.remove(post) 
           return HTTPException(status_code=204, detail=f"Post with Id :{id} deleted successfully")

       else:
           return Response(status_code=status.HTTP_404_NOT_FOUND)
      
    raise HTTPException(status_code=404, detail=f"Post with Id :{id} not found")

    



