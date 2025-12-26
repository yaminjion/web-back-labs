# lab9.py

from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required, current_user
import random

lab9 = Blueprint('lab9', __name__)

TOTAL_BOXES = 15

BOXES = [f'у{i}.jpg' for i in range(1, TOTAL_BOXES + 1)]
GIFTS = [f'п{i}.jpg' for i in range(1, TOTAL_BOXES + 1)]

CONGRATULATIONS = [
    "С Новым Годом! Пусть всё будет лучше!",
    "Пусть в новом году сбудутся все мечты!",
    "Желаю здоровья, радости и удачи!",
    "Пусть каждый день приносит только хорошее!",
    "Будьте счастливы, любите и будьте любимы!",
    "Пусть ваш дом всегда будет полон тепла и уюта!",
    "Пусть деньги текут рекой, а проблемы — в сторону!",
    "Желаю вам мира, добра и исполнения желаний!",
    "Пусть новый год принесёт вам успех и вдохновение!",
    "Пусть ваша жизнь будет яркой, как новогодняя ёлка!",
    "Желаю вам крепкого здоровья и отличного настроения!",
    "Пусть каждый день начинается с улыбки!",
    "Пусть рядом будут только добрые люди!",
    "Желаю вам много приятных сюрпризов!",
    "Пусть ваш год будет наполнен светом и любовью!"
]

# Подарки 10–14 (индексы 9–13) — только для авторизованных
PRIVATE_GIFT_INDICES = set(range(9, 14))


@lab9.route('/lab9/')
def main():
    if 'opened_boxes' not in session:
        session['opened_boxes'] = []
    if 'box_positions' not in session:
        positions = []
        for _ in range(TOTAL_BOXES):
            x = random.randint(50, 1200)
            y = random.randint(100, 600)
            positions.append((x, y))
        session['box_positions'] = positions

    box_data = []
    for i in range(TOTAL_BOXES):
        box_data.append({
            'name': BOXES[i],
            'x': session['box_positions'][i][0],
            'y': session['box_positions'][i][1],
            'index': i,
            'is_opened': i in session['opened_boxes']
        })

    remaining = TOTAL_BOXES - len(session['opened_boxes'])
    is_authenticated = current_user.is_authenticated

    return render_template('lab9/index.html',
                           box_data=box_data,
                           remaining=remaining,
                           is_authenticated=is_authenticated)


@lab9.route('/lab9/open_box', methods=['POST'])
def open_box():
    box_index = int(request.json.get('index'))

    if box_index in session['opened_boxes']:
        return jsonify({'status': 'already_opened'})

    if len(session['opened_boxes']) >= 3:
        return jsonify({'status': 'limit_reached'})

    if box_index in PRIVATE_GIFT_INDICES and not current_user.is_authenticated:
        return jsonify({'status': 'auth_required'})

    session['opened_boxes'].append(box_index)
    session.modified = True

    return jsonify({
        'status': 'success',
        'gift_image': GIFTS[box_index],
        'congratulation': CONGRATULATIONS[box_index],
        'remaining': TOTAL_BOXES - len(session['opened_boxes'])
    })


@lab9.route('/lab9/reset_boxes', methods=['POST'])
@login_required
def reset_boxes():
    session['opened_boxes'] = []
    session.modified = True
    return jsonify({'status': 'reset_success'})