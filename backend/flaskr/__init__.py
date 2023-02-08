import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import func

from models import setup_db, Question, Category

RESULTS_PER_PAGE = 10
API_VERSION = '/api/v1.0'

def paginate_request(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * RESULTS_PER_PAGE
    end = start + RESULTS_PER_PAGE

    formatted_response = [question.format() for question in selection]
    current_response = formatted_response[start:end]

    return current_response

def paginate_post_request(body, selection):
    page = body.get('page') or 1
    start = (page - 1) * RESULTS_PER_PAGE
    end = start + RESULTS_PER_PAGE
    
    formatted_response = [question.format() for question in selection]
    current_response = formatted_response[start:end]

    return current_response

def questions_query():
    selection = Question.query.order_by(Question.id).all()
    categories = Category.query.order_by(Category.id).all()
    paginated_questions = paginate_request(request, selection)
    formatted_categories = {category.id : category.type for category in categories}
    
    return {
        "success": True,
        "questions": paginated_questions,
        "total_questions": len(selection),
        "categories": formatted_categories,
        "current_category": 0,
    }

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    if test_config:
        setup_db(app, test_config['database_path'])
    else:
        setup_db(app)
        
    CORS(app, resources={r"/": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )

        return response

    @app.route(f'{API_VERSION}/categories')
    def get_categories():
        selection = Category.query.order_by(Category.id).all()
        formatted_categories = {category.id : category.type for category in selection}

        return jsonify({
            "success": True,
            "categories": formatted_categories,
            "total_categories": len(selection),
        })

    @app.route(f'{API_VERSION}/questions')
    def get_questions():
        error_id = 422
        category = request.args.get('category')

        try:
            if category:
                selection = Question.query.order_by(Question.id).filter(
                    Question.category == category
                ).all()
                current_category = Category.query.filter(Category.id == category).one_or_none()

                if current_category is None:
                    error_id = 404
                    abort()

                paginated_questions = paginate_request(request, selection)
                categories = Category.query.order_by(Category.id).all()
                formatted_categories = {category.id : category.type for category in categories}


                return jsonify({
                    'questions': paginated_questions,
                    'current_category': current_category.id,
                    'categories': formatted_categories,
                    'total_questions': len(selection),
                    "success": True,
                })
            else:
                questions = jsonify(questions_query())

            return questions
        except:
            abort(error_id)

    @app.route(f'{API_VERSION}/questions/<int:question_id>', methods=["DELETE", "PATCH"])
    def delete_question(question_id):
        error_id = 422
        try:
            if request.method == 'PATCH':
                body = request.get_json()
                new_rating = body.get("rating", None)
                question = Question.query.filter(Question.id == question_id).one_or_none()

                if question is None:
                    error_id = 404
                    abort()

                question.rating = new_rating

                question.update()

            elif request.method == 'DELETE':
                question = Question.query.filter(Question.id == question_id).one_or_none()

                if question is None:
                    error_id = 404
                    abort()
                
                question.delete()

            questions = questions_query()

            questions['deleted'] = question.id

            return jsonify(questions)


        except:
            abort(error_id)

    @app.route(f'{API_VERSION}/questions', methods=["POST"])
    def create_question():
        error_id = 422
        body = request.get_json()
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)
        search = body.get("search_term", None)

        is_question_data_none = (new_question == None
        ) and (new_answer == None
        ) and (new_difficulty == None
        ) and (new_category == None)

        get_questions_based_on_category = (new_question == None
        ) and (new_answer == None
        ) and (new_difficulty == None
        ) and (new_category != None)

        try:
            if search:
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike('%{}%'.format(search))
                )
                paginated_questions = paginate_post_request(body, selection)

                return jsonify({
                    'success': True,
                    'questions': paginated_questions,
                    "total_questions": len(selection.all())
                })
            elif is_question_data_none:
                abort()
            elif get_questions_based_on_category:
                selection = Question.query.order_by(Question.id).filter(
                    Question.category == new_category
                ).all()

                paginated_questions = paginate_post_request(body, selection)
                category = Category.query.filter(Category.id == new_category).one_or_none()

                return jsonify({
                    'success': True,
                    'current_category': category.id,
                    'questions': paginated_questions,
                    "total_questions": len(selection)
                })
            else:
                question = Question(question=new_question,
                    answer=new_answer,
                    difficulty=new_difficulty,
                    category=new_category,
                    rating=0)
                
                question.insert()

                questions = questions_query()
                questions['created'] = question.id

                return jsonify(questions)
        except:
            abort(error_id)

    @app.route(f'{API_VERSION}/quizzes', methods=["POST"])
    def play_quiz():
        error_id = 422

        try:
            body = request.get_json()
            previous_questions = body.get("previous_questions", None)
            quiz_category = body.get('quiz_category', None)
            quiz_category_id = int(quiz_category['id'])
            category = Category.query.filter(Category.id == quiz_category_id).one_or_none()
            filter_condition = (Question.category == quiz_category_id
                ) if (quiz_category_id > 0
                ) else (Question.category > 0)

            if quiz_category_id != 0 and category is None:
                error_id = 404
                abort()

            selection = Question.query.filter(
                Question.id not in previous_questions and filter_condition
            ).order_by(
                func.random()
            ).first()

            if selection is None:
                error_id = 404
                abort()

            return jsonify({
                'success': True,
                'previous_questions': previous_questions,
                'question': {
                    'id': selection.id,
                    'question': selection.question,
                    'answer': selection.answer,
                    'category': selection.category
                }
            })
        except:
            abort(error_id)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": 'resource not found'
        }), 404
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'bad request'
        }), 400

    @app.errorhandler(422)
    def unporcessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": 'unprocessable'
        }), 422

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": 'not allowed'
        }), 405
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": 'internal server error'
        }), 500

    return app

