
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired


class RegisterForm(FlaskForm):
    """" a form for adding a user"""

    username = StringField('Username',
                           validators=[InputRequired()])
    password = PasswordField('Password',
                             validators=[InputRequired()])
    email = EmailField('Email',
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


class AddNoteForm(FlaskForm):
    """ a form for adding a new note"""

    title = StringField(
        'Title',
        validators=[InputRequired()])
    content = TextAreaField(
        'Content',
        validators=[InputRequired()])


class EditNoteForm(FlaskForm):
    """ a form for adding a new note"""

    title = StringField(
        'Title',
        validators=[InputRequired()])
    content = TextAreaField(
        'Content',
        validators=[InputRequired()])
