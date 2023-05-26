import bcrypt


class Security:
    def __init__(self):
        self.salt = bcrypt.gensalt(rounds=12)

    def hash_password(self, password):
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), self.salt)
        return hashed_password

    @staticmethod
    def verify_password(password, hashed_password):
        if password and hashed_password:
            return bcrypt.checkpw(password, hashed_password)

    def send_email(self, email, message):
        # TODO: Implement this method
        pass
