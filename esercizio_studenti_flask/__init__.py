from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_security import Security, SQLAlchemyUserDatastore
import logging
import os

from flask_cors import CORS

try:
    db_host = os.environ['MYSQL_HOST']
except:
    print("MYSQL_HOST env not found, using 172.17.0.4")
    db_host = "172.17.0.4"
    
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:merlino@{db_host}/flask_mysql'
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

