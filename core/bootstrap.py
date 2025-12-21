from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqladmin import Admin
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from core.base_admin import AdminAuth
from core.database import engine
from core.config import settings
from tasks.routes import router as tasks_router
from tasks.admin import TaskAdmin
from tasks.tasks import my_first_task
from users.routes import router as users_router
from users.admin import UserAdmin

scheduler = AsyncIOScheduler()

def setup_admin(app: FastAPI) -> None:
    admin = Admin(
        app,
        engine,
        authentication_backend=AdminAuth(secret_key=settings.SQL_ADMIN_SECRET_KEY),
        templates_dir="./templates/sqladmin",
    )
    admin.add_view(UserAdmin)
    admin.add_view(TaskAdmin)


def setup_router(app: FastAPI) -> None:
    app.include_router(tasks_router)
    app.include_router(users_router)


def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def setup_app(app):
    setup_admin(app)
    setup_router(app)
    setup_middlewares(app)

@asynccontextmanager
async def lifespan(app:FastAPI):
    scheduler.add_job(my_first_task,IntervalTrigger(seconds=10))
    scheduler.start()
    FastAPICache.init(
        InMemoryBackend(),
        prefix="fastapi-cache",
    )
    yield
    scheduler.shutdown()