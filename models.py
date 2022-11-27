# элементы для определения атрибутов
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
# подклюение ядра базы данных
from sqlalchemy.ext.declarative import declarative_base
# подключение фичи, которая будет автомтически накладывать на таблицу repr
from sqlalchemy_repr import RepresentableBase
from sqlalchemy.orm import relationship

Base = declarative_base(cls=RepresentableBase)

user_answers = Table(
    'user_answers', Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('answer_id', ForeignKey('answers.id'))
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)

    answers = relationship('Answer', secondary='user_answers', back_populates='users')

    def __repr__(self):
        return f'{self.username}'


class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))

    answers = relationship('Answer', backref='question')

    def __repr__(self):
        return f'{self.text}'


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    text = Column(String)

    questions = relationship('Question', backref='category')

    def __repr__(self):
        return f'{self.text}'


class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    is_correct = Column(Boolean)
    question_id = Column(Integer, ForeignKey('questions.id'))

    users = relationship('User', secondary='user_answers', back_populates='answers')

    def __repr__(self):
        return f'{self.text}'
