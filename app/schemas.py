from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# =========================
# USER SCHEMAS
# =========================

class UserBase(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50
    )

    email: str = Field(
        min_length=5,
        max_length=100
    )


class UserCreate(UserBase):
    password: str = Field(
        min_length=8,
        max_length=100
    )


class UserLogin(BaseModel):
    email: str = Field(
        min_length=5,
        max_length=100
    )

    password: str = Field(
        min_length=8,
        max_length=100
    )


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================
# TASK SCHEMAS
# =========================

class TaskBase(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200
    )

    description: str | None = None

    due_time: datetime | None = None

    reminder_time: datetime | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200
    )

    description: str | None = None

    completed: bool | None = None

    due_time: datetime | None = None

    reminder_time: datetime | None = None


class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    due_time: datetime | None
    reminder_time: datetime | None

    model_config = ConfigDict(
        from_attributes=True
    )