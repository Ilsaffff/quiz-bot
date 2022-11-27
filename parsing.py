from bs4 import BeautifulSoup as bs
import codecs
from db import DBHelper

file = 'parsing_file.html'

number_answer = 1
questions = []
answers_correct = []
answers1 = []
answers2 = []
answers3 = []
r = codecs.open(file, 'r', 'utf-8')
soup = bs(r.read(), "html.parser")
questions_pars = soup.find_all('h2')
answers_correct_pars = soup.find_all(
    class_='bTest__query__variant js-test-item-variant background--success results')
answers_pars = soup.find_all(class_='bTest__query__variant js-test-item-variant results')
for question in questions_pars:
    questions.append(question.text)
for answer_pars in answers_correct_pars:
    answer_text = answer_pars.text[:-4]
    answers_correct.append(answer_text.strip())
for answer in answers_pars:
    if number_answer == 1:
        answer_text = answer.text[:-4]
        answers1.append(answer_text.strip())
        number_answer = 2
    elif number_answer == 2:
        answer_text = answer.text[:-4]
        answers2.append(answer_text.strip())
        number_answer = 3
    elif number_answer == 3:
        answer_text = answer.text[:-4]
        answers3.append(answer_text.strip())
        number_answer = 1
