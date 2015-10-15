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

app = Flask(__name__)

spoilers = [
        "Nothing is inside the jar of dirt.",
        "Jack dies.",
        "Hermione ends up with Ron.",
        "Ned Stark dies.",
        "Captain America's friend, Bucky, doesn't die but instead ends up "
            "becoming The Winter Soldier.",
]

@app.route("/")
def index():
    i = random.randrange(len(spoilers))
    spoiler = spoilers[i]
    return render_template("index.html", content=spoiler)

@app.route("/submit/")
def submit():
    return render_template("submit.html")

@app.route("/submit/", methods=["POST"])
def submit_post():
    """Adds a submitted spoiler."""
    spoiler = request.form['text']
    spoilers.append(spoiler)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
