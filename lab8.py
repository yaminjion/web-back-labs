from flask import Blueprint, render_template

lab8 = Blueprint('lab8', __name__, template_folder='templates')

@lab8.route('/lab8/')
def lab8_index():
    return render_template('lab8/lab8.html')