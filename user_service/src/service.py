import os
from datetime import timedelta, datetime

from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext

load_dotenv()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(user_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(user_password, hashed_password)

def create_token(payload:dict, expires_delta:timedelta | None = None):
    to_encode = payload.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm="HS256")
    return encoded_jwt
