from flask import Blueprint, render_template, request, redirect, url_for, session
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html',error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    if x2 == 0:
        return render_template('lab4/div.html',error='На ноль делить нельзя!')
    result = x1/x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


# Суммирование
@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')


@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    x1 = int(x1) if x1 != '' else 0
    x2 = int(x2) if x2 != '' else 0
    
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


# Вычитание
@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')


@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


# Умножение
@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')

@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    x1 = int(x1) if x1 != '' else 1
    x2 = int(x2) if x2 != '' else 1
    
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)


# Возведение в степень
@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')


@lab4.route('/lab4/pow', methods=['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    
    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='Ошибка: 0 в степени 0 не определено!')
    
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)


tree_count = 0
MAX_TREES = 10  

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    
    if request.method == 'GET':
        return render_template('lab4/tree.html', 
                             tree_count=tree_count, 
                             max_trees=MAX_TREES)

    operation = request.form.get('operation')

    if operation == 'cut':
        if tree_count > 0:
            tree_count -= 1
    elif operation == 'plant':
        if tree_count < MAX_TREES:
            tree_count += 1
    
    return redirect(url_for('lab4.tree'))


users = [
    {"login": 'alex', 'password': '123', "name": "Алексей Петров", "gender": "male"},
    {"login": 'bob', 'password': '555', "name": "Борис Иванов", "gender": "male"},
    {"login": 'maria', 'password': '789', "name": "Мария Сидорова", "gender": "female"},
    {"login": 'admin', 'password': 'admin123', "name": "Администратор", "gender": "male"},
    {"login": 'lena', 'password': '777', "name": "Елена Минько", "gender": "female"},
]

def get_current_user():
    login = session.get('login')
    if not login:
        return None
    for user in users:
        if user['login'] == login:
            return user
    session.clear()  
    return None

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            user_name = session.get('user_name', '')
            return render_template('lab4/login.html', authorized=True, user_name=user_name, login_value='')
        else:
            return render_template('lab4/login.html', authorized=False, login_value='')

    login_input = request.form.get('login')
    password = request.form.get('password')

    if not login_input:
        return render_template('lab4/login.html', error="Не введён логин", authorized=False, login_value='')

    if not password:
        return render_template('lab4/login.html', error="Не введён пароль", authorized=False, login_value='')

    for user in users:
        if login_input == user['login'] and password == user['password']:
            session['login'] = login_input
            session['user_name'] = user['name']
            return redirect(url_for('lab4.login'))

    return render_template('lab4/login.html', error="Неверные логин и/или пароль", authorized=False, login_value='')

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    session.pop('user_name', None)
    return redirect(url_for('lab4.login'))


@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab4/register.html')

    login = request.form.get('login', '').strip()
    name = request.form.get('name', '').strip()
    password = request.form.get('password', '')
    confirm = request.form.get('confirm', '')


    if not login:
        return render_template('lab4/register.html', error="Логин не может быть пустым")
    if not name:
        return render_template('lab4/register.html', error="Имя не может быть пустым")
    if not password:
        return render_template('lab4/register.html', error="Пароль не может быть пустым")
    if password != confirm:
        return render_template('lab4/register.html', error="Пароли не совпадают")

    for user in users:
        if user['login'] == login:
            return render_template('lab4/register.html', error="Пользователь с таким логином уже существует")


    users.append({
        "login": login,
        "password": password,
        "name": name,
        "gender": "unknown"  
    })

    return redirect(url_for('lab4.login'))


@lab4.route('/lab4/users')
def users_list():
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for('lab4.login'))

    return render_template('lab4/users.html', users=users, current_login=current_user['login'])


@lab4.route('/lab4/edit', methods=['GET', 'POST'])
def edit_profile():
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for('lab4.login'))

    if request.method == 'GET':
        return render_template('lab4/edit.html', user=current_user)


    new_login = request.form.get('login', '').strip()
    name = request.form.get('name', '').strip()
    password = request.form.get('password', '')
    confirm = request.form.get('confirm', '')


    if not new_login:
        return render_template('lab4/edit.html', user=current_user, error="Логин не может быть пустым")
    if not name:
        return render_template('lab4/edit.html', user=current_user, error="Имя не может быть пустым")


    for user in users:
        if user['login'] == new_login and user['login'] != current_user['login']:
            return render_template('lab4/edit.html', user=current_user, error="Логин уже занят")


    if password or confirm:
        if password != confirm:
            return render_template('lab4/edit.html', user=current_user, error="Пароли не совпадают")
        current_user['password'] = password


    current_user['login'] = new_login
    current_user['name'] = name


    session['login'] = new_login
    session['user_name'] = name

    return redirect(url_for('lab4.users_list'))

@lab4.route('/lab4/delete', methods=['POST'])
def delete_self():
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for('lab4.login'))

    global users
    users = [u for u in users if u['login'] != current_user['login']]
    session.clear()
    return redirect(url_for('lab4.login'))

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    temp_value = '' 
    if request.method == 'POST':
        temp_value = request.form.get('temperature', '').strip()

        if temp_value == '':
            return render_template('lab4/fridge.html',
                                   error="ошибка: не задана температура",
                                   temp_value=temp_value)

        try:
            temp = float(temp_value)
        except ValueError:
            return render_template('lab4/fridge.html',
                                   error="ошибка: температура должна быть числом",
                                   temp_value=temp_value)


        if temp < -12:
            return render_template('lab4/fridge.html',
                                   error="не удалось установить температуру — слишком низкое значение",
                                   temp_value=temp_value)

        if temp > -1:
            return render_template('lab4/fridge.html',
                                   error="не удалось установить температуру — слишком высокое значение",
                                   temp_value=temp_value)

        if -12 <= temp <= -9:
            snowflakes = "❄❄❄"
        elif -9 <= temp <= -5:
            snowflakes = "❄❄"
        elif -5 <= temp <= -1:
            snowflakes = "❄"

        message = f"Установлена температура: {temp}°С"
        return render_template('lab4/fridge.html',
                               message=message,
                               snowflakes=snowflakes,
                               temp_value=temp_value)

    return render_template('lab4/fridge.html', temp_value=temp_value)

@lab4.route('/lab4/grain_order', methods=['GET', 'POST'])
def grain_order():

    PRICES = {
        'barley': 12000,   
        'oats': 8500,      
        'wheat': 9000,     
        'rye': 15000       
    }


    GRAIN_NAMES = {
        'barley': 'ячмень',
        'oats': 'овёс',
        'wheat': 'пшеница',
        'rye': 'рожь'
    }

    selected_grain = ''
    weight_value = ''

    if request.method == 'GET':
        return render_template('lab4/grain_order.html', 
                               grains=GRAIN_NAMES,
                               selected_grain=selected_grain,
                               weight_value=weight_value)


    selected_grain = request.form.get('grain', '')
    weight_value = request.form.get('weight', '').strip()

    if not selected_grain or selected_grain not in PRICES:
        return render_template('lab4/grain_order.html',
                               error="Пожалуйста, выберите тип зерна",
                               grains=GRAIN_NAMES,
                               selected_grain=selected_grain,
                               weight_value=weight_value)


    if weight_value == '':
        return render_template('lab4/grain_order.html',
                               error="Вес не был указан",
                               grains=GRAIN_NAMES,
                               selected_grain=selected_grain,
                               weight_value=weight_value)


    try:
        weight = float(weight_value)
    except ValueError:
        return render_template('lab4/grain_order.html',
                               error="Вес должен быть числом",
                               grains=GRAIN_NAMES,
                               selected_grain=selected_grain,
                               weight_value=weight_value)

    if weight <= 0:
        return render_template('lab4/grain_order.html',
                               error="Вес должен быть больше 0",
                               grains=GRAIN_NAMES,
                               selected_grain=selected_grain,
                               weight_value=weight_value)

    if weight > 100:
        return render_template('lab4/grain_order.html',
                               error="Такого объёма сейчас нет в наличии",
                               grains=GRAIN_NAMES,
                               selected_grain=selected_grain,
                               weight_value=weight_value)


    price_per_ton = PRICES[selected_grain]
    total = weight * price_per_ton
    discount_applied = False
    discount_amount = 0


    if weight > 10:
        discount_applied = True
        discount_amount = total * 0.10
        total -= discount_amount

    grain_name = GRAIN_NAMES[selected_grain]
    success_message = f"Заказ успешно сформирован. Вы заказали {grain_name}. Вес: {weight} т. Сумма к оплате: {total:,.2f} руб.".replace(',', ' ')

    return render_template('lab4/grain_order.html',
                           success_message=success_message,
                           discount_applied=discount_applied,
                           discount_amount=discount_amount,
                           grains=GRAIN_NAMES,
                           selected_grain=selected_grain,
                           weight_value=weight_value)

