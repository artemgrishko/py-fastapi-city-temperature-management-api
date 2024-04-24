from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from city import schemas, crud


router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CityList])
def read_cities(
        skip: int | None = None,
        limit: int | None = None,
        db: Session = Depends(get_db)
) -> list[schemas.CityList]:
    return crud.get_cities(db=db, skip=skip, limit=limit)


@router.post("/cities/", response_model=schemas.CityList)
def create_city(
        city: schemas.CityCreate,
        db: Session = Depends(get_db)
) -> list[schemas.CityList]:
    return crud.create_city(db=db, city=city)


@router.delete("/cities/{city.id}/", response_model=schemas.CityList)
def delete_city(
        city_id: int,
        db: Session = Depends(get_db)
) -> HTTPException:
    del_city = crud.delete_city(db=db, city_id=city_id)

    if del_city is None:
        raise HTTPException(status_code=404, detail="City does not exist")

    return HTTPException(status_code=204, detail="City deleted")
