# элементы для определения атрибутов
from sqlalchemy import Table, Column, Integer, String, BLOB, ForeignKey, create_engine
# подклюение ядра базы данных
from sqlalchemy.ext.declarative import declarative_base
# подключение фичи, которая будет автомтически накладывать на таблицу repr
from sqlalchemy_repr import RepresentableBase

Base = declarative_base(cls=RepresentableBase)

user_answer = Table(
    'user_answer',
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
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
    id = Column(Integer, primary_key=True)
    username = Column(String)


class Questions(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    text = Column(String)


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    text = Column(String)


class Answers(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    is_correct = Column(BLOB)
