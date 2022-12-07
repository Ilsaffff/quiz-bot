# элементы для определения атрибутов
from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, DateTime, func
# подклюение ядра базы данных
from sqlalchemy.ext.declarative import declarative_base
# подключение фичи, которая будет автомтически накладывать на таблицу repr
from sqlalchemy_repr import RepresentableBase
from sqlalchemy.orm import relationship

Base = declarative_base(cls=RepresentableBase)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)

    answers = relationship('Answer', secondary='user_answers', back_populates='users')
    selected_category = relationship('Category', secondary='user_context', back_populates='users')

    def __repr__(self):
        return f'{self.id}'


class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))

    answers = relationship('Answer', backref='question')

    def __repr__(self):
        return f'{self.id}'


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    text = Column(String)

    questions = relationship('Question', backref='selected_category')
    users = relationship('User', secondary='user_context', back_populates='selected_category')

    def __repr__(self):
        return f'{self.id}'


class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    is_correct = Column(Boolean)
    question_id = Column(Integer, ForeignKey('questions.id'))

    users = relationship('User', secondary='user_answers', back_populates='answers')

    def __repr__(self):
        return f'{self.id}'


class UserAnswer(Base):
    __tablename__ = 'user_answers'
    date = Column(DateTime(), default=datetime.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    answer_id = Column(Integer, ForeignKey('answers.id'), primary_key=True)


class UserContext(Base):
    __tablename__ = 'user_context'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
