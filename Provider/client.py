from consts import QUEUE_GET_NAME, QUEUE_POST_NAME
from aiohttp import web
from provider import (
    provider_send_message_and_await_response,
)
from functools import partial
from validators import validate_request_data, validate_result_from_queue
import json


async def get_value_from_key_async(request):
    key = request.match_info["id"]

    server_response = await provider_send_message_and_await_response(
        loop=request.loop, message=key, queue_name=QUEUE_GET_NAME
    )

    if server_response is None:
        return web.HTTPBadRequest(text="400: Object with this key does not exists")
    return web.Response(text=f"{json.dumps(server_response[0])}")


async def post_key_value_from_body_async(request):
    body = await request.json()

    try:
        validate_request_data(body)
    except ValueError:
        return web.HTTPBadRequest(
            text="400: Not acceptable data format. Key must be numeric and value cannot be null"
        )

    server_response = await provider_send_message_and_await_response(
        loop=request.loop, message=body, queue_name=QUEUE_POST_NAME
    )

    try:
        validate_result_from_queue(server_response)
    except ValueError:
        return web.HTTPBadRequest(text="400: Object with this key already exists!")

    return web.Response(text=f"Data saved: {body}")


if __name__ == "__main__":
    pass
