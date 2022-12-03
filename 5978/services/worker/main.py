import logging

import uvicorn
from fastapi import FastAPI

from services.worker.routes import router

logger = logging.getLogger(__name__)

app = FastAPI(title="worker", debug=True)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8802, log_level="debug")
