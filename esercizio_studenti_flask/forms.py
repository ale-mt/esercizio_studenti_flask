from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email, Length, NumberRange, ValidationError, Optional
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
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField()


ROLES = [('admin', 'admin'), ('moderatore', 'moderatore'), ('nessuno', 'nessuno')] # value, label


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    # pick_role = SelectField('Ruolo', choices=ROLES, validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', 'Le password non combaciano')])
    admin = BooleanField('Admin')
    moderatore = BooleanField('Moderatore')
    submit = SubmitField()

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email in uso da un altro utente')


class DeleteStudentForm(FlaskForm):     # form per delete e edit di student
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=2, max=20)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, max=120)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    id = SelectField('ID', coerce=int)
    submit = SubmitField('Submit', validators=[Optional()])
    edit = SubmitField('Edit', validators=[Optional()])
    delete = SubmitField('Delete', validators=[Optional()])

    def validate_id(self, id):
        if id.data < 1:
            if not self.submit.data:
                raise ValidationError("Id non valido")

    def validate_email(self, email):
        student_bymail = Student.query.filter_by(email=email.data).first()
        print(f'student by mail {student_bymail}')
        student_byid = Student.query.filter_by(id=self.id.data).first() # utente puo modificare input value da ispeziona elemento
        print(f'student by id {student_byid}')
        if student_bymail and student_byid:
            print("dentro primo if")
            if not student_bymail.email == student_byid.email:
                print("dentro not")
                raise ValidationError('Email in uso da un altro studente')

        if self.submit.data:
            if student_bymail:
                raise ValidationError('Email in uso da un altro studente')



class DeleteUserForm(FlaskForm): # form per delete e edit di user
    email = StringField('Email', validators=[Email(), DataRequired()])
    # pick_role = SelectField('Ruolo', choices=ROLES, validators=[DataRequired()])
    id = IntegerField('ID')
    admin = BooleanField('Admin')
    moderatore = BooleanField('Moderatore')
    edit = SubmitField()
    delete = SubmitField()

    def validate_email(self, email):
        user_bymail = User.query.filter_by(email=email.data).first()
        user_byid = User.query.filter_by(id=self.id.data).first() # utente puo modificare input value da ispeziona elemento
        if user_bymail:
            if not user_bymail.email == user_byid.email:
                raise ValidationError('Email in uso da un altro utente')

    def validate_pick_role(self, pick_role):
        user = User.query.filter(User.id == self.id.data).first()
        role_chose = dict(ROLES).get(pick_role.data)
        print(role_chose)
        if user:
            print('user esistente')
            if role_chose in user.roles:
                print(f'{role_chose} in user.roles')
                raise ValidationError("L'utente ricopre attualmente questo questo ruolo")


