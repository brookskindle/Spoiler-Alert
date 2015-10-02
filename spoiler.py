#!/usr/bin/env python

"""
spoiler.py - the program entry point
"""

import random

from flask import Flask
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
    return spoilers[i]

if __name__ == "__main__":
    app.run(debug=True)
