import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

DB_NAME = os.getenv('DB_NAME', 'trivia')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '1234')
DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_DIALECT = os.getenv('DB_DIALECT', 'postgresql+psycopg2')
SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}/{}".format(
        DB_DIALECT, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
#database_path = "postgresql://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=SQLALCHEMY_DATABASE_URI):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Question

'''
class Question(db.Model):  
  __tablename__ = 'questions'

  id = Column(Integer, primary_key=True)
  question = Column(String)
  answer = Column(String)
  category = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
  difficulty = Column(Integer)
  # STANDOUT submission
  rating = Column(Integer)

  def __init__(self, question, answer, category, difficulty, rating):
    self.question = question
    self.answer = answer
    self.category = category
    self.difficulty = difficulty
    self.rating = rating

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer,
      'category': self.category,
      'difficulty': self.difficulty,
      'rating': self.rating
    }

'''
Category

'''
class Category(db.Model):  
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  type = Column(String)
  ques = db.relationship('Question', backref='cat', lazy=True)

  def __init__(self, type):
    self.type = type

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'type': self.type
    }