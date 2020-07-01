import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def get_formated_category():
    categories = Category.query.all()
    formated_categories = {
        category.id: category.type for category in categories}
    return formated_categories


def get_formated_question(page, searchTerm=''):
    questions = Question.query
    if searchTerm:
        questions = questions.filter(
            Question.question.ilike('%' + searchTerm + '%'))
    questions = questions.paginate(page, 10)
    formated_question = [question.format() for question in questions.items]
    total_questions = questions.total

    return {
        'questions': formated_question,
        'total_questions': total_questions
    }


def get_formated_question_by_category(page, categoy_id):
    questions = Question.query.filter(
        Question.category == categoy_id).paginate(page, 10)
    formated_question = [question.format() for question in questions.items]
    total_questions = questions.total

    return {
        'questions': formated_question,
        'total_questions': total_questions
    }


def get_question_by_category(category_id):
    return Question.query.filter(Question.category == category_id).all()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Allow-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Allow-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def all_categories():
        return jsonify({
            'success': True,
            'categories': get_formated_category()
        })

    @app.route('/categories/<int:categoy_id>/questions')
    def questions_by_category(categoy_id):
        page = request.args.get('page', 1, type=int)
        returndObj = {
            'success': True,
            'current_category': categoy_id,
            'categories': get_formated_category(),
            **get_formated_question_by_category(page, categoy_id)
        }
        return jsonify(returndObj)

    @app.route('/questions', methods=['GET', 'POST'])
    def get_question():
        try:
            extraInfo = {}
            formated_question = []
            total_questions = 0
            returndObj = {}
            if request.method == 'POST':
                body = request.get_json()
                searchTerm = body.get('searchTerm')
                if searchTerm is not None:
                    page = request.args.get('page', 1, type=int)
                    returndObj = {
                        'success': True,
                        **get_formated_question(page, searchTerm),
                        'current_category': None,
                        'categories': get_formated_category(),
                    }
                else:
                    question = Question(
                        question=body.get('question'),
                        answer=body.get('answer'),
                        category=body.get('category'),
                        difficulty=body.get('difficulty')
                    )
                    question.insert()
                    page = request.args.get('page', 1, type=int)
                    returndObj = {
                        'success': True,
                        **get_formated_question(page),
                        'current_category': None,
                        'categories': get_formated_category(),
                        'created': question.id
                    }

            elif request.method == 'GET':
                page = request.args.get('page', 1, type=int)
                returndObj = {
                    'success': True,
                    'current_category': None,
                    'categories': get_formated_category(),
                    **get_formated_question(page)
                }

            return jsonify(returndObj)

        except Exception:
            abort(422)

    @app.route('/question/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if question is None:
            abort(404)
        else:
            question.delete()
            return jsonify({
                'success': True,
                'id': question_id
            })

    @app.route('/quizzes', methods=['POST'])
    def play():
        try:
            body = request.get_json()
            previousQuestions = body.get('previous_questions')
            quizCategory = body.get('quiz_category')
            qId = quizCategory['id']
            questions = get_formated_category(
                qId) if quizCategory['id'] else Question.query.all()
            filterdQuestions = [question.format() for question in questions]
            randomQuestion = None
            if len(previousQuestions):
                newlist = []
                for question in filterdQuestions:
                    if question not in previousQuestions:
                        newlist.append(question)
                if len(newlist):
                    randomQuestion = random.choice(newlist)
            else:
                randomQuestion = random.choice(filterdQuestions)

            return jsonify({
                'success': True,
                'question': randomQuestion
            })

        except Exception:
            abort(422)

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': error,
            'message': "unprocessable"
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "resource not found!"
        })

    return app
