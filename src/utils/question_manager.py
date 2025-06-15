"""Question Manager for Survey System"""
import os
import random
from typing import List, Optional
from src.database.db_handler import DBHandler
from src.database.models import Test, Question

class QuestionManager:
    def __init__(self, db_handler: DBHandler):
        self.db = db_handler
        
    def get_all_tests(self) -> List[str]:
        """Get all test names from the database"""
        session = self.db.get_session()
        try:
            tests = session.query(Test).all()
            return [test.name for test in tests]
        finally:
            session.close()
            
    def get_questions_for_test(self, test_name: str) -> List[str]:
        """Get all questions for a specific test"""
        session = self.db.get_session()
        try:
            test = session.query(Test).filter(Test.name == test_name).first()
            if test:
                return [q.text for q in test.questions]
            return []
        finally:
            session.close()
            
    def create_test(self, test_name: str) -> bool:
        """Create a new test"""
        session = self.db.get_session()
        try:
            if session.query(Test).filter(Test.name == test_name).first():
                return False
            new_test = Test(name=test_name)
            session.add(new_test)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error creating test: {str(e)}")
            return False
        finally:
            session.close()
            
    def add_question_to_test(self, test_name: str, question_text: str) -> bool:
        """Add a question to a specific test"""
        session = self.db.get_session()
        try:
            test = session.query(Test).filter(Test.name == test_name).first()
            if not test:
                return False
            question = Question(text=question_text, test=test)
            session.add(question)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error adding question: {str(e)}")
            return False
        finally:
            session.close()
            
    def update_question(self, test_name: str, old_text: str, new_text: str) -> bool:
        """Update a question in a specific test"""
        session = self.db.get_session()
        try:
            test = session.query(Test).filter(Test.name == test_name).first()
            if not test:
                return False
            question = session.query(Question).filter(
                Question.test_id == test.id,
                Question.text == old_text
            ).first()
            if question:
                question.text = new_text
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"Error updating question: {str(e)}")
            return False
        finally:
            session.close()
            
    def delete_question(self, test_name: str, question_text: str) -> bool:
        """Delete a question from a specific test"""
        session = self.db.get_session()
        try:
            test = session.query(Test).filter(Test.name == test_name).first()
            if not test:
                return False
            question = session.query(Question).filter(
                Question.test_id == test.id,
                Question.text == question_text
            ).first()
            if question:
                session.delete(question)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"Error deleting question: {str(e)}")
            return False
        finally:
            session.close()
            
    def delete_test(self, test_name: str) -> bool:
        """Delete a test and all its questions"""
        session = self.db.get_session()
        try:
            test = session.query(Test).filter(Test.name == test_name).first()
            if test:
                session.delete(test)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"Error deleting test: {str(e)}")
            return False
        finally:
            session.close()

    def get_all_questions(self) -> List[str]:
        """Получает все вопросы из файла"""
        try:
            with open(self.questions_file, 'r', encoding='utf-8') as f:
                questions = [line.strip() for line in f.readlines() if line.strip()]
            return questions
        except Exception as e:
            print(f"Ошибка при чтении вопросов: {str(e)}")
            return []
    
    def save_questions(self, questions: List[str]):
        """Сохраняет вопросы в файл"""
        try:
            with open(self.questions_file, 'w', encoding='utf-8') as f:
                for question in questions:
                    f.write(f"{question}\n")
        except Exception as e:
            print(f"Ошибка при сохранении вопросов: {str(e)}")
            raise
    
    def get_random_questions(self, n: int) -> List[str]:
        """Получает n случайных вопросов"""
        questions = self.get_all_questions()
        if not questions:
            return []
        n = min(n, len(questions))
        return random.sample(questions, n) 