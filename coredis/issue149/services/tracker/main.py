import asyncio
import logging

from coredis import RedisCluster

from common.broker import create_broker_client
from services.tracker.config import Config

logger = logging.getLogger(__name__)


async def track(broker_client: RedisCluster, *, channel: str) -> None:
    logger.debug(f"Initing subscription to the {channel} channel")
    subscription = broker_client.pubsub()

    await subscription.subscribe(channel)

    while True:
        try:
            message = await subscription.get_message(ignore_subscribe_messages=True, timeout=1.0)

            if message is not None:
                data = message.get("data")
                logger.debug(f"Received a message: {data}")

        except asyncio.CancelledError:
            logger.debug("CancelledError: Stopping tracker")
            break




async def on_startup(config: Config) -> None:
    logger.debug("Initing tracker")
    broker_client = await create_broker_client(config.broker)

    await track(broker_client, channel=config.channel)


if __name__ == "__main__":
    asyncio.run(on_startup(config=Config()))
