import sqlite3


class DBHelper:
    def __init__(self, db_file):
        self.db_file = db_file
        self._init_tables()

    def _sql_query(self, query, *args):
        with sqlite3.connect(self.db_file) as connect:
            cursor = connect.cursor()
            cursor.execute(query, args)
            data = cursor.fetchall()
            connect.commit()
            return data

    def _init_tables(self):
        self._sql_query('''CREATE TABLE IF NOT EXISTS users (
                         id INTEGER PRIMARY KEY,
                         login TEXT);''')
        self._sql_query('''CREATE TABLE IF NOT EXISTS users_questions (
                        "user_id"	INTEGER,
                        "category_id"	INTEGER NOT NULL,
                        "question_id"	INTEGER NOT NULL,
                        "status"	INTEGER DEFAULT 0)
                        ''')

    def add_user(self, user_id, username):
        self._sql_query('INSERT OR IGNORE INTO users VALUES (?,?)', user_id, username)

    def delete_user(self, user_id):
        self._sql_query('''DELETE FROM users WHERE id = %(user_id)d''' % {'user_id': user_id})

    def get_categories(self):
        categories = self._sql_query('SELECT text FROM categories')
        categories = [elem[0] for elem in categories]  # [(name1,), (name2,)] -> [name1, name2]
        return categories

    def get_id_category(self, category):
        category_id = self._sql_query("""SELECT id FROM categories 
                    WHERE text = '%s'""" % (category))
        category_id = category_id[0][0]
        return category_id

    def get_id_questions(self, category_id):
        questions_id = self._sql_query('''SELECT question_id FROM question_category WHERE category_id = {}
                        '''.format(category_id))
        questions_id = [elem[0] for elem in questions_id]
        # questions = self._sql_query('''SELECT text FROM questions
        #                             WHERE id IN {}'''.format(questions_id))
        # questions = [elem[0] for elem in questions]
        return questions_id

    def get_question(self, question_id):
        question = self._sql_query('''SELECT text FROM questions 
                                    WHERE id = %(question_id)d''' % {'question_id': question_id})
        return question

    def select_category(self, category_id):
        category = self._sql_query('''SELECT text FROM categories 
                                   WHERE id = %(category_id)d''' % {'category_id': category_id})
        category = (list(category[0]))
        return category[0]

    def select_buttons(self, question_id):
        buttons_id = self._sql_query('''SELECT answer_id FROM answer_question WHERE question_id = %(question_id)d
                        ''' % {'question_id': question_id})
        buttons_id = tuple([elem[0] for elem in buttons_id])
        buttons = self._sql_query('''SELECT text
                        FROM answers
                        WHERE id IN {}'''.format(buttons_id))
        buttons = list([elem[0] for elem in buttons])
        return buttons

    def status_question(self, user_id, message):
        answer_id = self._sql_query("""SELECT id 
                        FROM answers
                        WHERE text = ? """, (message))
        answer_id = list(answer_id[0])[0]
        is_correct = self._sql_query("""SELECT is_correct 
                            FROM answer_question
                            WHERE answer_id = %(answer_id)d""" % {'answer_id': answer_id})
        is_correct = list(is_correct[0])[0]
        self._sql_query("""INSERT INTO users_questions VALUES (?,?,?)""", user_id, answer_id, is_correct)
        # self._sql_query("""INSERT INTO users_questions
        # VALUES (?,?,?,?)""", user_id, category_id, question_id, status)

    def count_result(self, user_id, category_id):
        questioins_id = self._sql_query("""SELECT question_id FROM question_category
                                            WHERE category_id = {}""".format(category_id))
        questioins_id = tuple([elem[0] for elem in questioins_id])
        answers_id = self._sql_query("""SELECT answer_id FROM answer_question
                                        WHERE question_id IN {}""".format(questioins_id))
        answers_id = tuple([elem[0] for elem in answers_id])
        count = self._sql_query("""SELECT COUNT(*) FROM users_questions 
                        WHERE user_id = {}
                        AND answer_id IN {}
                        AND status = 1""".format(user_id,answers_id))
        count = list(count[0])
        # self._sql_query("""DELETE FROM users_questions
        #                 WHERE user_id = %(user_id)d
        #                 AND category_id = %(category_id)d""" % {'user_id': user_id, 'category_id': category_id})
        return count[0]
