from fastapi import APIRouter

from .auth import router as auth_router
from .client import router_client
from .test import router_test

router = APIRouter(prefix="/api")
router.include_router(auth_router)
router.include_router(router_client)
router.include_router(router_test)
