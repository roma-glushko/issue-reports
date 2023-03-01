from pydantic import BaseSettings, Field

from common.broker import BrokerConfig


class Config(BaseSettings):
    broker: BrokerConfig = Field(default_factory=BrokerConfig)
    channel: str = Field(default="channels/heartbeat", env="HEARTBEAT_CHANNEL")
    publish_every_sec: int = Field(default=1, env="HEARTBEAT_PUBLISH_EVERY_SEC")
