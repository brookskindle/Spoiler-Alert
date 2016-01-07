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
from wtforms import BooleanField
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



def init_db():
    """Initializes the database."""
    db.create_all()


@login_manager.user_loader
def user_loader(user_id):
    """
    Return the User object from a given user_id
    """
    return User.query.get(int(user_id))



def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post)

if __name__ == "__main__":
    init_db()
    manager.add_command("shell", Shell(make_context=make_shell_context))
    manager.add_command("db", MigrateCommand)
    manager.run()
