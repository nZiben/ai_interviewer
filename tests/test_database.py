import unittest
from src.database.db_handler import DBHandler

class TestDatabase(unittest.TestCase):
    def test_db_save(self):
        db = DBHandler(db_url='sqlite:///:memory:')
        try:
            db.save_survey_result(
                first_name='Test',
                last_name='User',
                question='Test question?',
                answer='Test answer',
                feedback='Good job',
                score=4.5
            )
            self.assertTrue(True, "Database save worked.")
        except:
            self.fail("Database save failed.")

if __name__ == '__main__':
    unittest.main()
