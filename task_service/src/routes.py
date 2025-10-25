from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from task_service.core.database import get_db
from task_service.src.dependencies import get_current_user
from task_service.src.schemas import TaskRead, TaskCreate, User, TaskUpdate
from task_service.src.crud import create_task, get_task, get_tasks_by_owner, update_task, delete_task



router = APIRouter(tags=["Tasks"], prefix="/task")

@router.post("/create", response_model=TaskRead)
async def create_task_route(
    task: TaskCreate,
    session: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return await create_task(task, current_user, session)

@router.get("/{task_id}", response_model=TaskRead)
async def read_task_route(
    task_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    task = await get_task(task_id, session)
    if not task or task.owner_id != current_user:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/", response_model=list[TaskRead])
async def read_tasks_route(
    session: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return await get_tasks_by_owner(current_user, session)

@router.put("/{task_id}", response_model=TaskRead)
async def update_task_route(
    task_id: int,
    task_data: TaskUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    task = await get_task(task_id, session)
    if not task or task.owner_id != current_user:
        raise HTTPException(status_code=404, detail="Task not found")
    return await update_task(task, task_data, session)

@router.delete("/{task_id}")
async def delete_task_route(
    task_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    task = await get_task(task_id, session)
    if not task or task.owner_id != current_user:
        raise HTTPException(status_code=404, detail="Task not found")
    await delete_task(task, session)
    return {"detail": "Task deleted successfully"}