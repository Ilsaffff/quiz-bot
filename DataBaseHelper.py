import re
import sqlite3
from set import serverDB


class DBHelper:
    def deleteUser(user_id):
        with sqlite3.connect(serverDB) as connect:
            cursor = connect.cursor()
            cursor.execute(f"DELETE from users where id=?", (user_id,))
            connect.commit()

    def addUserinTable(user_id, username):
        with sqlite3.connect(serverDB) as connect:
            cursor = connect.cursor()
            sql_script = """CREATE TABLE IF NOT EXISTS users (
                         id INTEGER PRIMARY KEY,
                         login TEXT);"""
            cursor.executescript(sql_script)
            connect.commit()

        # проверка на уже существущий id
        cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
        data = cursor.fetchone()
        if data is None:
            # запись данных в соотвествующие столбцы
            users = [user_id, username]
            sqlite_insert = """INSERT INTO users 
                    (id, login)
                    VALUES (?,?)"""
            cursor.execute(sqlite_insert, users)
            connect.commit()

    def selectQuestion(category, id_question):
        with sqlite3.connect('server.db') as connect:
            cursor = connect.cursor()
            sql_select = f"""SELECT question 
                               FROM questions
                               WHERE 
                               category = '{category}'
                               AND
                               id = {id_question}
                               AND 
                               status = 0
                               """
            cursor.execute(sql_select)
            question = cursor.fetchall()
            return question

    def selectCategory(id_caregory):
        with sqlite3.connect('server.db') as connect:
            cursor = connect.cursor()
            sql_select = f"""SELECT category 
                                      FROM categories
                                      WHERE 
                                      id = {id_caregory}
                                      """
            cursor.execute(sql_select)
            category = cursor.fetchall()
            categoryStr = "".join(filter(str.isalpha, str(category)))
            return categoryStr
