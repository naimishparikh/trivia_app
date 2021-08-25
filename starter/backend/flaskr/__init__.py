import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # CORS(app, resources={r"*/api/*" : {'origins': '*'}})
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # gets the questions per page based on the given page number
    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = [ques.format() for ques in selection]
        current_ques = questions[start:end]
        return current_ques

    # gets all categories ordered by category id.
    # format is for e.g. { 3:"Art"}
    @app.route('/categories')
    def retrieve_categories():
        categories = Category.query.order_by(Category.id).all()
        cats = {}
        for category in categories:
            cats[category.id] = category.type

        return jsonify({
                 'success': True,
                 'categories': cats
               })

    # get all questions ordered by question id for given page. also returns all
    # categories and total number of questions. questions are paginated. by
    # default page is the first page if page not provided in the request
    # categories are returned in the format { 1:"Art", 2:"History"}
    @app.route('/questions')
    def retrieve_questions():
        try:
            selection = Question.query.order_by(Question.id).all()
            current_ques = paginate_questions(request, selection)
            if len(current_ques) == 0:
                abort(404)

            categories = Category.query.order_by(Category.id).all()

            cats = {}
            for category in categories:
                cats[category.id] = category.type

            json = jsonify({
              'success': True,
              'questions': current_ques,
              'total_questions': len(Question.query.all()),
              'categories': cats
               })
            return json

        except:
            abort(422)

    # delete the question with given question id. returns the successfully
    # deleted question id
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_book(question_id):
        try:

            question = Question.query.filter(Question.id ==
                                             question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id
                #  'books': current_books,
                #  'total_books': len(Book.query.all())
            })
        except:
            abort(422)

    # create a new question based on the  given question info in  the request
    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            body = request.get_json()

            ques = body.get('question', None)
            answer = body.get('answer', None)
            difficulty = body.get('difficulty', None)
            category = body.get('category', None)

            # STANDOUT submission rating
            rating = body.get('rating', None)

            if ques is None or \
               answer is None or\
               difficulty is None or \
               category is None or \
               rating is None:
                abort(422)

            question = Question(question=ques,
                                answer=answer,
                                difficulty=difficulty,
                                category=category,
                                rating=rating)

            question.insert()
            return jsonify({
               'success': True,
               'created': question.id
               #  'books': current_books,
               #  'total_books': len(Book.query.all())
            })
        except:
            abort(422)

    # search for questions with given search term. returns all
    # matching questions with given search term.
    @app.route('/questions_search', methods=['POST'])
    def search_questions():
        try:
            body = request.get_json()

            search = body.get('searchTerm', "")

            selection = Question.query.order_by(Question.id).\
                filter(Question.question.ilike('%{}%'.format(search)))
            current_ques = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'questions': current_ques,
                'total_questions': len(selection.all())
            })
        except:
            abort(422)

    # get the questions with the given category id.
    # returns paginated questions
    @app.route('/categories/<int:cat_id>/questions')
    def retrieve_questions_by_category(cat_id):
        try:
            questions = Question.query.filter_by(category=cat_id)
            current_ques = paginate_questions(request, questions)
            if len(current_ques) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': current_ques,
                'total_questions': questions.count(),
                'current_category': cat_id
            })
        except:
            abort(422)

    # gets a random question with the given category id if the question is
    # not in the given previous questions. previous questions is a list.
    # and category is of the form {'type': 'History', 'id': '4'}
    # returns the current quiz question which is randomly selected.
    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        try:
            body = request.get_json()

            prevQuestions = body.get('previous_questions', [])
            quiz_category = body.get('quiz_category', {})

            cat_id = quiz_category['id']

            # category id of 0 means all questions else questions from the
            # given category id.
            if cat_id == 0:
                selection = Question.query.order_by(Question.id)
            else:
                selection = Question.query.order_by(Question.id).\
                    filter_by(category=cat_id)

            selLength = len(selection.all())

            if selLength == 0:
                abort(422)

            current_question = {}
            allQuestions = set()

            # loop until we find a question not present in previous
            # questions list or we looped through all questions and they are
            # all present in previous questions. if all questions are covered
            # return empty current_questions dictionary.
            # the current_question is returned in the format as per the format()
            # method of the Question class in model
            while len(allQuestions) < selLength:

                # get a random integer between 0 and selLength-1
                # both included.
                # random integer is the index of the questions list from
                # the selection query above.
                randInteger = random.randint(0, selLength-1)

                current_question = selection[randInteger].format()

                # save the current question in allQuestions set
                # before checking if the randomly selected question
                # is present in the previous questions.
                allQuestions.add(current_question['id'])

                if current_question['id'] not in prevQuestions:
                    break
            else:
                current_question = {}

            return jsonify({
                'success': True,
                'question': current_question
                })
        except:
            abort(422)

    # STANDOUT Submission
    # create a new category in the database with the given category name
    @app.route('/categories', methods=['POST'])
    def create_category():
        try:
            body = request.get_json()

            categoryName = body.get('categoryName', None)

            if categoryName is None:
                abort(422)

            cat = Category(type=categoryName)
            cat.insert()

            return jsonify({
               'success': True,
               'created': cat.id
               #  'books': current_books,
               #  'total_books': len(Book.query.all())
            })
        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
          "success": False,
          "error": 404,
          "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
          "success": False,
          "error": 405,
          "message": "method not allowed"
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):

        return jsonify({
          "success": False,
          "error": 500,
          "message": "internal server error"
        }), 500

    @app.errorhandler(501)
    def not_implemented(error):
        return jsonify({
            "success": False,
            "error": 501,
            "message": "not implemented"
        }), 501

    @app.errorhandler(502)
    def bad_gateway(error):
        return jsonify({
            "success": False,
            "error": 502,
            "message": "bad gateway"
        }), 502

    @app.errorhandler(503)
    def service_unavailable(error):
        return jsonify({
            "success": False,
            "error": 503,
            "message": "service unavailable"
        }), 503

    @app.errorhandler(504)
    def gateway_timeout(error):
        return jsonify({
            "success": False,
            "error": 504,
            "message": "gateway timeout"
        }), 504

    @app.errorhandler(505)
    def http_version_unsupported(error):
        return jsonify({
            "success": False,
            "error": 505,
            "message": "http version unsupported"
        }), 505

    return app
