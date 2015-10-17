from sqlalchemy import Column, Integer, String
from database import Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    content = Column(String(160), unique=False)

    def __init__(self, content=None):
        self.content = content

    def __repr__(self):
        return "id={0}, content={1}".format(self.id, self.content)
