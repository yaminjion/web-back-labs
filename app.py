from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
from collections import deque
import threading
from lab1 import lab1
app = Flask(__name__)
app.register_blueprint(lab1)
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


@app.route('/lab2/')
def lab2():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная работа 2</title>
    </head>
    <body>
        <a href="/">На главную</a>
        
        <h1>Лабораторная работа 2</h1>
        
        <h2>Список всех адресов:</h2>
        <ul>
            <li><a href="/lab2/a">/lab2/a (без слэша)</a></li>
            <li><a href="/lab2/a/">/lab2/a/ (со слэшем)</a></li>
            <li><a href="/lab2/flowers">/lab2/flowers - Все цветы</a></li>
            <li><a href="/lab2/flowers/0">/lab2/flowers/0 - Цветок с ID 0</a></li>
            <li><a href="/lab2/flowers/1">/lab2/flowers/1 - Цветок с ID 1</a></li>
            <li><a href="/lab2/flowers/2">/lab2/flowers/2 - Цветок с ID 2</a></li>
            <li><a href="/lab2/flowers/3">/lab2/flowers/3 - Цветок с ID 3</a></li>
            <li><a href="/lab2/add_flower_form">/lab2/add_flower_form - Форма добавления цветка</a></li>
            <li><a href="/lab2/clear_flowers">/lab2/clear_flowers - Очистка списка цветов</a></li>
            <li><a href="/lab2/example">/lab2/example - Пример шаблона</a></li>
            <li><a href="/lab2/filters">/lab2/filters - Фильтры Jinja2</a></li>
            <li><a href="/lab2/calc/">/lab2/calc/ - Калькулятор (по умолчанию)</a></li>
            <li><a href="/lab2/calc/5">/lab2/calc/5 - Калькулятор с одним числом</a></li>
            <li><a href="/lab2/calc/10/3">/lab2/calc/10/3 - Калькулятор с двумя числами</a></li>
            <li><a href="/lab2/books/">/lab2/books/ - Список книг</a></li>
            <li><a href="/lab2/objects/">/lab2/objects/ - Галерея объектов</a></li>
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


@app.route('/lab2/a')
def a():
    return '''
<!doctype html>
<html>
    <body>
        <p>без слэша</p>
        <a href="/">На главную</a>
    </body>
</html>
'''


@app.route('/lab2/a/')
def a2():
    return '''
<!doctype html>
<html>
    <body>
        <p>со слэшем</p>
        <a href="/">На главную</a>
    </body>
</html>
'''


flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']
def get_default_flowers():
    """Возвращает список цветов по умолчанию"""
    return ['роза', 'тюльпан', 'незабудка', 'ромашка']


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
        <a href="/">На главную</a>
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
        <a href="/">На главную</a>
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
        <a href="/">На главную</a>
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
        <a href="/">На главную</a>
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
        <a href="/">На главную</a>
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
        <a href="/">На главную</a>
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
            <a href="/">На главную</a>
        </div>
        <p><a href="/lab2/calc/">Вернуться к значениям по умолчанию (1/1)</a></p>
    </body>
    </html>
    """
    
    return html

# Данные о книгах
books = [
    {'author': 'Фёдор Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 551},
    {'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман-эпопея', 'pages': 1225},
    {'author': 'Михаил Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
    {'author': 'Александр Пушкин', 'title': 'Евгений Онегин', 'genre': 'Роман в стихах', 'pages': 240},
    {'author': 'Николай Гоголь', 'title': 'Мёртвые души', 'genre': 'Поэма', 'pages': 352},
    {'author': 'Иван Тургенев', 'title': 'Отцы и дети', 'genre': 'Роман', 'pages': 288},
    {'author': 'Михаил Лермонтов', 'title': 'Герой нашего времени', 'genre': 'Роман', 'pages': 224},
    {'author': 'Антон Чехов', 'title': 'Вишнёвый сад', 'genre': 'Пьеса', 'pages': 96},
    {'author': 'Иван Гончаров', 'title': 'Обломов', 'genre': 'Роман', 'pages': 464},
    {'author': 'Александр Островский', 'title': 'Гроза', 'genre': 'Драма', 'pages': 128},
]

# Обработчик для списка книг
@app.route('/lab2/books/')
def books_list():
    return render_template('books.html', books=books)

# Данные по объектам из фото
objects = [
    {'name': 'Ведьмы', 'description': 'Мистические существа', 'image': 'ведьмы.jpg'},
    {'name': 'веселушки', 'description': 'Веселые персонажи', 'image': 'веселушки.jpg'},
    {'name': 'весна', 'description': 'Весеннее время года', 'image': 'весна.jpg'},
    {'name': 'вместе', 'description': 'Дружная компания', 'image': 'вместе.jpg'},
    {'name': 'головы', 'description': 'Изображения голов', 'image': 'головы.jpg'},
    {'name': 'Гяру', 'description': 'Японский стиль моды', 'image': 'гяру.jpg'},
    {'name': 'зайчик', 'description': 'Милый кролик', 'image': 'зайчик.jpg'},
    {'name': 'зима', 'description': 'Зимнее время года', 'image': 'зима.jpg'},
    {'name': 'кот', 'description': 'Домашний питомец', 'image': 'кот.jpg'},
    {'name': 'котики', 'description': 'Милые котята', 'image': 'котики.jpg'},
    {'name': 'Мику', 'description': 'Вокалоид Хацунэ Мику', 'image': 'мику.jpg'},
    {'name': 'няя', 'description': 'Аниме персонаж', 'image': 'няя.jpg'},
    {'name': 'очкарики', 'description': 'Персонажи в очках', 'image': 'очкарики.jpg'},
    {'name': 'река', 'description': 'Водный поток', 'image': 'река.jpg'},
    {'name': 'рин и лен', 'description': 'Вокалоиды Кагамине', 'image': 'рин и лен.jpg'},
    {'name': 'Рыжая', 'description': 'Рыжеволосая девушка', 'image': 'рыжая.jpg'},
    {'name': 'фото', 'description': 'Фотографии', 'image': 'фото.jpg'},
    {'name': 'художница', 'description': 'Девушка-художник', 'image': 'художница.jpg'},
    {'name': 'циклопы', 'description': 'Существа с одним глазом', 'image': 'циклопы.jpg'},
    {'name': 'чай', 'description': 'Напиток', 'image': 'чай.jpg'}
]

@app.route('/lab2/objects/')
def objects_list():
    return render_template('objects.html', objects=objects)