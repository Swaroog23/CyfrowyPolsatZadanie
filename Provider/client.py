from aiohttp import web
from .publisher import (
    establish_connection_and_channel,
    publish_message_to_queue,
    publisher_declare_queue,
    publisher_queue_consume_callback,
)
from functools import partial
from .validators import validate_request_data
import json


async def get_value_from_key_async(request):
    key = request.match_info["id"]
    loop = request.loop
    future = loop.create_future()

    channel = await establish_connection_and_channel(loop)
    queue = await publisher_declare_queue(channel)

    await publish_message_to_queue(channel, key, "get", queue)
    await queue.consume(partial(publisher_queue_consume_callback, future))

    result = await future
    if result is None:
        return web.HTTPBadRequest(
            text="400: Object with this key does not exists"
            )
    return web.Response(text=f"{json.dumps(result[0])}")


async def post_key_value_async(request):
    body = await request.json()
    loop = request.loop
    future = loop.create_future()

    try:
        validate_request_data(body)
    except ValueError:
        return web.HTTPBadRequest(
            text="400: Not acceptable data format. Key must be numeric and value cannot be null"
            )

    channel = await establish_connection_and_channel(loop)
    queue = await publisher_declare_queue(channel)

    await publish_message_to_queue(channel, str(body), "post", queue)
    await queue.consume(partial(publisher_queue_consume_callback, future))

    result = await future
    if result is not None:
        return web.HTTPBadRequest(
            text="400: Object with this key already exists!"
            )
    return web.Response(text=f"Data saved: {body}")
