from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, \
                password={self.password})>"
