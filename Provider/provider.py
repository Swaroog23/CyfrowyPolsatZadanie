from functools import partial
from typing import Any
from consts import RABBIT_HOST_NAME
from aio_pika import (
    connect_robust,
    Message,
    DeliveryMode,
    Channel,
    Queue,
    IncomingMessage,
)
import pickle
import uuid
import asyncio


async def provider_establish_connection_and_channel_async(
    async_loop: asyncio.AbstractEventLoop, host: str
) -> Channel:
    connection = await connect_robust(host=host, loop=async_loop)
    channel = await connection.channel()
    return channel


async def provider_declare_queue_async(channel: Channel) -> Queue:
    queue = await channel.declare_queue(exclusive=True, durable=True)
    return queue


async def provider_send_message_async(
    channel: Channel, message: str, routing_key: str, callback_queue: Queue
) -> None:
    await channel.default_exchange.publish(
        Message(
            body="{}".format(message).encode(),
            correlation_id=str(uuid.uuid4()),
            reply_to=callback_queue.name,
            delivery_mode=DeliveryMode.PERSISTENT,
        ),
        routing_key,
    )


async def provider_queue_consume_callback_async(
    future: asyncio.Future, message: IncomingMessage
) -> asyncio.Future:
    with message.process():
        return future.set_result(pickle.loads(message.body))


async def provider_send_message_and_await_response_async(
    async_loop: asyncio.AbstractEventLoop,
    message_to_send: Any,
    queue_name: str,
    host: str = RABBIT_HOST_NAME,
) -> asyncio.Future:
    future = async_loop.create_future()
    channel = await provider_establish_connection_and_channel_async(async_loop, host)
    queue = await provider_declare_queue_async(channel)

    await provider_send_message_async(channel, str(message_to_send), queue_name, queue)

    await queue.consume(partial(provider_queue_consume_callback_async, future))
    return await future


if __name__ == "__main__":
    pass
