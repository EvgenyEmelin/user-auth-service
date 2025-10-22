from argon2 import PasswordHasher

ph = PasswordHasher()
def get_password_hash(password: str) -> str:
    return ph.hash(password)