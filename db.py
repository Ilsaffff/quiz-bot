from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, query
from models import User, Category, Question, Answer, user_answers
from models import Base
import random


class DBHelper:

    def __init__(self, db_file):
        self.db_file = db_file
        self.engine = create_engine(f'sqlite:///{db_file}', echo=False, connect_args={"check_same_thread": False})
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_user(self, user_id, username):

        try:
            self.session.add(User(id=user_id, username=username))
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

    def delete_user(self, user_id):
        self.session.query(User).filter_by(id=user_id).delete()
        self.session.commit()

    def get_categories(self):
        categories = self.session.query(Category).all()
        return categories

    def add_user_answer(self, user_id, answer_id):
        user = self.session.query(User).filter_by(id=user_id).first()
        answer = self.session.query(Answer).filter_by(id=answer_id).first()
        user.answers.append(answer)
        self.session.commit()

    def get_result(self, user_id, questions_max_count):
        result = 0
        question_count = 0
        user = self.session.query(User).filter_by(id=user_id).first()
        answers = user.answers
        for answer in list(reversed(answers)):
            if question_count < questions_max_count:
                question_count = question_count + 1
                if answer.is_correct:
                    result = result + 1
            else:
                break
        return result

    def add_question(self, question_text, category_id):
        self.session.add(Question(text=question_text, category_id=category_id))
        self.session.commit()

    def get_question_id(self, question_text):
        question_id = self.session.query(Question).filter_by(text=question_text).first().id
        return question_id

    def add_answer_true(self, answer_text, question_id):
        self.session.add(Answer(text=answer_text, is_correct=True, question_id=question_id))
        self.session.commit()

    def add_answer_false(self, answer_text, question_id):
        self.session.add(Answer(text=answer_text, is_correct=False, question_id=question_id))
        self.session.commit()


db = DBHelper('testing.db')
