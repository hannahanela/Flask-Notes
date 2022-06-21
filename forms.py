# from email import message
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, PasswordField
from wtforms.validators import InputRequired, Optional, Email, EqualTo, AnyOf, URL


class RegisterForm(FlaskForm):
    """" a form for adding a user"""

    username = StringField('Username',
                           validators=[InputRequired()])
    password = PasswordField('Password',
                             validators=[InputRequired()])
    email = StringField('Email',
                        validators=[InputRequired()])
    first_name = StringField('Fiest Name',
                             validators=[InputRequired()])
    last_name = StringField('Last Name',
                            validators=[InputRequired()])


class LoginForm(FlaskForm):
    """" a form for logging in an existing user"""

    username = StringField('Username',
                           validators=[InputRequired()])
    password = PasswordField('Password',
                             validators=[InputRequired()])


class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""
