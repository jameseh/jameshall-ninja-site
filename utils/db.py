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
        # Create the collection "users"
        self.db.collection("users")

    def create_post_kind(self):
        # Create the collection "posts"
        self.db.collection("posts")

    def add_user(self, username, password):
        # Generate a unique ID
        user_id = uuid4()

        # Create a new user document
        user_document = {
            "id": user_id,
            "username": username,
            "password": password,
        }
        self.db.collection("users").document(user_id).set(user_document)

    def login(self, request, username, password):
        # Get the user document
        user_document = self.db.collection("users").document(username).get()

        # Check if the user exists and the password is correct
        if user_document is not None and self.security.verify_password(
                password, user_document.get("password")):
            return user_document
        return None

    def get_user_by_username(self, username):
        # Get the user document
        return self.db.collection("users").document(username).get()

    def get_user_by_id(self, user_id):
        # Get the user document
        return self.db.collection("users").document(user_id).get()

    def get_password(self, username):
        # Get the user document
        user_document = self.db.collection("users").document(username).get()

        # Check if the user exists
        if user_document is not None:
            return user_document.get("password")
        return None

    def get_posts(self):
        # Get all posts
        return self.db.collection("posts").get()

    def get_post(self, id):
        # Get the post document
        return self.db.collection("posts").document(id).get()

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
        self.db.collection("posts").document().set(post_document)

    def update_post(self, id, title, description, image, user, type,
                    created_at):
        # Get the post document
        post_document = self.db.collection("posts").document(id).get()

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
        self.db.collection("posts").document(id).set(post_document)

    def delete_post(self, id):
        # Delete the post document
        self.db.collection("posts").document(id).delete()
