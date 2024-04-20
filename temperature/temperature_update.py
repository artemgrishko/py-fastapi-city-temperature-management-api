from httpx import AsyncClient
from fastapi import HTTPException

from settings import settings
from temperature import crud
from city.crud import get_cities


async def fetch_temperatures(db):
    async with AsyncClient() as client:
        cities = get_cities(db)
        for city in cities:
            response = await client.get(
                settings.WEATHER_API_URL,
                params={"key": settings.WEATHER_API_KEY, "q": city.name}
            )
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
