from esercizio_studenti_flask import db, login_manager
from flask_login import UserMixin
from flask_security import RoleMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, unique=True)

    def __repr__(self):
        return f'id={self.id}, fullname={self.name} {self.lastname}, age={self.age}, email={self.email}'

    def as_dict(self):
        return {
                'id': self.id,
                'name': self.name,
                'lastname': self.lastname,
                'age': self.age,
                'email': self.email
                }


# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), primary_key=True),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id'), primary_key=True))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'

    def as_dict(self):
        return {'name': self.name, 'description': self.description}


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f'User(id={self.id}, email={self.email}, ruolo=({self.roles}))'

    def as_dict(self):
        ruoli = [str(ruolo) for ruolo in self.roles]

        return {
                'id': self.id,
                'email': self.email,
                'password': self.password,
                'active': self.active,
                'confirmed_at': self.confirmed_at,
                'ruoli': ruoli
                }


