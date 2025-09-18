from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.route("/web")
def web(): 
    return """<!doctype html> 
        <html>
            <body>
                <h1>web-сервер на flask</h1>
                <a href="/author">author</a>
            </body> 
        </html>""", 200, {
            'X-сервер':'sample',
            'Content-Type': 'text/plain; charset=utf-8'
                          }

@app.route("/author")
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
                <a href="/web">web</a>
            </body>
        </html>""" 

@app.route('/lab1/image')
def image():
    image_path = url_for("static", filename="leon.jpg")
    css_path = url_for("static", filename="lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Леон</h1>
        <img src="''' + image_path + '''" alt="Леон">
    </body>
</html>
'''

count=0
@app.route('/counter')
def counter():
    global count
    count+=1
    time=datetime.datetime.today()
    url=request.url
    client_ip = request.remote_addr
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: '''+ str(count) + '''
        <hr>
        Дата и время:''' + str(time) + '''<br>
        Запрошенный адрес:''' + str(url) + '''<br>
        Ваш IP-адрес: ''' + str(client_ip) + '''<br>
    </body>
</html>
'''

@app.route("/info")
def info():
    return redirect("/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1> Создано успешно </h1>
        <div><i> Что-то создано... </i></div>
    </body>
</html>
''', 201

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404