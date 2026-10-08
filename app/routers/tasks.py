from datetime import datetime

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.crud import (
    create_task,
    delete_task,
    get_task_by_id,
    get_user_tasks,
    toggle_task_completion,
    update_task,
)
from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import TaskCreate, TaskUpdate


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# =========================
# CREATE TASK
# =========================

@router.post("/")
def add_task(
    title: str = Form(...),
    description: str | None = Form(default=None),
    due_time: str | None = Form(default=None),
    reminder_time: str | None = Form(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    parsed_due_time = None
    parsed_reminder_time = None

    if due_time:
        parsed_due_time = datetime.fromisoformat(
            due_time
        )

    if reminder_time:
        parsed_reminder_time = datetime.fromisoformat(
            reminder_time
        )

    task_data = TaskCreate(
        title=title,
        description=description,
        due_time=parsed_due_time,
        reminder_time=parsed_reminder_time
    )

    create_task(
        db=db,
        task_data=task_data,
        user_id=current_user.id
    )

    return RedirectResponse(
        url="/dashboard",
        status_code=status.HTTP_303_SEE_OTHER
    )


# =========================
# GET ALL USER TASKS
# =========================

@router.get("/")
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_user_tasks(
        db=db,
        user_id=current_user.id
    )


# =========================
# GET SINGLE TASK
# =========================

@router.get("/{task_id}")
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    task = get_task_by_id(
        db=db,
        task_id=task_id,
        user_id=current_user.id
    )

    if task is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


# =========================
# UPDATE TASK
# =========================

@router.put("/{task_id}")
def edit_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    task = get_task_by_id(
        db=db,
        task_id=task_id,
        user_id=current_user.id
    )

    if task is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return update_task(
        db=db,
        task=task,
        task_data=task_data
    )


# =========================
# DELETE TASK
# =========================

@router.delete("/{task_id}")
def remove_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    task = get_task_by_id(
        db=db,
        task_id=task_id,
        user_id=current_user.id
    )

    if task is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    delete_task(
        db=db,
        task=task
    )

    return {
        "message": "Task deleted successfully"
    }


# =========================
# TOGGLE TASK COMPLETION
# =========================

@router.patch("/{task_id}/complete")
def complete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    task = get_task_by_id(
        db=db,
        task_id=task_id,
        user_id=current_user.id
    )

    if task is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return toggle_task_completion(
        db=db,
        task=task
    )