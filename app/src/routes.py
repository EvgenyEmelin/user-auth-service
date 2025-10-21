import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_async_session
from app.src.models import User
from app.src.schemas import UserRegisterIn, UserRegisterOut, UserLoginIn, UserLoginOut, Token

from app.src.service import hash_password, verify_password, create_token

import hashlib

router = APIRouter()

@router.post("/register", response_model=UserRegisterOut)
async def register(user: UserRegisterIn, session: AsyncSession = Depends(get_async_session)):
    stmt = await session.execute(select(User).where(User.email == user.email))
    result = stmt.scalar()
    if result:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        user_password = hash_password(user.password)
        new_user = User(email=user.email, hashed_password=user_password.decode("utf8"))
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

@router.post("/login", response_model=UserLoginOut)
async def login(user: UserLoginIn, session: AsyncSession = Depends(get_async_session)):
    stmt = await session.execute(select(User).where(User.email == user.email))
    result = stmt.scalar()
    if not result:
        raise HTTPException(status_code=400, detail="Incorrect login or password")

    sha256_hash = hashlib.sha256(user.password.encode('utf-8')).digest()

    if not bcrypt.checkpw(sha256_hash, result.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Incorrect login or password")

    access_token = create_token({"sub": result.email, "id": result.id})

    return UserLoginOut(
        id=result.id,
        email=result.email,
        is_active=result.is_active,
        token=Token(access_token=access_token, token_type="bearer")
    )


