import asyncio
import os

from httpx import AsyncClient
from fastapi import HTTPException

from settings import settings
from temperature import crud
from city.crud import get_cities


async def get_weather_api(city, client):
    result = await client.get(
        os.environ["WEATHER_API"],
        params={"key": settings.WEATHER_API_KEY, "q": city.name}
    )

    return result, city


async def fetch_temperatures(db):
    async with AsyncClient() as client:
        cities = get_cities(db)
        tasks = [get_weather_api(city, client) for city in cities]
        results = await asyncio.gather(*tasks)
        for response, city in results:
            if response.status_code == 200:
                temperature_data = response.json()
                if "temperature" in temperature_data:
                    crud.update_temperature(
                        db, city.id,
                        temperature_data["temperature"]
                    )
                else:
                    raise HTTPException(
                        status_code=404,
                        detail="Temperature data not found"
                    )
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to fetch temperature data"
                )

        return {"message": "Temperatures updated successfully"}
