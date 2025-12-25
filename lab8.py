from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash
from db import db
from db.models import users, articles

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
    
    return redirect('/lab8/')