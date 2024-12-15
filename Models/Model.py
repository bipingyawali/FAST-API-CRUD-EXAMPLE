from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean, default=True)
    rating = Column(Integer, None)
    