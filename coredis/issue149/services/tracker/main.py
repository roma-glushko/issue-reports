import asyncio
import json
import logging
import sys
from datetime import datetime
from typing import cast

import coredis
from coredis import RedisCluster

from common.broker import create_broker_client
from common.protocol import Heartbeat
from services.tracker.config import Config

logging.basicConfig(
    format="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
    stream=sys.stdout,
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)


async def track(broker_client: RedisCluster, *, channel: str) -> None:
    logger.debug(f"Initing subscription to the {channel} channel")
    subscription = broker_client.pubsub()

    await subscription.subscribe(channel)

    while True:
        try:
            message = await subscription.get_message(
                ignore_subscribe_messages=True, timeout=1.0
            )

            now: datetime = datetime.utcnow()

            if message is not None:
                data: bytes = cast(bytes, message.get("data"))
                beat_data = Heartbeat(**json.loads(data))

                logger.debug(
                    f"Received a message: {beat_data.dict()} (took {now - beat_data.created_at} to receive)"
                )

        except asyncio.CancelledError:
            logger.debug("CancelledError: Stopping tracker")
            break
        except coredis.exceptions.ConnectionError as e:
            logger.warning(f"ConnectionError: Could not read a message ({e!r}")

async def on_startup(config: Config) -> None:
    logger.debug("Initing tracker")
    broker_client = await create_broker_client(config.broker)

    await track(broker_client, channel=config.channel)


if __name__ == "__main__":
    asyncio.run(on_startup(config=Config()))
