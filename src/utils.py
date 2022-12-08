import json
import requests
from src.config import settings


def send_message(data):
    url = settings.BOT_ENDPOINT + "/sendMessage"
    response = requests.post(url, json=data)
    json_response = response.json()
    return {"status_code": response.status_code, "response": json_response}
