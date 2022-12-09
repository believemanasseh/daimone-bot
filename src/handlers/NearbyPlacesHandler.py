import jsonpickle
from src.main import redis_cache
from src.utils import GoogleMaps

google_map = GoogleMaps()


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

            if keyword in {"none", "None"}:
                search_response = google_map.get_nearby_search(latitude, longitude)
            else:
                search_response = google_map.get_nearby_search(latitude, longitude, keyword=keyword)
            
            results = search_response["response"]["results"]
            if results:
                message = results
            else:
                message = "No results found."
        else:
            message = steps[deserialized_response_map["step"] - 1]
        deserialized_response_map["step"] += 1
        deserialized_response_map["response"].append(response)
        await cache.set(chat_id, jsonpickle.encode(deserialized_response_map), expire=5)
        return message


def get_steps():
    return [
        "Please share your location data",
        "Please input search keyword (if no _preferred_ keyword, type 'None')"
    ]
