# file for models and mock user data
# We’ll use werkzeug.security for hashing and verification.

from werkzeug.security import generate_password_hash, check_password_hash

# Mock user database
users = {}

# Register a new user
def register_user(username, password):
    if username in users:
        return False  # User already exists
    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
    users[username] = hashed_password
    return True


# Verify user credentials
def verify_user(username, password):
    hashed_password = users.get(username)
    if hashed_password and check_password_hash(hashed_password, password):
        return True
    return False
