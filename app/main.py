from typing import Union, Optional
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends
from psycopg2.extras import RealDictCursor
import psycopg2
from psycopg2 import pool
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import SessionLocal, engine, get_db
from .database import Base
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from .routers import post, user, login


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

db_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=5000,
    host="localhost",
    database="FastAPI",
    user="postgres",
    password="password123",
    cursor_factory=RealDictCursor,
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(login.router)
