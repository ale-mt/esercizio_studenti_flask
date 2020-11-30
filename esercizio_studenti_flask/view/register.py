from flask import render_template, flash, redirect, url_for, Blueprint, request
from esercizio_studenti_flask.forms import RegisterForm, DeleteStudentForm, RegisterStudentForm, ROLES
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


@register.route('/student', defaults={"id": None})
@register.route('/student/<int:id>', methods=['POST', 'GET'])
@roles_accepted('admin', 'moderatore')
def student(id=None):
    if request.method == "POST":
        form = DeleteStudentForm()
        list_of_id = [(-1, 'No')]
        for student in Student.query.all():
            tupla = (student.id, f'Modifica studente con ID: {student.id}')
            list_of_id.append(tupla)

        print(list_of_id)

        form.id.choices = list_of_id

        student = Student.query.filter_by(id=id).first()

        if form.edit.data and form.validate():
            print("dentro edit")
            student = Student.query.filter_by(id=form.id.data).first()
            student.name = form.name.data
            student.lastname = form.lastname.data
            student.age = form.age.data
            student.email = form.email.data
            db.session.commit()
            flash(f'Student {student.email} {student.lastname} edited!', 'success')
            return redirect(url_for('home.home'))

        if form.submit.data and form.validate_on_submit():
            print("dentro submit")
            student = Student(name=form.name.data, lastname=form.lastname.data, age=form.age.data, email=form.email.data)
            db.session.add(student)
            db.session.commit()
            flash(f'Student {student.name} {student.lastname} added!', 'success')
            return redirect(url_for('home.home'))

        if form.delete.data and form.validate_on_submit():
            student = Student.query.filter_by(id=form.id.data).first()
            db.session.delete(student)
            db.session.commit()
            flash(f'Student {student.name} {student.lastname} Removed!', 'success')
            return redirect(url_for('home.home'))

    if request.method == "GET":

        form = DeleteStudentForm()
        list_of_id = [(-1, 'No')]
        for student in Student.query.all():
            tupla = (student.id, f'Modifica studente con ID: {student.id}')
            list_of_id.append(tupla)

        print(list_of_id)

        form.id.choices = list_of_id
        student = Student.query.filter_by(id=id).first()
        return render_template('insert_student.html', title='Register', form=form, student=student, student_id=id)
