import asyncio

from main import get_weather
from models import WeatherRequest


async def test_weather():
    city = WeatherRequest(city = "Baku") 
    city_weather = await get_weather(city)
    print(f"{city_weather}")


if __name__ == '__main__':
    asyncio.run(test_weather())

# использовать PyTest или Unittest для тестов!!!
