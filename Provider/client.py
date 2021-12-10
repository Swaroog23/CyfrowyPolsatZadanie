from aiohttp import web
from .publisher import (
    establish_connection_and_channel,
    publish_message_to_exchange,
    publisher_declare_exchange,
)
import asyncio

async def get_value_from_key_async(request):
    key = request.match_info["id"]
    connection, channel = await establish_connection_and_channel("localhost")
    exchange = await publisher_declare_exchange(channel, "get")
    await publish_message_to_exchange(exchange, key, "get")
    await connection.close()
    return web.Response(text=f"hello!")


async def post_key_value_async(request):
    body = await request.json()
    connection, channel = await establish_connection_and_channel("localhost")
    exchange = await publisher_declare_exchange(channel, "post")
    await publish_message_to_exchange(exchange, str(body), "post")
    await connection.close()
    return web.Response(text=f"Id: {body}")
