import asyncio
import logging

from common.broker import create_broker_client
from services.publisher.config import Config
from services.publisher.handler import publish_messages

logger = logging.getLogger(__name__)


async def on_startup(config: Config) -> None:
    broker_client = await create_broker_client(config.broker)

    await publish_messages(
        broker_client,
        channel=config.channel,
        publish_every_sec=config.publish_every_sec,
    )


if __name__ == "__main__":
    asyncio.run(on_startup(config=Config()))
