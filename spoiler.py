#!/usr/bin/env python

"""
spoiler.py - the program entry point
"""

import random

from flask import Flask, render_template
app = Flask(__name__)

spoilers = [
        "Nothing is inside the jar of dirt.",
        "Jack dies.",
        "Hermione ends up with Ron.",
        "Ned Stark dies.",
        "Captain America's friend, Bucky, doesn't die but instead ends up "
            "becoming The Winter Soldier.",
]

def pseudo_index():
    return render_template('index.html', my_string="Wheeeee!",
            my_list=[0,1,2,3,4,5])

@app.route("/")
def index():
    return pseudo_index()
    i = random.randrange(len(spoilers))
    spoiler = spoilers[i]
    return render_template("index.html", content=spoiler)

if __name__ == "__main__":
    app.run(debug=True)
