from flask import render_template, flash, redirect, url_for, Blueprint
from esercizio_studenti_flask.forms import RegisterForm, RegisterStudentForm
from esercizio_studenti_flask.model import Student, User
from esercizio_studenti_flask import bcrypt, db
from flask_login import login_required

register = Blueprint('register', __name__, template_folder='../templates', url_prefix='/register')


@register.route('/admin', methods=['POST', 'GET'])
@login_required
def admin():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_psw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, password=hashed_psw)
        db.session.add(user)
        db.session.commit()
        flash(f'Privileged user {user.name} added', 'success')
        return redirect(url_for('home.home'))
    return render_template('register.html', title='Register', form=form)
# suddividere per post e get


@register.route('/student', methods=['POST', 'GET'])
@login_required
def student():
    form = RegisterStudentForm()
    if form.validate_on_submit():
        student = Student(name=form.name.data, lastname=form.lastname.data, age=form.age.data, email=form.email.data)
        db.session.add(student)
        db.session.commit()
        flash(f'Student {student.name} {student.lastname} added!', 'success')
        return redirect(url_for('home.home'))
    return render_template('insert_student.html', title='Register', form=form)
