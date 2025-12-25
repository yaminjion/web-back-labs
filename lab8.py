from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash
from db import db
from db.models import users, articles
from werkzeug.security import check_password_hash
from flask_login import login_required
from flask_login import login_user, logout_user, login_required

lab8 = Blueprint('lab8', __name__, template_folder='templates')

@lab8.route('/lab8/')
def lab8_index():
    return render_template('lab8/lab8.html')

@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    repeat_password = request.form.get('repeat_password')
    
    if not login or not password or not repeat_password:
        return render_template('lab8/register.html', 
                               error="Все поля обязательны", 
                               login=login)
    
    if password != repeat_password:
        return render_template('lab8/register.html', 
                               error="Пароли не совпадают", 
                               login=login)
    
    if users.query.filter_by(login=login).first():
        return render_template('lab8/register.html', 
                               error="Такой логин уже существует", 
                               login=login)
    
    hashed = generate_password_hash(password)
    new_user = users(login=login, password=hashed)
    
    db.session.add(new_user)
    db.session.commit()
    
    login_user(new_user)
    
    return redirect('/lab8/')


@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_str = request.form.get('login')
    password = request.form.get('password')
    
    if not login_str or not password:
        return render_template('lab8/login.html', error="Заполните все поля")
    
    user = users.query.filter_by(login=login_str).first()
    if not user:
        return render_template('lab8/login.html', error="Пользователь не найден")
    
    if not check_password_hash(user.password, password):
        return render_template('lab8/login.html', error="Неверный пароль")
    
    login_user(user) 
    return redirect('/lab8/')

@lab8.route('/lab8/articles')
@login_required
def articles():
    return "Список статей"

@lab8.route('/lab8/logout')
def logout():
    logout_user()
    return redirect('/lab8/')