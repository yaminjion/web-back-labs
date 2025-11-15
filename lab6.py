from flask import Blueprint, request, jsonify, session, render_template

lab6 = Blueprint('lab6', __name__, template_folder='templates')

offices = [{"number": i, "tenant": None} for i in range(1, 11)]

@lab6.route('/lab6/')
def lab6_main():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.get_json()
    method = data.get('method')
    params = data.get('params')
    req_id = data.get('id')

    if method == 'info':
        return jsonify({
            'jsonrpc': '2.0',
            'result': offices,
            'id': req_id
        })

    elif method == 'booking':
        if 'login' not in session:
            return jsonify({
                'jsonrpc': '2.0',
                'error': {'code': 1, 'message': 'Пользователь не авторизован'},
                'id': req_id
            })

        office_number = params
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] is not None:
                    return jsonify({
                        'jsonrpc': '2.0',
                        'error': {'code': 2, 'message': 'Офис уже занят'},
                        'id': req_id
                    })
                office['tenant'] = session['login']
                return jsonify({
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': req_id
                })
        # Неверный номер офиса
        return jsonify({
            'jsonrpc': '2.0',
            'error': {'code': -32602, 'message': 'Неверный номер офиса'},
            'id': req_id
        })

    elif method == 'cancellation':
        office_number = params
        for office in offices:
            if office['number'] == office_number:
                office['tenant'] = None
                return jsonify({
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': req_id
                })
        return jsonify({
            'jsonrpc': '2.0',
            'error': {'code': -32602, 'message': 'Неверный номер офиса'},
            'id': req_id
        })

    else:
        # Метод не найден
        return jsonify({
            'jsonrpc': '2.0',
            'error': {'code': -32601, 'message': 'Метод не найден'},
            'id': req_id
        })