import logging
import uuid

from fastapi import APIRouter, Request, Response, status
from pydantic import BaseModel

from services.scheduler.config import Config
from services.scheduler.services import deploy_worker, stop_worker

logger = logging.getLogger(__name__)

config = Config()
router = APIRouter()


class SchedulerInfo(BaseModel):
    worker_image: str


@router.get("/")
async def info(
        request: Request,
) -> SchedulerInfo:
    return SchedulerInfo(
        worker_image=config.worker_image,
    )


@router.post("/worker/")
async def start_worker(
    request: Request,
) -> Response:
    await deploy_worker(
        namespace=config.namespace,
        worker_image=config.worker_image,
        worker_id=str(uuid.uuid4()),
    )

    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.delete("/worker/{worker_id}/")
async def stop_worker(
    request: Request,
    worker_id: str,
) -> Response:
    await stop_worker(
        namespace=config.namespace,
        worker_id=worker_id,
    )

    return Response(status_code=status.HTTP_202_ACCEPTED)
