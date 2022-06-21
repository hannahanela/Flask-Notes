"""Flask app for Notes"""
from flask import Flask, jsonify, request, url_for, render_template, redirect, flash

#from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User
from forms import RegisterForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()


@app.get('/')
def go_to_homepage():
    """ redirects to register page"""

    return redirect('/register')


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user: produce form & handle form submission."""

    form = RegisterForm()

    if form.validate_on_submit():

        name = form.username.data
        pwd = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(username=name,
                    password=pwd,
                    email=email,
                    first_name=first_name,
                    last_name=last_name)

        db.session.add(user)
        db.session.commit()
        # on successful login, redirect to secret page
        return redirect("/secret")

    else:
        return render_template("register.html", form=form)

