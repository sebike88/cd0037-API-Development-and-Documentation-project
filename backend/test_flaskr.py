import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('student:student@localhost:5432', self.database_name)

        self.new_question = {
            "question": "Anansi Boys",
            "answer": "Neil Gaiman",
            "difficulty": 3,
            "category": 3,
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = db
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_paginated_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_categories'])

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_questions'])

    # def test_delete_question(self):
    #     QUESTION_ID = 14
    #     item_string = "/questions/{}".format(QUESTION_ID)
    #     res = self.client().delete(item_string)
    #     data = json.loads(res.data)
        
    #     with self.app.app_context():
    #         question = Question.query.filter(Question.id == QUESTION_ID).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["deleted"], QUESTION_ID)
    #     self.assertTrue(data["total_questions"])
    #     self.assertTrue(len(data["questions"]))
    #     self.assertEqual(question, None)

    def test_post_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["questions"]))

    def test_405_if_question_creation_is_not_allowed(self):
        res = self.client().post('/questions/34', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "not allowed")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()