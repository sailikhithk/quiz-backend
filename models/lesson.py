import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, JSON, Text
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship, backref


class Lesson(Base):
    __tablename__ = "lesson"

    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    data = Column(Text)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    is_active = Column(Boolean, default=True) 
    created_date = Column(DateTime, default=func.now(), nullable=False)
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
