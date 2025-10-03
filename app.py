from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
from collections import deque
import threading

app = Flask(__name__)

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

@app.route("/lab1")
def lab1():
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

@app.route("/lab1/web")
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

@app.route("/lab1/author")
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

@app.route('/lab1/image')
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

@app.route('/lab1/counter')
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

@app.route('/lab1/reset_counter')
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

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
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
    
    css_path = url_for("static", filename="error.css")
    image_path = url_for("static", filename="apple.jpg")
    
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
    result = 10 / 0
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

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return f'''
<!doctype html>
<html>
    <head>
        <title>Информация о цветке</title>
    </head>
    <body>
        <h1>Информация о цветке</h1>
        <p><strong>Цветок:</strong> {flower_list[flower_id]}</p>
        <p><strong>ID:</strong> {flower_id}</p>
        <p><a href="/lab2/flowers">Посмотреть все цветы</a></p>
        <p><a href="/lab2/add_flower_form">Добавить новый цветок</a></p>
    </body>
</html>
'''

@app.route('/lab2/add_flower/<name>')
def add_flower_by_url(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен цветок</h1>
    <p><strong>Название нового цветка:</strong> {name}</p>
    <p><strong>Всего цветов:</strong> {len(flower_list)}</p>
    <p><strong>Полный список:</strong> {', '.join(flower_list)}</p>
    <p><a href="/lab2/flowers">Посмотреть все цветы</a></p>
    <p><a href="/lab2/add_flower_form">Добавить еще один цветок</a></p>
    </body>
</html>
'''

@app.route('/lab2/add_flower/')
def add_flower_from_form():
    name = request.args.get('name')
    if not name:
        abort(400, "вы не задали имя цветка")
    
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен цветок</h1>
    <p><strong>Название нового цветка:</strong> {name}</p>
    <p><strong>Всего цветов:</strong> {len(flower_list)}</p>
    <p><strong>Полный список:</strong> {', '.join(flower_list)}</p>
    <p><a href="/lab2/flowers">Посмотреть все цветы</a></p>
    <p><a href="/lab2/add_flower_form">Добавить еще один цветок</a></p>
    </body>
</html>
'''

@app.route('/lab2/flowers')
def all_flowers():
    return f'''
<!doctype html>
<html>
    <head>
        <title>Все цветы</title>
    </head>
    <body>
        <h1>Список всех цветов</h1>
        <p><strong>Общее количество цветов:</strong> {len(flower_list)}</p>
        <ul>
            {"".join([f'<li>{i}. {flower}</li>' for i, flower in enumerate(flower_list)])}
        </ul>
        <p><a href="/lab2/clear_flowers">Очистить список цветов</a></p>
        <p><a href="/lab2/add_flower_form">Добавить новый цветок</a></p>
    </body>
</html>
'''

@app.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return '''
<!doctype html>
<html>
    <body>
        <h1>Список цветов очищен</h1>
        <p>Все цветы были удалены из списка.</p>
        <p><a href="/lab2/flowers">Посмотреть все цветы</a></p>
        <p><a href="/lab2/add_flower_form">Добавить новый цветок</a></p>
    </body>
</html>
'''

@app.route('/lab2/add_flower_form')
def add_flower_form():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Добавить новый цветок</h1>
        <form action="/lab2/add_flower/" method="get">
            <label for="name">Название цветка:</label>
            <input type="text" id="name" name="name" required>
            <button type="submit">Добавить</button>
        </form>
        <p><a href="/lab2/flowers">Посмотреть все цветы</a></p>
    </body>
</html>
'''
@app.route('/lab2/example')
def example():
    name = 'Елена Минько'
    lab_number = 2
    group = 'ФБИ-34'
    course = 3
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95}, 
        {'name': 'манго', 'price': 321}]
    return render_template('example.html', 
                         name=name, 
                         lab_number=lab_number, 
                         group=group, 
                         course=course,
                         fruits=fruits)
@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = " О <b> сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

# Обработчик для /lab2/calc/ - перенаправляет на /lab2/calc/1/1
@app.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('calc_two_numbers', a=1, b=1))

# Обработчик для /lab2/calc/<int:a> - перенаправляет на /lab2/calc/a/1
@app.route('/lab2/calc/<int:a>')
def calc_one_number(a):
    return redirect(url_for('calc_two_numbers', a=a, b=1))

# Основной обработчик для двух чисел
@app.route('/lab2/calc/<int:a>/<int:b>')
def calc_two_numbers(a, b):
    # Выполняем математические операции
    addition = a + b
    subtraction = a - b
    multiplication = a * b
    division = a / b if b != 0 else "не определено (деление на ноль)"
    power = a ** b
    
    # Формируем HTML ответ
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Математические операции</title>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .operations {{ background-color: #f5f5f5; padding: 20px; border-radius: 5px; }}
            h1 {{ color: #333; }}
        </style>
    </head>
    <body>
        <h1>Расчёт с параметрами:</h1>
        <div class="operations">
            <p>{a} + {b} = {addition}</p>
            <p>{a} - {b} = {subtraction}</p>
            <p>{a} × {b} = {multiplication}</p>
            <p>{a} / {b} = {division}</p>
            <p>{a}<sup>{b}</sup> = {power}</p>
        </div>
        <p><a href="/lab2/calc/">Вернуться к значениям по умолчанию (1/1)</a></p>
    </body>
    </html>
    """
    
    return html