import asyncio
import os

import httpx
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException 

from models import WeatherResponse, WeatherRequest
from services import WeatherApiService
# убрать неиспользуемые либы


app = FastAPI()

load_dotenv()

WEATHER_APP_KEY = os.getenv("WEATHER_APP_KEY") 
WEATHER_APP_BASE_URL = os.getenv("WEATHER_APP_BASE_URL")
# подтягивать в другом файле (например, config.py), импортировать сюда

weatherApiService = WeatherApiService(
    api_key=WEATHER_APP_KEY,
    base_url=WEATHER_APP_BASE_URL
)
# лучше создавать объект при каждом запросе

@app.get("/weather")
async def get_weather(place: WeatherRequest) -> WeatherResponse:

    return await weatherApiService.get_weather(place)
    weatherApiService  # ???

# можно сделать автотесты, используя библиотеку, автотесты в последнюю очередь


if __name__ == "__main__":
    # asyncio.run(test_weather())

    uvicorn.run(app, host="127.0.0.1", port=8000)

# использовать либу black для форматирования кода
