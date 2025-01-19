import asyncio
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from models import WeatherResponse, WeatherRequest
from services import WeatherApiService
import config


app = FastAPI()

KEY = config.get_app_key()
URL = config.get_app_url()

weatherApiService = WeatherApiService(api_key=KEY, base_url=URL)


@app.get("/weather")
async def get_weather(place: WeatherRequest) -> WeatherResponse:

    return await weatherApiService.get_weather(place)


# можно сделать автотесты, используя библиотеку, автотесты в последнюю очередь


if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8000)

# использовать либу black для форматирования кода
