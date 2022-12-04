import logging

from fastapi import APIRouter, Request, status
from pydantic import BaseModel

from services.worker.config import Config

logger = logging.getLogger(__name__)

config = Config()
router = APIRouter()


class WorkerInfo(BaseModel):
    id: str
    image: str


@router.get("/", status_code=status.HTTP_200_OK)
async def info(
    request: Request,
) -> WorkerInfo:
    return WorkerInfo(
        id=config.worker_id,
        image=config.worker_image,
    )
