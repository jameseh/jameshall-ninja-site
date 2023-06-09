from uuid import uuid4

from google.cloud import datastore

from utils.security import Security


class DB:
    def __init__(self, app):
        self.app = app
        self.db = datastore.Client()
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
        query = self.db.query(kind="users")
        query.filter("username", username)
        user_document = query.get()

        # Check if the user exists and the password is correct
        if user_document is not None and self.security.verify_password(
                password, user_document.get("password")):
            return user_document
        return None

    def get_user_by_username(self, username):
        # Get the user document
        query = self.db.query(kind="users")
        query.filter("username", username)
        user_document = query.get()
        return user_document

    def get_user_by_id(self, user_id):
        # Get the user document
        query = self.db.query(kind="users")
        query.filter("id", user_id)
        user_document = query.get()
        return user_document

    def get_password(self, username):
        # Get the user document
        query = self.db.query(kind="users")
        query.filter("username", username)
        user_document = query.get()

        # Check if the user exists
        if user_document is not None:
            return user_document.get("password")
        return None

    def get_posts(self):
        # Get all posts
        query = self.db.query(kind="posts")
        posts = list(query.fetch())
        return posts

    def get_post(self, id, type):
        # Get the post document
        query = self.db.query(kind="posts")
        query.filter("id", id)
        post_document = query.get()
        return post_document

    def get_posts_by_type(self, type):
        # Get the post documents
        posts = []
        query = self.db.query(kind="posts")
        query.add_filter("type", "=", type)
        while True:
            try:
                post = next(query.fetch())
                posts.append(post)
            except StopIteration:
                break
        return posts

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
        query = self.db.query(kind="posts")
        query.filter("id", id)
        post_document = query.get()

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
        query = self.db.query(kind="posts")
        query.filter("id", id)
        post_document = query.get()
        self.db.delete(post_document)
