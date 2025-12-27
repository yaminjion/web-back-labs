from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from db.models import users
from db import db
import random

lab9 = Blueprint('lab9', __name__)

# Подарки
BOXES = [f"у{i}.jpg" for i in range(1, 16)]
GIFTS = [f"п{i}.jpg" for i in range(1, 16)]

CONGRATULATIONS = [
    "С Новым годом! Пусть каждый день будет ярче солнца!",
    "Пусть в вашем доме всегда царит тепло и уют!",
    "Желаю вам исполнения всех заветных желаний!",
    "Пусть счастье постучится в вашу дверь и останется навсегда!",
    "Будьте здоровы, счастливы и окружены любовью!",
    "Пусть новый год принесёт вам удачу и вдохновение!",
    "Желаю вам море радости и океан вдохновения!",
    "Пусть все ваши мечты станут реальностью!",
    "Пусть каждый день будет наполнен смехом и добром!",
    "С праздником! Пусть всё будет прекрасно!",
    "Пусть удача идёт рядом, а радость — впереди!",
    "Желаю, чтобы в новом году всё задуманное сбылось!",
    "Пусть дом наполнится счастьем, а сердце — любовью!",
    "Пусть каждый новый день приносит повод для улыбки!",
    "С Новым Годом! Пусть он будет самым лучшим!"
]

PRIVATE_GIFT_INDICES = set(range(9, 14))  # п10–п14


def generate_positions():
    positions = []
    attempts = 50
    min_dist = 140
    w, h = 1120, 520
    for i in range(15):
        placed = False
        for _ in range(attempts):
            x = random.randint(40, w - 100)
            y = random.randint(40, h - 100)
            too_close = False
            for p in positions:
                px = p['x'] if isinstance(p, dict) else p[0]
                py = p['y'] if isinstance(p, dict) else p[1]
                if (px - x)**2 + (py - y)**2 < min_dist**2:
                    too_close = True
                    break
            if not too_close:
                positions.append({'x': x, 'y': y})
                placed = True
                break
        if not placed:
            positions.append({'x': 40 + (i % 5) * 200, 'y': 40 + (i // 5) * 180})
    return positions


# === АВТОРИЗАЦИЯ ===

@lab9.route('/lab9/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab9/login.html')
    login_val = request.form.get('login')
    password = request.form.get('password')
    if not login_val or not password:
        return render_template('lab9/login.html', error="Логин и пароль обязательны")
    
    user = users.query.filter_by(login=login_val).first()
    # Используем user.password (а не password_hash)
    if not user or not check_password_hash(user.password, password):
        return render_template('lab9/login.html', error="Неверный логин или пароль")
    
    login_user(user)
    return redirect('/lab9/')


@lab9.route('/lab9/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab9/register.html')
    login_val = request.form.get('login')
    password = request.form.get('password')
    repeat = request.form.get('repeat_password')
    if not login_val or not password or not repeat:
        return render_template('lab9/register.html', error="Все поля обязательны")
    if password != repeat:
        return render_template('lab9/register.html', error="Пароли не совпадают")
    if len(password) < 4:
        return render_template('lab9/register.html', error="Пароль ≥4 символов")
    if users.query.filter_by(login=login_val).first():
        return render_template('lab9/register.html', error="Логин занят")
    
    hashed = generate_password_hash(password)
    # Используем password (а не password_hash)
    new_user = users(login=login_val, password=hashed)
    db.session.add(new_user)
    db.session.commit()
    
    login_user(new_user)
    return redirect('/lab9/')


@lab9.route('/lab9/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab9/')


# === ПОДАРКИ ===

@lab9.route('/lab9/')
def main():
    raw_opened = session.get('opened_boxes', {})
    if isinstance(raw_opened, list):
        opened = {str(i): True for i in raw_opened}
    else:
        opened = raw_opened if isinstance(raw_opened, dict) else {}

    raw_positions = session.get('box_positions')
    if raw_positions is None:
        positions = generate_positions()
        session['box_positions'] = positions
    else:
        positions = []
        for p in raw_positions:
            if isinstance(p, (list, tuple)):
                positions.append({'x': p[0], 'y': p[1]})
            else:
                positions.append(p)

    boxes_data = []
    for i in range(15):
        boxes_data.append({
            'id': i,
            'image': BOXES[i],
            'is_opened': opened.get(str(i), False),
            'x': positions[i]['x'],
            'y': positions[i]['y']
        })

    opened_count = sum(opened.values())
    remaining_count = 15 - opened_count
    is_authenticated = current_user.is_authenticated

    session['opened_boxes'] = opened
    session['box_positions'] = positions
    session.modified = True

    return render_template(
        'lab9/index.html',
        boxes_data=boxes_data,
        gifts=GIFTS,
        opened_count=opened_count,
        remaining_count=remaining_count,
        is_authenticated=is_authenticated,
        current_user=current_user
    )


@lab9.route('/lab9/open_box', methods=['POST'])
def open_box():
    data = request.get_json()
    if not data or 'box_id' not in data:
        return jsonify({'success': False, 'message': 'Неверный запрос.'})

    try:
        box_id = int(data['box_id'])
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'Неверный ID.'})

    if not (0 <= box_id < 15):
        return jsonify({'success': False, 'message': 'Неверный номер коробки.'})

    raw = session.get('opened_boxes', {})
    if isinstance(raw, list):
        opened = {str(i): True for i in raw}
    else:
        opened = raw if isinstance(raw, dict) else {}

    if opened.get(str(box_id), False):
        return jsonify({'success': False, 'message': 'Коробка уже открыта!'})
    if sum(opened.values()) >= 3:
        return jsonify({'success': False, 'message': 'Можно открыть только 3 коробки!'})
    if box_id in PRIVATE_GIFT_INDICES and not current_user.is_authenticated:
        return jsonify({'success': False, 'message': 'Только для авторизованных!'})

    opened[str(box_id)] = True
    session['opened_boxes'] = opened
    session.modified = True

    return jsonify({
        'success': True,
        'congratulation': CONGRATULATIONS[box_id],
        'gift_image': GIFTS[box_id],
        'box_id': box_id,
        'opened_count': sum(opened.values())
    })


@lab9.route('/lab9/reset_boxes', methods=['POST'])
@login_required
def reset_boxes():
    session['opened_boxes'] = {}
    session.modified = True
    return jsonify({'success': True})