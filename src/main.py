import jsonpickle
import re
from typing import Union

from fastapi_cache import caches, close_caches
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend

from fastapi import Depends, FastAPI, Header, status

from handlers import NearbyPlacesHandler, WelcomeHandler
from src.base import Request
from src.config import settings
from src.utils import send_message

app = FastAPI()


def redis_cache():
    return caches.get(CACHE_KEY)


def retrieve_handler(text):
    handlers = {"Nearby Places Recommendation": NearbyPlacesHandler}
    return handlers[text]


@app.get("/")
def home():
    return "Welcome to daimone-bot"


@app.post("/webhook")
async def webhook(
    request: Request,
    x_telegram_bot_api_secret_token: Union[str, None] = Header(default=None),
    cache: RedisCacheBackend = Depends(redis_cache),
):
    print(request.message)
    if not x_telegram_bot_api_secret_token:
        return status.HTTP_400_BAD_REQUEST

    if x_telegram_bot_api_secret_token != settings.SECRET_TOKEN:
        return status.HTTP_400_BAD_REQUEST

    username = request.message["from"]["username"]
    chat_id = request.message["chat"]["id"]
    message = request.message.get("text")
    location = request.message.get("location")

    context = {"step": 0, "response": []}

    current_response_map = await cache.get(chat_id)
    print(current_response_map, "Her")
    if not current_response_map:
        await cache.set(chat_id, jsonpickle.encode(context), expire=5)

    current_response_map = await cache.get(chat_id)
    deserialized_response_map = jsonpickle.decode(current_response_map)

    if message:
        if re.search("^([a-zA-Z]|\d)+", message):
            if deserialized_response_map["step"] == 0:
                deserialized_response_map["step"] += 1
                deserialized_response_map["response"].append(message)
                await cache.set(chat_id, jsonpickle.encode(deserialized_response_map), expire=5)
                return send_message(
                    {
                        "chat_id": chat_id,
                        "text": WelcomeHandler.handle(username),
                        "reply_markup": {
                            "keyboard": [
                                [{"text": "Nearby Places Recommendation"}],
                                [{"text": "Places Search"}],
                            ],
                            "resize_keyboard": True,
                            "one_time_keyboard": True,
                            "input_field_placeholder": "Select a suitable option",
                        },
                    }
                )
            elif deserialized_response_map["step"] == 1:
                deserialized_response_map["handler"] = retrieve_handler(message)
                await cache.set(chat_id, jsonpickle.encode(deserialized_response_map))
    
    if location:
        location = request.message.get("location")
        deserialized_response_map["location"] = location
        await cache.set(chat_id, jsonpickle.encode(deserialized_response_map))

    message = await deserialized_response_map["handler"].handle(chat_id, message)
    return send_message({"chat_id": chat_id, "text": message})


@app.on_event('startup')
async def on_startup():
    rc = RedisCacheBackend('redis://127.0.0.1:6379/0')
    caches.set(CACHE_KEY, rc)


@app.on_event('shutdown')
async def on_shutdown():
    await close_caches()
