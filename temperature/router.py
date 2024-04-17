from django.test import AsyncClient
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from settings import settings
from temperature import schemas, crud
from city.crud import get_cities

router = APIRouter()


@router.get(
    "/temperatures/",
    response_model=list[schemas.TemperatureList]
)
def read_temperatures(
    city_id: int | None = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    return crud.get_temperatures(
        city_id=city_id, skip=skip, limit=limit, db=db
    )


load_dotenv()

WEATHER_API = "https://api.weatherapi.com/v1/current.json"


@router.post("/temperatures/update/", response_model=dict)
async def update_temperatures(db: Session = Depends(get_db)):
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
