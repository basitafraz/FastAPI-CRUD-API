from pydantic import BaseModel, EmailStr
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False
    id: Optional[int] = None


class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    pass

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str 

class UserOut(BaseModel):
    email: EmailStr
    name: str
    id: int

    class Config:
        from_attributes = True


class Login(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
    
    
