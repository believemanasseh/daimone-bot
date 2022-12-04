from fastapi import FastAPI, Header, status
from pydantic import BaseModel
from config import settings

app = FastAPI()

class Request(BaseModel):
    update_id: str
    message: dict | None = None


@app.get("/")
async def home():
    return "Welcome to daimone-bot"


@app.post("/webhook")
async def webhook(request: Request, x_telegram_bot_api_secret_token: str | None = Header(default=None)):
   
    if not x_telegram_bot_api_secret_token:
        return status.HTTP_400_BAD_REQUEST

    if x_telegram_bot_api_secret_token != settings.SECRET_TOKEN:
        return status.HTTP_400_BAD_REQUEST
    
    return settings.SECRET_TOKEN
    