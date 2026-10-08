from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.crud import get_user_tasks
from app.database import get_db
from app.dependencies import get_current_user
from app.models import User


router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


# =========================
# HOME PAGE
# =========================

@router.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


# =========================
# LOGIN PAGE
# =========================

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):

    error = request.query_params.get("error")
    registered = request.query_params.get("registered")
    logout = request.query_params.get("logout")

    message = None
    message_type = None

    if error == "invalid_credentials":

        message = "Invalid email or password."
        message_type = "error"

    elif registered == "true":

        message = "Account created successfully. Please login."
        message_type = "success"

    elif logout == "true":

        message = "You have been logged out."
        message_type = "success"

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "message": message,
            "message_type": message_type
        }
    )


# =========================
# REGISTER PAGE
# =========================

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):

    error = request.query_params.get("error")

    message = None

    if error == "email_exists":

        message = "Email is already registered."

    elif error == "username_exists":

        message = "Username already exists."

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "message": message
        }
    )


# =========================
# DASHBOARD
# =========================

@router.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    tasks = get_user_tasks(
        db=db,
        user_id=current_user.id
    )

    # Count only incomplete tasks
    total_tasks = sum(
        1 for task in tasks
        if not task.completed
    )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "user": current_user,
            "tasks": tasks,
            "total_tasks": total_tasks
        }
    )


# =========================
# 404 PAGE
# =========================

@router.get(
    "/404",
    response_class=HTMLResponse
)
def page_not_found(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="404.html",
        context={}
    )