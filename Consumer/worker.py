from Database.database import create_database_and_tables
from consumer import (
    consumer_declare_queue,
    consumer_establish_connection_and_channel,
    consumer_process_get_message,
    consumer_process_post_message
    )
from functools import partial
import asyncio


async def main(loop):
    connection, channel = await consumer_establish_connection_and_channel(loop=loop)
    await channel.set_qos(prefetch_count=100)
    post_queue = await consumer_declare_queue(channel, "post")
    get_queue = await consumer_declare_queue(channel, "get")

    await post_queue.consume(consumer_process_post_message)
    await get_queue.consume(partial(
        consumer_process_get_message, channel.default_exchange
        ))

    return connection


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(main(loop))
    create_database_and_tables()
    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())