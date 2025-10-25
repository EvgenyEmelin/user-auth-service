from datetime import timedelta
from dotenv import load_dotenv
from fastapi import Depends, APIRouter, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from user_service.core.database import get_async_session
from user_service.src.crud import get_user_by_email, get_user_by_id, create_user, update_user, delete_user
from user_service.src.dependency import get_current_user, superuser_required
from user_service.src.models import User
from user_service.src.schemas import UserRead, UserCreate, UserUpdate, Token, UserLogin
from user_service.src.service import verify_password, create_token
router = APIRouter(tags=["Users"], prefix="/user")
load_dotenv()
@router.get('/id/{user_id}', response_model=UserRead)
async def get_user_by_id_router(user_id: int, session: AsyncSession = Depends(get_async_session), current_user: str = Depends(get_current_user)):
    user = await get_user_by_id(user_id, session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
@router.get('/email/{user_email}', response_model=UserRead)
async def get_user_by_email_router(user_email: EmailStr, session: AsyncSession = Depends(get_async_session), current_user: str = Depends(get_current_user)):
    user = await get_user_by_email(user_email, session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
@router.post('/create', response_model=UserRead)
async def create_user_router(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User).where(or_(User.email == user.email,User.username == user.username)))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    created_user = await create_user(user, session)
    return created_user
@router.put('/update/{user_id}', response_model=UserRead)
async def update_user_router(user_id:int,user_data: UserUpdate, session: AsyncSession = Depends(get_async_session), current_user: str = Depends(get_current_user)):
    user_db = await get_user_by_id(user_id, session)
    user = await update_user(user_db,user_data, session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
@router.delete('/delete/{user_id}', dependencies=[Depends(superuser_required)])
async def delete_user_router(user_id: int , session: AsyncSession = Depends(get_async_session), current_user: str = Depends(get_current_user)):
    user = await delete_user(user_id, session)
    return user
@router.post('/login', response_model=Token)
async def login_user(user: UserLogin, session: AsyncSession = Depends(get_async_session)):
    stmt = await session.execute(select(User).where(User.email == user.email))
    existing_user = stmt.scalar_one_or_none()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    user_data = {
        'user_id': existing_user.id,
        'username': existing_user.username,
        'email': existing_user.email,
        'role': existing_user.role,
        'is_active': existing_user.is_active,
        'is_superuser': existing_user.is_superuser,
        'is_verified': existing_user.is_verified,
    }
    access_token_expires = timedelta(minutes=15)
    access_token = create_token(user_data, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}
@router.put('/promote/{user_id}', response_model=UserRead)
async def promote_user_to_superuser(user_id: int, session: AsyncSession = Depends(get_async_session), current_user_id: str = Depends(get_current_user)):
    current_user = await get_user_by_id(current_user_id, session)
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="You are not a superuser")
    user = await get_user_by_id(user_id, session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_superuser = True
    await session.commit()
    await session.refresh(user)
    return user