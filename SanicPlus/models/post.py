from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Date, LargeBinary


Base = declarative_base()


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    description = Column(Text)
    image = Column(LargeBinary(length=None))
    user = Column(Text)
    type = Column(String(8))
    created_at = Column(Date, default=datetime.now())
    updated_at = Column(Date, default=None)

    def __init__(self, title, description, image, user, type):
        self.title = title
        self.description = description
        self.image = image
        self.user = user
        self.type = type

    def __repr__(self):
        return f'Post({self.id}, {self.title}, {self.description}, \
            {self.image}, {self.user_id}, {self.type})'
