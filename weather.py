# Author : Massoud Ibrahim
# Date 2024-06-04
# weather.py file has the functions required for /weather command.

#pip install pytz
# https://timeapi.io/ used this for the Swagger
import aiohttp
import os
import pytz
import discord
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
TIMEZONE_API_KEY = os.getenv('TIMEZONE_API_KEY')

weather_emojis = {
    "clear sky": ":sunny:",
    "few clouds": ":white_sun_small_cloud:",
    "scattered clouds": ":white_sun_behind_cloud:",
    "overcast clouds": ":cloud:",
    "shower rain": ":cloud_rain:",
    "rain": ":cloud_rain:",
    "thunderstorm": ":thunder_cloud_rain:",
    "snow": ":cloud_snow:",
    "mist": ":fog:",
    "haze": ":fog:"
}

def get_weather_emoji(description, local_hour_str):
    if 23 <= local_hour_str or local_hour_str < 6:
        return ":crescent_moon:"

    description = description.lower()
    if "rain" in description:
        return ":cloud_rain:"
    elif "cloud" in description:
        return ":cloud:"
    elif "snow" in description:
        return ":cloud_snow:"
    elif "mist" in description:
        return ":fog:"
    return weather_emojis.get(description)

async def get_timezone(lat: float, lon: float):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://timeapi.io/api/Time/current/coordinate?latitude={lat}&longitude={lon}"
        ) as response:
            if response.status == 200:
                data = await response.json()
                timezone_name = data['timeZone']
                local_date_str = data['date']
                local_time_str = data['time']
                local_day_str = data['dayOfWeek']
                local_hour_str = data['hour']
                return timezone_name, local_date_str, local_time_str, local_day_str, local_hour_str
            else:
                return None, None


async def get_weather(city: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        ) as response:
            if response.status == 200:
                data = await response.json()
                weather_description = data['weather'][0]['description']
                temperature = data['main']['temp']
                feels_like = data['main']['feels_like']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']
                farenheit = format((temperature * 9/5) + 32, ".2f")
                feels_like_fahrenheit = format((feels_like * 9 / 5) + 32, ".2f")

                lat = data['coord']['lat']
                lon = data['coord']['lon']

                timezone_name, local_date_str, local_time_str, local_day_str, local_hour_str = await get_timezone(lat, lon)
                # The color that will be the embed for better interface
                color = discord.Color.yellow() if not (
                            23 <= local_hour_str or local_hour_str < 6) else discord.Color.dark_blue()

                if timezone_name:
                    weather_info = (
                        f"**Current local time**:\n"
                        f"{timezone_name}\n"
                        f"{local_date_str}, {local_day_str}, {local_time_str}\n\n"
                        f"** :thermometer: Temperature**: {temperature}°C / {farenheit}°F \n"
                        f"   **Feels like**: {feels_like}°C / {feels_like_fahrenheit}°F \n"
                        f"Humidity: {humidity}%\n"
                        f"{weather_description}\n"
                    )

                    emoji = get_weather_emoji(weather_description, local_hour_str)
                    return weather_info, emoji, color
                else:
                    return None
            else:
                return None
