import sqlite3

class Database():
    def __init__(self, db_path = "utils/db_api/main.db"):
        self.path = db_path
        self.connect = sqlite3.connect(self.path)
        self.cursor = self.connect.cursor()
        self.important_piece()

    def important_piece(self):
        sql = """CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        user_id TEXT,
        name TEXT,
        surname TEXT,
        patronymic TEXT,
        rasm TEXT,
        birthday TEXT,
        group_id TEXT);"""
        self.cursor.execute(sql)
        self.connect.commit()

    def get_all(self):
        sql = """SELECT * FROM users;"""
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def up_data(self, user_id, name, surname, patronymic, rasm, birthday, group_id):
        sql = """INSERT INTO users(user_id, name, surname, patronymic, rasm, birthday, group_id) VALUES(?,?,?,?,?,?,?);"""
        self.cursor.execute(sql, (user_id, name, surname, patronymic, rasm, birthday, group_id))
        self.connect.commit()

    def delete_birthday(self, id_):
        sql = """DELETE FROM users WHERE id = ?;"""
        self.cursor.execute(sql, (id_,))
        self.connect.commit()

    def bormi_birth(self, name, surname, patronymic):
        sql = """SELECT * FROM users WHERE name = ? AND surname = ? AND patronymic = ?;"""
        self.cursor.execute(sql, (name, surname, patronymic,))
        return self.cursor.fetchall()

    def bormi(self, user_id):
        print(user_id)
        sql = """SELECT * FROM users WHERE user_id = ?"""
        self.cursor.execute(sql, (user_id,))
        return self.cursor.fetchall()
    
    def get_birthdays(self, group_id):
        sql = """SELECT * FROM users WHERE group_id = ?;"""
        self.cursor.execute(sql, (f"group_id:{group_id}",))
        return self.cursor.fetchall()
    
    def get_birthdays_by_user(self, user_id):
        sql = """SELECT * FROM users WHERE user_id = ?;"""
        self.cursor.execute(sql, (user_id,))
        return self.cursor.fetchall()
    
    def get_birthdays_by_user_and_id(self, user_id, id_):
        sql = """SELECT * FROM users WHERE user_id = ? AND id = ?;"""
        self.cursor.execute(sql, (user_id, id_,))
        return self.cursor.fetchall()
    
    def update_birthday(self, birthday, id_):
        sql = """UPDATE users SET birthday = ? WHERE id = ?;"""
        self.cursor.execute(sql, (birthday, id_))
        self.connect.commit()
    
    def update_pic(self, file_id, id_):
        sql = """UPDATE users SET rasm = ? WHERE id = ?;"""
        self.cursor.execute(sql, (file_id, id_))
        self.connect.commit()

    def update_name(self, name, id_):
        sql = """UPDATE users SET name = ? WHERE id = ?;"""
        self.cursor.execute(sql, (name, id_))
        self.connect.commit()
    
    def update_surname(self, surname, id_):
        sql = """UPDATE users SET surname = ? WHERE id = ?;"""
        self.cursor.execute(sql, (surname, id_))
        self.connect.commit()

    def update_patronymic(self, patronymic, id_):
        sql = """UPDATE users SET patronymic = ? WHERE id = ?;"""
        self.cursor.execute(sql, (patronymic, id_))
        self.connect.commit()
        