"""Database Handler for Survey Results"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .models import Base, SurveyResult, Test, Question
import os
from pathlib import Path
from typing import List, Optional

class DBHandler:
    def __init__(self, db_url: str = None):
        """Initialize database connection"""
        if db_url is None:
            db_url = os.getenv("DATABASE_URL", "sqlite:///interview.db")
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
    
    def get_session(self) -> Session:
        """Get a new database session"""
        return self.Session()
    
    def save_survey_result(self, first_name: str, last_name: str, question: str, 
                          answer: str, feedback: str, llm_score: float, 
                          human_score: float = None) -> bool:
        """Save survey result to database"""
        session = self.get_session()
        try:
            result = SurveyResult(
                first_name=first_name,
                last_name=last_name,
                question=question,
                answer=answer,
                feedback=feedback,
                llm_score=llm_score,
                human_score=human_score
            )
            session.add(result)
            session.commit()
            print(f"Saved survey result for {first_name} {last_name}")
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error saving survey result: {str(e)}")
            return False
        finally:
            session.close()
    
    def update_human_score(self, result_id: int, score: float) -> bool:
        """Update human score for a survey result"""
        session = self.get_session()
        try:
            result = session.query(SurveyResult).filter(SurveyResult.id == result_id).first()
            if result:
                result.human_score = score
                session.commit()
                print(f"Updated human score for result {result_id}")
                return True
            print(f"No result found with id {result_id}")
            return False
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error updating human score: {str(e)}")
            return False
        finally:
            session.close()
    
    def get_all_survey_results(self):
        """Get all survey results from database"""
        session = self.get_session()
        try:
            results = session.query(SurveyResult).all()
            print(f"Retrieved {len(results)} survey results")
            return results
        except SQLAlchemyError as e:
            print(f"Error getting survey results: {str(e)}")
            return []
        finally:
            session.close()
    
    def get_survey_results_by_name(self, first_name, last_name):
        """Get survey results for a specific person"""
        session = self.get_session()
        try:
            results = session.query(SurveyResult).filter_by(
                first_name=first_name,
                last_name=last_name
            ).all()
            print(f"Retrieved {len(results)} results for {first_name} {last_name}")
            return results
        except SQLAlchemyError as e:
            print(f"Error getting survey results: {str(e)}")
            return []
        finally:
            session.close()
    
    def get_test_by_name(self, test_name: str) -> Optional[Test]:
        """Get test by name"""
        session = self.get_session()
        try:
            return session.query(Test).filter_by(name=test_name).first()
        finally:
            session.close()
    
    def get_all_tests(self) -> List[str]:
        """Get all test names"""
        session = self.get_session()
        try:
            tests = session.query(Test).all()
            return [test.name for test in tests]
        finally:
            session.close()
    
    def create_test(self, test_name: str) -> bool:
        """Create a new test"""
        session = self.get_session()
        try:
            if session.query(Test).filter_by(name=test_name).first():
                return False
            test = Test(name=test_name)
            session.add(test)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error creating test: {str(e)}")
            return False
        finally:
            session.close()
    
    def add_question_to_test(self, test_name: str, question_text: str) -> bool:
        """Add a question to a test"""
        session = self.get_session()
        try:
            test = session.query(Test).filter_by(name=test_name).first()
            if not test:
                return False
            question = Question(text=question_text, test=test)
            session.add(question)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error adding question: {str(e)}")
            return False
        finally:
            session.close()
    
    def update_question(self, test_name: str, old_text: str, new_text: str) -> bool:
        """Update a question in a test"""
        session = self.get_session()
        try:
            test = session.query(Test).filter_by(name=test_name).first()
            if not test:
                return False
            question = session.query(Question).filter_by(test=test, text=old_text).first()
            if not question:
                return False
            question.text = new_text
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error updating question: {str(e)}")
            return False
        finally:
            session.close()
    
    def delete_question(self, test_name: str, question_text: str) -> bool:
        """Delete a question from a test"""
        session = self.get_session()
        try:
            test = session.query(Test).filter_by(name=test_name).first()
            if not test:
                return False
            question = session.query(Question).filter_by(test=test, text=question_text).first()
            if not question:
                return False
            session.delete(question)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error deleting question: {str(e)}")
            return False
        finally:
            session.close()
    
    def delete_test(self, test_name: str) -> bool:
        """Delete a test and all its questions"""
        session = self.get_session()
        try:
            test = session.query(Test).filter_by(name=test_name).first()
            if not test:
                return False
            session.delete(test)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error deleting test: {str(e)}")
            return False
        finally:
            session.close()

    def add_survey_result(self, result: SurveyResult) -> bool:
        """Add a survey result to the database"""
        session = self.get_session()
        try:
            session.add(result)
            session.commit()
            return True
        except SQLAlchemyError:
            session.rollback()
            return False
        finally:
            session.close()

    def get_survey_results(self, test_name: Optional[str] = None) -> List[SurveyResult]:
        """Get all survey results, optionally filtered by test name"""
        session = self.get_session()
        try:
            query = session.query(SurveyResult)
            if test_name:
                query = query.filter_by(test_name=test_name)
            return query.all()
        finally:
            session.close()
