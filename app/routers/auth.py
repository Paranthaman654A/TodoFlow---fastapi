from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.auth import verify_password
from app.crud import (
    create_user,
    get_user_by_email,
    get_user_by_username,
)
from app.database import get_db
from app.schemas import UserCreate


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# =========================
# REGISTER
# =========================

@router.post("/register")
def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    existing_email = get_user_by_email(
        db,
        email
    )

    if existing_email:
        return RedirectResponse(
            url="/register?error=email_exists",
            status_code=status.HTTP_303_SEE_OTHER
        )

    existing_username = get_user_by_username(
        db,
        username
    )

    if existing_username:
        return RedirectResponse(
            url="/register?error=username_exists",
            status_code=status.HTTP_303_SEE_OTHER
        )

    user_data = UserCreate(
        username=username,
        email=email,
        password=password
    )

    create_user(
        db,
        user_data
    )

    return RedirectResponse(
        url="/login?registered=true",
        status_code=status.HTTP_303_SEE_OTHER
    )


# =========================
# LOGIN
# =========================

@router.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    user = get_user_by_email(
        db,
        email
    )

    if user is None:
        return RedirectResponse(
            url="/login?error=invalid_credentials",
            status_code=status.HTTP_303_SEE_OTHER
        )

    password_valid = verify_password(
        password,
        user.password_hash
    )

    if not password_valid:
        return RedirectResponse(
            url="/login?error=invalid_credentials",
            status_code=status.HTTP_303_SEE_OTHER
        )

    response = RedirectResponse(
        url="/dashboard",
        status_code=status.HTTP_303_SEE_OTHER
    )

    response.set_cookie(
        key="session_token",
        value=str(user.id),
        httponly=True,
        samesite="lax"
    )

    return response


# =========================
# LOGOUT
# =========================

@router.get("/logout")
def logout():

    response = RedirectResponse(
        url="/login?logout=true",
        status_code=status.HTTP_303_SEE_OTHER
    )

    response.delete_cookie(
        key="session_token"
    )

    return response