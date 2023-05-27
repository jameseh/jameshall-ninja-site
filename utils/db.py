from uuid import uuid4
from os import environ

from google.cloud import datastore

from utils.security import Security


class DB:
    def __init__(self, app):
        self.app = app
        self.db = datastore.Client(environ("PROJECT_ID"))
        self.security = Security()

    def create_user_kind(self):
        # Create the collection "users"
        self.db.kind("users").create()

    def create_post_kind(self):
        # Create the collection "posts"
        self.db.kind("posts").create()

    def add_user(self, username, password):
        # Generate a unique ID
        user_id = uuid4()

        # Create a new user document
        user_document = {
            "id": user_id,
            "username": username,
            "password": password,
        }
        self.db.put(user_document)

    def login(self, request, username, password):
        # Get the user document
        user_document = self.db.query(kind="users").filter(
                "username", username).get()

        # Check if the user exists and the password is correct
        if user_document is not None and self.security.verify_password(
                password, user_document.get("password")):
            return user_document
        return None

    def get_user_by_username(self, username):
        # Get the user document
        return self.db.query(kind="users").filter("username", username).get()

    def get_user_by_id(self, user_id):
        # Get the user document
        return self.db.query(kind="users").filter("id", user_id).get()

    def get_password(self, username):
        # Get the user document
        user_document = self.db.query(kind="users").filter(
                "username", username).get()

        # Check if the user exists
        if user_document is not None:
            return user_document.get("password")
        return None

    def get_posts(self):
        # Get all posts
        query = self.db.query(kind="posts")
        return query.fetch()

    def get_post(self, id):
        # Get the post document
        return self.db.query(kind="posts").filter("id", id).get()

    def create_post(self, title, description, image, user, type):
        # Create a new post document
        post_document = {
            "title": title,
            "description": description,
            "image": image,
            "user": user,
            "type": type,
            "created_at": datastore.Timestamp.now(),
            "updated_at": "",
        }
        self.db.put(post_document)

    def update_post(self, id, title, description, image, user, type,
                    created_at):
        # Get the post document
        post_document = self.db.query(kind="posts").filter("id", id).get()

        # Update the post document
        post_document.update({
            "title": title,
            "description": description,
            "image": image,
            "user": user,
            "type": type,
            "created_at": created_at,
            "updated_at": datastore.Timestamp.now(),
        })
        self.db.put(post_document)

    def delete_post(self, id):
        # Delete the post document
        self.db.query(kind="posts").filter("id", id).delete()
