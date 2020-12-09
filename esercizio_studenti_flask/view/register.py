from flask import render_template, flash, redirect, url_for, Blueprint, request, jsonify
from esercizio_studenti_flask.forms import RegisterForm, DeleteStudentForm, RegisterStudentForm, ROLES
from esercizio_studenti_flask.model import Student, User, Role
from esercizio_studenti_flask import bcrypt, db
from flask_security import login_required, roles_accepted
from customException import FormValidation
import json
import re

register = Blueprint('register', __name__, template_folder='../templates', url_prefix='/register')


# Make a regular expression
# for validating an Email
regex = '^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$'
# for custom mails use: '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'


def check(email):
    if re.search(regex, email):
        print("Valid Email")
    else:
        print("Invalid Email")
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


@register.route('/admin', methods=['POST', 'GET'])
@roles_accepted('admin', 'moderatore')
def admin():
    form = RegisterForm()

    if form.validate_on_submit():
        role = Role.query.filter_by(name='admin').first()
        role_2 = Role.query.filter_by(name='moderatore').first()

        # role_chose = dict(ROLES).get(form.pick_role.data)

        hashed_psw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_psw)

        if form.admin.data:
            if not role:
                role = Role(name='admin', description='admin')

            user.roles.append(role)

        if form.moderatore.data:
            if not role_2:
                role_2 = Role(name='moderatore', description='moderatore')

            user.roles.append(role_2)

        db.session.add(user)
        db.session.commit()
        flash(f'User {user.email} added', 'success')
        return redirect(url_for('home.home'))
    else:
        print(form.errors)
    return render_template('register.html', title='Register', form=form)


@register.route('/student', methods=['POST', 'GET'])
@roles_accepted('admin', 'moderatore')
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
                print("trovato id per studnete")
                student = Student.query.filter_by(id=student_dict['id']).first()
                print(f"studente da cancellare: {student}")
                db.session.delete(student)
                db.session.commit()
                flash(f'Student {student.name} {student.lastname}, {student.email} - {student.id} Removed!', 'success')
                return jsonify({"redirect": '/home'})

    if request.method == "GET":
        print("GET method")
        id = request.args.get('id')
        student = Student.query.filter(Student.id == id).first()

        return render_template('insert_student.html', title='Register', student=student, student_id=id)


@register.route("/getdata/<int:id>", methods=['GET'])
@roles_accepted('admin', 'moderatore')
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


@register.route('/update_insert', methods=['POST'])
def update_insert():

    student = Student.query.filter_by(id=request.form.get('id')).first()
    name = student.name
    lastname = student.lastname
    age = student.age
    email = student.email
    id = student.id

    return jsonify(name=name, lastname=lastname, age=age, email=email, id=id)
