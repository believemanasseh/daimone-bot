import jsonpickle
from src.main import redis_cache


class NearbyPlacesHandler:
    @classmethod
    async def handle(cls, chat_id: int):
        steps = get_steps()
        cache = redis_cache()
        deserialized_response_map = jsonpickle.decode(await cache.get(chat_id))
        message = steps[deserialized_response_map["step"] - 1]
        deserialized_response_map["step"] += 1
        deserialized_response_map["response"].append(message)
        await cache.set(chat_id, jsonpickle.encode(deserialized_response_map), expire=5)
        return message


def get_steps():
    return [
        "Please share your location data",
        "Please input search keyword"
    ]