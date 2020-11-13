from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email, Length, NumberRange, ValidationError
from esercizio_studenti_flask.model import Student, User


class RegisterStudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=2, max=20)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, max=120)])
    email = StringField('Email', validators=[DataRequired(), Email()])

    submit = SubmitField()

    def validate_email(self, email):
        student = Student.query.filter_by(email=email.data).first()
        if student:
            raise ValidationError('Email in uso da un altro studente')


class Loginform(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField()


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField()

    def validate_name(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('Nome utente non disponibile')


class DeleteStudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=2, max=20)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, max=120)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    id = IntegerField('ID')
    edit = SubmitField()
    delete = SubmitField()

    def validate_email(self, email):
        student_bymail = Student.query.filter_by(email=email.data).first()
        student_byid = Student.query.filter_by(id=self.id.data).first() # utente puo modificare input value da ispeziona elemento
        if student_bymail:
            if not student_bymail.email == student_byid.email:
                raise ValidationError('Email in uso da un altro studente')


