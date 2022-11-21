# элементы для определения атрибутов
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
# подклюение ядра базы данных
from sqlalchemy.ext.declarative import declarative_base
# подключение фичи, которая будет автомтически накладывать на таблицу repr
from sqlalchemy_repr import RepresentableBase
from sqlalchemy.orm import relationship

Base = declarative_base(cls=RepresentableBase)


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    answers = relationship('UsersAnswers')


class Questions(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    answers = relationship('Answers')


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    questions = relationship('Questions')


class Answers(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    question_id = Column(Integer, ForeignKey('questions.id'))
    users = relationship('UsersAnswers')
    # is_correct_answers = relationship('UsersAnswers')
    is_correct = Column(Boolean)


class UsersAnswers(Base):
    __tablename__ = 'users_answers'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    answer_id = Column(Integer, ForeignKey('answers.id'))
    # is_correct = Column(Boolean, ForeignKey('answers.is_correct'))

# class QuestionsCategory(Base):
#     __tablename__ = 'questions_category'
#     question_id = Column(Integer, ForeignKey('questions.id'), primary_key=True)
#     category_id = Column(Integer, ForeignKey('categories.id'))
