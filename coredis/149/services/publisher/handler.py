import asyncio

from coredis import RedisCluster

async def publish_messages(broker_client: RedisCluster, *, publish_every_sec: int, channel: str) -> None:

    while True:
        try:
            ...
            await asyncio.sleep(publish_every_sec)
        except Exception:
            ...