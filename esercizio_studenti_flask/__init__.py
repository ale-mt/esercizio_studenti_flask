from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_security import Security, SQLAlchemyUserDatastore
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:merlino@172.17.0.2/flask_mysql'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:merlino@localhost:4000/flask_mysql'
app.config['SECRET_KEY'] = '2e5d0b485deec8c0b7e530611f7b492a'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login.login'
login_manager.login_message_category = 'info'

logging.basicConfig(filename='./esercizio_studenti_flask/log/api.log', level=logging.INFO)

from esercizio_studenti_flask.view.register import register
from esercizio_studenti_flask.view.home import home_bp
from esercizio_studenti_flask.view.login import login_bp
from esercizio_studenti_flask.view.logout import logout_bp
from esercizio_studenti_flask.view.manage import manage_bp
from esercizio_studenti_flask.view.api_get import api_get_bp
from esercizio_studenti_flask.view.api_post import api_post_bp
from esercizio_studenti_flask.view.api_put import api_put_bp
from esercizio_studenti_flask.view.api_delete import api_delete_bp


app.register_blueprint(register)
app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(manage_bp)
app.register_blueprint(api_get_bp)
app.register_blueprint(api_post_bp)
app.register_blueprint(api_put_bp)
app.register_blueprint(api_delete_bp)



from esercizio_studenti_flask.model import User, Role, Student

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.route('/update', methods=['POST'])
def update():
    student = Student.query.filter_by(id=request.form['id']).first()
    print('dentro update')
    db.session.delete(student)
    db.session.commit()
    return jsonify(student_id=student.id, student_name=student.name)


@app.route('/display', methods=['GET'])
def display():
    student = Student.query.first()
    return student.name

