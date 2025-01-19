import aiohttp
from aiohttp import ClientResponse
from fastapi import HTTPException
from pydantic import ValidationError

from models import WeatherRequest, WeatherResponse


class WeatherApiService:

    ## Class Methods ##
    def __init__(self, api_key: str, base_url: str) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self._session = None
        self._url_template = f"{self.base_url}?appid={self.api_key}&q={{city}}"

    @property
    def session(self) -> aiohttp.ClientSession:
        if self._session == None:
            self._session = aiohttp.ClientSession()
        return self._session


    ## Public Methods ##
    async def get_weather(self, place: WeatherRequest) -> WeatherResponse:
        url = await self._build_url(place)

        return await self._get_weather_by_url(url)


    ## Private Methods ##
    async def _request(self, method: str, url: str) -> ClientResponse:
        response = await self.session.request(method, url)

        if response.status == 200:  # OK
            # TODO: Добавить обработку других кодов
            return response
        else:
            raise HTTPException(status_code=response.status, detail="Not Found")

    async def _get_weather_by_url(self, url: str) -> WeatherResponse:
        response = await self._request("GET", url)

        data = await response.json()
        weather_info = await self._parse_data(data=data)

        return weather_info

    async def _build_url(self, place: WeatherRequest) -> str:
        return self._url_template.format(city=place.city)

    async def _parse_data(self, data: dict) -> WeatherResponse:
        try:
            return WeatherResponse(
                city=data.get("name"),
                temperature=round(int(data.get("main").get("temp")) - 273.15, 2),
                humidity=data.get("main").get("humidity"),
                description=data.get("weather")[0].get("description"),
            )

        except (KeyError, IndexError) as e:
            raise HTTPException(status_code=422, detail="Missing required fields")

        except ValidationError as e:
            raise HTTPException(status_code=422, detail="Invalid or no data")
