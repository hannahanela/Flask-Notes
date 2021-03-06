"""Flask app for Notes"""
from flask import Flask, render_template, redirect, session

# from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Note
from forms import RegisterForm, LoginForm, CSRFProtectForm, AddNoteForm, EditNoteForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///notes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

##### user routes ###############################################################


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

        user = User.register(
            username=name,
            password=pwd,
            email=email,
            first_name=first_name,
            last_name=last_name)

        db.session.add(user)
        db.session.commit()
        session["username"] = user.username

        return redirect(f"/users/{user.username}")

    else:
        return render_template("register_form.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data

        user = User.authenticate(username, pwd)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login_form.html", form=form)


@app.get('/users/<username>')
def secret_page(username):
    """ displays text to let user know they are logged in"""

    # TODO: only allow current user to access user page

    if "username" not in session:

        return redirect("/login")

    # only render_template of matching username
    form = CSRFProtectForm()

    user = User.query.get_or_404(username)

    if user.username == session["username"]:

        return render_template('user_page.html', user=user, form=form)

    return redirect("/login")


@app.post("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    form = CSRFProtectForm()
    if form.validate_on_submit():
        session.pop("username", None)

    return redirect('/')


@app.post('/users/<username>/delete')
def delete_user(username):
    """ deletes user """

    user = User.query.get_or_404(username)
    notes = Note.query.filter(Note.owner == username).all()

    for note in notes:
        db.session.delete(note)

    db.session.delete(user)
    db.session.commit()

    form = CSRFProtectForm()
    if form.validate_on_submit():
        session.pop("username", None)

    return redirect('/')


@app.route('/users/<username>/notes/add', methods=["GET", "POST"])
def add_note(username):
    """Show add note form and create new note, add to database, and return to
    user page."""

    user = User.query.get_or_404(username)

    form = AddNoteForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_note = Note(
            title=title,
            content=content,
            owner=user.username
        )

        db.session.add(new_note)
        db.session.commit()

        if user:
            session["username"] = user.username

            return redirect(f"/users/{user.username}")

    else:

        return render_template("add_note_form.html", form=form)


@app.get('/notes/<int:id>')
def posts_show(id):
    """Show a page with info on a specific post"""

    note = Note.query.get_or_404(id)
    return render_template('notes-show.html', note=note)


@app.route('/notes/<int:id>/update', methods=["GET", "POST"])
def update_note(id):
    """Show add note form and create new note, add to database, and return to
    user page."""

    note = Note.query.get_or_404(id)
    user = User.query.get(note.user.username)

    form = EditNoteForm()

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        if user:
            session["username"] = user.username

            return redirect(f"/users/{user.username}")

    else:

        return render_template("add_note_form.html", form=form, note=note)
