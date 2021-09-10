# Еще один, более "красивый" оконный модуль
import PySimpleGUI as sg

# requests и json для разбора api запросов
import requests
import json
import time


# Token для запросов api vk
TOKEN = "5a8f33be911a70661d1215e33800a2dba8391099cd3cc2e8039b015c9a51205bc2e65018c2ae10ceaf28a"
# vk api версия
VER = '5.130'
# Число попыток для запроса при неудаче
RESPONSE_TRY = 3


# Верификация Роли пользователя для сообщения его прав
def role_text(role):
    if role == 'Guest':
        return 'Вы можете получать только общую информацию о сообществе.'
    if role == 'User':
        return 'Вы можете получать общую информацию о сообществе и ограниченную статистику.'
    if role == 'Admin':
        return 'Вы можете получать полную информацию и статистику сообщества.'


# Функция для get запроса api
def try_get_request(url):
    idle_iter = 0
    while idle_iter < RESPONSE_TRY:
        response = requests.get(url)
        if response.ok:
            return response
        else:
            time.sleep(3)
            idle_iter += 1
    return None


# Фнукция получения значения из словаря если есть ключ
def get_dict(dict, key):
    null_msg = 'Недоступно'
    if key in dict:
        return dict[key]
    else:
        return null_msg


# Удаление из текста переносов строки
def trim_str(str):
    str = str.replace('\n', '')
    str = str.strip()
    return  str


# Преобразование даты
def get_date(date):
    null_msg = 'Недоступно'
    date = str(date)
    if len(date) != 8:
        return null_msg
    return date[6:8] + '.' + date[4:6] + '.' + date[:4]


# Получение статистики
def get_stat(id, role):
    err_msg = 'Информация о сообществе недоступна'
    null_msg = 'Недоступно'
    url_groupinfo_sformat = f"https://api.vk.com/method/groups.getById?group_id=%s&extended=1&access_token={TOKEN}&fields=description,city,activity,status,start_date,members_count,fixed_post&v={VER}"

    # Подстраховываем подключение по api через оберточную функцию try_get_request
    response = try_get_request(url_groupinfo_sformat % id)
    if not response:
        return err_msg

    # Преобразуем json формат результата запроса в словарь
    res_dict = json.loads(response.text)
    if 'response' not in res_dict:
        return err_msg
    res_dict = res_dict['response'][0]

    # Достаем все значения из результатов запроса
    name = get_dict(res_dict, 'name')
    description = get_dict(res_dict, 'description')
    description = trim_str(description)
    if 'city' in res_dict:
        city = res_dict['city']['title']
    else:
        city = null_msg
    activity = get_dict(res_dict, 'activity')

    # Валидируем размер информации в зависимости от роли пользователя(второй аргумент функции)
    tmp_text_1 = 'Наименование сообщества: %s\n\nОписание сообщества: %s\n\nГород сообщества: %s\n\nКатегория сообщества: %s\n\n'
    status = get_dict(res_dict, 'status')
    start_date = get_dict(res_dict, 'start_date')
    start_date = get_date(start_date)
    tmp_text_2 = 'Текущий статус: %s\n\nДата создания сообщества: %s\n\n'
    members_count = get_dict(res_dict, 'members_count')
    fixed_post = get_dict(res_dict, 'fixed_post')
    tmp_text_3 = 'Число участников: %s\n\nКолличество постов: %s'

    res1 = tmp_text_1 % (name, description, city, activity)
    res2 = tmp_text_2 % (status, start_date)
    res3 = tmp_text_3 % (members_count, fixed_post)

    if role == 'Guest':
        return res1
    elif role == 'User':
        return res1 + res2
    else:
        return res1 + res2 + res3


# Главное окно программы
def main_window(name, role):
    layout = [
        [sg.Text('Добро пожаловать, %s!' % name, size=(40, 1), justification='center', font=("Helvetica", 20))],
        [sg.Text('')],
        [sg.Text('Ваш уровень прав в программе: %s' % role)],
        [sg.Text(role_text(role))],
        [sg.Text('')],
        [sg.Text('Введите идентификатор сообщества:', size=(40, 1), font=("Helvetica", 12)), sg.Text('', size=(23, 1)), sg.InputText('', size=(20, 1))],
        [sg.Text('', size=(40, 1)), sg.Submit('OK')],
        [sg.Output(size=(100, 20), key='-OUTPUT-')],
        [sg.Text('', size=(40, 1)), sg.Cancel('Exit')]
    ]

    window = sg.Window('Получение статистики Сообществ в vk', layout)
    while True:
        event, values = window.read()
        if event in (None, 'Exit', sg.WIN_CLOSED):
            window.close()
            exit(0)
        if event == 'OK':
            # Специальные метод очистики окна вывода в реальном режиме
            window['-OUTPUT-'].update('')
            print(get_stat(values[0], role))

    window.close()