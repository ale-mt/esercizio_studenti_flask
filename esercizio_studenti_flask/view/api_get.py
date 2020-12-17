from flask import Blueprint, request, jsonify, json, make_response
from esercizio_studenti_flask.model import Student, User, Role
import logging
from flask_security import roles_accepted


api_get_bp = Blueprint('get', __name__, url_prefix='/api/')




@api_get_bp.route("student/<int:id>", methods=['GET'])
def get_student(id):
    logging.info("ricevuta richiesta di dati (student)")
    if request.method == "GET":

        logging.info(f"ricevuto id: {id}")

        student = Student.query.filter_by(id=id).first()

        if student:
            student_dict = student.as_dict()
            logging.info(f"student json: {student_dict}")
            return jsonify(student=student_dict)

        else:
            logging.error("id non associato a nessuno studente")
            return make_response(jsonify({'error': 'not found'}), 404)


@api_get_bp.route("student/", methods=['GET'])
def get_student_list():
    logging.info("ricevuta richiesta di lista dati (students)")
    if request.method == "GET":

        student = [student.as_dict() for student in Student.query.all()]

        if len(student) == 0:
            logging.error("nessuno studente trovato")
            return make_response(jsonify({'error': 'not found'}), 404)
        else:
            logging.info(f"student json: {json.dumps(student, indent=1)}")
            return jsonify(students=student)


@api_get_bp.route("user/<int:id>", methods=['GET'])
def get_user(id):
    logging.info("ricevuta richiesta di dati (user)")
    if request.method == "GET":

        logging.info(f"ricevuto id: {id}")

        user = User.query.filter_by(id=id).first()
        if user:
            user_dict = user.as_dict()
            logging.debug(f"user json: {user_dict}")
            return jsonify(user=user_dict)
        else:

            logging.error("nessun utente assocciato all'id")
            return make_response(jsonify({'error': 'not found'}), 404)


@api_get_bp.route("user/", methods=['GET'])
def get_user_list():
    logging.info("ricevuta richiesta di lista dati (users)")
    if request.method == "GET":

        user = [user.as_dict() for user in User.query.all()]

        if len(user) == 0:
            logging.error("nessun utente trovato")
            return make_response(jsonify({'error': 'not found'}), 404)
        else:

            logging.info(f"users json: {json.dumps(user, indent=1)}")
            return jsonify(user=user)


@api_get_bp.route("role/<int:id>", methods=['GET'])
def get_role(id):
    logging.info("ricevuta richiesta di dati (role)")
    if request.method == "GET":

        logging.info(f"ricevuto id: {id}")

        role = Role.query.filter_by(id=id).first()

        if role:
            role = role.as_dict()
            logging.info(f"role json: {role}")
            return jsonify(role=role)
        else:
            logging.error("nessun ruolo assocciato all'id")
            return make_response(jsonify({'error': 'not found'}), 404)


@api_get_bp.route("role/", methods=['GET'])
def get_role_list():
    if request.method == "GET":

        role = [role.as_dict() for role in Role.query.all()]

        if len(role) == 0:
            logging.error("nessun ruolo trovato")
            return make_response(jsonify({'error': 'not found'}), 404)
        else:
            logging.info(f"role json: {json.dumps(role, indent=1)}")
            return jsonify(role=role)


