from flask import render_template, Blueprint
from esercizio_studenti_flask.model import Student, User
from flask_security import roles_required

manage_bp = Blueprint('manage', __name__, template_folder='../templates')


@manage_bp.route('/manage')
# @roles_required('admin')
def manage():
    students = Student.query.all()
    return render_template('manage.html', title='Manage', students=students)


