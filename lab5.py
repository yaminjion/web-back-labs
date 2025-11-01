from flask import Blueprint, render_template, request, redirect, url_for, session
lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html')