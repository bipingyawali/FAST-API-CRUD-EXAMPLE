from fastapi import APIRouter, status, Path, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Annotated
from database import SessionLocal
from sqlalchemy.orm import Session
from Models.Model import Post

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]        

class PostRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str
    published: bool = True
    rating: int = Field(None, gt=0, lt=6)

@router.get("/", status_code=status.HTTP_200_OK)
async def index(db: db_dependency, limit: int = Query(10, ge=10), offset: int = Query(0, ge=0)):
    # Query the total count of posts
    total_posts = db.query(Post).count()
    
    posts = db.query(Post).limit(limit=limit).offset(offset=offset).all()
    return {'data': posts, 'paginate': { 'total': total_posts }}

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def show(db: db_dependency, id: int = Path(gt=0)):
    post_model = db.query(Post).filter(Post.id == id).first()
    if post_model is None: 
        raise HTTPException(status_code=404, detail="Post not found with given Id")
    return {"data": post_model}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def store(db: db_dependency, post_request: PostRequest):
    post_model = Post(**post_request.model_dump())
    db.add(post_model)
    db.commit()

@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update(db: db_dependency, id: int, post_request: PostRequest):
    post_model = db.query(Post).filter(Post.id == id).first()
    
    if post_model is None:
        raise HTTPException(status_code=404, detail="Post Not found with give ID")
    
    post_model.title = post_request.title
    post_model.content = post_request.content
    post_model.published = post_request.published
    post_model.rating = post_request.rating
    
    db.add(post_model)
    db.commit()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(db: db_dependency, id: int = Path(gt=0)):
    post_model = db.query(Post).filter(Post.id == id).first()
    
    if post_model is None: 
        raise HTTPException(status_code=404, detail="Post Not found with given ID")
    
    db.delete(post_model)
    db.commit()


