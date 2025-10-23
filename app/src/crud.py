from fastapi import HTTPException

from app.src.service import get_password_hash
from pydantic import EmailStr

from app.core.database import AsyncSession
from app.src.models import User
from app.src.schemas import UserCreate, UserUpdate

from sqlalchemy import select

async def get_user_by_id(user_id:int, session: AsyncSession):
    stmt = await session.execute(select(User).where(User.id == user_id))
    return stmt.scalar_one_or_none()

async def get_user_by_email(user_email: EmailStr, session: AsyncSession):
    stmt = await session.execute(select(User).where(User.email == user_email))
    return stmt.scalar_one_or_none()

async def create_user(user_data:UserCreate, session: AsyncSession):
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        username=user_data.username
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

async def update_user(user_db: User, user_data:UserUpdate, session: AsyncSession):
    update_data = user_data.dict(exclude_unset=True)
    if "username" in update_data and update_data["username"] != user_db.username:
        existing_user = await session.execute(
            select(User).where(User.username == update_data["username"])
        )
        if existing_user.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Username already exists")

    if "email" in update_data and update_data["email"] != user_db.email:
        existing_user = await session.execute(
            select(User).where(User.email == update_data["email"])
        )
        if existing_user.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already exists")
    if 'password' in update_data:
        update_data['password'] = get_password_hash(update_data.pop('password'))
    for key, value in update_data.items():
        setattr(user_db, key, value)
    await session.commit()
    await session.refresh(user_db)
    return user_db

async def delete_user(user_id: int, session: AsyncSession):
    stmt = await session.execute(select(User).where(User.id == user_id))
    result = stmt.scalar_one_or_none()
    if result:
        await session.delete(result)
        await session.commit()
    return result



