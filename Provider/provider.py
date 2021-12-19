from functools import partial
import pickle
from consts import RABBIT_HOST_NAME
from aio_pika import connect_robust, Message, DeliveryMode
import uuid


async def provider_establish_connection_and_channel(loop, host):
    connection = await connect_robust(host=host, loop=loop)
    channel = await connection.channel()
    return channel


async def provider_declare_queue(channel):
    queue = await channel.declare_queue(exclusive=True, durable=True)
    return queue


async def provider_send_message(channel, message, routing_key, callback_queue):
    await channel.default_exchange.publish(
        Message(
            body="{}".format(message).encode(),
            correlation_id=str(uuid.uuid4()),
            reply_to=callback_queue.name,
            delivery_mode=DeliveryMode.PERSISTENT,
        ),
        routing_key,
    )


async def provider_queue_consume_callback(future, message):
    with message.process():
        return future.set_result(pickle.loads(message.body))


async def provider_send_message_and_await_response(
    async_loop, message, queue_name, host=RABBIT_HOST_NAME
):
    future = async_loop.create_future()
    channel = await provider_establish_connection_and_channel(async_loop, host)
    queue = await provider_declare_queue(channel)

    await provider_send_message(channel, str(message), queue_name, queue)

    await queue.consume(partial(provider_queue_consume_callback, future))
    return await future


if __name__ == "__main__":
    pass
