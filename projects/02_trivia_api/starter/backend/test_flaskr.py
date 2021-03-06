import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
import re


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question':  'What is love?',
            'answer': "Oh baby, don't hurt me",
            'difficulty': '100500',
            'category': '2'
        }

        self.invalid_question = {
            'question':  0,
            'answer': 0,
            'difficulty': 0,
            'category': 0
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_questions_by_category(self):
        """Test get questions by category Id"""
        category_id = Category.query.first().id
        res = self.client().get('/categories/%s/questions' % category_id)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']))

    def test_404_get_questions_by_category(self):
        """Test if the category not exist"""
        res = self.client().get('/categories/0/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_get_paginated_questions(self):
        """Test get all questions as pages"""
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(len(data['questions']), 10)

    def test_404_get_paginated_questions(self):
        res = self.client().get('/questions?page=10000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_post_new_question(self):
        """Test post new question"""
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])

    def test_422_post_empty_question(self):
        """Test 422 error when send empty information"""
        res = self.client().post('/questions',json=self.invalid_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])


    def test_search_questions(self):
        """Test search question API"""
        randomTerm = Question.query.first().question.split(' ', 1)[0]
        data_json = json.dumps(dict(searchTerm=randomTerm))
        res = self.client().post('/questions', data=data_json,
                                 content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']))
        # check if the search results are correct
        for question in data['questions']:
            self.assertTrue(re.search(randomTerm, question['question'], re.I))

    def test_delete_question(self):
        """Test delete a question"""
        existID = Question.query.first().id
        res = self.client().delete('/questions/%s' % existID)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['id'], existID)
        self.assertFalse(Question.query.get(existID))

        # if the id not exist

    def test_404_delete_question(self):
        """Test 404 error when delete a question with wrong id"""
        res = self.client().delete('/questions/0')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_quiz(self):
        """Test post quizzes API"""
        category_id = Category.query.first().id
        total_question = len(Question.query.filter(
            Question.category == category_id).all())
        total_request = 0
        previous_question = []
        while total_request < total_question:
            res = self.client().post('/quizzes', data=json.dumps(dict(
                previous_questions=previous_question,
                quiz_category={'id': category_id}
            )),
                content_type='application/json')
            data = json.loads(res.data)
            previous_question.append(data['question'])
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])
            self.assertTrue(data['question'])
            total_request = total_request + 1


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
