# file for models and mock user data
# We’ll use werkzeug.security for hashing and verification.
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# Mock user database
#users = {}

# Register a new user
#def register_user(username, password):
#    if username in users:
#        return False  # User already exists
#    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
#    users[username] = hashed_password
#    return True


# Verify user credentials
#def verify_user(username, password):
#    hashed_password = users.get(username)
#    if hashed_password and check_password_hash(hashed_password, password):
#        return True
#    return False

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    