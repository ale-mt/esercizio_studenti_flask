from flask import render_template, flash, redirect, url_for, Blueprint, request, jsonify
from esercizio_studenti_flask.forms import RegisterForm, DeleteStudentForm, RegisterStudentForm, ROLES
from esercizio_studenti_flask.model import Student, User, Role
from esercizio_studenti_flask import bcrypt, db
from flask_security import login_required, roles_accepted
from customException import FormValidation
import json
import re

register = Blueprint('register', __name__, template_folder='../templates', url_prefix='/register')


# regex per mail
regex = '^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$'
# for custom mails use: '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'


def check(email):
    if re.search(regex, email):
        print("Regex Valid Email")
        return True
    else:
        print("Regex Invalid Email")
        raise FormValidation(error='Email non valida', target=['email'])


def validate(student_dict):
    def validate_email():
        check(student_dict.get('email'))
        student_bymail = Student.query.filter_by(email=student_dict.get('email')).first()
        print(f'student by mail {student_bymail}')
        student_byid = Student.query.filter_by(id=student_dict.get('id')).first()
        print(f'student by id {student_byid}')
        if student_bymail and student_byid:
            if not student_bymail.email == student_byid.email:
                msg = "Email in uso da un altro studente"
                target_list = ['email']
                raise FormValidation(error=msg, target=target_list)
        elif student_dict['action'] == 'submit':
            if student_bymail:
                msg = "Email in uso da un altro studente"
                target_list = ['email']
                raise FormValidation(error=msg, target=target_list)
        else:
            return True

    # nessun campo deve essere vuoto
    if student_dict['name'] and student_dict['lastname'] and student_dict['age'] and student_dict['email']:
        validate_email()
        if 18 > int(student_dict['age']) or int(student_dict['age']) > 100:
            msg = "Eta' non valida"
            raise FormValidation(error=msg, target=['age'])
        else:
            print("validato")
            return True
    else:
        msg = "Campo vuoto"
        print(msg)
        target_list = []
        for key in student_dict:
            if not student_dict[key]:
                target_list.append(key)  # lista dei campi vuoti da segnalare

        raise FormValidation(error=msg, target=target_list)


def validate_user(user_dict):
    def validate_email():
        check(user_dict.get('email'))
        user_bymail = User.query.filter_by(email=user_dict.get('email')).first()
        print(f'user by mail {user_bymail}')
        if user_bymail:
            msg = "Email in uso da un altro utente"
            target_list = ['email']
            raise FormValidation(error=msg, target=target_list)
        else:
            return True

    # nessun campo deve essere vuoto
    if user_dict['email'] and user_dict['password'] and user_dict['confirm_password']:
        validate_email()

        if user_dict['password'] == user_dict['confirm_password']:
            print("validato")
            return True
        else:
            msg = "Le password non corrispondono"
            target_list = ['password', 'confirm_password']
            print(msg)
            raise FormValidation(error=msg, target=target_list)
    else:
        msg = "Campo vuoto"
        print(msg)
        target_list = []
        for key in user_dict:
            if not user_dict[key]:
                target_list.append(key)  # lista dei campi vuoti da segnalare

        raise FormValidation(error=msg, target=target_list)


@register.route('/admin', methods=['POST', 'GET'])
# @roles_accepted('admin', 'moderatore')
def admin():
    if request.method == "POST":
        print("post request")
        user_dict = request.get_json()
        action = user_dict['action']
        print(user_dict)
        print(action)

        if user_dict['action'] == 'edit':
            print("dentro edit")
            try:
                email = user_dict["email"]
                if email and check(user_dict.get('email')):
                    print("email passed regex")
                else:
                    raise FormValidation(error="Mail non valida", target=['email'])

                user_bymail = User.query.filter_by(email=user_dict.get('email')).first()
                user_byid = User.query.filter_by(id=user_dict.get('id')).first()
                print(f'user by mail {user_bymail}')
                print(f'user by id {user_byid}')
                if user_bymail and user_byid:
                    if not (user_bymail.email == user_byid.email):
                        msg = "Email in uso da un altro utente"
                        target_list = ['email']
                        raise FormValidation(error=msg, target=target_list)

            except FormValidation as err:
                return jsonify(error=err.error, target=err.target)
            else:
                user = User.query.filter_by(id=user_dict.get('id')).first()

                user.email = email

                role_admin = Role.query.filter_by(name='admin').first()
                role_mod = Role.query.filter_by(name='moderatore').first()

                if not role_admin:  # il record admin esiste gia' nella tabella dei ruoli?
                    role_admin = Role(name='admin', description='admin')

                if user_dict["admin"]:  # inviata richiesta di diventare admin?
                    if 'admin' not in user.roles:   # l'utente e' gia' admin?
                        user.roles.append(role_admin)
                else:
                    if 'admin' in user.roles:  # l'utente non e' gia' admin?
                        user.roles.remove(role_admin)

                if not role_mod:  # il record moderatore esiste gia' nella tabella dei ruoli?
                    role_mod = Role(name='moderatore', description='moderatore')

                if user_dict["moderatore"]:  # inviata richiesta di diventare moderatore?
                    if 'moderatore' not in user.roles:  # l'utente non e' gia' moderatore?
                        user.roles.append(role_mod)
                else:
                    if 'moderatore' in user.roles:  # l'utente non e' gia' moderatore?
                        user.roles.remove(role_mod)

                db.session.commit()
                flash(f'User {user.email} edited', 'success')
                return jsonify({"redirect": "/home"})

        if user_dict['action'] == 'delete':
            print("dentro delete")
            user = User.query.filter_by(email=user_dict["email"]).first()
            db.session.delete(user)
            db.session.commit()
            flash(f'User {user.email} Removed!', 'success')
            return jsonify({"redirect": '/home'})

        if user_dict['action'] == 'submit':
            print("dentro submit")
            try:
                validate_user(user_dict)
            except FormValidation as err:
                return jsonify(error=err.error, target=err.target)
            else:
                role_admin = Role.query.filter_by(name='admin').first()
                role_mod = Role.query.filter_by(name='moderatore').first()

                hashed_psw = bcrypt.generate_password_hash(user_dict["password"]).decode('utf-8')
                user = User(email=user_dict["email"], password=hashed_psw)

                if user_dict["admin"]:
                    if not role_admin:
                        role_admin = Role(name='admin', description='admin')

                    user.roles.append(role_admin)

                if user_dict["moderatore"]:
                    if not role_mod:
                        role_mod = Role(name='moderatore', description='moderatore')

                    user.roles.append(role_mod)

                db.session.add(user)
                db.session.commit()
                flash(f'User {user.email} added', 'success')
                return jsonify({"redirect": "/home"})

    if request.method == "GET":
        print("GET method requested")
        id = request.args.get('id')
        return render_template('register.html', title='Register', user_id=id)


@register.route('/student', methods=['POST', 'GET'])
# @roles_accepted('admin', 'moderatore')
def student():

    if request.method == "POST":
        print("post request")
        student_dict = request.get_json()
        print(f"dati ricevuti: {student_dict}")
        action = student_dict['action']
        print(f"azione richiesta: {action}")

        if student_dict["action"] == "edit":
            print("ricevuta richiesta di edit")
            try:
                validate(student_dict)
            except FormValidation as err:
                return jsonify(error=err.error, target=err.target)
            else:
                student = Student.query.filter_by(id=student_dict['id']).first()
                student.name = student_dict['name']
                student.lastname = student_dict['lastname']
                student.age = student_dict['age']
                student.email = student_dict['email']
                db.session.commit()
                flash(f'Student {student.email} {student.lastname} edited!', 'success')
                return jsonify({"redirect": '/home'})

        if student_dict['action'] == 'submit':
            print("dentro submit")
            try:
                validate(student_dict)
            except FormValidation as err:
                return jsonify(error=err.error, target=err.target)
            else:
                student = Student(name=student_dict['name'], lastname=student_dict['lastname'], age=student_dict['age'], email=student_dict['email'])
                db.session.add(student)
                db.session.commit()
                flash(f'Student {student.name} {student.lastname} added!', 'success')
                return jsonify({"redirect": '/home'})

        if student_dict['action'] == 'delete':
            print("ricevuta richiesta di delete")

            # verifica che form abbia fornito id e che esista tra quelli creati
            id_list = [s.id for s in Student.query.all()]
            print(id_list)
            print(student_dict.get('id'))
            if int(student_dict.get('id')) in id_list:
                print("trovato id per studente")
                student = Student.query.filter_by(id=student_dict['id']).first()
                print(f"studente da cancellare: {student}")
                db.session.delete(student)
                db.session.commit()
                flash(f'Student {student.name} {student.lastname}, {student.email} - {student.id} Removed!', 'success')
                return jsonify({"redirect": '/home'})

    if request.method == "GET":
        print("GET method")
        id = request.args.get('id')
        return render_template('insert_student.html', title='Register', student_id=id)


@register.route("/getdata/<int:id>", methods=['GET'])
# @roles_accepted('admin', 'moderatore')
def getdata(id):
    print("ricevuta richiesta di dati (getdata)")
    if request.method == "GET":

        id_list = [s.id for s in Student.query.all()]

        print(id_list)
        student = Student.query.filter_by(id=id).first()
        if id:
            student_dict = {
                "name": student.name,
                "lastname": student.lastname,
                "age": student.age,
                "email": student.email,
                "id": student.id
            }

            print(f"ricevuto id: {id}")
            print(f"student json: {student_dict}")
        return jsonify(studente=student_dict, lista_id=id_list)


@register.route("user/getdata/<int:id>", methods=['GET'])
# @roles_accepted('admin', 'moderatore')
def getdata_user(id):
        print("ricevuta richiesta di dati utente (user/getdata)")
        if request.method == "GET":
            user = User.query.filter_by(id=id).first()
            ruoli = [str(ruolo) for ruolo in user.roles]
            print(type(ruoli))
            if id:
                user_dict = {
                    "email": user.email,
                    "ruolo": ruoli
                }

                print(f"user json: {user_dict}")
            return jsonify(user=user_dict)


@register.route('/update_insert', methods=['POST'])
def update_insert():

    student = Student.query.filter_by(id=request.form.get('id')).first()
    name = student.name
    lastname = student.lastname
    age = student.age
    email = student.email
    id = student.id

    return jsonify(name=name, lastname=lastname, age=age, email=email, id=id)

