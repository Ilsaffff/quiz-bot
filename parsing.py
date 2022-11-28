from bs4 import BeautifulSoup as bs
import requests
from db import DBHelper
import models

URL = 'https://dropi.ru/....'
# tests from https://dropi.ru/

r = requests.get(URL)
soup = bs(r.text, "html.parser")
db = DBHelper('db.file')

for parent_block in soup.find_all(class_='bTest__query__item js-test-item'):
    question = parent_block.find('h2')
    db.session.add(models.Question(text=question.text, category_id=4))
    question_id = db.session.query(models.Question).filter_by(text=question.text).first().id
    answers_correct_block = parent_block.find_all('p')
    for answer_block in answers_correct_block:
        if answer_block['data-correct'] == 'true':
            db.session.add(models.Answer(text=answer_block.text, is_correct=True, question_id=question_id))
        elif answer_block['data-correct'] == 'false':
            db.session.add(models.Answer(text=answer_block.text, is_correct=False, question_id=question_id))
    db.session.commit()
