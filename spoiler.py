#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Specify encoding so we may use unicode within our source code.

"""
spoiler.py - the program entry point
"""

# System imports.
import random

# Third party imports.
from flask import Flask
from flask import flash  # Flash a message on the screen.
from flask import redirect  # To redirect to another page
from flask import render_template  # For html template rendering.
from flask import request  # For obtaining POST information (?)
from flask import url_for  # Gets the url for a given name
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_required, login_user
from flask.ext.login import current_user, logout_user
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Local imports.

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.secret_key = "THIS ISN'T A VERY SECURE SECRET KEY!"
db = SQLAlchemy(app)  # Create the db
login_manager = LoginManager()
login_manager.init_app(app)  # Create the login_manager

"""-------------------------------------------------------------------------"""
"""---------------------------------MODELS----------------------------------"""
"""-------------------------------------------------------------------------"""


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

"""-------------------------------------------------------------------------"""
"""---------------------------------ROUTES----------------------------------"""
"""-------------------------------------------------------------------------"""


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
    if request.method == "GET":
        return render_template("submit.html")
    # Else POST
    user_id = current_user.get_id()
    spoiler = request.form['text']
    post = Post(user_id, spoiler)
    db.session.add(post)
    db.session.commit()
    return redirect("/", code=302)


@app.route("/register/", methods=["GET", "POST"])
def register():
    # TODO: implement https for a production server
    if request.method == "GET":
        return render_template("register.html")
    # Else "POST"
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username).first()
    if user is not None:  # User already exists
        return render_template("register.html")
    # User doesn't exist, add him!
    user = User()
    user.username = username
    user.password = password
    db.session.add(user)
    db.session.commit()
    flash("Successfully registered.")
    return redirect(url_for("login"))


@app.route("/login/", methods=["GET", "POST"])
def login():
    # TODO: implement https for a production server
    if request.method == "GET":
        return render_template("login.html")
    # Else "POST"
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username).first()
    if user is not None and user.verify_password(password):
        # Valid username and password
        login_user(user)
        return redirect(url_for("submit"))
    flash("Error, incorrect username and/or password")
    return redirect(url_for("login"))


@app.route("/logout/", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("You have been successfully logged out!")
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
