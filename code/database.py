# Работаем с sqlite для максимальной переносимости программы
# self.database можно инициализировать любым сокетом sql базы данных
import sqlite3


class Database():
    # Класс sql запросов в кабзе данных

    def __init__(self, database_name):
        # При инициализации в качестве аргумента принимает имя файла с базой данных.
        # Создает саму базу и вызывает метод создания таблицы пользователей.

        self.database = sqlite3.connect(database_name)
        self.cursor = self.database.cursor()
        self.create_table()

    def create_table(self):
        # Метод создания таблицы пользователей
        # Name, Surname, Email - референсные поля с данными пользователя
        # Username, Password, Role - ключевые поля для авторизации

        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS usernames (Name text, Surname text, Email text, Username text, Password text, Role text)''')
        self.database.commit()

    def insert_row(self, name, surname, username, password, email, role):
        # Метод добавления новой записи в таблицу польхователей

        self.cursor.execute('''INSERT INTO usernames (Name,Surname,Username,Password,Email,Role) values (?,?,?,?,?,?)''',
                            (name, surname, username, password, email, role))
        self.database.commit()

    def retrieve_user(self, username):
        # Метод получения пользователя по его логину

        self.data = self.cursor.execute('''SELECT * FROM usernames WHERE Username = ?''', (username,))
        for row in self.data:
            return row

    def delete_user(self, username):
        # Метод удаления пользователя по его логину

        self.cursor.execute('''DELETE FROM usernames WHERE Username = ?''', (username,))
        self.database.commit()

    def update_user(self, username, name=None, surname=None, password=None, email=None, role=None):
        # Метод изменения данных пользователя

        if name:
            self.cursor.execute('''UPDATE usernames SET Name = ?''', (name,))
            self.database.commit()
        if surname:
            self.cursor.execute('''UPDATE usernames SET Surname = ?''', (surname,))
            self.database.commit()
        if password:
            self.cursor.execute('''UPDATE usernames SET Password = ?''', (password,))
            self.database.commit()
        if email:
            self.cursor.execute('''UPDATE usernames SET Email = ?''', (email,))
            self.database.commit()
        if role:
            self.cursor.execute('''UPDATE usernames SET Role = ?''', (role,))
            self.database.commit()
