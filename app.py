from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
from collections import deque
import threading
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
app = Flask(__name__)
app.secret_key = 'секретно-секретный секрет'
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
count = 0

@app.route("/")


@app.route("/index")
def index():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        
        <main>
            <nav>
                <ul>
                    <li><a href="/lab1">Первая лабораторная</a></li>
                    <li><a href="/lab2/">Вторая лабораторная</a></li>
                    <li><a href="/lab3/">Третья лабораторная</a></li>
                    <li><a href="/lab4/">Четвертая лабораторная</a></li>
                    <li><a href="/lab5/">Пятая лабораторная</a></li>
                </ul>
            </nav>
        </main>
        
        <footer>
            <hr>
            <p>Минько Елена Михайловна, ФБИ-34, 3 курс, 2025</p>
        </footer>
    </body>
</html>
'''


@app.route('/400')
def bad_request():
    return '''
<!doctype html>
<html>
    <head>
        <title>400 Bad Request</title>
    </head>
    <body>
        <h1>400 Bad Request</h1>
        <p>Сервер не может обработать запрос из-за неверного синтаксиса.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 400


@app.route('/401')
def unauthorized():
    return '''
<!doctype html>
<html>
    <head>
        <title>401 Unauthorized</title>
    </head>
    <body>
        <h1>401 Unauthorized</h1>
        <p>Требуется аутентификация для доступа к ресурсу.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 401


@app.route('/402')
def payment_required():
    return '''
<!doctype html>
<html>
    <head>
        <title>402 Payment Required</title>
    </head>
    <body>
        <h1>402 Payment Required</h1>
        <p>Требуется оплата для доступа к ресурсу.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 402


@app.route('/403')
def forbidden():
    return '''
<!doctype html>
<html>
    <head>
        <title>403 Forbidden</title>
    </head>
    <body>
        <h1>403 Forbidden</h1>
        <p>Доступ к запрошенному ресурсу запрещен.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 403


@app.route('/405')
def method_not_allowed():
    return '''
<!doctype html>
<html>
    <head>
        <title>405 Method Not Allowed</title>
    </head>
    <body>
        <h1>405 Method Not Allowed</h1>
        <p>Метод запроса не поддерживается для данного ресурса.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 405


@app.route('/418')
def teapot():
    return '''
<!doctype html>
<html>
    <head>
        <title>418 I'm a teapot</title>
    </head>
    <body>
        <h1>418 I'm a teapot</h1>
        <p>Я чайник и не могу заваривать кофе.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 418

access_log = deque(maxlen=100)
log_lock = threading.Lock()


@app.errorhandler(404)
def not_found(err):
    user_ip = request.remote_addr
    access_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url
    
    with log_lock:
        access_log.append({
            'ip': user_ip,
            'date': access_date,
            'url': requested_url,
            'user_agent': request.user_agent.string
        })
    
    css_path = url_for("static", filename="lab1/error.css")
    image_path = url_for("static", filename="lab1/apple.jpg")
    
    return f'''
<!doctype html>
<html>
    <head>
        <title>404 - Страница не найдена</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="error-container">
            <h1>404</h1>
            <h2>Не переживай</h2>
            <img src="{image_path}" alt="мяу" class="error-image">
            <p>Сейчас на вертолете прилетил Крис Редфилд</p>
            <p>Он скинет ракетницу</p>
            <a href="/" class="home-link">И все взорвется</a>
            
            <!-- Информация о запросе -->
            <div class="info-section">
                <h3>Информация о запросе:</h3>
                <p><strong>IP-адрес:</strong> {user_ip}</p>
                <p><strong>Дата и время:</strong> {access_date}</p>
                <p><strong>Запрошенный URL:</strong> {requested_url}</p>
                <p><strong>Вернуться на:</strong> <a href="/" style="color: #cccccc; text-decoration: underline;">Главную страницу</a></p>
            </div>
            
            <!-- История обращений -->
            <div class="log-section">
                <h3>История обращений:</h3>
                {generate_log_html()}
            </div>
        </div>
    </body>
</html>
''', 404


def generate_log_html():
    """Генерирует HTML для отображения лога обращений"""
    with log_lock:
        logs = list(access_log)
    
    if not logs:
        return "<p>Лог пуст</p>"
    
    log_html = []
    for log in reversed(logs):
        log_html.append(f'''
        <div class="log-entry">
            <p><strong>IP:</strong> {log['ip']} | 
               <strong>Дата:</strong> {log['date']}</p>
            <p><strong>URL:</strong> {log['url']}</p>
            <p><strong>Браузер:</strong> {log['user_agent'][:80]}...</p>
        </div>
        ''')
    
    return ''.join(log_html)


@app.route("/lab1/error")
def server_error():
    result = 10 / 0  # Деление на ноль
    return str(result)


@app.errorhandler(500)
def internal_server_error(err):
    return '''
<!doctype html>
<html>
    <head>
        <title>500 - Ошибка сервера</title>
    </head>
    <body>
        <h1>500 - Внутренняя ошибка сервера</h1>
        <p>На сервере произошла непредвиденная ошибка.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 500
