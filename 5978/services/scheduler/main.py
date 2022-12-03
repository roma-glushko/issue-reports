import logging
from functools import partial

import uvicorn
from fastapi import FastAPI
from kubernetes_asyncio import config

from services.scheduler.routes import router

logger = logging.getLogger(__name__)


async def on_startup(app: FastAPI) -> None:
    logger.debug("Starting the scheduler service..")

    await config.load_kube_config()


app = FastAPI(title="scheduler", debug=True)

app.include_router(router)
app.on_event('startup')(partial(on_startup, app))


if __name__ == "__main__":
    uvicorn.run("main:app", port=8801, log_level="debug")
