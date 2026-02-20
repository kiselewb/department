from fastapi import APIRouter
from app.api.v1.endpoints.plans import router as plans_router


router = APIRouter()
router.include_router(plans_router)
