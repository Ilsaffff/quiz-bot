from bs4 import BeautifulSoup as bs
import requests
from db import DBHelper

URL = 'https://dropi.ru/posts/test-na-proverku-nachitannosti-vechnyj-shedevry-smozhete-skazat-kto-avtor-etix-legendarnyx-proizvedenij'
# tests from https://dropi.ru/
category_id = 2

r = requests.get(URL)
soup = bs(r.text, "html.parser")
db = DBHelper('context.db')

for parent_block in soup.find_all(class_='bTest__query__item js-test-item'):
    question = parent_block.find('h2')
    db.add_question(question_text=question.text, category_id=category_id)
    question_id = db.get_question_id(question_text=question.text)
    answers_block = parent_block.find_all(class_='bTest__query__variant js-test-item-variant')
    for answer_block in answers_block:
        if answer_block['data-correct'] == 'true':
            db.add_answer_true(answer_text=answer_block.text, question_id=question_id)
        elif answer_block['data-correct'] == 'false':
            db.add_answer_false(answer_text=answer_block.text, question_id=question_id)
print('Done!')
