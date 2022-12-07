from bs4 import BeautifulSoup as bs
import requests
from db import DBHelper

db = DBHelper('foregun.db')
MAIN_URL = 'https://dropi.ru'
URL_TESTS = 'https://dropi.ru/c/worldhistory'

category_id = 5

r = requests.get(URL_TESTS)
soup = bs(r.text, "html.parser")

href_all = soup.find('div', class_='grid__col grid__col--xs-12 grid__col--md-7 grid__col--lg-8 content__col').find_all(
    'a', {'class': 'link link--text'})
for href in href_all:
    req = requests.get(MAIN_URL + href.get('href'))
    soup = bs(req.text, "html.parser")
    for parent_block in soup.find_all(class_='bTest__query__item js-test-item'):
        question = parent_block.find('h2')
        db.add_question(question_text=question.text, category_id=category_id)
        question_id = db.get_question_id(question_text=question.text)
        answers_block = parent_block.find_all(class_='bTest__query__variant js-test-item-variant')
        for answer_block in answers_block:
            if answer_block['data-correct'] == 'true':
                db.add_answer(answer_text=answer_block.text, is_correct=True, question_id=question_id)
            elif answer_block['data-correct'] == 'false':
                db.add_answer(answer_text=answer_block.text, is_correct=False, question_id=question_id)
print('Done!')
