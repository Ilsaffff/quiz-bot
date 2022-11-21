from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Users, Categories, Questions, Answers, UsersAnswers
from models import Base
import random


class DBHelper:
    def __init__(self, db_file):
        self.db_file = db_file
        self.engine = create_engine(f'sqlite:///{db_file}', echo=True)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_user(self, user_id, username):
        exists = self.session.query(Users).filter_by(id=user_id, username=username).first()
        if not exists:
            self.session.add(Users(id=user_id, username=username))
            self.session.commit()

    def delete_user(self, user_id):
        self.session.query(Users).filter_by(id=user_id).delete()
        self.session.commit()

    def get_categories(self):
        categories = self.session.query(Categories.text).all()
        categories = [element[0] for element in categories]
        return categories

    def get_category_id(self, category):
        category_id = self.session.query(Categories.id).filter_by(text=category).first()
        return category_id[0]

    def get_question_id(self, question):
        question_id = self.session.query(Questions.id).filter_by(text=question).first()
        return question_id[0]

    def get_questions_id(self, category_id):
        questions_id = self.session.query(Questions.id).filter_by(category_id=category_id).all()
        questions_id = [element[0] for element in questions_id]
        questions_id = random.choice(questions_id)
        return questions_id

    def parsing(self, category, questions, answers_correct, answers1, answers2, answers3):
        exists = self.session.query(Categories).filter_by(text=category).first()
        if not exists:
            self.session.add(Categories(text=category))
        category_id = self.get_category_id(category)
        question_number = 10
        for i in range(question_number):
            self.session.add(Questions(text=questions[i], category_id=category_id))
            self.session.add(
                Answers(text=answers_correct[i], question_id=self.get_question_id(questions[i]), is_correct=True))
            self.session.add(
                Answers(text=answers1[i], question_id=self.get_question_id(questions[i]), is_correct=False))
            self.session.add(
                Answers(text=answers2[i], question_id=self.get_question_id(questions[i]), is_correct=False))
            self.session.add(
                Answers(text=answers3[i], question_id=self.get_question_id(questions[i]), is_correct=False))
        self.session.commit()

