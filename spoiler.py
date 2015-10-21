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
from flask import render_template  # For html template rendering.
from flask import request  # For obtaining POST information (?)
from flask import redirect  # To redirect to another page

# Local imports.
from database import db
from models.models import Post, User

app = Flask(__name__)

@app.teardown_appcontext
def shutdown_session(exception=None):
    """Remove database session at end of request/when app is shut down."""
    db_session.remove()

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
    db_session.add(post)
    db_session.commit()
    return redirect("/", code=302)

@app.route("/register/", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    # Else "POST"
    user = User(request.form["username"], request.form["password"])
    # TODO: do we need to check for username validity?
    db.session.add(user)
    db.session.commit()
    falsh("Successfully registered.")
    return redirect(url_for("login"))

@app.route("/login/", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    # Else "POST"
    # TODO: do we need to check login credentials?
    return redirect(url_for("index"))

@app.route("/logout/")
def logout():
    """Logs a user out, if he was logged in."""
    pass

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
