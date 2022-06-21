"""Models for Flask-Notes."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()


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