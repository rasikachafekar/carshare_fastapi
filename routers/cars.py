from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session, select

from db import get_session
from schemas import Car, CarInput, CarOutput, Trip, TripInput

router = APIRouter(prefix="/api/cars")

@router.get("/")
def get_cars(session: Annotated[Session, Depends(get_session)],
             size: str|None = None, doors: int|None = None) -> list[Car]:
    query = select(Car)
    if size:
        query = query.where(Car.size == size)
    if doors:
        query = query.where(Car.doors >= doors)
    return session.exec(query).all()


@router.get("/{id}")
def car_by_id(session: Annotated[Session, Depends(get_session)],
              id: int) -> Car:
    car = session.get(Car, id)
    if car:
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car found with id = {id}")


@router.get("/{id}/trips")
def get_car_trips(session: Annotated[Session, Depends(get_session)],
              id: int) -> CarOutput:
    car = session.get(Car, id)
    if car:
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car found with id = {id}")


@router.post("/")
def add_car(session: Annotated[Session, Depends(get_session)],
            car_input: CarInput) -> Car:
    """
    use car = Car.from_orm(car_input) to create lazy relations correctly.
    """
    car = Car.model_validate(car_input)
    session.add(car)
    session.commit()
    session.refresh(car)
    return car


@router.delete("/{id}", status_code=204)
def remove_car(session: Annotated[Session, Depends(get_session)], id: int) -> None:
    """
    Remove a car provided with `id` in URL and return session code 204 for No content.
    """
    car = session.get(Car, id)
    if car:
        session.delete(car)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No car found with id = {id}")


@router.put("/{id}")
def change_car(session: Annotated[Session, Depends(get_session)],
               id: int, new_data: CarInput) -> Car:
    car = session.get(Car, id)
    if car:
        car.fuel = new_data.fuel
        car.size = new_data.size
        car.doors = new_data.doors
        car.transmission = new_data.transmission
        session.commit()
        return car
    else:
        raise HTTPException(status_code=404, detail=f"Car with id={id} not found")


@router.post("/{car_id}/trips")
def add_trip(car_id: int, trip: TripInput,
             session: Session = Depends(get_session)) -> Trip:
    car = session.get(Car, car_id)
    if car:
        new_trip = Trip.model_validate(trip, update={"car_id": car_id})
        car.trips.append(new_trip)
        session.commit()
        session.refresh(new_trip)
        return new_trip
    else:
        raise HTTPException(status_code=404, detail=f"Car with id {car_id} not found")