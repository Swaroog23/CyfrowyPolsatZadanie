from aiohttp import web
from client import get_value_from_key_async, post_key_value_async


app = web.Application()
app.add_routes(
    [
        web.get(r"/get-value/{id:\d+}", get_value_from_key_async),
        web.post("/add-value", post_key_value_async),
    ]
)


if __name__ == "__main__":
    pass
