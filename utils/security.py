from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from flask import current_app
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def hash_password(password):
    """
    Securely hash a password using PBKDF2 (works in Python 3.9+)
    """
    try:
        # Explicitly use PBKDF2 with SHA256 to avoid scrypt issues in Python < 3.10
        return generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=16
        )
    except Exception as e:
        logger.error(f"Password hashing failed: {str(e)}")
        raise ValueError("Could not hash password") from e

def verify_password(hashed_password, password):
    """
    Verify a password against its hash
    """
    try:
        return check_password_hash(hashed_password, password)
    except Exception as e:
        logger.error(f"Password verification failed: {str(e)}")
        return False

def create_jwt_token(user_id):
    """
    Create a JWT token with 7-day expiration
    """
    try:
        expires = datetime.utcnow() + timedelta(days=7)
        return jwt.encode(
            {
                'user_id': user_id,
                'exp': expires
            },
            current_app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )
    except Exception as e:
        logger.error(f"JWT creation failed: {str(e)}")
        raise ValueError("Could not create token") from e

def decode_jwt_token(token):
    """
    Decode and verify a JWT token
    """
    try:
        payload = jwt.decode(
            token,
            current_app.config['JWT_SECRET_KEY'],
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Expired JWT token")
        return None
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid JWT token: {str(e)}")
        return None