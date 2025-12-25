from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from db import db
from db.models import users, articles as Article
from sqlalchemy import or_, func

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
        return render_template('lab8/register.html', error="Все поля обязательны", login=login)
    
    if password != repeat_password:
        return render_template('lab8/register.html', error="Пароли не совпадают", login=login)
    
    if users.query.filter_by(login=login).first():
        return render_template('lab8/register.html', error="Такой логин уже существует", login=login)
    
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
    if not user or not check_password_hash(user.password, password):
        return render_template('lab8/login.html', error="Неверный логин или пароль")
    
    login_user(user)  
    return redirect('/lab8/')

@lab8.route('/lab8/logout')
def logout():
    logout_user()
    return redirect('/lab8/')

@lab8.route('/lab8/articles')
@login_required
def articles():
    user_articles = Article.query.filter_by(user_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=user_articles)

@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')
    
    title = request.form.get('title', '').strip()
    text = request.form.get('article_text', '').strip()
    is_favorite = bool(request.form.get('is_favorite'))
    is_public = bool(request.form.get('is_public'))

    if not title or not text:
        return render_template('lab8/create.html', error="Заголовок и текст обязательны")
    
    new_article = Article(
        user_id=current_user.id,
        title=title,
        article_text=text,
        is_favorite=is_favorite,
        is_public=is_public,
        likes=0
    )
    db.session.add(new_article)
    db.session.commit()
    return redirect('/lab8/articles')

@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = Article.query.filter_by(id=article_id, user_id=current_user.id).first()
    if not article:
        return redirect('/lab8/articles')
    
    if request.method == 'GET':
        return render_template('lab8/edit.html', article=article)
    
    title = request.form.get('title', '').strip()
    text = request.form.get('article_text', '').strip()
    is_favorite = bool(request.form.get('is_favorite'))
    is_public = bool(request.form.get('is_public'))

    if not title or not text:
        return render_template('lab8/edit.html', article=article, error="Заголовок и текст обязательны")
    
    article.title = title
    article.article_text = text
    article.is_favorite = is_favorite
    article.is_public = is_public
    db.session.commit()
    return redirect('/lab8/articles')

@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = Article.query.filter_by(id=article_id, user_id=current_user.id).first()
    if article:
        db.session.delete(article)
        db.session.commit()
    return redirect('/lab8/articles')

@lab8.route('/lab8/public')
def public_articles():
    public_arts = Article.query.filter_by(is_public=True).all()
    return render_template('lab8/public.html', articles=public_arts)

@lab8.route('/lab8/search')
def search_articles():
    query = request.args.get('q', '').strip()
    if not query:
        return render_template('lab8/search.html', articles=[], query='')

    public = Article.query.filter(
        Article.is_public == True,
        or_(
            func.lower(Article.title).like(f"%{query.lower()}%"),
            func.lower(Article.article_text).like(f"%{query.lower()}%")
        )
    )

    if current_user.is_authenticated:
        own = Article.query.filter(
            Article.user_id == current_user.id,
            or_(
                func.lower(Article.title).like(f"%{query.lower()}%"),
                func.lower(Article.article_text).like(f"%{query.lower()}%")
            )
        )
        results = public.union(own).all()
    else:
        results = public.all()

    return render_template('lab8/search.html', articles=results, query=query)