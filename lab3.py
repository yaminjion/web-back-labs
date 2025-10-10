from flask import Blueprint, render_template, redirect, request, make_response
lab3 = Blueprint ('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    
    if name is None:
        name = "Аноним"
    
    if age is None:
        age = "не указан"
    
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response (redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response (redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user']='Заполните поле!'
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    # Пусть кофе стоит 120 рублей, чёрный чай – 80 рублей, зелёный – 70 рублей.
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70
    
    # Добавка молока удорожает напиток на 30 рублей, а сахара – на 10.
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    # Получаем параметры заказа и пересчитываем цену
    price = 0
    drink = request.args.get('drink')
    
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    elif drink == 'green-tea':
        price = 70
    
    # Добавки
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    font_style = request.args.get('font_style')
    
    if color or bg_color or font_size or font_style:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_style:
            resp.set_cookie('font_style', font_style)
        return resp

    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size')
    font_style = request.cookies.get('font_style')
    
    resp = make_response(render_template('lab3/settings.html', 
                                        color=color, 
                                        bg_color=bg_color, 
                                        font_size=font_size, 
                                        font_style=font_style))
    return resp


@lab3.route('/lab3/ticket')
def ticket():
    errors = {}
    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    linen = request.args.get('linen') == 'on'
    luggage = request.args.get('luggage') == 'on'
    age = request.args.get('age')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    travel_date = request.args.get('travel_date')
    insurance = request.args.get('insurance') == 'on'
    
    return render_template('lab3/ticket.html', 
                         fio=fio, shelf=shelf, linen=linen, luggage=luggage,
                         age=age, departure=departure, destination=destination,
                         travel_date=travel_date, insurance=insurance, errors=errors)

@lab3.route('/lab3/ticket_result')
def ticket_result():
    errors = {}
    
    # Получаем данные из формы
    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    linen = request.args.get('linen') == 'on'
    luggage = request.args.get('luggage') == 'on'
    age_str = request.args.get('age')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    travel_date = request.args.get('travel_date')
    insurance = request.args.get('insurance') == 'on'
    
    # Проверка на пустые поля
    if not fio:
        errors['fio'] = 'Заполните ФИО пассажира'
    if not shelf:
        errors['shelf'] = 'Выберите полку'
    if not age_str:
        errors['age'] = 'Заполните возраст'
    if not departure:
        errors['departure'] = 'Заполните пункт выезда'
    if not destination:
        errors['destination'] = 'Заполните пункт назначения'
    if not travel_date:
        errors['travel_date'] = 'Выберите дату поездки'
    
    # Проверка возраста
    if age_str:
        try:
            age = int(age_str)
            if age < 1 or age > 120:
                errors['age'] = 'Возраст должен быть от 1 до 120 лет'
        except ValueError:
            errors['age'] = 'Возраст должен быть числом'
    
    # Если есть ошибки, возвращаем к форме
    if errors:
        return render_template('lab3/ticket.html', 
                             fio=fio, shelf=shelf, linen=linen, luggage=luggage,
                             age=age_str, departure=departure, destination=destination,
                             travel_date=travel_date, insurance=insurance, errors=errors)
    
    age = int(age_str)
    
    # Расчет стоимости
    if age < 18:
        price = 700  # Детский билет
    else:
        price = 1000  # Взрослый билет
    
    # Доплаты
    if shelf in ['lower', 'lower-side']:
        price += 100  # Доплата за нижнюю полку
    
    if linen:
        price += 75  # Бельё
    
    if luggage:
        price += 250  # Багаж
    
    if insurance:
        price += 150  # Страховка
    
    return render_template('lab3/ticket_result.html',
                         fio=fio, shelf=shelf, linen=linen, luggage=luggage,
                         age=age, departure=departure, destination=destination,
                         travel_date=travel_date, insurance=insurance, price=price)


@lab3.route('/lab3/clear_settings')
def clear_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('font_style')
    return resp


@lab3.route('/lab3/products')
def products():
    # Список товаров (смартфоны)
    products_list = [
        {'name': 'iPhone 15 Pro', 'price': 120000, 'brand': 'Apple', 'color': 'Титановый', 'storage': '256GB'},
        {'name': 'Samsung Galaxy S24', 'price': 89990, 'brand': 'Samsung', 'color': 'Черный', 'storage': '256GB'},
        {'name': 'Xiaomi 14', 'price': 69990, 'brand': 'Xiaomi', 'color': 'Белый', 'storage': '256GB'},
        {'name': 'Google Pixel 8', 'price': 75990, 'brand': 'Google', 'color': 'Серый', 'storage': '128GB'},
        {'name': 'OnePlus 12', 'price': 64990, 'brand': 'OnePlus', 'color': 'Зеленый', 'storage': '256GB'},
        {'name': 'iPhone 14', 'price': 79990, 'brand': 'Apple', 'color': 'Синий', 'storage': '128GB'},
        {'name': 'Samsung Galaxy A54', 'price': 34990, 'brand': 'Samsung', 'color': 'Фиолетовый', 'storage': '128GB'},
        {'name': 'Xiaomi Redmi Note 13', 'price': 24990, 'brand': 'Xiaomi', 'color': 'Черный', 'storage': '128GB'},
        {'name': 'Realme 11 Pro', 'price': 29990, 'brand': 'Realme', 'color': 'Золотой', 'storage': '256GB'},
        {'name': 'Nothing Phone 2', 'price': 45990, 'brand': 'Nothing', 'color': 'Белый', 'storage': '256GB'},
        {'name': 'iPhone 15 Pro Max', 'price': 149000, 'brand': 'Apple', 'color': 'Синий', 'storage': '512GB'},
        {'name': 'Samsung Galaxy Z Flip5', 'price': 99990, 'brand': 'Samsung', 'color': 'Фиолетовый', 'storage': '256GB'},
        {'name': 'Google Pixel 7a', 'price': 44990, 'brand': 'Google', 'color': 'Голубой', 'storage': '128GB'},
        {'name': 'Xiaomi Poco X6 Pro', 'price': 32990, 'brand': 'Xiaomi', 'color': 'Желтый', 'storage': '256GB'},
        {'name': 'Asus ROG Phone 8', 'price': 89990, 'brand': 'Asus', 'color': 'Черный', 'storage': '256GB'},
        {'name': 'Vivo V29', 'price': 39990, 'brand': 'Vivo', 'color': 'Красный', 'storage': '256GB'},
        {'name': 'Oppo Find X6', 'price': 59990, 'brand': 'Oppo', 'color': 'Зеленый', 'storage': '256GB'},
        {'name': 'Honor Magic 5', 'price': 49990, 'brand': 'Honor', 'color': 'Синий', 'storage': '256GB'},
        {'name': 'Motorola Edge 40', 'price': 37990, 'brand': 'Motorola', 'color': 'Черный', 'storage': '256GB'},
        {'name': 'Nokia G42', 'price': 19990, 'brand': 'Nokia', 'color': 'Серый', 'storage': '128GB'}
    ]
    
    # Получаем цены из куки или используем значения из формы
    min_price_cookie = request.cookies.get('min_price')
    max_price_cookie = request.cookies.get('max_price')
    
    # Получаем параметры из GET-запроса
    min_price_input = request.args.get('min_price', '')
    max_price_input = request.args.get('max_price', '')
    
    # Определяем минимальную и максимальную цены для отображения
    if min_price_input != '':
        min_price = min_price_input
    elif min_price_cookie:
        min_price = min_price_cookie
    else:
        min_price = ''
    
    if max_price_input != '':
        max_price = max_price_input
    elif max_price_cookie:
        max_price = max_price_cookie
    else:
        max_price = ''
    
    # Рассчитываем общие минимальную и максимальную цены для плейсхолдеров
    all_prices = [product['price'] for product in products_list]
    overall_min_price = min(all_prices)
    overall_max_price = max(all_prices)
    
    # Фильтрация товаров
    filtered_products = products_list
    has_filter = False
    
    if min_price != '' or max_price != '':
        has_filter = True
        
        try:
            min_val = float(min_price) if min_price != '' else overall_min_price
            max_val = float(max_price) if max_price != '' else overall_max_price
            
            # Если пользователь перепутал мин и макс, меняем их местами
            if min_val > max_val:
                min_val, max_val = max_val, min_val
                min_price, max_price = str(max_val), str(min_val)
            
            filtered_products = [
                product for product in products_list
                if min_val <= product['price'] <= max_val
            ]
            
        except ValueError:
            # Если введены некорректные значения, показываем все товары
            filtered_products = products_list
    
    # Если нажата кнопка сброса
    if 'reset' in request.args:
        min_price = ''
        max_price = ''
        filtered_products = products_list
        has_filter = False
    
    # Подготавливаем ответ
    resp = make_response(render_template(
        'lab3/products.html',
        products=filtered_products,
        min_price=min_price,
        max_price=max_price,
        overall_min_price=overall_min_price,
        overall_max_price=overall_max_price,
        has_filter=has_filter,
        products_count=len(filtered_products)
    ))
    
    # Сохраняем значения в куки (если не сброс)
    if 'reset' not in request.args:
        if min_price != '':
            resp.set_cookie('min_price', min_price)
        else:
            resp.delete_cookie('min_price')
        
        if max_price != '':
            resp.set_cookie('max_price', max_price)
        else:
            resp.delete_cookie('max_price')
    else:
        # Очищаем куки при сбросе
        resp.delete_cookie('min_price')
        resp.delete_cookie('max_price')
    
    return resp