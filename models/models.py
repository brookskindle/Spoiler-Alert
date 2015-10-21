# TODO: use db.Model instead of Base
from flask.est.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Since we're using Flask-Login, User must be created a specific way:
# See: https://flask-login.readthedocs.org/en/latest/#your-user-class
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(160), unique=True)
    password = db.Column(db.String(64), unique=False)
    authenticated = db.Column(db.Boolean, default=False)

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

    def __init__(self, content=None):
        self.content = content

    def __repr__(self):
        return "id={0}, content={1}".format(self.id, self.content)
