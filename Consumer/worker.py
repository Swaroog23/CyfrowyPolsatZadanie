from Database.database import create_database_and_tables
from consumer import (
    consumer_declare_exchage_and_queue,
    consumer_establish_connection_and_channel,
    consumer_process_get_message,
    consumer_process_post_message
    )
import asyncio


async def main(loop):
    connection, channel = await consumer_establish_connection_and_channel(loop=loop)
    await channel.set_qos(prefetch_count=100)

    post_queue = await consumer_declare_exchage_and_queue(channel, "post")
    get_queue = await consumer_declare_exchage_and_queue(channel, "get")
    await post_queue.consume(consumer_process_post_message, exclusive=True)
    await get_queue.consume(consumer_process_get_message, exclusive=True)
    print("WAITING FOR MESSAGES")
    return connection


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(main(loop))
    create_database_and_tables()
    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())