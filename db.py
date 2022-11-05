import sqlite3


def sql_request(sql_script, db_file, is_select):
    if is_select:
        with sqlite3.connect('server.db') as connect:
            cursor = connect.cursor()
            cursor.execute(sql_script)
            data = cursor.fetchall()
            connect.commit()
            return data

    else:
        with sqlite3.connect(db_file) as connect:
            cursor = connect.cursor()
            cursor.execute(sql_script)
            connect.commit()


class DBHelper:
    def __init__(self, db_file):
        self.db_file = db_file

    def delete_user(self, user_id):
        sql_script = f"DELETE FROM users WHERE id = {user_id}"
        sql_request(sql_script, self.db_file, False)

    def add_user(self, user_id, username):
        sql_script = """CREATE TABLE IF NOT EXISTS users (
                         id INTEGER PRIMARY KEY,
                         login TEXT);"""
        sql_request(sql_script, self.db_file, False)
        sql_script = f"""INSERT OR IGNORE INTO users VALUES ({user_id},'{username}')"""
        sql_request(sql_script, self.db_file, False)
        sql_script = """CREATE TABLE IF NOT EXISTS users_questions (
                        "user_id"	INTEGER,
                        "category_id"	INTEGER NOT NULL,
                        "question_id"	INTEGER NOT NULL,
                        "status"	INTEGER DEFAULT 0)
                        """
        sql_request(sql_script, self.db_file, False)

    def select_question(self, id_category, id_question):
        sql_script = f"""SELECT question FROM questions WHERE id_category = {id_category}
                        AND id = {id_question} AND status = 0"""
        question = sql_request(sql_script, self.db_file, True)
        return question

    def select_category(self, id_category):
        sql_script = f"""SELECT category FROM categories WHERE id ={id_category}"""
        category = sql_request(sql_script, self.db_file, True)
        category_str = "".join(filter(str.isalpha, str(category)))
        return category_str

    def select_keyboards(self, id_question):
        sql_script = f"""SELECT key,choice1, choice2, choice3
                        FROM choices
                        WHERE id_question = {id_question}"""
        keyboards = sql_request(sql_script, self.db_file, True)
        keyboards_list = list(keyboards[0])
        return keyboards_list

    def status_question(self, user_id, id_category, id_question, status):
        sql_script = f"""INSERT INTO users_questions
        VALUES ({user_id}, {id_category}, {id_question}, {status})"""
        sql_request(sql_script, self.db_file, False)

    def count_result(self, user_id, id_category):
        sql_script = f"""SELECT COUNT(*) FROM users_questions 
                        WHERE user_id = {user_id}
                        AND category_id = {id_category}
                        AND status = 1"""
        count = sql_request(sql_script, self.db_file, True)
        count_list = list(count[0])
        sql_script = f"""DELETE FROM users_questions
                        WHERE user_id = {user_id}
                        AND category_id = {id_category}"""
        sql_request(sql_script, self.db_file, False)
        return count_list[0]
