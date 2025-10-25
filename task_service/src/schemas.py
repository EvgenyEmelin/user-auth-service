from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class Task(BaseModel):
    title: str
    description: str
    is_completed: bool = False

class TaskCreate(Task):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

class TaskRead(BaseModel):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool
    is_superuser: bool

