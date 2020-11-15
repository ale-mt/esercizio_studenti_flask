from flask import render_template, Blueprint, request, flash, redirect, url_for
from esercizio_studenti_flask.forms import DeleteStudentForm, DeleteUserForm, ROLES
from esercizio_studenti_flask.model import Student, User, Role, roles_users
from esercizio_studenti_flask import db
from flask_security import roles_required, login_required, roles_accepted

edit = Blueprint('edit', __name__, template_folder='../templates', url_prefix='/edit')


@edit.route("/student/<int:student_id>", methods=['GET', 'POST'])
@roles_accepted('admin')
def student(student_id=None):
    form = DeleteStudentForm()
    student = Student.query.filter_by(id=student_id).first()
    # if request.method == 'POST' --> mi va in errore la validazione
    if form.delete.data:
        db.session.delete(student)
        db.session.commit()
        flash(f'Studente {student.email} {student.lastname} eliminato!', 'success')
        return redirect(url_for('home.home'))

    if form.validate_on_submit():
        student.email = form.name.data
        student.lastname = form.lastname.data
        student.age = form.age.data
        student.email = form.email.data
        db.session.commit()
        flash(f'Student {student.email} {student.lastname} edited!', 'success')
        return redirect(url_for('home.home'))
    # if request.method == 'GET' --> mi va in errore la validazione
    return render_template('edit_student.html', title='Edit', form=form, student=student)



@edit.route("/user/<int:user_id>", methods=['GET', 'POST'])
@roles_required('admin')
def user(user_id=None):
    form = DeleteUserForm()
    user_db = User.query.filter_by(id=user_id).first()



    if form.delete.data:
        for err in form.email.errors:
            print(err)
        db.session.delete(user_db)
        db.session.commit()
        flash(f'User {user_db.email} eliminato!', 'success')
        return redirect(url_for('home.home'))

    if form.validate_on_submit():
        role = Role.query.filter_by(name='admin').first()
        role_2 = Role.query.filter_by(name='moderatore').first()

        user_db.roles = []
        db.session.commit()

        if form.admin.data:
            if not role:
                role = Role(name='admin', description='admin')

            user_db.roles.append(role)

        if form.moderatore.data:
            if not role_2:
                role_2 = Role(name='moderatore', description='moderatore')

            user_db.roles.append(role_2)

        user_db.email = form.email.data
        db.session.commit()
        flash(f'User {user_db.email} edited!', 'success')
        return redirect(url_for('home.home'))

    return render_template('edit_user.html', title='Edit', form=form, user=user_db)



