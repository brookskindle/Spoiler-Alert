#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Specify encoding so we may use unicode within our source code.

"""
spoiler.py - the program entry point
"""

# System imports.
import random
from functools import wraps

# Third party imports.
from flask import Flask, abort
from flask import flash  # Flash a message on the screen.
from flask import redirect  # To redirect to another page
from flask import render_template  # For html template rendering.
from flask import request  # For obtaining POST information (?)
from flask import url_for  # Gets the url for a given name
from flask.ext.bootstrap import Bootstrap  # Pretty user interface
from flask.ext.login import LoginManager, login_user, login_required
from flask.ext.login import UserMixin
from flask.ext.login import current_user, logout_user
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from wtforms import StringField, TextField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash

# Local imports.

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.secret_key = "THIS ISN'T A VERY SECURE SECRET KEY!"
db = SQLAlchemy(app)  # Create the db
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)  # Create the login_manager
bootstrap = Bootstrap(app)
manager = Manager(app)
migrate = Migrate(app, db)


# -----------------------------------------------------------------------------
# ----------------------------------DECORATORS---------------------------------
# -----------------------------------------------------------------------------
def disabled(f):
    """
    Decorator that returns an HTTP 503 (Service Unavailable) error code when a
    route is invoked.

    Because of the order of decorator execution, this decorator should come
    immediatly after registering the route and before any other decorators.

    As an example:
        @app.route("/account/")
        @disabled
        @...(other decorators)
        def account():
            pass
    """
    @wraps(f)
    def _wrapper(*args, **kwargs):
        return abort(503)
    return _wrapper

def user_allowed(user_name):
    """ Allows only a given user access to a route.  """
    def _decorator(f):
        @wraps(f)
        def _wrapper(*args, **kwargs):
            if current_user.is_anonymous:
                pass
            elif current_user.username == user_name:
                return f(*args, **kwargs)
            return abort(403)
        return _wrapper
    return _decorator

# --------------------------------------------------------------------------
# ----------------------------------MODELS----------------------------------
# --------------------------------------------------------------------------


class User(UserMixin, db.Model):
    # Since we're using Flask-Login, User must be created a specific way:
    # See: https://flask-login.readthedocs.org/en/latest/#your-user-class
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128), unique=False)
    posts = db.relationship("Post", backref="user", lazy="dynamic")

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    """Represents a post made by a user."""
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(160), unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, user_id, content):
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return "id={0}, content={1}".format(self.id, self.content)


def init_db():
    """Initializes the database."""
    db.create_all()


@login_manager.user_loader
def user_loader(user_id):
    """
    Return the User object from a given user_id
    """
    return User.query.get(int(user_id))

# --------------------------------------------------------------------------
# ----------------------------------FORMS-----------------------------------
# --------------------------------------------------------------------------


class PostForm(Form):
    """
    A form for submitting a spoiler post.
    """
    post = TextField("Give us a spoiler!", validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(Form):
    """
    A form to allow users to log in.
    """
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class RegisterForm(Form):
    """
    A form that people can use to register an account.
    """
    username = StringField("Create a username", validators=[DataRequired()])
    password = PasswordField("Create a password", validators=[DataRequired(),
                EqualTo('password_repeat', message="Passwords must match")])
    password_repeat = PasswordField("Repeat password",
                                    validators=[DataRequired()])
    submit = SubmitField("Register")

# --------------------------------------------------------------------------
# ----------------------------------ROUTES----------------------------------
# --------------------------------------------------------------------------


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Remove database session at end of request/when app is shut down."""
    db.session.remove()


@app.route("/")
def index():
    default_post = "We're all spoiled out. Give us a hand and tell us yours!"
    # TODO: querying the entire post table is inefficient and will not scale. A
    # better solution for this needs to be found when relevant.
    posts = Post.query.all()
    spoiler = default_post
    if posts:  # At least one spoiler post
        i = random.randrange(len(posts))
        spoiler = posts[i].content
    return render_template("index.html", content=spoiler)


@app.route("/submit/", methods=["GET", "POST"])
@login_required
def submit():
    """Adds a submitted spoiler."""
    content = None
    user_id = None
    form = PostForm()
    if form.validate_on_submit():
        user_id = current_user.get_id()
        content = form.post.data
        post = Post(user_id, content)
        db.session.add(post)
        db.session.commit()
        return redirect("/", code=302)
    return render_template("submit.html", form=form)


@app.route("/register/", methods=["GET", "POST"])
def register():
    # TODO: implement https for a production server
    form = RegisterForm()
    if form.validate_on_submit():  # POST and form data validated.
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is not None:  # User already exists
            flash("{} is already in use.".format(username))
        else:  # User doesn't exist, add him!
            user = User()
            user.username = username
            user.password = password
            db.session.add(user)
            db.session.commit()
            flash("Successfully registered.")
            return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login/", methods=["GET", "POST"])
def login():
    # TODO: implement https for a production server
    form = LoginForm()
    if form.validate_on_submit():  # POST request with valid form data.
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is not None and user.verify_password(password):
            # Valid credentials supplied.
            login_user(user)
            # TODO: Validate the "next" argument, lest I invite an open
            # redirect security violation.
            return redirect(request.args.get("next") or url_for("index"))
        else:
            # Invalid login credentials.
            flash("Invalid username or password supplied.")
    return render_template("login.html", form=form)


@app.route("/logout/", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("You have been successfully logged out!")
    return redirect(url_for("index"))

def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post)

if __name__ == "__main__":
    init_db()
    manager.add_command("shell", Shell(make_context=make_shell_context))
    manager.add_command("db", MigrateCommand)
    manager.run()
