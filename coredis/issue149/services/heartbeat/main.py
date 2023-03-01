import asyncio
import logging

import coredis.exceptions
from coredis import RedisCluster

from common.broker import create_broker_client
from common.protocol import Heartbeat
from services.heartbeat.config import Config

logger = logging.getLogger(__name__)


async def heartbeat(
    broker_client: RedisCluster, *, publish_every_sec: int, channel: str
) -> None:
    beat_id: int = 0

    while True:
        try:
            await broker_client.publish(channel, Heartbeat(id=beat_id).json())

            logger.debug(f"Published a message (beat_id: {beat_id})")
            beat_id += 1

            await asyncio.sleep(publish_every_sec)
        except asyncio.CancelledError:
            logger.debug("CancelledError: Stopping heartbeat")
            break
        except coredis.exceptions.ConnectionError as e:
            logger.debug(f"ConnectionError: Could not publish the message ({e!r}")


async def on_startup(config: Config) -> None:
    logger.debug("Initing heartbeat")
    broker_client = await create_broker_client(config.broker)

    await heartbeat(
        broker_client,
        channel=config.channel,
        publish_every_sec=config.publish_every_sec,
    )


if __name__ == "__main__":
    asyncio.run(on_startup(config=Config()))
