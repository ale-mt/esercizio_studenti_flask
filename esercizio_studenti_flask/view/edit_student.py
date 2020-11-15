from flask import render_template, Blueprint, request, flash, redirect, url_for
from esercizio_studenti_flask.forms import DeleteStudentForm
from esercizio_studenti_flask.model import Student
from esercizio_studenti_flask import db
from flask_login import login_required

edit_student = Blueprint('edit_student', __name__, template_folder='../templates', url_prefix='/edit')


@edit_student.route("/student/<int:student_id>", methods=['GET', 'POST'])
@login_required
def student(student_id=None):
    form = DeleteStudentForm()
    student = Student.query.filter_by(id=student_id).first()
    if request.method == 'POST':
        if form.delete.data:
            db.session.delete(student)
            db.session.commit()
            flash(f'Studente {student.name} {student.lastname} eliminato!', 'success')
            return redirect(url_for('home.home'))
        if form.validate_on_submit():
            student.name = form.name.data
            student.lastname = form.lastname.data
            student.age = form.age.data
            student.email = form.email.data
            db.session.commit()
            flash(f'Student {student.name} {student.lastname} edited!', 'success')
            return redirect(url_for('home.home'))
    if request.method == 'GET':
        return render_template('edit_student.html', title='Edit', form=form, student=student)



