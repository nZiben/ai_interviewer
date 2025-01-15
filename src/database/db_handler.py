"""Database Handler"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, SurveyResult

class DBHandler:
    def __init__(self, db_url: str = 'sqlite:///survey.db'):
        self.engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def save_survey_result(self, first_name, last_name, question, answer, feedback, score):
        session = self.Session()
        try:
            record = SurveyResult(
                first_name=first_name,
                last_name=last_name,
                question=question,
                answer=answer,
                feedback=feedback,
                score=score
            )
            session.add(record)
            session.commit()
        except Exception as e:
            print(f"[DB Error] {str(e)}")
            session.rollback()
        finally:
            session.close()
