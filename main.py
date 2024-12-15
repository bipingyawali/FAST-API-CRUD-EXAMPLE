from fastapi import FastAPI
from routes import post
from database import engine
from Models.Model import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(post.router)
