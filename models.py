"""Models for Flask-Notes."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """
    User class that includes an username, password, email,
    the user's first name, last name.
    """

    __tablename__ = "users"

    username = db.Column(db.String(20),
                         primary_key=True,
                         nullable=False)

    password = db.Column(db.String(100),
                         nullable=False)

    email = db.Column(db.String(50),
                      unique=True,
                      nullable=False)

    first_name = db.Column(db.String(30),
                           nullable=False)

    last_name = db.Column(db.String(30),
                          nullable=False)

    @classmethod
    def register(cls, username, pwd):
        """Register user w/hashed password & return user."""
        hashed = bcrypt.generate_password_hash(pwd).decode('utf8')
        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.
        Return user if valid; else return False.
        """
        u = cls.query.filter_by(username=username).one_or_none()
        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False
