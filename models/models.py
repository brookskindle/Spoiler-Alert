from sqlalchemy import Column, Integer, String, Boolean
from database import Base


# Since we're using Flask-Login, User must be created a specific way:
# See: https://flask-login.readthedocs.org/en/latest/#your-user-class
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(160), unique=True)
    password = Column(String(64), unique=False)
    authenticated = Column(Boolean, default=False)

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
        return self.username


class Post(Base):
    """Represents a post made by a user."""
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    content = Column(String(160), unique=False)

    def __init__(self, content=None):
        self.content = content

    def __repr__(self):
        return "id={0}, content={1}".format(self.id, self.content)
