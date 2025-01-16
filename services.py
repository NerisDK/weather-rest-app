import asyncio

import aiohttp
from aiohttp import ClientResponse
from fastapi import HTTPException
from pydantic import ValidationError

from models import WeatherRequest, WeatherResponse
# некоторые либы не используется


class WeatherApiService():

    def __init__(self, api_key:str, base_url: str) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.session = aiohttp.ClientSession()
        # сделать self.session как property (создавать если нет, отдавать если есть)
        
    async def __aexit__(self, exc_type, exc_value, ext_tb):
        await self.session.close()
        # вроде бы это используется у контекстного метода. если так, то он здесь не нужен

    async def _request(self, method: str, url: str) -> ClientResponse:
        response = await session.request(method, url) # ошибка

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
            # лучше отдельным методом делать парсер, либо в модели (у пайдантика ВРОДЕ есть возможность делать), либо в самой либе, зависит от того планируется ли переиспользовать либу
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
        # этот построенный url можно хранить в селф, меняется только город, который можно указывать внутри внешнего метода
        return f'{self.base_url}?appid={self.api_key}&q={place.city}'

# разделить комментарием публичные и приватные методы (просто для визуального удобства)