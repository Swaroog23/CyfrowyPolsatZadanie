from consumer import consumer_declare_exchage_and_queue, consumer_establish_connection_and_channel, consumer_process_message
import asyncio


async def main(loop):
    connection, channel = await consumer_establish_connection_and_channel(loop=loop)
    await channel.set_qos(prefetch_count=100)

    queue = await consumer_declare_exchage_and_queue(channel, "post")
    await queue.consume(consumer_process_message, exclusive=True)
    print("WAITING FOR MESSAGES")
    return connection


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(main(loop))

    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())