import aio_pika


async def establish_connection_and_channel(host=""):
    connection = await aio_pika.connect_robust()
    channel = await connection.channel()
    return [connection, channel]


async def publisher_declare_exchange(channel, exchange_name):
    exchange = await channel.declare_exchange(exchange_name)
    return exchange


async def publish_message_to_exchange(exchange, message, routing_key):
    await exchange.publish(
        aio_pika.Message(body="{}".format(message).encode()), routing_key
    )
