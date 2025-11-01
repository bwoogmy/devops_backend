from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional

from app.database import get_db
from app.models.post import Post, Like
from app.schemas.post import PostCreate, PostResponse, PostList, LikeResponse

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("", response_model=PostList)
def get_posts(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    total = db.query(Post).count()
    posts = db.query(Post).order_by(desc(Post.created_at)).offset(offset).limit(limit).all()
    return {"total": total, "posts": posts}


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return None


@router.post("/{post_id}/like", response_model=LikeResponse)
def like_post(
    post_id: int,
    user_identifier: str = "anonymous",
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    existing_like = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_identifier == user_identifier
    ).first()
    
    if existing_like:
        raise HTTPException(status_code=400, detail="Already liked")
    
    like = Like(post_id=post_id, user_identifier=user_identifier)
    db.add(like)
    post.likes_count += 1
    db.commit()
    db.refresh(post)
    
    return {"id": post.id, "likes_count": post.likes_count}


@router.delete("/{post_id}/like", response_model=LikeResponse)
def unlike_post(
    post_id: int,
    user_identifier: str = "anonymous",
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    like = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_identifier == user_identifier
    ).first()
    
    if not like:
        raise HTTPException(status_code=400, detail="Not liked yet")
    
    db.delete(like)
    post.likes_count -= 1
    db.commit()
    db.refresh(post)
    
    return {"id": post.id, "likes_count": post.likes_count}
