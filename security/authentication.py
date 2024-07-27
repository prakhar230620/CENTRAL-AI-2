import bcrypt
import jwt
import logging
from datetime import datetime, timedelta

class Authentication:
    def __init__(self, secret_key, token_expiry=30):
        self.secret_key = secret_key
        self.token_expiry = token_expiry  # in minutes
        self.logger = logging.getLogger(__name__)

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    def generate_token(self, user_id):
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(minutes=self.token_expiry)
        }
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        self.logger.info(f"Generated token for user {user_id}")
        return token

    def verify_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            self.logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError:
            self.logger.warning("Invalid token")
            return None

    def login(self, username, password, user_database):
        user = user_database.get(username)
        if user and self.check_password(password, user['password']):
            token = self.generate_token(user['id'])
            self.logger.info(f"User {username} logged in successfully")
            return token
        self.logger.warning(f"Failed login attempt for user {username}")
        return None

    def logout(self, token):
        # In a real-world scenario, you might want to invalidate the token
        # For simplicity, we'll just log the logout
        user_id = self.verify_token(token)
        if user_id:
            self.logger.info(f"User {user_id} logged out successfully")
            return True
        return False