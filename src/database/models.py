"""SQLAlchemy Models"""
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Test(Base):
    __tablename__ = 'tests'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    questions = relationship("Question", back_populates="test")

class Question(Base):
    __tablename__ = 'questions'
    
    id = Column(Integer, primary_key=True)
    test_id = Column(Integer, ForeignKey('tests.id'))
    text = Column(String, nullable=False)
    test = relationship("Test", back_populates="questions")

class SurveyResult(Base):
    __tablename__ = 'survey_results'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    test_name = Column(String, nullable=False)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    feedback = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    llm_score = Column(Float)  # Оценка от LLM
    human_score = Column(Float)  # Оценка от человека
