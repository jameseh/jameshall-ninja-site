from uuid import uuid4

from google.cloud import datastore

from utils.security import Security


class DB:
    def __init__(self, app):
        self.app = app
        self.db = datastore.Client()
        self.security = Security()
        self.create_user_kind()
        self.create_post_kind()

    def create_user_kind(self):
        # Create the kind "users"
        self.db.kind("users")

    def create_post_kind(self):
        # Create the kind "posts"
        self.db.kind("posts")

    def add_user(self, username, password):
        # Generate a unique ID
        user_id = uuid4()

        # Create a new user entity
        user_entity = datastore.Entity(kind="users")
        user_entity.update({
            "id": user_id,
            "username": username,
            "password": password,
        })
        self.db.put(user_entity)

    def login(self, request, username, password):
        # Get the user entity
        user_entity = self.db.query(kind="users").filter(
                "username", username).get()

        # Check if the user exists and the password is correct
        if user_entity is not None and self.security.verify_password(
                password, user_entity.get("password")):
            return user_entity
        return None

    def get_user_by_username(self, username):
        # Get the user entity
        return self.db.query(kind="users").filter("username", username).get()

    def get_user_by_id(self, user_id):
        # Get the user entity
        return self.db.query(kind="users").filter("id", user_id).get()

    def get_password(self, username):
        # Get the user entity
        user_entity = self.db.query(kind="users").filter(
                "username", username).get()

        # Check if the user exists
        if user_entity is not None:
            return user_entity.get("password")
        return None

    def get_posts(self):
        # Get all posts
        return self.db.query(kind="posts").fetch()

    def get_post(self, id):
        # Get the post entity
        return self.db.query(kind="posts").filter("id", id).get()

    def create_post(self, title, description, image, user, type):
        # Create a new post entity
        post_entity = datastore.Entity(kind="posts")
        post_entity.update({
            "title": title,
            "description": description,
            "image": image,
            "user": user,
            "type": type,
            "created_at": datastore.DateTime.now(),
            "updated_at": "",
        })
        self.db.put(post_entity)

    def update_post(self, id, title, description, image, user, type,
                    created_at):
        # Get the post entity
        post_entity = self.db.query(kind="posts").filter("id", id).get()

        # Update the post entity
        post_entity.update({
            "title": title,
            "description": description,
            "image": image,
            "user": user,
            "type": type,
            "created_at": created_at,
            "updated_at": datastore.DateTime.now(),
        })
        self.db.put(post_entity)

    def delete_post(self, id):
        # Get the post entity
        post_entity = self.db.query(kind="posts").filter("id", id).get()

        # Delete the post entity
        self.db.delete(post_entity)
