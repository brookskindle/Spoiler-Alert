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
from database import db_session, init_db
from models.models import Post

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


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
