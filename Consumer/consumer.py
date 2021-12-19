import asyncio
from Database.database import get_data_from_db, insert_data_to_db
from ast import literal_eval
from aio_pika import (
    connect_robust,
    Message,
    DeliveryMode,
    Channel,
    Connection,
    Queue,
    IncomingMessage,
    Exchange,
)
import pickle


async def consumer_establish_connection_and_channel_async(
    async_loop: asyncio.AbstractEventLoop, host: str
) -> list[Connection, Channel]:
    connection = await connect_robust(host=host, loop=async_loop)
    channel = await connection.channel()
    return [connection, channel]


async def consumer_declare_queue_async(channel: Channel, queue_name: str) -> Queue:
    queue = await channel.declare_queue(queue_name, durable=True)
    return queue


async def consumer_process_post_message_async(
    exchange: Exchange, message: IncomingMessage
) -> None:
    async with message.process():
        data = literal_eval(message.body.decode("utf-8"))
        result_list = []
        for key, value in data.items():
            result_list.append(insert_data_to_db(key, value))

        await exchange.publish(
            Message(
                body=pickle.dumps(result_list),
                correlation_id=message.correlation_id,
                delivery_mode=DeliveryMode.PERSISTENT,
            ),
            message.reply_to,
        )


async def consumer_process_get_message_async(
    exchange: Exchange, message: IncomingMessage
) -> None:
    async with message.process():
        key = message.body.decode("utf-8")
        db_result = get_data_from_db(key)

        await exchange.publish(
            Message(
                body=pickle.dumps(db_result), correlation_id=message.correlation_id
            ),
            message.reply_to,
        )
