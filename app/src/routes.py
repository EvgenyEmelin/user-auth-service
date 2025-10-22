from fastapi import Depends, APIRouter, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.core.database import get_async_session
from app.src.crud import get_user_by_email, get_user_by_id, create_user, update_user, delete_user
from app.src.models import User
from app.src.schemas import UserRead, UserCreate, UserUpdate

router = APIRouter(tags=["Users"], prefix="/users")

@router.get('/id/{user_id}', response_model=UserRead)
async def get_user_by_id_router(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user = await get_user_by_id(user_id, session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get('/email/{user_email}', response_model=UserRead)
async def get_user_by_email_router(user_email: EmailStr, session: AsyncSession = Depends(get_async_session)):
    user = await get_user_by_email(user_email, session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post('/', response_model=UserRead)
async def create_user_router(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User).where(or_(User.email == user.email,User.username == user.username)))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    created_user = await create_user(user, session)
    return created_user

@router.put('/update/{user_id}', response_model=UserRead)
async def update_user_router(user_id:int,user_data: UserUpdate, session: AsyncSession = Depends(get_async_session)):
    user_db = await get_user_by_id(user_id, session)
    user = await update_user(user_db,user_data, session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete('/delete/{user_id}')
async def delete_user_router(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user = await delete_user(user_id, session)
    return user

