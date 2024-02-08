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

    
    
    class Config:
        from_attributes = True
    

