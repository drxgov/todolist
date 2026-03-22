from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.security import get_current_user
from database import get_db
from models.tasks import Task
from models.user import User
from schemas.tasks import TaskCreate, TaskOut, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskOut)
async def create_tast(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = Task(**data.model_dump(), user_id=current_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/", response_model=list[TaskOut])
async def get_tasks(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return db.query(Task).filter(Task.user_id == current_user.id).all()


@router.patch("/{tasks_id}", response_model=TaskOut)
async def update_task(
    tasks_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = (
        db.query(Task)
        .filter(Task.id == tasks_id, Task.user_id == current_user.id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=401, detail="задача не найдена")
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{tasks_id}")
async def delete_task(
    tasks_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = (
        db.query(Task)
        .filter(Task.id == tasks_id, Task.user_id == current_user.id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="задача не найдена")
    db.delete(task)
    db.commit()
    return {"message": "задача удалена"}
