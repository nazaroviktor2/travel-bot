from conf.config import settings
from fastapi import APIRouter

from webapp.api.v1.auth.router import auth_router
from webapp.api.v1.items.router import items_router

router = APIRouter(prefix=settings.API_V1)


router.include_router(auth_router, prefix="/auth", tags=["AUTH"])
router.include_router(items_router, prefix="/items", tags=["ITEMS"])
