from flask import Blueprint, render_template, request, redirect, url_for, session
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
lab5 = Blueprint('lab5', __name__)

def db_connect():
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='lena_minko_knowledge_base',
        user='lena_minko_knowledge_base',
        password='l3na'
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html')




@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()

    try:
        cur.execute("SELECT login FROM users WHERE login = %s;", (login,))
        if cur.fetchone():
            db_close(conn, cur)
            return render_template('lab5/register.html', error="Такой пользователь уже существует")

        hashed_password = generate_password_hash(password)
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, hashed_password))
        db_close(conn, cur)
        return render_template('lab5/success.html', login=login)
    except Exception as e:
        db_close(conn, cur)
        print(f"Ошибка базы данных: {e}")
        return render_template('lab5/register.html', error=f"Ошибка базы данных: {e}")


@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login_str = request.form.get('login')
    password = request.form.get('password')

    if not login_str or not password:
        return render_template('lab5/login.html', error="Заполните все поля")

    conn, cur = db_connect()

    try:
        cur.execute("SELECT * FROM users WHERE login = %s;", (login_str,))
        user = cur.fetchone()

        if not user:
            db_close(conn, cur)
            return render_template('lab5/login.html', error="Пользователь не найден")

        if not check_password_hash(user['password'], password):
            db_close(conn, cur)
            return render_template('lab5/login.html', error="Неверный пароль")

        session['login'] = user['login']
        db_close(conn, cur)
        return render_template('lab5/success_login.html', login=user['login'])
    except Exception as e:
        db_close(conn, cur)
        print(f"Ошибка базы данных: {e}")
        return render_template('lab5/login.html', error=f"Ошибка базы данных: {e}")