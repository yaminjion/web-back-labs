from flask import Blueprint, render_template, jsonify, request

lab7 = Blueprint('lab7', __name__)

# Список фильмов
films = [
    {
        "title": "Interstellar",
        "title_ru": "Интерстеллар", 
        "year": 2014,
        "description": "Когда засуха, пыльные бури и вымирание растений приводят человечество к продовольственному кризису, коллектив исследователей и учёных отправляется сквозь червоточину в путешествие, чтобы превзойти прежние ограничения для космических путешествий человека и найти планету с подходящими для человечества условиями."
    },
    {
        "title": "The Shawshank Redemption",
        "title_ru": "Побег из Шоушенка",
        "year": 1994,
        "description": "Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника. Оказавшись в тюрьме под названием Шоушенк, он сталкивается с жестокостью и беззаконием, царящим по обе стороны решётки. Каждый, кто попадает в эти стены, становится их рабом до конца жизни."
    },
    {
        "title": "The Green Mile",
        "title_ru": "Зеленая миля", 
        "year": 1999,
        "description": "Пол Эджкомб — начальник блока смертников в тюрьме «Холодная гора». В его жизни появляется Джон Коффи, обвинённый в страшном преступлении."
    },
    {
        "title": "Fight Club",
        "title_ru": "Бойцовский клуб",
        "year": 1999, 
        "description": "Страховой сотрудник встречает загадочного торговца мылом Тайлера Дёрдена и вместе они создают подпольный бойцовский клуб."
    },
    {
        "title": "Léon",
        "title_ru": "Леон",
        "year": 1994,
        "description": "Профессиональный убийца Леон неожиданно становится наставником юной Матильды, чья семья погибает от рук коррумпированного полицейского."
    }
]

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

# REST API для получения всех фильмов
@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)

# REST API для получения конкретного фильма по ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        return {"error": "Фильм не найден"}, 404
    return jsonify(films[id])

# REST API для удаления фильма по ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        return {"error": "Фильм не найден"}, 404
    del films[id]
    return '', 204

# REST API для добавления нового фильма
@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    data = request.get_json()
    
    # Преобразуем все значения к строке
    title_ru = str(data.get('title_ru', '')).strip()
    description = str(data.get('description', '')).strip()
    title = str(data.get('title', '')).strip()
    
    # ВАЖНО: если title пустое, используем title_ru
    if not title:
        title = title_ru
    
    # Проверяем обязательные поля
    if not title_ru:
        return {"title_ru": "Заполните русское название"}, 400
    if not description:
        return {"description": "Заполните описание"}, 400
    
    year = 0
    try:
        year = int(data.get('year', 0))
    except (TypeError, ValueError):
        pass
    
    new_film = {
        "title": title,  # Здесь будет либо введенное title, либо title_ru
        "title_ru": title_ru,
        "year": year,
        "description": description
    }
    
    films.append(new_film)
    return jsonify({"id": len(films) - 1}), 201


# REST API для редактирования фильма по ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        return {"error": "Фильм не найден"}, 404

    data = request.get_json()
    if not isinstance(data, dict):
        return {"error": "Неверный формат данных"}, 400

    title_ru = str(data.get('title_ru', '')).strip()
    description = str(data.get('description', '')).strip()
    title = str(data.get('title', '')).strip()

    if not title_ru:
        return {"title_ru": "Заполните русское название"}, 400
    if not description:
        return {"description": "Заполните описание"}, 400

    if not title:
        title = title_ru

    year = 0
    try:
        year = int(data.get('year', 0))
    except (TypeError, ValueError):
        pass

    films[id] = {
        "title": title,
        "title_ru": title_ru,
        "year": year,
        "description": description
    }
    return jsonify(films[id])