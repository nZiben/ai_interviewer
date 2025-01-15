"""SQLAlchemy Models"""
from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SurveyResult(Base):
    __tablename__ = 'survey_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    question = Column(Text)
    answer = Column(Text)
    feedback = Column(Text)
    score = Column(Float)
