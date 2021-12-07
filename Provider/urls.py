from aiohttp import web
from .client import get_value_from_key_async, post_key_value_async


app = web.Application()
app.add_routes(
    [
        web.get("/get-value/{id}", get_value_from_key_async),
        web.post("/add-value", post_key_value_async),
    ]
)

web.run_app(app)
