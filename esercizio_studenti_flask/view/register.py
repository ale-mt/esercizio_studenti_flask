from flask import render_template, flash, redirect, url_for, Blueprint, request
from esercizio_studenti_flask.forms import RegisterForm, RegisterStudentForm, ROLES
from esercizio_studenti_flask.model import Student, User, Role
from esercizio_studenti_flask import bcrypt, db
from flask_security import login_required, roles_accepted

register = Blueprint('register', __name__, template_folder='../templates', url_prefix='/register')


@register.route('/admin', methods=['POST', 'GET'])
@roles_accepted('admin', 'moderatore')
def admin():
    form = RegisterForm()

    if form.validate_on_submit():
        role = Role.query.filter_by(name='admin').first()
        role_2 = Role.query.filter_by(name='moderatore').first()

        # role_chose = dict(ROLES).get(form.pick_role.data)

        hashed_psw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_psw)

        if form.admin.data:
            if not role:
                role = Role(name='admin', description='admin')

            user.roles.append(role)

        if form.moderatore.data:
            if not role_2:
                role_2 = Role(name='moderatore', description='moderatore')

            user.roles.append(role_2)

        db.session.add(user)
        db.session.commit()
        flash(f'User {user.email} added', 'success')
        return redirect(url_for('home.home'))
    else:
        print(form.errors)
    return render_template('register.html', title='Register', form=form)


@register.route('/student', methods=['POST', 'GET'])
@roles_accepted('admin', 'moderatore')
def student():
    form = RegisterStudentForm()
    if form.validate_on_submit():
        student = Student(name=form.name.data, lastname=form.lastname.data, age=form.age.data, email=form.email.data)
        db.session.add(student)
        db.session.commit()
        flash(f'Student {student.name} {student.lastname} added!', 'success')
        return redirect(url_for('home.home'))
    return render_template('insert_student.html', title='Register', form=form)
