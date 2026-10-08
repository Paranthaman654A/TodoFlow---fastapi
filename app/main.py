from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import models
from app.database import Base, engine
from app.routers import auth, pages, tasks


# =========================
# CREATE FASTAPI APP
# =========================

app = FastAPI(
    title="Todo List App",
    description="A full-stack Todo application built with FastAPI",
    version="1.0.0"
)


# =========================
# CREATE DATABASE TABLES
# =========================

Base.metadata.create_all(
    bind=engine
)


# =========================
# STATIC FILES
# =========================

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


# =========================
# ROUTERS
# =========================

app.include_router(
    pages.router
)

app.include_router(
    auth.router
)

app.include_router(
    tasks.router
)