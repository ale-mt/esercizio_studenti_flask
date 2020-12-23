from flask import Blueprint, json, make_response, request, jsonify
from esercizio_studenti_flask.model import Student, User, Role
from esercizio_studenti_flask import bcrypt, db
from customException import FormValidation
import re, logging
from flask_security import roles_accepted


api_put_bp = Blueprint('put', __name__, url_prefix='/api/')


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


def validate(student_dict, id):
    def validate_email(id):
        check(student_dict.get('email'))
        student_bymail = Student.query.filter_by(email=student_dict.get('email')).first()
        logging.info(f'student by mail {student_bymail}')
        student_byid = Student.query.filter_by(id=id).first()
        logging.info(f'student by id {student_byid}')

        if student_bymail and student_byid:
            if not student_bymail.email == student_byid.email:
                msg = "Email in uso da un altro studente"
                target_list = ['email']
                logging.error(msg)
                raise FormValidation(error=msg, target=target_list)
        else:
            return True

    # e' possibile non modificare ogni campo

    if 'name' in student_dict and type(student_dict['name']) is not str:
        msg = "Nome' non valido"
        raise FormValidation(error=msg, target=['name'])

    elif 'lastname' in student_dict and type(student_dict['lastname']) is not str:
        msg = "Lastname' non valido"
        raise FormValidation(error=msg, target=['lastname'])

    elif ('age' in student_dict and type(student_dict['age']) is not int) or\
            ('age' in student_dict and (18 > int(student_dict['age']) or int(student_dict['age']) > 100)):
        msg = "Age non valida"
        raise FormValidation(error=msg, target=['age'])

    elif 'email' in student_dict:
        validate_email(id)

    else:
        return True


def validate_user(user_dict, id):
    def validate_email(id):
        check(user_dict.get('email'))
        user_bymail = User.query.filter_by(email=user_dict.get('email')).first()
        logging.info(f'user by mail {user_bymail}')
        user_byid = User.query.filter_by(id=id).first()
        logging.info(f'user by id {user_byid}')

        if user_bymail and user_byid:
            if not user_bymail.email == user_byid.email:
                msg = "Email in uso da un altro utente"
                target_list = ['email']
                logging.error(msg)
                raise FormValidation(error=msg, target=target_list)
        else:
            return True

    if 'ruoli' in user_dict:
        if type(user_dict['ruoli']) is not list:
            msg = "Campo ruoli non valido"
            logging.error(msg)
            raise FormValidation(error=msg, target=['ruoli'])
        else:
            for ruolo in user_dict['ruoli']:
                if ruolo != "admin" and ruolo != "moderatore":
                    msg = f"Ruolo {ruolo} non valido. Ruoli validi ['moderatore', 'admin']"
                    logging.error(msg)
                    raise FormValidation(error=msg, target=['ruoli'])

    if 'email' in user_dict:
        validate_email(id)

    return True


@api_put_bp.route("student/<int:id>", methods=['PUT'])
def put_student(id):
    logging.info("ricevuta richiesta di update (student)")
    if request.method == "PUT":

        logging.info(f"ricevuto id: {id}")

        student_dict = request.get_json()
        logging.info(student_dict)

        try:
            validate(student_dict, id)
        except FormValidation as err:
            return make_response(jsonify(error=err.error, target=err.target), 400)
        else:
            student = Student.query.filter_by(id=id).first()
            student.name = student_dict.get('name', student.name)
            student.lastname = student_dict.get('lastname', student.lastname)
            student.age = student_dict.get('age', student.age)
            student.email = student_dict.get('email', student.email)
            db.session.commit()
            return make_response(jsonify({'student': student.as_dict()}), 201)


@api_put_bp.route("user/<int:id>", methods=['PUT'])
def put_user(id):
    logging.info("ricevuta richiesta di update (user)")
    if request.method == "PUT":

        logging.info(f"ricevuto id: {id}")

        user_dict = request.get_json()
        logging.info(user_dict)

        try:
            validate_user(user_dict, id)
        except FormValidation as err:
            return make_response(jsonify(error=err.error, target=err.target), 400)
        else:
            user = User.query.filter_by(id=id).first()

            user.email = user_dict.get('email', user.email)

            role_admin = Role.query.filter_by(name='admin').first()
            role_mod = Role.query.filter_by(name='moderatore').first()

            if not role_admin:  # il record admin esiste gia' nella tabella dei ruoli?
                role_admin = Role(name='admin', description='admin')

            if not role_mod:  # il record moderatore esiste gia' nella tabella dei ruoli?
                role_mod = Role(name='moderatore', description='moderatore')

            if "ruoli" in user_dict:
                if type(user_dict['ruoli']) is list and len(user_dict['ruoli']) == 0: # e' stata fornita una lista vuota di ruoli
                    user.roles = []
                elif type(user_dict['ruoli']) is list and len(user_dict['ruoli']) > 0:
                    if 'admin' in user_dict.get("ruoli"): # se non e' fornito array RUOLI, la variabile sara' None causando errore
                        if role_admin not in user.roles:
                            user.roles.append(role_admin)
                    else:
                        if role_admin in user.roles:
                            user.roles.remove(role_admin)

                    if 'moderatore' in user_dict.get("ruoli"):
                        if role_mod not in user.roles:
                            user.roles.append(role_mod)
                    else:
                        if role_mod in user.roles:
                            user.roles.remove(role_mod)

            db.session.commit()
            return make_response(jsonify({'user': user.as_dict()}), 201)

