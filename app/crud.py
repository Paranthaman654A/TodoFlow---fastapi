from datetime import datetime

from sqlalchemy.orm import Session

from app.auth import hash_password
from app.models import Task, User
from app.schemas import TaskCreate, TaskUpdate, UserCreate


# =========================
# USER CRUD OPERATIONS
# =========================

def get_user_by_email(
    db: Session,
    email: str
) -> User | None:
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def get_user_by_username(
    db: Session,
    username: str
) -> User | None:
    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )


def create_user(
    db: Session,
    user_data: UserCreate
) -> User:

    hashed_password = hash_password(
        user_data.password
    )

    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# =========================
# TASK CRUD OPERATIONS
# =========================

def create_task(
    db: Session,
    task_data: TaskCreate,
    user_id: int
) -> Task:

    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        due_time=task_data.due_time,
        reminder_time=task_data.reminder_time
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_user_tasks(
    db: Session,
    user_id: int
) -> list[Task]:

    return (
        db.query(Task)
        .filter(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
        .all()
    )


def get_task_by_id(
    db: Session,
    task_id: int,
    user_id: int
) -> Task | None:

    return (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == user_id
        )
        .first()
    )


def update_task(
    db: Session,
    task: Task,
    task_data: TaskUpdate
) -> Task:

    update_data = task_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


def delete_task(
    db: Session,
    task: Task
) -> None:

    db.delete(task)
    db.commit()


def toggle_task_completion(
    db: Session,
    task: Task
) -> Task:

    task.completed = not task.completed

    db.commit()
    db.refresh(task)

    return task


def get_due_tasks(
    db: Session,
    user_id: int
) -> list[Task]:

    now = datetime.utcnow()

    return (
        db.query(Task)
        .filter(
            Task.user_id == user_id,
            Task.due_time.isnot(None),
            Task.due_time <= now,
            Task.completed.is_(False)
        )
        .order_by(Task.due_time.asc())
        .all()
    )