from Database.database import get_data_from_db, insert_data_to_db
from ast import literal_eval
import aio_pika
import pickle


async def consumer_establish_connection_and_channel(loop=None):
    if loop is not None:
        connection = await aio_pika.connect_robust(loop=loop)
    else:
        connection = await aio_pika.connect_robust()
    channel = await connection.channel()
    return [connection, channel]


async def consumer_declare_queue(channel, queue_name):
    queue = await channel.declare_queue(queue_name)
    return queue


async def consumer_process_post_message(message):
    async with message.process():
        data = literal_eval(message.body.decode("utf-8"))
        for key, value in data.items():
            insert_data_to_db(key, value)


async def consumer_process_get_message(exchange, message):
    async with message.process():
        key = message.body.decode("utf-8")
        db_result = get_data_from_db(key)

        await exchange.publish(
            aio_pika.Message(body=pickle.dumps(db_result), correlation_id=message.correlation_id),
            routing_key=message.reply_to,
        )
