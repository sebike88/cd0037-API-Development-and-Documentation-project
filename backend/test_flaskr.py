import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, db
from dotenv import load_dotenv

load_dotenv()
API_VERSION = '/api/v1.0'

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = 'trivia_test'
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(user, password, 'localhost:5432', self.database_name)
        self.app = create_app({'database_path': self.database_path})
        self.client = self.app.test_client

        self.new_question = {
            "question": "Anansi Boys",
            "answer": "Neil Gaiman",
            "difficulty": 3,
            "category": 3,
            "rating": 0
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get(f'{API_VERSION}/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_categories'])
    
    def test_get_categories_404(self):
        res = self.client().get(f'{API_VERSION}/categories/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_paginated_questions(self):
        res = self.client().get(f'{API_VERSION}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_questions'])
    
    def test_get_paginated_questions_no_results(self):
        res = self.client().get(f'{API_VERSION}/questions', query_string={'page': '453'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_questions'])

    def test_get_questions_based_on_category(self):
        category_id = 1
        res = self.client().get(f'{API_VERSION}/questions', query_string={'category': category_id})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['current_category'], category_id)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
    
    def test_get_questions_based_on_nonexistent_category(self):
        category_id = 8
        res = self.client().get(f'{API_VERSION}/questions', query_string={'category': category_id})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    # def test_delete_question(self):
    #     QUESTION_ID = 15
    #     item_string = '{}/questions/{}'.format(API_VERSION, QUESTION_ID)
    #     res = self.client().delete(item_string)
    #     data = json.loads(res.data)
        
    #     with self.app.app_context():
    #         question = Question.query.filter(Question.id == QUESTION_ID).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["deleted"], QUESTION_ID)
    #     self.assertTrue(data["total_questions"])
    #     self.assertTrue(len(data["questions"]))
    #     self.assertIsNone(question)

    def test_delete_nonexistent_question_404(self):
        QUESTION_ID = 56
        item_string = '{}/questions/{}'.format(API_VERSION, QUESTION_ID)
        res = self.client().delete(item_string)
        data = json.loads(res.data)
        
        with self.app.app_context():
            question = Question.query.filter(Question.id == QUESTION_ID).one_or_none()

        self.assertIsNone(question)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_post_new_question(self):
        res = self.client().post(f'{API_VERSION}/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["questions"]))

    def test_405_if_question_creation_is_not_allowed(self):
        res = self.client().post(f'{API_VERSION}/questions/34', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "not allowed")

    def test_search_question_with_results(self):
        res = self.client().post(f'{API_VERSION}/questions', json={"search_term": "Which"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertGreater(len(data["questions"]), 0)

    def test_search_question_without_results(self):
        res = self.client().post(f'{API_VERSION}/questions', json={"search_term": "asfawfawga"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_questions"], 0)
        self.assertEqual(len(data["questions"]), 0)

    def test_quizes(self):
        res = self.client().post(f'{API_VERSION}/quizzes', json={
            "previous_questions": [3],
            "quiz_category": {
                "type": "click",
                "id": 0
            }
        })
        data = json.loads(res.data)
        previous_questions = data['previous_questions']
        previous_questions.append(data['question']['id'])

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['question']['id'] != 3)
        self.assertEqual(data["previous_questions"], [3, data['question']['id']])

    def test_quizes_failure_nonexistent_category(self):
        res = self.client().post(f'{API_VERSION}/quizzes', json={
            "previous_questions": [3],
            "quiz_category": {
                "type": "Astronomy",
                "id": 8
            }
        })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()