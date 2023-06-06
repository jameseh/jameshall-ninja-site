from sanic.response import redirect
from functools import wraps

from utils.security import Security


class Auth:
    def __init__(self, app, db, auth0_client):
        self.app = app
        self.db = db
        self.security = Security()
        self.auth0_client = auth0_client

    async def authenticate(self, request):
        # Get the access token from the request
        access_token = request.headers.get("Authorization")

        if not access_token:
            return False

        # Get the user from Auth0
        user = await self.auth0_client.get_user(access_token)

        if user:
            # Return the user
            return user

    def login(self, request, code):
        # Exchange the code for an access token and ID token
        tokens = await self.auth0_client.get_tokens_from_code(code)

        # Get the user from Auth0
        user = await self.auth0_client.get_user(tokens["access_token"])

        # Set the user in the session
        request.session["user"] = user

        # Redirect the user to the dashboard page
        return redirect("/dashboard")

    async def protected(self, f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # Authenticate the user
            user = await self.auth0_client.get_user(request)

            if user:
                response = await f(request, user, *args, **kwargs)
                return response
            else:
                return redirect("/login")
        return decorated_function
