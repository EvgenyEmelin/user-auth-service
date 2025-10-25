from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from task_service.core.database import get_db
from task_service.src.schemas import Task, TaskCreate, TaskUpdate, TaskRead, User
from task_service.src.model import TaskModel




async def get_task(task_id: int, session: AsyncSession) -> Task | None:
    result = await session.execute(select(TaskModel).where(TaskModel.id == task_id))
    return result.scalar_one_or_none()

async def get_tasks_by_owner(owner_id: int, session: AsyncSession):
    result = await session.execute(select(TaskModel).where(TaskModel.owner_id == owner_id))
    return result.scalars().all()

async def create_task(task: TaskCreate,owner_id: int,session: AsyncSession) -> Task:
    new_task = TaskModel(
        title=task.title,
        description=task.description,
        owner_id=owner_id,
        is_completed=task.is_completed if task.is_completed is not None else False
    )
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    return new_task

async def update_task(task: Task, task_data: TaskUpdate, session: AsyncSession):
    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(task, key, value)
    await session.commit()
    await session.refresh(task)
    return task

async def delete_task(task: Task, session: AsyncSession):
    await session.delete(task)
    await session.commit()