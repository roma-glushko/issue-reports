from pydantic import BaseSettings, Field

from common.broker import BrokerConfig


class Config(BaseSettings):
    broker: BrokerConfig = Field(default_factory=BrokerConfig)
    channel: str
    publish_every_sec: int = 1