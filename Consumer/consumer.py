from Database.database import get_data_from_db, insert_data_to_db
from ast import literal_eval
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


async def consumer_process_post_message(message):
    async with message.process():
        data = literal_eval(message.body.decode("utf-8"))
        print(f"MESSAGE RECIVED: {data.keys()}")
        for key, value in data.items():
            insert_data_to_db(key, value)


async def consumer_process_get_message(message):
    async with message.process():
        key = message.body.decode("utf-8")
        db_result = get_data_from_db(key)
        print(db_result)
        print(f"MESSAGE RECIVED: {message.body}")
