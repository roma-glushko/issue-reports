from pydantic import BaseSettings, Field

from common.broker import BrokerConfig


class Config(BaseSettings):
    broker: BrokerConfig = Field(default_factory=BrokerConfig)
    channel: str = Field(default="channels/heartbeat", env="TRACKER_CHANNEL")
