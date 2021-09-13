from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from app.routers import router
from app.config import settings


def create_app() -> FastAPI:
    """Create the application instance"""
    app = FastAPI(title=settings.SERVER_NAME)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    @app.get("/", tags=["Root"])
    async def root():
        """Redirect to documentation"""
        return RedirectResponse(url="/docs")

    add_pagination(app)
    return app
