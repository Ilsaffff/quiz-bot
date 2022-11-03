import re
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

    def select_question(self, category, id_question):
        sql_script = f"""SELECT question FROM questions WHERE id_category = {category}
                        AND id = {id_question} AND status = 0"""
        question = sql_request(sql_script, self.db_file, True)
        return question

    def select_category(self, id_category):
        sql_script = f"""SELECT category FROM categories WHERE id ={id_category}"""
        category = sql_request(sql_script, self.db_file, True)
        category_str = "".join(filter(str.isalpha, str(category)))
        return category_str

# сделать выбор нужен fetchall или нет?
