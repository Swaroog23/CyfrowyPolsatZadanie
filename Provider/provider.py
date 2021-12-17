from asyncio import futures
import pickle
import aio_pika
import uuid


async def provider_establish_connection_and_channel(loop, host):
    connection = await aio_pika.connect_robust(host=host,loop=loop)
    channel = await connection.channel()
    return channel


async def provider_declare_queue(channel):
    queue = await channel.declare_queue(exclusive=True)
    return queue


async def provider_send_message_to_queue(channel, message, routing_key, callback_queue):
    correlation_id = str(uuid.uuid4())
    await channel.default_exchange.publish(
        aio_pika.Message(
            body="{}".format(message).encode(),
            correlation_id=correlation_id,
            reply_to=callback_queue.name,
        ),
        routing_key,
    )
    return correlation_id


async def provider_queue_consume_callback(future, message):
    with message.process():
        return future.set_result(pickle.loads(message.body))


if __name__ == "__main__":
    pass
