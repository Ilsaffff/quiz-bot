from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, query
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

    def get_questions(self, category_id):
        questions = self.session.query(Question).filter_by(category_id=category_id).all()
        return questions

    def get_answers(self, question_id):
        answers = self.session.query(Answer).filter_by(question_id=question_id).all()
        return answers

    def get_user(self, user_id):
        user = self.session.query(User).filter_by(user_id=user_id).first()
        return user

    def add_user_answer(self, user_id, answer_id):
        user = self.session.query(User).filter_by(id=user_id).first()
        answer = self.session.query(Answer).filter_by(id=answer_id).first()
        user.answers.append(answer)
        self.session.commit()


if __name__ == "__main__":
    pass
