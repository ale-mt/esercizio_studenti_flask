from flask import render_template, Blueprint
from esercizio_studenti_flask.model import Student, User
from flask_security import login_required

home_bp = Blueprint('home', __name__, template_folder='../templates')


@home_bp.route('/')
@home_bp.route('/home')
@login_required
def home():
    students = Student.query.all()
    admins = User.query.all()
    return render_template('home.html', title='Home', students=students, users=admins)


