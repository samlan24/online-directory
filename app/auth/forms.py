from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, FileField, DateTimeField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileAllowed, FileRequired
from app.models import Agent, Role

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
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords not matching')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    location = SelectField('Location', coerce=int)
    image = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    description = TextAreaField('Description', validators=[Length(0, 255)])
    Submit = SubmitField('Register')

    # check if email is in use
    def validate_email(self, field):
        if Agent.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    # check if username is in use
    def validate_name(self, field):
        if Agent.query.filter_by(name=field.data).first():
            raise ValidationError('name already in use.')

# form to change agent details
class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = SelectField('Location', coerce=int)
    description = TextAreaField('About me')
    image = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Submit')

#form to delete an account
class DeleteProfileForm(FlaskForm):
    submit = SubmitField('Delete Account')

# form to send message
class MessageForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    content = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')


class DeleteMessageForm(FlaskForm):
    submit = SubmitField('Delete')