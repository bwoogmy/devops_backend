from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    content: str = Field(..., max_length=280, min_length=1)
    author: str = Field(..., max_length=50, min_length=1)


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    likes_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class PostList(BaseModel):
    total: int
    posts: list[PostResponse]


class LikeResponse(BaseModel):
    id: int
    likes_count: int
