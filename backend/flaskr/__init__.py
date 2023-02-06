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

def questions_query():
    selection = Question.query.order_by(Question.id).all()
    categories = Category.query.order_by(Category.id).all()
    paginated_questions = paginate_request(request, selection)
    formatted_categories = {category.id : category.type for category in categories}

    if len(selection) == 0:
        abort(404)
    
    return {
        "success": True,
        "questions": paginated_questions,
        "total_questions": len(selection),
        "categories": formatted_categories,
    }

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    ✅: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs 
    """
    CORS(app, resources={r"/": {"origins": "*"}})

    """
    ✅: Use the after_request decorator to set Access-Control-Allow ✅
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )

        return response

    """
    ✅
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route(f'{API_VERSION}/categories')
    def get_categories():
        selection = Category.query.order_by(Category.id).all()
        formatted_categories = {category.id : category.type for category in selection}

        if len(selection) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "categories": formatted_categories,
            "total_categories": len(selection),
        })


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route(f'{API_VERSION}/questions')
    def get_questions():
        category = request.args.get('category')

        if category:
            selection = Question.query.order_by(Question.id).filter(Question.category == category).all()
            current_category = Category.query.filter(Category.id == category).one_or_none()
            paginated_questions = paginate_request(request, selection)

            return jsonify({
                'questions': paginated_questions,
                'category': current_category.id,
                'total_questions': len(selection)
            })
        else:
            questions = jsonify(questions_query())

        return questions
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route(f'{API_VERSION}/questions/<int:question_id>', methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)
            
            question.delete()
            questions = questions_query()

            questions['deleted'] = question.id

            return jsonify(questions)


        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route(f'{API_VERSION}/questions', methods=["POST"])
    def create_question():
        body = request.get_json()
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)
        search = body.get("searchTerm", None)

        try:
            if search:
                selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
                paginated_questions = paginate_request(request, selection)

                return jsonify({
                    'success': True,
                    'questions': paginated_questions,
                    "total_questions": len(selection.all())
                })
            else:
                question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
                question.insert()

                questions = questions_query()
                questions['created'] = question.id

                return jsonify(questions)
        except:
            abort(422)


        # question: this.state.question,
        # answer: this.state.answer,
        # difficulty: this.state.difficulty,
        # category: this.state.category,

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route(f'{API_VERSION}/quizzes', methods=["POST"])
    def play_quiz():
        body = request.get_json()
        previous_questions = body.get("previous_questions", None)
        quiz_category = body.get('quiz_category', None)
        quiz_category_id = int(quiz_category['id'])
        filter_condition = Question.category == quiz_category_id if quiz_category_id > 0 else Question.category > 0

        selection = Question.query.filter(
            Question.id not in previous_questions and filter_condition
        ).order_by(
            func.random()
        ).first()

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

        

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": 'resource not found'
        }), 404

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

    return app

