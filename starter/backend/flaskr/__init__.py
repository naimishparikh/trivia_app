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
        print("After Request")
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        print("done after request")
        return response


    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [ques.format() for ques in selection]
        current_ques = questions[start:end]
        return current_ques


    @app.route('/categories')
    def retrieve_categories():
        categories = Category.query.order_by(Category.id).all()
        cats = {}
        for category in categories:
            cats[category.id] = category.type

        print("categories", cats)
        return jsonify({
                 'success': True,
                 'categories': cats
               })


    @app.route('/questions')
    def retrieve_questions():
        try:
            selection = Question.query.order_by(Question.id).all()
            print("selectioin  length and type",len(selection),type(selection))
            current_ques = paginate_questions(request, selection)
            print("current_ques",current_ques)
            if len(current_ques) == 0:
                abort(404)

            categories = Category.query.order_by(Category.id).all()

            cats = {}
            for category in categories:
                cats[category.id] = category.type

            print("cats",cats)
            json = jsonify({
              'success': True,
              'questions': current_ques,
              'total_questions': len(Question.query.all()),
              'categories': cats
               })
            print("printing json" , json)
            return json

        except:
            print("in except abort")
            abort(422)



    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_book(question_id):
        try:
            print("In DELETE")
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                print("in delete none")
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id
              #  'books': current_books,
              #  'total_books': len(Book.query.all())
            })
        except:
            print("in except abort")
            abort(422)


    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            print("in create question")
            body = request.get_json()

            ques = body.get('question', None)
            answer = body.get('answer', None)
            difficulty = body.get('difficulty', None)
            category = body.get('category', None)

            # STANDOUT submission rating
            rating = body.get('rating', None)

            print("rating ", rating)
            if ques == None or answer == None or difficulty==None or category==None or rating==None:
                abort(422)

            print("in question creation")
            question = Question(question=ques, answer=answer, difficulty=difficulty, category=category,rating=rating)
            print("in question creaTED")

            question.insert()
            print("in question INSERTED")
            return jsonify({
               'success': True,
               'created': question.id,
        #  'books': current_books,
        #  'total_books': len(Book.query.all())
            })
        except:
            abort(422)


    @app.route('/questions_search', methods=['POST'])
    def search_questions():
        try:
            print("in search questions")
            body = request.get_json()

            search = body.get('searchTerm', "")

            print("search term", search, "searchTerm")
            selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
            current_ques = paginate_questions(request, selection)
            print("current questions in search", current_ques)

            return jsonify({
                'success': True,
                'questions': current_ques,
                'total_questions': len(selection.all())
            })
        except:
            abort(422)


    @app.route('/categories/<int:cat_id>/questions')
    def retrieve_questions_by_category(cat_id):
        try:
            questions = Question.query.filter_by(category=cat_id)
            current_ques = paginate_questions(request, questions)
            print("in retrieve by category")
            if len(current_ques) == 0:
                abort(404)

            print("QUESTIONS", questions)
            print("Current_Ques" , current_ques)
            return jsonify({
                'success': True,
                'questions': current_ques,
                'total_questions': questions.count(),
                'current_category': cat_id
            })
        except:
            print("in except abort")
            abort(422)


    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        try:
            body = request.get_json()

            prevQuestions = body.get('previous_questions', [])
            quiz_category = body.get('quiz_category', {})


            print("quiz category",quiz_category)
            print("prevQuestion",prevQuestions)
            cat_id = quiz_category['id']
            print("cat_id",cat_id)
            if cat_id == 0:
                print("In if cat_id")
                selection = Question.query.order_by(Question.id)
            else:
                print("In else cat_id")
                selection = Question.query.order_by(Question.id).filter_by(category=cat_id)

            selLength = len(selection.all())

            if selLength == 0:
                 print("selLength",selLength)
                 abort(422)

            current_question = {}
            allQuestions = set()
            while len(allQuestions) < selLength:
                print("selection", selection[0])
                print("selectionEnd", selection[selLength-1])
                randInteger = random.randint(0,selLength-1)
                print("randInteger index",randInteger)
                current_question = selection[randInteger].format()
                print("current_question",current_question)
                allQuestions.add(current_question['id'])
                print("after allquestions add ",current_question['id'])
                print("all Questions ",allQuestions)
                if current_question['id'] not in prevQuestions:
                    print("not in PrevQuestion")
                    break
            else:
                print("current question empty")
                current_question = {}

            print("CURRENT QUESTION",current_question)

            return jsonify({
                'success': True,
                'question': current_question
                })
        except:
            abort(422)


    #STANDOUT Submission
    @app.route('/categories', methods=['POST'])
    def create_category():
        try:
            body = request.get_json()

            categoryName = body.get('categoryName', None)

            print("CAtegory Name ", categoryName)
            if categoryName == None:
                abort(422)

            print("in Category creation")
            cat = Category(type=categoryName)
            print("categoryCreated")
            cat.insert()
            print("category inserted")

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
        print("In abort 404")
        return jsonify({
          "success": False,
          "error": 404,
          "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        print("returning unprocessable")
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
        print("405 not allowed")
        return jsonify({
          "success": False,
          "error": 405,
          "message": "method not allowed"
        }), 405

    return app

    