from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from models.user import User
from models.post import Post
from utils.security import Security


class DB:
    def __init__(self, app):
        self.app = app
        self.engine = create_engine(f"sqlite:///{self.app.config.DB_NAME}")
        self.session = sessionmaker(bind=self.engine)
        self.security = Security()
        self.create_user_table()
        self.create_post_table()

    def create_database(self, db_name):
        self.engine.execute(
                f"CREATE DATABASE IF NOT EXISTS {self.app.config.DB_NAME}")

    def create_user_table(self):
        # Create the table "users"
        session = self.get_session()
        session.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              username VARCHAR(255),
              password VARCHAR(255)
              );
            """))

        # Commit the changes to the database
        session.commit()

        # Close the session
        session.close()

    def create_post_table(self):
        # Create the table "posts"
        session = self.get_session()
        session.execute(text("""
            CREATE TABLE IF NOT EXISTS posts (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              title VARCHAR(255),
              description TEXT,
              image LONGBLOB,
              user TEXT,
              type VARCHAR(255),
              created_at DATETIME,
              updated_at DATETIME
              );
            """))
        session.commit()

        # Close the session
        session.close()

    def set_session(self, request, username, password):
        with self.get_session() as session:
            user = User(id, username, password)
            session.add(user)
            session.commit()

    def get_session(self):
        return self.session()

    def add_user(self, username, password):
        with self.get_session() as session:
            user = User(username, password)
            session.add(user)
            session.commit()
            session.refresh(user)  # refresh the user to get the assigned ID
        return user

    def login(self, request, username, password):
        user = self.db.query(User).filter_by(username=username).first()
        if user is not None and self.security.verify_password(
                password, user.password):
            self.session.commit()
            return user
        return None

    def get_user_by_username(self, username):
        with self.get_session() as session:
            return session.query(User).filter_by(username=username).first()

    def get_user_by_id(self, user_id):
        with self.get_session() as session:
            return session.query(User).filter_by(id=user_id).first()

    def get_password(self, username):
        with self.get_session() as session:
            user = session.query(User).filter_by(username=username).first()
            if user is not None:
                return user.password
        return None

    def get_posts(self):
        with self.get_session() as session:
            return session.query(Post).all()

    def get_post(self, id):
        with self.get_session() as session:
            return session.query(Post).filter_by(id=id).first()

    def create_post(self, title, description, image, user, type):
        with self.get_session() as session:
            # Get the current transaction
            transaction = session.begin()

            # Add the post to the transaction
            post = Post(title, description, image, user, type)
            session.add(post)

            # Commit the transaction
            transaction.commit()

            # Refresh the post
            session.refresh(post)

            return post

    def update_post(self, id, title, description, image, user, type,
                    created_at):
        with self.get_session() as session:
            post = session.query(Post).filter_by(id=id).first()
            post.id = id
            post.title = title
            post.description = description
            post.image = image
            post.type = type
            post.created_at = created_at
            post.updated_at = post.updated  # todo
            session.commit()
            return post

    def delete_post(self, id):
        with self.get_session() as session:
            post = session.query(Post).filter_by(id=id).first()
            session.delete(post)
            session.commit()
            return post
