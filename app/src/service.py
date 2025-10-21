import hashlib
from datetime import timedelta, datetime
from typing import Optional

import bcrypt
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#Хэширование через SHA-256 и bcrypt для уменьшения длинны хэша пароля
def hash_password(password: str) -> bytes:
    sha256_hash = hashlib.sha256(password.encode('utf-8')).digest()
    bcrypt_hash = bcrypt.hashpw(sha256_hash, bcrypt.gensalt())
    return bcrypt_hash

#Верификация пароля
def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

#Создание JWT токена для юзера
def create_token(payload:dict, expires_delta: Optional[timedelta]=None) -> str:
    to_encode = payload.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, 'secret', algorithm='HS256')
    return encoded_jwt