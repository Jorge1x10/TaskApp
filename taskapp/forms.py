import email
from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import DateField, StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from taskapp.models import User, Project
from flask_login import current_user



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username taken, Please choose another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Theres already an account with this email.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()]) 
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

def project_query():
    # Esta función devuelve los proyectos del usuario que ha iniciado sesión.
    return Project.query.filter_by(user_id=current_user.id).all()

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()]) # Ahora la descripción es opcional
    deadline = DateField('Deadline', validators=[Optional()]) # Ahora la fecha de vencimiento es opcional
    # Usamos query_factory para poblar las opciones y allow_blank para permitir no seleccionar ninguno.
    project = QuerySelectField('Project', query_factory=project_query, allow_blank=True, get_label='name', validators=[Optional()])
    submit = SubmitField('Save')

class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    deadline = DateField('Deadline', validators=[Optional()])
    submit = SubmitField('save')

class RequestResetForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    submit= SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must resgister first')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')