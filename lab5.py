from flask import Blueprint, render_template, request, redirect, url_for, session
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from dotenv import load_dotenv
load_dotenv() 
lab5 = Blueprint('lab5', __name__)


def db_connect():
    db_type = os.environ.get('DB_TYPE', 'postgres')
    print(f"DEBUG: DB_TYPE = {db_type}") 
    if db_type == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='lena_minko_knowledge_base',
            user='lena_minko_knowledge_base',
            password='l3na'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(dir_path, 'database.db')
        print(f"DEBUG: SQLite path = {db_path}")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
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
    name = request.form.get('name', '').strip()

    if not login or not password or not name:
        return render_template('lab5/register.html', error='Заполните все поля (включая имя)')

    conn, cur = db_connect()
    try:
        db_type = os.environ.get('DB_TYPE', 'postgres')
        if db_type == 'postgres':
            cur.execute("SELECT login FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT login FROM users WHERE login = ?;", (login,))

        if cur.fetchone():
            db_close(conn, cur)
            return render_template('lab5/register.html', error="Такой пользователь уже существует")

        hashed_password = generate_password_hash(password)
        if db_type == 'postgres':
            cur.execute("INSERT INTO users (login, password, name) VALUES (%s, %s, %s);", (login, hashed_password, name))
        else:
            cur.execute("INSERT INTO users (login, password, name) VALUES (?, ?, ?);", (login, hashed_password, name))

        db_close(conn, cur)
        return render_template('lab5/success.html', login=login)
    except Exception as e:
        db_close(conn, cur)
        print(f"Ошибка базы данных: {e}")
        return render_template('lab5/register.html', error="Ошибка базы данных")

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
        db_type = os.environ.get('DB_TYPE', 'postgres')
        if db_type == 'postgres':
            cur.execute("SELECT * FROM users WHERE login = %s;", (login_str,))
        else:
            cur.execute("SELECT * FROM users WHERE login = ?;", (login_str,))

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
        return render_template('lab5/login.html', error="Ошибка базы данных")


@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    if 'login' not in session:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()
    is_favorite = bool(request.form.get('is_favorite'))
    is_public = bool(request.form.get('is_public'))

    if not title or not article_text:
        return render_template('lab5/create_article.html', error="Название и текст статьи не должны быть пустыми")

    login = session['login']
    conn, cur = db_connect()
    try:
        db_type = os.environ.get('DB_TYPE', 'postgres')
        if db_type == 'postgres':
            cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login = ?;", (login,))
        user = cur.fetchone()
        if not user:
            db_close(conn, cur)
            return render_template('lab5/create_article.html', error="Пользователь не найден")

        if db_type == 'postgres':
            cur.execute("""
                INSERT INTO articles (user_id, title, article_text, is_favorite, is_public, likes)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (user['id'], title, article_text, is_favorite, is_public, 0))
        else:
            cur.execute("""
                INSERT INTO articles (user_id, title, article_text, is_favorite, is_public, likes)
                VALUES (?, ?, ?, ?, ?, ?);
            """, (user['id'], title, article_text, is_favorite, is_public, 0))

        db_close(conn, cur)
        return redirect('/lab5/list')
    except Exception as e:
        db_close(conn, cur)
        print(f"Ошибка при создании статьи: {e}")
        return render_template('lab5/create_article.html', error="Ошибка при сохранении статьи")

@lab5.route('/lab5/list')
def list_articles():
    if 'login' not in session:
        return redirect('/lab5/login')

    login = session['login']
    conn, cur = db_connect()
    try:
        db_type = os.environ.get('DB_TYPE', 'postgres')
        if db_type == 'postgres':
            cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login = ?;", (login,))
        user = cur.fetchone()
        if not user:
            db_close(conn, cur)
            return render_template('lab5/articles.html', error="Пользователь не найден")

        if db_type == 'postgres':
            cur.execute("SELECT * FROM articles WHERE user_id = %s ORDER BY is_favorite DESC, id DESC;", (user['id'],))
        else:
            cur.execute("SELECT * FROM articles WHERE user_id = ? ORDER BY is_favorite DESC, id DESC;", (user['id'],))

        articles = cur.fetchall()
        db_close(conn, cur)
        return render_template('lab5/articles.html', articles=articles)
    except Exception as e:
        db_close(conn, cur)
        print(f"Ошибка при загрузке статей: {e}")
        return render_template('lab5/articles.html', error="Ошибка при загрузке статей")
    
@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5/')

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    if 'login' not in session:
        return redirect('/lab5/login')

    login = session['login']
    conn, cur = db_connect()
    try:
        db_type = os.environ.get('DB_TYPE', 'postgres')

        if db_type == 'postgres':
            cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login = ?;", (login,))
        user = cur.fetchone()
        if not user:
            db_close(conn, cur)
            return redirect('/lab5/login')

        if db_type == 'postgres':
            cur.execute("SELECT * FROM articles WHERE id = %s AND user_id = %s;", (article_id, user['id']))
        else:
            cur.execute("SELECT * FROM articles WHERE id = ? AND user_id = ?;", (article_id, user['id']))
        article = cur.fetchone()
        if not article:
            db_close(conn, cur)
            return render_template('lab5/articles.html', error="Статья не найдена или недоступна")

        if request.method == 'GET':
            db_close(conn, cur)
            return render_template('lab5/edit_article.html', article=article)

        title = request.form.get('title', '').strip()
        article_text = request.form.get('article_text', '').strip()
        is_favorite = bool(request.form.get('is_favorite'))
        is_public = bool(request.form.get('is_public'))

        if not title or not article_text:
            db_close(conn, cur)
            return render_template('lab5/edit_article.html', article=article, error="Название и текст статьи не могут быть пустыми")

        if db_type == 'postgres':
            cur.execute("""
                UPDATE articles 
                SET title = %s, article_text = %s, is_favorite = %s, is_public = %s 
                WHERE id = %s AND user_id = %s;
            """, (title, article_text, is_favorite, is_public, article_id, user['id']))
        else:
            cur.execute("""
                UPDATE articles 
                SET title = ?, article_text = ?, is_favorite = ?, is_public = ? 
                WHERE id = ? AND user_id = ?;
            """, (title, article_text, is_favorite, is_public, article_id, user['id']))

        db_close(conn, cur)
        return redirect('/lab5/list')

    except Exception as e:
        db_close(conn, cur)
        print(f"Ошибка при редактировании статьи: {e}")
        return render_template('lab5/edit_article.html', article=article, error="Ошибка при сохранении статьи")

@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    if 'login' not in session:
        return redirect('/lab5/login')

    login = session['login']
    conn, cur = db_connect()
    try:
        db_type = os.environ.get('DB_TYPE', 'postgres')
        if db_type == 'postgres':
            cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login = ?;", (login,))
        user = cur.fetchone()
        if not user:
            db_close(conn, cur)
            return redirect('/lab5/login')

        if db_type == 'postgres':
            cur.execute("DELETE FROM articles WHERE id = %s AND user_id = %s;", (article_id, user['id']))
        else:
            cur.execute("DELETE FROM articles WHERE id = ? AND user_id = ?;", (article_id, user['id']))

        db_close(conn, cur)
        return redirect('/lab5/list')
    except Exception as e:
        db_close(conn, cur)
        print(f"Ошибка при удалении статьи: {e}")
        return redirect('/lab5/list')

@lab5.route('/lab5/users')
def users_list():
    conn, cur = db_connect()
    try:
        db_type = os.environ.get('DB_TYPE', 'postgres')
        if db_type == 'postgres':
            cur.execute("SELECT login, name FROM users ORDER BY login;")
        else:
            cur.execute("SELECT login, name FROM users ORDER BY login;")
        users = cur.fetchall()
        db_close(conn, cur)
        return render_template('lab5/users.html', users=users)
    except Exception as e:
        db_close(conn, cur)
        print(f"Ошибка загрузки пользователей: {e}")
        return render_template('lab5/users.html', error="Ошибка загрузки списка пользователей")
    
@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    if 'login' not in session:
        return redirect('/lab5/login')

    login = session['login']
    conn, cur = db_connect()
    try:
        db_type = os.environ.get('DB_TYPE', 'postgres')
        if db_type == 'postgres':
            cur.execute("SELECT id, name FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT id, name FROM users WHERE login = ?;", (login,))
        user = cur.fetchone()
        if not user:
            db_close(conn, cur)
            return redirect('/lab5/login')

        if request.method == 'GET':
            db_close(conn, cur)
            return render_template('lab5/profile.html', user=user)

        new_name = request.form.get('name', '').strip()
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_name != '':
            if db_type == 'postgres':
                cur.execute("UPDATE users SET name = %s WHERE id = %s;", (new_name, user['id']))
            else:
                cur.execute("UPDATE users SET name = ? WHERE id = ?;", (new_name, user['id']))

        if old_password or new_password or confirm_password:
            if not old_password:
                db_close(conn, cur)
                return render_template('lab5/profile.html', user=user, error="Введите текущий пароль")
            if not new_password or not confirm_password:
                db_close(conn, cur)
                return render_template('lab5/profile.html', user=user, error="Введите новый пароль и подтверждение")
            if new_password != confirm_password:
                db_close(conn, cur)
                return render_template('lab5/profile.html', user=user, error="Пароли не совпадают")

            if db_type == 'postgres':
                cur.execute("SELECT password FROM users WHERE id = %s;", (user['id'],))
            else:
                cur.execute("SELECT password FROM users WHERE id = ?;", (user['id'],))
            stored_hash = cur.fetchone()['password']
            if not check_password_hash(stored_hash, old_password):
                db_close(conn, cur)
                return render_template('lab5/profile.html', user=user, error="Неверный текущий пароль")

            new_hash = generate_password_hash(new_password)
            if db_type == 'postgres':
                cur.execute("UPDATE users SET password = %s WHERE id = %s;", (new_hash, user['id']))
            else:
                cur.execute("UPDATE users SET password = ? WHERE id = ?;", (new_hash, user['id']))

        db_close(conn, cur)
        return render_template('lab5/profile.html', user=user, success="Данные успешно обновлены")
    except Exception as e:
        db_close(conn, cur)
        print(f"Ошибка обновления профиля: {e}")
        return render_template('lab5/profile.html', user=user, error="Ошибка при сохранении")
    
@lab5.route('/lab5/public')
def public_articles():
    conn, cur = db_connect()
    try:
        db_type = os.environ.get('DB_TYPE', 'postgres')
        if db_type == 'postgres':
            cur.execute("""
                SELECT a.title, a.article_text, u.login 
                FROM articles a
                JOIN users u ON a.user_id = u.id
                WHERE a.is_public = TRUE
                ORDER BY a.id DESC;
            """)
        else:
            cur.execute("""
                SELECT a.title, a.article_text, u.login 
                FROM articles a
                JOIN users u ON a.user_id = u.id
                WHERE a.is_public = 1
                ORDER BY a.id DESC;
            """)
        articles = cur.fetchall()
        db_close(conn, cur)
        return render_template('lab5/public_articles.html', articles=articles)
    except Exception as e:
        db_close(conn, cur)
        print(f"Ошибка загрузки публичных статей: {e}")
        return render_template('lab5/public_articles.html', error="Ошибка загрузки")