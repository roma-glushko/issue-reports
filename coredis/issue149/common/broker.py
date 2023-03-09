import logging
from typing import Optional, Union

from coredis import RedisCluster
from coredis import exceptions as RedisExceptions
from pydantic import BaseSettings, Field, SecretStr

logger = logging.getLogger(__name__)


class BrokerConfig(BaseSettings):
    host: str = Field(default="localhost", env="BROKER_HOST")
    port: int = Field(default=6379, env="BROKER_PORT")

    username: Optional[SecretStr] = Field(default=None, env="BROKER_USERNAME")
    password: Optional[SecretStr] = Field(default=None, env="BROKER_PASSWORD")

    db: Union[str, int] = Field(
        default="0",
        env="BROKER_DB",
    )

    cluster_require_full_coverage: bool = Field(
        default=False, env="BROKER_REQUIRE_FULL_COVERAGE"
    )
    read_from_replicas: bool = Field(default=False, env="BROKER_READ_FROM_REPLICAS")
    follow_cluster: bool = Field(default=False, env="BROKER_FOLLOW_CLUSTER")

def create_redis_cluster_client(broker_config: BrokerConfig) -> RedisCluster:
    username: Optional[SecretStr] = broker_config.username
    password: Optional[SecretStr] = broker_config.password

    # solution for saas
    cluster_client = RedisCluster(
        host=broker_config.host,
        port=broker_config.port,
        username=username.get_secret_value() if username else None,
        password=password.get_secret_value() if password else None,
        skip_full_coverage_check=not broker_config.cluster_require_full_coverage,
        read_from_replicas=broker_config.read_from_replicas,
        nodemanager_follow_cluster=broker_config.follow_cluster,
        connect_timeout=1,
    )

    return cluster_client


async def create_broker_client(broker_config: BrokerConfig) -> RedisCluster:
    try:
        redis_client = create_redis_cluster_client(broker_config)

        logger.debug(
            "Connecting to broker (redis cluster)...",
            extra={"broker_config": broker_config},
        )

        pong = await redis_client.ping()
        logger.debug(
            "Has been connected to broker (redis cluster)",
            extra={
                "pong": pong,
            },
        )

        return redis_client
    except RedisExceptions.ConnectionError as e:
        logger.warning(
            "Could not connect to broker. Please double check your credentials",
            extra={
                "broker_config": broker_config,
            },
            exc_info=True,
        )
        raise e
