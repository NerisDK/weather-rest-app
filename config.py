import os

from dotenv import load_dotenv


load_dotenv()

_WEATHER_APP_KEY = os.getenv("WEATHER_APP_KEY") 
_WEATHER_APP_BASE_URL = os.getenv("WEATHER_APP_BASE_URL")


def get_app_key():
    return _WEATHER_APP_KEY

def get_app_url():
    return _WEATHER_APP_BASE_URL