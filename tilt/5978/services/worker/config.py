from pydantic import BaseSettings, Field


class Config(BaseSettings):
    worker_id: str = Field(..., env="WORKER_ID")
    worker_image: str = Field(..., env="WORKER_IMAGE")
