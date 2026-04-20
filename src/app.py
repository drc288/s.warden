from fastapi import FastAPI

from src.core.settings import settings
from src.modules.health.presentation.routers import router as health_router
from src.modules.incidents.presentation.router import router as incidents_router

app = FastAPI(
    title=settings.APPLICATION_TITLE,
    description=settings.APPLICATION_DESCRIPTION,
    version=settings.APPLICATION_VERSION,
    debug=settings.APPLICATION_ENVIRONMENT != "production",
)

routers = [health_router, incidents_router]

for router in routers:
    app.include_router(router)
