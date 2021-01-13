from flask import render_template, flash, redirect, url_for, request, Blueprint
from esercizio_studenti_flask import bcrypt
from flask_security import login_user
import logging

from esercizio_studenti_flask.model import User


login_bp = Blueprint('login', __name__, template_folder='../templates')


@login_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        logging.info("login post request")
        email = request.form.get('email')
        pswd = request.form.get('pswd')

        print("dentro submit")

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, pswd):
            login_user(user)
            flash(f'You logged in as {user.email}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home.home'))
        else:
            flash('Login failed!', 'warning')

    return render_template('login.html', title='Login')
