import jsonpickle
from src.main import redis_cache
from src.utils import GoogleMap

google_map = GoogleMap()


class NearbyPlacesHandler:
    @classmethod
    async def handle(cls, chat_id: int, response: str):
        steps = get_steps()
        cache = redis_cache()
        deserialized_response_map = jsonpickle.decode(await cache.get(chat_id))
        print(deserialized_response_map)
        if deserialized_response_map["step"] == 3:
            latitude = deserialized_response_map["location"]["latitude"]
            longitude = deserialized_response_map["location"]["latitude"]
            keyword = deserialized_response_map["response"][-1]
            response = google_map.get_nearby_search(latitude, longitude, keyword=keyword)
            message = response["response"]
        else:
            message = steps[deserialized_response_map["step"] - 1]
        deserialized_response_map["step"] += 1
        deserialized_response_map["response"].append(response)
        await cache.set(chat_id, jsonpickle.encode(deserialized_response_map))
        return message


def get_steps():
    return [
        "Please share your location data",
        "Please input search keyword"
    ]