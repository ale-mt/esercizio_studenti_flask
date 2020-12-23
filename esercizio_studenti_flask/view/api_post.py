from flask import Blueprint, json, make_response, flash, request, jsonify
from esercizio_studenti_flask.model import Student, User, Role
from esercizio_studenti_flask import bcrypt, db
from customException import FormValidation
import re, logging
from flask_security import roles_accepted


api_post_bp = Blueprint('post', __name__, url_prefix='/api/')

# regex per mail
regex = '^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$'
# for custom mails use: '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'


def check(email):
    if re.search(regex, email):
        logging.info("Regex Valid Email")
        return True
    else:
        logging.error("Regex Invalid Email")
        raise FormValidation(error='Email non valida', target=['email'])


def validate(student_dict):
    def validate_email():
        check(student_dict.get('email'))
        student_bymail = Student.query.filter_by(email=student_dict.get('email')).first()
        logging.info(f'student by mail {student_bymail}')

        if student_bymail:
            msg = "Email in uso da un altro studente"
            target_list = ['email']
            logging.error(msg)
            raise FormValidation(error=msg, target=target_list)
        else:
            return True

    # nessun campo deve essere vuoto
    if student_dict.get('name') and student_dict.get('lastname') and student_dict.get('age') and student_dict.get('email'):
        validate_email()
        if 18 > int(student_dict['age']) or int(student_dict['age']) > 100:
            msg = "Eta' non valida"
            raise FormValidation(error=msg, target=['age'])
        else:
            logging.info("validato")
            return True
    else:
        msg = "Campo vuoto"
        logging.error(msg)
        target_list = []
        s1 = Student()
        for key in s1.as_dict():
            if not student_dict.get(key):
                target_list.append(key)  # lista dei campi vuoti da segnalare

        raise FormValidation(error=msg, target=target_list)


def validate_user(user_dict):
    def validate_email():
        check(user_dict.get('email'))
        user_bymail = User.query.filter_by(email=user_dict.get('email')).first()
        logging.info(f'user by mail {user_bymail}')
        if user_bymail:
            msg = "Email in uso da un altro utente"
            target_list = ['email']
            raise FormValidation(error=msg, target=target_list)
        else:
            return True

    if 'ruoli' in user_dict:
        if type(user_dict['ruoli']) is not list:
            msg = "Campo ruoli non valido"
            raise FormValidation(error=msg, target=['ruoli'])
        else:
            for ruolo in user_dict['ruoli']:
                if ruolo != "admin" and ruolo != "moderatore":
                    msg = f"Ruolo {ruolo} non valido. Ruoli validi ['moderatore', 'admin']"
                    raise FormValidation(error=msg, target=['ruoli'])

    # nessun campo deve essere vuoto
    if user_dict.get('email') and user_dict.get('password') and user_dict.get('confirm_password') and ("ruoli" in user_dict):
        validate_email()

        if user_dict['password'] == user_dict['confirm_password']:
            logging.info("validato")
            return True
        else:
            msg = "Le password non corrispondono"
            target_list = ['password', 'confirm_password']
            logging.error(msg)
            raise FormValidation(error=msg, target=target_list)
    else:
        msg = "Campo vuoto"
        logging.error(msg)
        u1 = User()

        # 2 modi per filtrare i campi necessari
        # due liste + list comprehension
        not_list = ["id", "active", "confirmed_at"]
        target_list = [key for key in u1.as_dict() if not user_dict.get(key) and key not in not_list]

        # due set + intersezione tra set A-B
        # not_necessary_fields = {"id", "active", "confirmed_at"} # set di campi non necessari per la validazione
        # target_list = set(target_list) # set di campi che comprende sia quelli necessari sia quelli non necessari
        # target_list = list(target_list - not_necessary_fields) # diff set ottiene come output solo campi necessari
        logging.error(target_list)
        raise FormValidation(error=msg, target=target_list)


@api_post_bp.route("student/", methods=['POST'])
def post_student():
    if request.method == "POST":
        logging.info("post request student")
        student_dict = request.get_json()
        logging.info(f"dati ricevuti: {student_dict}")

        try:
            validate(student_dict)
        except FormValidation as err:
            return make_response(jsonify(error=err.error, target=err.target), 400)
        else:
            student = Student(name=student_dict['name'], lastname=student_dict['lastname'],
                              age=int(student_dict['age']), email=student_dict['email'])
            db.session.add(student)
            db.session.commit()
            return make_response(jsonify({'student': student.as_dict()}), 201)


@api_post_bp.route("user/", methods=['POST'])
def post_user():
    if request.method == "POST":
        logging.info("post request")
        user_dict = request.get_json()
        logging.info(user_dict)
        try:
            validate_user(user_dict)
        except FormValidation as err:
            return make_response(jsonify(error=err.error, target=err.target), 400)
        else:
            hashed_psw = bcrypt.generate_password_hash(user_dict["password"]).decode('utf-8')
            user = User(email=user_dict["email"], password=hashed_psw)

            user.email = user_dict.get('email', user.email)

            role_admin = Role.query.filter_by(name='admin').first()
            role_mod = Role.query.filter_by(name='moderatore').first()

            if not role_admin:  # il record admin esiste gia' nella tabella dei ruoli?
                role_admin = Role(name='admin', description='admin')

            if not role_mod:  # il record moderatore esiste gia' nella tabella dei ruoli?
                role_mod = Role(name='moderatore', description='moderatore')

            if 'admin' in user_dict.get("ruoli"):
                user.roles.append(role_admin)

            if 'moderatore' in user_dict.get("ruoli"):
                user.roles.append(role_mod)

            db.session.add(user)
            db.session.commit()
            return make_response(jsonify({'user': user.as_dict()}), 201)


