from flask import Blueprint, request, jsonify, json, make_response
from esercizio_studenti_flask.model import Student, User, Role
from esercizio_studenti_flask import bcrypt, db
from flask_security import roles_accepted
import logging

api_delete_bp = Blueprint('delete', __name__, url_prefix='/api/')


@api_delete_bp.route("student/<int:id>", methods=['DELETE'])
def get_student(id):
    logging.info("ricevuta richiesta di cancellazione (student)")
    if request.method == "DELETE":

        logging.info(f"ricevuto id: {id}")

        # verifica che form abbia fornito id e che esista tra quelli creati
        id_list = [s.id for s in Student.query.all()]

        if id in id_list:
            logging.info("trovato id per studente")
            student = Student.query.filter_by(id=id).first()
            logging.info(f"studente da cancellare: {student}")
            db.session.delete(student)
            db.session.commit()
            return make_response(jsonify({'student': student.as_dict()}), 201)
        else:
            logging.error("id non associato a nessuno studente")
            return make_response(jsonify({'error': 'id not found'}), 404)


@api_delete_bp.route("user/<int:id>", methods=['DELETE'])
def get_user(id):
    logging.info("ricevuta richiesta di cancellazione (user)")
    if request.method == "DELETE":

        logging.info(f"ricevuto id: {id}")

        # verifica che form abbia fornito id e che esista tra quelli creati
        id_list = [u.id for u in User.query.all()]

        if id in id_list:
            logging.info("trovato id per utente")
            user = User.query.filter_by(id=id).first()
            logging.info(f"user da cancellare: {user}")
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'user': user.as_dict()}), 201)
        else:
            logging.error("id non associato a nessun user")
            return make_response(jsonify({'error': 'id not found'}), 404)
