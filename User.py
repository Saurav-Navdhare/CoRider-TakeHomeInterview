import re
import bcrypt

class User:

    def __init__(self, name, email, password):
        name, email, password = name.strip(), email.strip(), password.strip()
        if " " in email or " " in password:
            raise Exception("Email and password cannot contain spaces")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise Exception("Invalid email")
        if(len(password) < 6):
            raise Exception("Password must be at least 6 characters")
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.name = name
        self.email = email
        self.password =  password_hash.decode('utf-8')

    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        # Check if the provided password matches the stored hash
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password
        }