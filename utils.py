import requests
from config import settings


def send_message(chat_id, text, reply_markup):
    url = settings.BOT_ENDPOINT + "/sendMessage"
    data = {}
    response = requests.post(url, json=data)
    json_response = response.json()
    return {"status_code": response.status_code, "response": json_response}