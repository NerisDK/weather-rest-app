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
        self.session = aiohttp.ClientSession()
        
    async def __aexit__(self, exc_type, exc_value, ext_tb):
        await self.session.close()

    async def _request(self, method: str, url: str) -> ClientResponse:
        response = await session.request(method, url)

        if response.status == 200: # OK
        # TODO: Добавить обработку других кодов
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
                city = data.get('name'),
                temperature = round(
                    int(data.get('main').get('temp')) - 273.15, 2),
                humidity = data.get('main').get('humidity'),
                description = data.get('weather')[0].get('description'),
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

