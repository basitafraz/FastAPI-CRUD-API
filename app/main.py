from typing import Union, Optional
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends
from psycopg2.extras import RealDictCursor
import psycopg2
import time
from psycopg2 import pool
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine, get_db
from .database import Base
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
 
db_pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=5000,
        host='localhost',
        database='FastAPI',
        user='postgres',
        password='password123',
        cursor_factory=RealDictCursor 
)
   
@app.get("/")
def get_all_posts(db: Session = Depends(get_db)):
    conn = db_pool.getconn()
    try:
        posts = db.query(models.Post).all()
        return posts
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        db_pool.putconn(conn)
        
        

@app.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db), response_model= schemas.PostResponse):
    try:
        post = db.query(models.Post).filter(models.Post.id == id).first()
        if post:
            return post
        raise HTTPException(status_code=404, detail=f"Post with Id {id} not found")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@app.post("/post", response_model= schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    try:
        db_post = models.Post(**post.dict())
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=400, detail="An error occurred while inserting the post.")
    
    

@app.put("/update/{id}", response_model= schemas.PostCreate, status_code=status.HTTP_200_OK)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    try:
        # Retrieve the existing post by ID
        db_post = db.query(models.Post).filter(models.Post.id == id).first()

        if db_post:
            # Update the post with the new data from updated_post
            for key, value in updated_post.dict(exclude_unset=True).items():
                setattr(db_post, key, value)

            db.commit()
            db.refresh(db_post)
            return db_post
        else:
            raise HTTPException(status_code=404, detail=f"Post with ID {id} not found")
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    try:
        # Retrieve the existing post by ID
        db_post = db.query(models.Post).filter(models.Post.id == id).first()

        if db_post:
            # Delete the post
            db.delete(db_post)
            db.commit()
        else:
            raise HTTPException(status_code=404, detail=f"Post with ID {id} not found")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
        


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model= schemas.UserOut) 
def create_user(user: schemas.UserCreate ,db: Session = Depends(get_db)):
    try:
        db_user = models.User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=400, detail="An error occurred while inserting the post.")

