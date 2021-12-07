import aio_pika


async def consumer_establish_connection_and_channel(host="", loop=None):
    if loop is not None:
        connection = await aio_pika.connect_robust(loop=loop)
    else:
        connection = await aio_pika.connect_robust()
    channel = await connection.channel()
    return [connection, channel]


async def consumer_declare_exchage_and_queue(channel, exchange_name):
    exchange = await channel.declare_exchange(exchange_name)
    queue = await channel.declare_queue(auto_delete=True)
    await queue.bind(exchange, exchange_name)
    return queue


async def consumer_process_message(message):
    async with message.process():
        print(f"MESSAGE RECIVED: {message.body}")