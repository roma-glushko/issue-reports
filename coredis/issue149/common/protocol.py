from datetime import datetime

from pydantic import BaseModel, Field


class Heartbeat(BaseModel):
    id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
