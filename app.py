import os
import logging
from base64 import b64encode

from auth0.authentication import Social
from sanic import Sanic
from sanic.response import html, json, redirect
from jinja2 import Environment, FileSystemLoader

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

# Create an instance of the Social class
social_auth = Social(
    client_id=os.environ.get("CLIENT_ID"),
    client_secret=os.environ.get("CLIENT_SECRET"),
    domain=os.environ.get("AUTH0_DOMAIN"),
)

# Initialize the auth, security, db objects
security = Security()

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


@app.route("/login")
async def login(request):
    # Redirect the user to the Google login page
    response = await social_auth.login(
            request.get["access_token"], "google")
    return response


@app.route("/login/callback")
async def login_callback(request):
    # Set a timelimit on the cookie
    cookie_max_age = 60 * 60 * 24 * 7

    # Set the response
    response = redirect("/dashboard")

    # Set the cookie
    response.set_cookie(
        response=request.response,
        user_id=request.args["user_id"],
        cookie_max_age=cookie_max_age,
    )

    # Redirect the user to the dashboard page
    return response


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


@app.route("/post")
async def get_post(request):
    # Get the user_id from cookie
    user = request.cookies.get("user_id")

    # If the user is not authenticated, redirect to the login page
    if not user:
        return html(env.get_template("login.html").render(
            request=request, current_page=request.path))

    # Get the post from the database
    post = db.get_post(request.args.get("id"))

    # If the post does not exist, redirect to the homepage
    if not post:
        return redirect("/")

    # Render the post page template
    return html(env.get_template("post.html").render(
        post=post, request=request, current_page=request.path, user=user))


@app.route("/post", methods=["POST"])
async def post_post(request):
    # Get the user_id from cookie
    user = request.cookies.get("user_id")

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


@app.route("/dashboard")
async def dashboard(request):
    # Get the user_id from cookie
    user = request.cookies.get("user_id")

    # If the user is not authenticated, redirect to the login page
    if not user:
        return html(env.get_template("login.html").render(
            request=request, current_page=request.path))

    # Get the user's posts from the database
    posts = db.get_posts_by_user(user.username)

    # Render the dashboard page template with the user's posts
    return html(env.get_template("dashboard.html").render(
        posts=posts, request=request, current_page=request.path, user=user))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(port), debug=False)
