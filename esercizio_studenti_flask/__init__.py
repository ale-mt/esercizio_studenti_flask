from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:merlino@localhost:4000/flask_mysql'
app.config['SECRET_KEY'] = '2e5d0b485deec8c0b7e530611f7b492a'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login.login'
login_manager.login_message_category = 'info'


from esercizio_studenti_flask.view.register import register
from esercizio_studenti_flask.view.home import home_bp
from esercizio_studenti_flask.view.login import login_bp

from esercizio_studenti_flask.view.logout import logout_bp
from esercizio_studenti_flask.view.edit import edit

app.register_blueprint(register)
app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(edit)








from esercizio_studenti_flask.model import User, Role

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
