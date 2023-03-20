from fastapi import APIRouter

from app.result.views import result_router


api_router = APIRouter()


api_router.include_router(result_router, prefix="/results", tags=["Result"])
