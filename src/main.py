import json
import re
from typing import Union

from fastapi_cache import caches, close_caches
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend
from fastapi import Depends, FastAPI, Header, status

from base import Request
from config import settings
from utils import send_message

app = FastAPI()


@app.on_event("startup")
async def on_startup() -> None:
    rc = RedisCacheBackend("redis://127.0.0.1:6379")
    caches.set(CACHE_KEY, rc)


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await close_caches()


def redis_cache():
    return caches.get(CACHE_KEY)


@app.get("/")
def home():
    return "Welcome to daimone-bot"


@app.post("/webhook")
async def webhook(
    request: Request,
    x_telegram_bot_api_secret_token: Union[str, None] = Header(default=None),
    cache: RedisCacheBackend = Depends(redis_cache),
):
    if not x_telegram_bot_api_secret_token:
        return status.HTTP_400_BAD_REQUEST

    if x_telegram_bot_api_secret_token != settings.SECRET_TOKEN:
        return status.HTTP_400_BAD_REQUEST

    username = request.message["from"]["username"]
    chat_id = request.message["chat"]["id"]
    message = request.message["message"]["text"]

    context = {"step": 0, "response": []}

    current_response_map = await cache.get(username)
    if not current_response_map:
        await cache.set(chat_id, json.dumps(context))

    if re.search("^([a-zA-Z]|\d)+", message):
        send_message({"chat_id": chat_id, "text": "Hello"})

    return status.HTTP_200_OK
