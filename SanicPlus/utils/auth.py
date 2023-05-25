from cryptography.hazmat.primitives.asymmetric import rsa
import jwt
from sanic.response import redirect
from functools import wraps

from utils.security import Security


class Auth:
    def __init__(self, app, db):
        self.app = app
        self.db = db
        self.security = Security()

        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()

    async def authenticate(self, request):
        # Get the cookie
        cookie = request.cookies.get("user_token")

        if not cookie:
            return False

        # Decode the token
        token = jwt.decode(
                    cookie,
                    self.public_key,
                    algorithms=["RS256"]
                    )

        user = self.db.get_user_by_id(token["user_id"])
        if user:
            # Return the user
            return user

    def login(self, request, username, password):
        # Check if the username and password are valid
        password = password.encode("utf-8")
        hashed_password = self.db.get_password(username)

        if self.security.verify_password(password, hashed_password):
            # Get the user from the database
            user = self.db.get_user_by_username(username)

            # Define the payload
            token = jwt.encode(
                    {"user_id": user.id},
                    self.private_key,
                    algorithm="RS256"
                    )
            # Define the respone to bind the payload to
            response = redirect("/dashboard")

            # Set cookie
            response.add_cookie(
                    "user_token",
                    token,
                    secure=False,
                    max_age=6000000,
                    httponly=True
                    )
            return response

    async def protected(self, f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            user = await self.authenticate(request)

            if user:
                response = await f(request, user, *args, **kwargs)
                return response
        return decorated_function
