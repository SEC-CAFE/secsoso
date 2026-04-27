from fastapi import APIRouter
from src.routers import search


router = APIRouter()
router.include_router(search.router, tags=["search"], prefix="/search")
# router.include_router(auth.router, tags=["authentication"], prefix="/api/auth")
# router.include_router(settings.router, tags=["settings"], prefix="/api/settings")
