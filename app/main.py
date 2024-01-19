from typing import Union, Optional
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends
from pydantic import BaseModel
import random
from psycopg2.extras import RealDictCursor
import psycopg2
import time
from psycopg2 import pool
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import models
from .database import SessionLocal, engine, get_db

from .database import Base

models.Base.metadata.create_all(bind=engine)






app = FastAPI()





class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    
db_pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=5000,
        host='localhost',
        database='FastAPI',
        user='postgres',
        password='password123',
        cursor_factory=RealDictCursor 
)
   

    
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
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM posts")
            posts = cursor.fetchall()
            print(posts)
        return {"posts": posts}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        db_pool.putconn(conn)

@app.get("/{id}")
def get_post(id: int):
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
            post = cursor.fetchone()

            if post:
                return {"data": post}

            raise HTTPException(status_code=404, detail=f"Post with Id {id} not found")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        db_pool.putconn(conn)

@app.post("/post", status_code= status.HTTP_201_CREATED)
def create_post(post: Post):
    
    
    post_id = random.randrange(0, 100000)
    new_post = post.dict()
    new_post['id'] = post_id
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO posts (id, title, content, published) VALUES (%s, %s, %s, %s) RETURNING *",
                (post_id, post.title, post.content, post.published)
            )
            conn.commit()  # Commit the transaction
            created_post = cursor.fetchone()  # Get the created post with all columns
            return {"data": created_post}
    except psycopg2.Error as e:
        conn.rollback()  # Rollback the transaction on error
        print(e)
        raise HTTPException(status_code=400, detail="An error occurred while inserting the post.")
    
    

@app.put("/update/{id}", status_code=200)
def update_post(id: int, updated_post: Post):
        
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM posts WHERE id = {id}")
            existing_post = cursor.fetchone()

            if existing_post:
                # Update the post with the new data from updated_post
                cursor.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s", 
                    (updated_post.title, updated_post.content, id))


                conn.commit()
                return {"message": f"Post with ID {id} has been updated.", "data": updated_post}
            else:
                raise HTTPException(status_code=404, detail=f"Post with ID {id} not found")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        conn.close()


@app.delete("/delete/{id}", status_code=204)
def delete_post(id: int):
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cursor:  # Create and manage the cursor within the context
            cursor.execute(f"SELECT * FROM posts WHERE id = {id}")
            existing_post = cursor.fetchone()

            if existing_post:
                # Delete the post with the specified ID
                cursor.execute(f"DELETE FROM posts WHERE id = {id}")
                conn.commit()
            else:
                raise HTTPException(status_code=404, detail=f"Post with ID {id} not found")
    except HTTPException:
        # Re-raise HTTPException to propagate it
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        conn.close()
        
        
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}



