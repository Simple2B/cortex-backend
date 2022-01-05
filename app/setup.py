from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from fastapi_pagination import add_pagination

from app.routers import router
from app.config import settings


def create_app() -> FastAPI:
    """Create the application instance"""
    app = FastAPI(
        title=settings.SERVER_NAME,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @router.get("/", tags=["Root"])
    async def root():
        """Redirect to documentation"""
        return RedirectResponse(url="/api/docs")

    app.include_router(router)

    add_pagination(app)
    return app
