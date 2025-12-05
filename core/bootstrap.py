from fastapi import FastAPI
from tasks.routes import router as tasks_router
from users.routes import router as users_router
from sqladmin import Admin 
from core.base_admin import AdminAuth
from core.database import engine
from core.config import settings

from users.admin import UserAdmin
from tasks.admin import TaskAdmin


def setup_admin(app: FastAPI) -> None:
    admin = Admin(app, engine,authentication_backend=AdminAuth(secret_key=settings.SQL_ADMIN_SECRET_KEY),templates_dir='./templates/sqladmin')
    admin.add_view(UserAdmin)
    admin.add_view(TaskAdmin)

def setup_router(app: FastAPI) -> None:
    app.include_router(tasks_router)
    app.include_router(users_router)

def setup_middlewares(app: FastAPI) -> None:
    pass  


def setup_app(app):
    setup_admin(app)
    setup_router(app)
    setup_middlewares(app)