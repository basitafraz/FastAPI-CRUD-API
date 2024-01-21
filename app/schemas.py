from pydantic import BaseModel
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

