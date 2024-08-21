from fastapi import APIRouter
from app.controllers import task_controller

router = APIRouter()
router.include_router(task_controller.router, prefix="/tasks", tags=["tasks"])
