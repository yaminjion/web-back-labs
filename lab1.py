from flask import Blueprint, url_for, request, redirect, abort
import datetime
from collections import deque
import threading
lab1=Blueprint('lab1', __name__)

count = 0

@lab1.route("/lab1")
def lab():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <p>Flask — фреймворк для создания веб-приложений на языке
программирования Python, использующий набор инструментов
Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
называемых микрофреймворков — минималистичных каркасов
веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
        
        <a href="/">На главную</a>
        
        <h2>Список роутов</h2>
        <ul>
            <li><a href="/">Главная страница</a></li>
            <li><a href="/index">Index (альтернативная главная)</a></li>
            <li><a href="/400">400 - Bad Request</a></li>
            <li><a href="/401">401 - Unauthorized</a></li>
            <li><a href="/402">402 - Payment Required</a></li>
            <li><a href="/403">403 - Forbidden</a></li>
            <li><a href="/404">404 - Страница не найдена</a></li>
            <li><a href="/405">405 - Method Not Allowed</a></li>
            <li><a href="/418">418 - I'm a teapot</a></li>
            <li><a href="/lab1/web">Web-сервер</a></li>
            <li><a href="/lab1/author">Информация об авторе</a></li>
            <li><a href="/lab1/image">Изображение</a></li>
            <li><a href="/lab1/counter">Счетчик посещений</a></li>
            <li><a href="/lab1/reset_counter">Сброс счетчика</a></li>
            <li><a href="/lab1/info">Перенаправление (redirect)</a></li>
            <li><a href="/lab1/created">201 - Created</a></li>
            <li><a href="/lab1/error">Тест ошибки 500</a></li>
        </ul>
    </body>
</html>
'''


@lab1.route("/lab1/web")
def web(): 
    return """<!doctype html> 
        <html>
            <body>
                <h1>web-сервер на flask</h1>
                <a href="/lab1/author">author</a>
                <br>
                <a href="/">На главную</a>
            </body> 
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/html; charset=utf-8'
        }

@lab1.route("/lab1/author")
def author():
    name = "Минько Елена Михайловна"
    group = "ФБИ-34"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """ </p>
                <p>Группа: """ + group + """ </p>
                <p>Факультет: """ + faculty + """ </p>
                <a href="/lab1/web">web</a>
                <br>
                <a href="/">На главную</a>
            </body>
        </html>"""

@lab1.route('/lab1/image')
def image():
    image_path = url_for("static", filename="leon.jpg")
    css_path = url_for("static", filename="lab1.css")
    content = '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Леон</h1>
        <img src="''' + image_path + '''" alt="Леон">
        <br>
        <a href="/">На главную</a>
    </body>
</html>
'''
    return content, 200, {
        'Content-Language': 'ru',
        'X-Umbrella-Corp': 'T-Virus Research Division',
        'X-Raccoon-City': 'Quarantine Zone',
        'X-Server': 'sample',
        'Content-Type': 'text/html; charset=utf-8'
    }

@lab1.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время:''' + str(time) + '''<br>
        Запрошенный адрес:''' + str(url) + '''<br>
        Ваш IP-адрес: ''' + str(client_ip) + '''<br>
        <hr>
        <a href="/lab1/reset_counter">Сбросить счетчик</a>
        <br>
        <a href="/">На главную</a>
    </body>
</html>
'''

@lab1.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    return '''
<!doctype html>
<html>
    <body>
        <h1>Счетчик сброшен!</h1>
        <p>Счетчик был обнулен.</p>
        <a href="/lab1/counter">Вернуться к счетчику</a>
        <br>
        <a href="/">На главную</a>
    </body>
</html>
'''

@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@lab1.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1> Создано успешно </h1>
        <div><i> Что-то создано... </i></div>
        <a href="/">На главную</a>
    </body>
</html>
''', 201



