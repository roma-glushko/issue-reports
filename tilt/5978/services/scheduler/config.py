from pydantic import BaseSettings, Field


class Config(BaseSettings):
    namespace: str = Field(..., env="WORKER_NAMESPACE")
    worker_image: str = Field(..., env="WORKER_IMAGE")
