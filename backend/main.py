from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import Session, select

from db import check_database_connection, get_session
from models import Task
from security import authorize_user

app = FastAPI(
    title="Todo App API",
    description="FastAPI backend for Todo App - Phase II",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response
class TaskCreate(BaseModel):
    title: str
    description: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


class TaskResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    updated_at: datetime


@app.get("/health")
def health_check() -> dict:
    """Health check endpoint returning server and database status."""
    is_connected, message = check_database_connection()
    return {
        "status": "ok",
        "database": message,
    }


# Task endpoints - all protected with auth
@app.get("/api/{user_id}/tasks", response_model=list[TaskResponse])
async def list_tasks(
    user_id: Annotated[str, Depends(authorize_user)],
    completed: bool | None = None,
    session: Session = Depends(get_session),
) -> list[Task]:
    """List all tasks for the authenticated user."""
    statement = select(Task).where(Task.user_id == UUID(user_id))
    if completed is not None:
        statement = statement.where(Task.completed == completed)
    statement = statement.order_by(Task.created_at.desc())
    tasks = session.exec(statement).all()
    return list(tasks)


@app.post(
    "/api/{user_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    user_id: Annotated[str, Depends(authorize_user)],
    task_data: TaskCreate,
    session: Session = Depends(get_session),
) -> Task:
    """Create a new task for the authenticated user."""
    task = Task(
        user_id=UUID(user_id),
        title=task_data.title,
        description=task_data.description,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.get("/api/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: Annotated[str, Depends(authorize_user)],
    task_id: UUID,
    session: Session = Depends(get_session),
) -> Task:
    """Get a specific task by ID."""
    task = session.get(Task, task_id)
    if not task or task.user_id != UUID(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@app.put("/api/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: Annotated[str, Depends(authorize_user)],
    task_id: UUID,
    task_data: TaskUpdate,
    session: Session = Depends(get_session),
) -> Task:
    """Update an existing task."""
    task = session.get(Task, task_id)
    if not task or task.user_id != UUID(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed

    task.updated_at = datetime.now(timezone.utc)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete(
    "/api/{user_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    user_id: Annotated[str, Depends(authorize_user)],
    task_id: UUID,
    session: Session = Depends(get_session),
) -> None:
    """Delete a task."""
    task = session.get(Task, task_id)
    if not task or task.user_id != UUID(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    session.delete(task)
    session.commit()


@app.patch("/api/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_complete(
    user_id: Annotated[str, Depends(authorize_user)],
    task_id: UUID,
    session: Session = Depends(get_session),
) -> Task:
    """Toggle the completion status of a task."""
    task = session.get(Task, task_id)
    if not task or task.user_id != UUID(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    task.completed = not task.completed
    task.updated_at = datetime.now(timezone.utc)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
