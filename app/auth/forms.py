from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from app.models import Agent

# form to login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')

# form to register new account
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    name = StringField('name', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                            'Usernames must have only letters, '
                                                                                            'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords not matching')])
    password2 = PasswordField('password2', validators=[DataRequired()])
    Submit = SubmitField('Register')

# check if email is in use
def validate_email(self, field):
    if Agent.query.filter_by(email=field.data).first():
        raise ValidationError('Email already registered.')

# check if username is in use
def validate_name(self, field):
    if Agent.query.filter_by(name=field.data).first():
        raise ValidationError('name already in use.')