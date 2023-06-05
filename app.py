import os
import logging
from base64 import b64encode

import auth0
from sanic import Sanic
from sanic.response import html, json, redirect
from jinja2 import Environment, FileSystemLoader

from utils.auth import Auth
from utils.security import Security
from utils.db import DB


# Setup app
app = Sanic('jameshall_ninja_site')
port = os.environ.get('PORT')

# Initiate database, to do: add configuration options
db = DB(app)

# Setup jinja2
env = Environment(loader=FileSystemLoader('./public/templates'))
app.ctx.env = env

# Define the base template
base_template = env.get_template('base.html')
app.ctx.base_template = base_template

# Initialize the auth, security, db objects
auth = Auth(app, db)
security = Security()

# Define auth0 environment variables
client_id = os.environ("CLIENT_ID")
client_secret = os.environ("CLIENT_SECRET")
domain = os.environ("AUTH0_DOMAIN")

client = auth0.WebAuthClient(
    client_id=client_id,
    client_secret=client_secret,
    domain=domain,
    )

# Set the static folder
app.static('/public', './public')


@app.route("/")
async def homepage(request):
    # Get all the posts from the database
    posts = db.get_posts()

    # Convert the images to a base64 string
    for post in posts:
        post = b64encode(post.image)

    # Render the homepage template
    return html(env.get_template("index.html").render(
        posts=posts, request=request, current_page=request.path))


@app.route("/about")
async def about(request):
    # Render the "about" template
    return html(env.get_template("about.html").render(
        request=request, current_page=request.path))


@app.route("/contact")
async def contact(request):
    # If the form is valid, send email to the contact email address
    if request.form.is_valid():
        email = request.form.email.data
        message = request.form.message.data

        logging.info("Sending email to %s", email)
        security.send_email(email, message)

        # Render the contact page template with the form
        return html(env.get_template("contact.html").render(
            request=request, current_page=request.path))


@app.route("/blog")
async def blog(request):
    # Get the blog posts from firestore
    posts = db.get_post_by_type("Blog")

    # Render the blog page template with the blog posts
    return html(env.get_template("blog.html").render(
        posts=posts, request=request, current_page=request.path))


@app.route("/projects")
async def projects(request):
    # Get the project from the database
    posts = db.get_post_by_type("Project")

    # Render the projects page template with the projects
    return html(env.get_template("projects.html").render(
        posts=posts, request=request, current_page=request.path))


@app.route("/login")
async def login(request):
    # Get the authorization code from the request
    code = request.args.get("code")

    # Exchange the authorization code for tokens
    tokens = await client.get_tokens(code)

    # Authenticate the user with the access token
    user = await auth.verify_id_token(tokens["access_token"])

    # If the user is authenticated, redirect to the dashboard page
    if user:
        return redirect("/dashboard")

    # Otherwise, redirect to the login page
    return redirect("/login")


@app.route("/login/callback")
async def login_callback(request):
    # Get the access token from the request
    access_token = request.args.get("access_token")

    # Authenticate the user with the access token
    user = await auth.verify_id_token(access_token)

    # If the user is authenticated, redirect to the dashboard page
    if user:
        return redirect("/dashboard")

    # Otherwise, redirect to the login page
    return redirect("/login")


@app.route("/logout")
async def logout(request):
    # Revoke the user's access token
    await auth.revoke_access_token(request)

    # Redirect the user to the homepage
    return redirect("/")


@auth.protected
@app.route("/post")
async def get_post(request):
    # Authenticate the user
    user = await auth.authenticate(request)

    # If the user is not authenticated, redirect to the login page
    if not user:
        return html(env.get_template("login.html").render(
            request=request, current_page=request.path))

    # Render the post page template
    return html(env.get_template("post.html").render(
        request=request, current_page=request.path, user=user))


@auth.protected
@app.route("/post", methods=["POST"])
async def post_post(request):
    # Authenticate the user
    user = await auth.authenticate(request)

    # If the user is not authenticated, redirect to the login page
    if not user:
        return html(env.get_template("login.html").render(
            request=request, current_page=request.path))

    # Get the post data from the request
    title = request.form.get("title")
    description = request.form.get("description")
    image = request.form.get("image")
    type = request.form.get("type")

    # Validate the post data
    if not title:
        return json({"message": "Title is required"})
    if not description:
        return json({"message": "Description is required"})
    if not image:
        return json({"message": "Image is required"})
    if type not in ["blog", "project"]:
        return json({"message": "Type is invalid"})

    # Convert the image property to a bytes object
    image = image.encode('utf-8')

    # Save the post to the database
    db.create_post(title, description, image, user.username, type)

    return html(env.get_template("post.html").render(
        request=request, current_page=request.path, user=user))


@auth.protected
@app.route("/dashboard")
async def dashboard(request):
    # Authenticate the user
    user = await auth.authenticate(request)

    # If the user is not authenticated, redirect to the login page
    if not user:
        return html(env.get_template("login.html").render(
            request=request, current_page=request.path))

    # Render the dashboard page template
    return html(env.get_template("dashboard.html").render(
            request=request, current_page=request.path, user=user))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=False)
