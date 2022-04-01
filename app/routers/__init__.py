from fastapi import APIRouter

from .auth import router as auth_router
from .client import router_client
from .test import router_test
from .clients_intake import router_clients_intake
from .clients_queue import router_clients_queue
from .note import router_note
from .stripe import router_stripe
from .visits import router_visits

router = APIRouter(prefix="/api")
router.include_router(auth_router)
router.include_router(router_client)
router.include_router(router_test)
router.include_router(router_clients_intake)
router.include_router(router_clients_queue)
router.include_router(router_note)
router.include_router(router_stripe)
router.include_router(router_visits)
