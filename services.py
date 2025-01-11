import asyncio

import aiohttp
from aiohttp import ClientResponse
from fastapi import HTTPException
from pydantic import ValidationError

from models import WeatherRequest, WeatherResponse


class WeatherApiService():

    def __init__(self, api_key:str, base_url: str) -> None:
        self.api_key = api_key
        self.base_url = base_url
        

    async def _request(self, method: str, url: str) -> ClientResponse:

        async with aiohttp.ClientSession() as session:
            print(url)
            response = await session.request(method, url)

            if response.status == 200: # OK
                return response
            else:
                raise HTTPException(
                    status_code=response.status,
                    detail="Not Found")

    
    async def _get_weather_by_url(self, url: str) -> WeatherResponse:
        response = await self._request("GET", url)

        data = await response.json()

        try:
            return WeatherResponse(
                city = data['name'],
                temperature = round(
                    int(data['main']['temp']) - 273.15, 2),
                humidity = data['main']['humidity'],
                description = data['weather'][0]['description'],
            ) 
        except ValidationError as e:
            raise HTTPException(
               status_code=422,
               detail='Invalid or no data'
            ) 

    async def get_weather(self, place: WeatherRequest) -> WeatherResponse:
        url = self._build_url(place)

        return await self._get_weather_by_url(url)

    def _build_url(self, place: WeatherRequest) -> str:
        return f'{self.base_url}?appid={self.api_key}&q={place.city}'

