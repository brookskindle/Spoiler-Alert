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
from flask.ext.login import LoginManager

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


class User(db.Model):
    # Since we're using Flask-Login, User must be created a specific way:
    # See: https://flask-login.readthedocs.org/en/latest/#your-user-class
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(160), unique=True)
    password = db.Column(db.String(64), unique=False)
    authenticated = db.Column(db.Boolean, default=False)
    posts = db.relationship("Post", backref="user", lazy="dynamic")

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "<user: {}>".format(self.username)

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True  # All users are active

    def is_anonymous(self):
        return False  # Disable anonymous users

    def get_id(self):
        return self.id


class Post(db.Model):
    """Represents a post made by a user."""
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(160), unique=False)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, userid, content=None):
        self.content = content
        # TODO: validate user id?
        self.userid = userid

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
    return User.query.get(user_id)

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


@app.route("/submit/")
def submit():
    return render_template("submit.html")


@app.route("/submit/", methods=["POST"])
def submit_post():
    """Adds a submitted spoiler."""
    spoiler = request.form['text']
    # TODO: Does this need to go through any user sanitization?
    post = Post(spoiler)
    db.session.add(post)
    db.session.commit()
    return redirect("/", code=302)


@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    # Else "POST"
    user = User(request.form["username"], request.form["password"])
    # TODO: do we need to check for username validity?
    db.session.add(user)
    db.session.commit()
    flash("Successfully registered.")
    return redirect(url_for("login"))


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    # Else "POST"
    # TODO: do we need to check login credentials?
    return redirect(url_for("index"))


@app.route("/logout/")
def logout():
    """Logs a user out, if he was logged in."""
    # TODO: Log a user out.
    flash("TODO: Actually perform a log out.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
