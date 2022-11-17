# элементы для определения атрибутов
from sqlalchemy import Table, Column, Integer, String, BLOB, ForeignKey
# элементы для создания отношений между объектами
from sqlalchemy.orm import relationship, backref
# подклюение ядра базы данных
from sqlalchemy.ext.declarative import declarative_base
# подключение фичи, которая будет автомтически накладывать на таблицу repr
from sqlalchemy_repr import RepresentableBase

Base = declarative_base(cls=RepresentableBase)

user_answer = Table(
    'user_answer',
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("answer_id", Integer, ForeignKey("answers.id")),
    Column("is_correct", Integer, ForeignKey("answers.is_correct"))
)

answers_question = Table(
    'question_answers',
    Base.metadata,
    Column("answer_id", Integer, ForeignKey("answers.id")),
    Column("question_id", Integer, ForeignKey("questions.id"))
)

questions_category = Table(
    'questions_category',
    Base.metadata,
    Column("question_id", Integer, ForeignKey("questions.id")),
    Column("category_id", Integer, ForeignKey("categories.id"))
)


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer)
    login = Column(String)


class Questions(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    answers_id = relationship("Answers", backref=backref("questions"))


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    text = Column(String)


class Answers(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    is_correct = Column(BLOB)
    question_id = Column(Integer, ForeignKey("questions.id"))