# Для работы программы требуются следующие пакеты
# pip install pysqlite3
# pip install tk
# pip install PySimpleGUI
# pip install requests


# Модуль регулярных выражений для проверки маски почты
import re
# Модуль оконных функций
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Модули нашей программы (Модуль БД и модуль API)
from database import Database
from api import main_window


# Глобальные константы
DB_NAME = "user.db"
VALIDATE_EMAIL = 1
VALIDATE_PASSWORD = 0


class App(tk.Tk):
    # Главный класс оконного модуля Tkinter

    def __init__(self):
        # Инициализиурем класс и отображаем окно логина

        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(LoginFrame)

    def switch_frame(self, frame_class):
        # Смена окна, при переключение с Логина на Регистрацию и обратно

        self.new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = self.new_frame
        self._frame.pack()


class LoginFrame(tk.Frame):
    # Окно логина/входа

    def __init__(self, master):
        # При инициализации окна расчитываем его размер и положение

        super().__init__(master)

        master.title("Вход")

        w = 220
        h = 120
        ws = master.winfo_screenwidth()
        hs = master.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        master.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # Метки окна

        self.label_username = tk.Label(self, text="Логин")
        self.label_password = tk.Label(self, text="Пароль")

        # Поля ввода

        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")

        # Размещение меток и полей ввода в окне

        self.label_username.grid(row=0)
        self.label_password.grid(row=1)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        # Кнопка Входа

        self.logbtn = tk.Button(self, text="Войти", command=self.login_btn_clicked)
        self.logbtn.grid(row=3, column=0, sticky="ew")

        # Кнопка Регистрации пользователя

        self.create_new_user_button = tk.Button(self, text="Зарегистрироваться", command=lambda: master.switch_frame(SignUpFrame))
        self.create_new_user_button.grid(row=3, column=1, sticky="e")

        self.pack(expand=1)

    def login_btn_clicked(self):
        # Метод запускающийся при нажатии на кнопку

        # Получаем данные из полей ввода

        self.username = self.entry_username.get()
        self.password = self.entry_password.get()

        if len(self.username) == 0 and len(self.password) == 0:
            # Ошибка если не введены поля логина и пароля

            messagebox.showerror("Вход", "Введите логин и пароль")
        elif len(self.username) == 0:
            # Не введен логин

            messagebox.showerror("Вход", "Введите логин")
        elif len(self.password) == 0:
            # Не введен пароль

            messagebox.showerror("Вход", "Введите пароль")
        else:
            # Подключение к базе
            self.database = Database(DB_NAME)

            # Если база пустая - создаем таблицу
            self.database.create_table()

            # Получения записи о пользователе из базы
            self.check = self.database.retrieve_user(self.username)

            if self.check is None:
                # Ошибка - пользователь не найден

                messagebox.showerror("Ошибка входа", "Пользователя не существует")
            else:
                if self.username == self.check[3] and self.password == self.check[4]:
                    # Если авторизауия прошла успешно

                    #messagebox.showinfo("Login info", "Добро пожаловать " + self.check[0])
                    self.master.destroy()

                    # Запускаем главное окно из модуля api.py
                    main_window(self.check[0], self.check[5])
                else:
                    # Если пользователя не существует

                    messagebox.showerror("Ошибка входа", "Наверная пара логин - пароль")


class SignUpFrame(tk.Frame):
    # Форма регистрации

    def __init__(self, master):
        # Инициализация формы и вычисления ее размеров
        super().__init__(master)

        master.title("Регистрация")

        w = 220
        h = 190
        ws = master.winfo_screenwidth()
        hs = master.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        master.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # Метки

        self.information_label = tk.Label(self, text="Все поля обязательны!")
        self.role_label = tk.Label(self, text="Роль")
        self.name_label = tk.Label(self, text="Имя")
        self.surname_label = tk.Label(self, text="Фамилия")
        self.email_label = tk.Label(self, text="Email")
        self.username_label = tk.Label(self, text="Логин")
        self.password_label = tk.Label(self, text="Пароль")

        # Поля

        self.role_entry = ttk.Combobox(self, values=["Guest", "User", "Admin"], state="readonly")
        self.role_entry.current(0)
        self.name_entry = tk.Entry(self)
        self.surname_entry = tk.Entry(self)
        self.email_entry = tk.Entry(self)
        self.username_entry = tk.Entry(self)
        self.password_entry = tk.Entry(self, show="*")

        # Верстка

        self.information_label.grid(row=0, column=1, sticky="w")

        self.role_label.grid(row=1, column=0, sticky="w")
        self.role_entry.grid(row=1, column=1)

        self.name_label.grid(row=2, column=0, sticky="w")
        self.name_entry.grid(row=2, column=1)

        self.surname_label.grid(row=3, column=0, sticky="w")
        self.surname_entry.grid(row=3, column=1)

        self.email_label.grid(row=4, column=0, sticky="w")
        self.email_entry.grid(row=4, column=1)

        self.username_label.grid(row=5, column=0, sticky="w")
        self.username_entry.grid(row=5, column=1)

        self.password_label.grid(row=6, column=0, sticky="w")
        self.password_entry.grid(row=6, column=1)

        # Кнопки

        self.return_button = tk.Button(self, text="Отмена", command=lambda: master.switch_frame(LoginFrame))
        self.return_button.grid(row=7, column=0, sticky="w")

        self.submit_button = tk.Button(self, text="Регистрация", command=self.createUser)
        self.submit_button.grid(row=7, column=1, sticky="e")

        self.pack(expand=1)


    def createUser(self):
        # Вставка пользователя в базу

        # Получем данные из формы регистрации

        self.name_entry_content = self.name_entry.get()
        self.surname_entry_content = self.surname_entry.get()
        self.username_entry_content = self.username_entry.get()
        self.password_entry_content = self.password_entry.get()
        self.email_entry_content = self.email_entry.get()
        self.role_entry_content = self.role_entry.get()

        if self.validate_data(self.name_entry_content, self.surname_entry_content,
                              self.username_entry_content, self.password_entry_content,
                              self.email_entry_content):
            # Валидируем введенные данные

            # Создаем таблицу если база пуста
            self.database.create_table()

            self.database.insert_row(self.name_entry_content, self.surname_entry_content, self.username_entry_content,
                                     self.password_entry_content, self.email_entry_content, self.role_entry_content)
            messagebox.showinfo("Регистрация", "Пользователь зарегистрирован")
            self.master.switch_frame(LoginFrame)

    def validate_data(self,
                      name, surname,
                      username, password,
                      email):
        # Метод валидирующий данные

        if self.validate_name(name) and self.validate_surname(surname) and self.validate_email(
                email) and self.validate_username(username) and self.validate_password(password):
            return True

    def validate_name(self, name):
        # Валидация имени

        if len(name) == 0:
            messagebox.showerror("Регистрация", "Введите Имя")
        else:
            return True

    def validate_surname(self, surname):
        # Валидация фамилии

        if len(surname) == 0:
            messagebox.showerror("Регистрация", "Введите фамилию")
        else:
            return True

    def validate_password(self, password):
        # Валидация пароля по 2-м уровням

        # Проверка на размер
        if len(password) == 0:
            messagebox.showerror("Регистрация", "Введите пароль")

        # Если включена константа VALIDATE_PASSWORD пароль валидируется на сложность
        elif VALIDATE_PASSWORD:
            if len(password) < 8:
                messagebox.showerror("Sign Up Info", "The password cannot be less than 8 characters")
            elif not re.search(r"[A-Z]", password):
                messagebox.showerror("Sign Up Info", "The password must contain an uppercase letter")
            elif not re.search(r"[!@#]", password):
                messagebox.showerror("Sign Up Info", "The password must contain one special character")
            else:
                return True
        else:
            return True

    def validate_username(self, username):
        # Валидация пользователя

        if len(username) == 0:
            messagebox.showerror("Регистрация", "Пожалуйста введите имя пользователя")
        else:
            self.database = Database(DB_NAME)
            if self.database.retrieve_user(username) == None:
                return True
            else:
                messagebox.showerror("Регистрация", "Такой пользователь уже существует")
                return False

    def validate_email(self, email):
        # Валидация адреса электронной почты

        if len(email) == 0:
            # Проверка на пустоту поля

            messagebox.showerror("Регистрация", "Укажите адрес электронной почты")
        elif not VALIDATE_EMAIL:
            return True
        else:
            if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
                # Проверка по маске электронного ящика

                return True
            else:
                messagebox.showerror("Регистрация", "Почтовый адрес не верен")
                return False


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()