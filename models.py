from pydantic import BaseModel


class WeatherRequest(BaseModel):
    city: str


class WeatherResponse(BaseModel):
    city: str
    temperature: float
    humidity: int
    description: str