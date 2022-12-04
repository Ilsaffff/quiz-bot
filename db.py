from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Category, Question, Answer
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

    def add_user_category(self, user_id, category_id):
        user = self.session.query(User).filter_by(id=user_id).first()
        category = self.session.query(Category).filter_by(id=category_id).first()
        user.category = [category]
        self.session.commit()

    def get_user(self, user_id):
        user = self.session.query(User).filter_by(id=user_id).first()
        return user

    def get_result(self, user_id, questions_max_count):
        result = 0
        answers = self.session.query(Answer).join(User.answers).filter(
            User.id == user_id).all()[::-1][:questions_max_count]
        for answer in answers:
            if answer.is_correct:
                result += 1
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

    def get_question_by_id(self, question_id):
        question = self.session.query(Question).filter_by(id=question_id).first()
        return question

    def get_next_user_question(self, user_id, category_id):
        questions_new = []
        questions_user = []
        questions_all = self.session.query(Question).filter_by(category_id=category_id).all()
        answers_user = self.session.query(User).filter_by(id=user_id).first().answers
        if answers_user:
            for answer_user in answers_user:
                questions_user.append(self.get_question_by_id(answer_user.question_id))
            for question in questions_all:
                if question in questions_user:
                    continue
                else:
                    questions_new.append(question)
        else:
            questions_new = questions_all
        question = random.choice(questions_new)
        return question