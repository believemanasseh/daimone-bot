import json
import requests
from src.config import settings, urls


def send_message(data):
    url = settings.BOT_ENDPOINT + "/sendMessage"
    response = requests.post(url, json=data)
    json_response = response.json()
    return {"status_code": response.status_code, "response": json_response}


class GoogleMap:
    def get_nearby_search(self, latitude, longitude, keyword=None):
        url = f"{urls.NEARBY_SEARCH_ENDPOINT}?keyword={keyword}&location={latitude}%2C{longitude}&radius=300000&key={settings.API_KEY}"
        response = requests.post(url)
        json_response = response.json()
        return {"status_code": response.status_code, "response": json_response}
        