from consts import QUEUE_GET_NAME, QUEUE_POST_NAME, RABBIT_HOST_NAME
from Database.database import create_database_and_tables_if_not_exists
from consumer import (
    consumer_declare_queue,
    consumer_establish_connection_and_channel,
    consumer_process_get_message,
    consumer_process_post_message,
)
from functools import partial
import asyncio


async def main(loop):
    connection, channel = await consumer_establish_connection_and_channel(
        loop=loop, host=RABBIT_HOST_NAME
    )

    await channel.set_qos(prefetch_count=100)

    post_queue = await consumer_declare_queue(
        channel=channel, queue_name=QUEUE_POST_NAME
    )
    get_queue = await consumer_declare_queue(channel=channel, queue_name=QUEUE_GET_NAME)

    await post_queue.consume(
        partial(consumer_process_post_message, channel.default_exchange)
    )
    await get_queue.consume(
        partial(consumer_process_get_message, channel.default_exchange)
    )

    return connection


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(main(loop))
    create_database_and_tables_if_not_exists()
    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())
