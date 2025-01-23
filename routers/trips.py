from db import get_session
from schemas import Car, Trip, TripInput


from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session

router = APIRouter(prefix="/api/cars/trips")

class BadTripException(Exception):
    pass

@router.post("/{car_id}/add")
def add_trip(car_id: int, trip: TripInput,
             session: Session = Depends(get_session)) -> Trip:
    car = session.get(Car, car_id)
    if car:
        new_trip = Trip.model_validate(trip, update={"car_id": car_id})
        if new_trip.end < new_trip.start:
            raise BadTripException("Trip end before start")
        car.trips.append(new_trip)
        session.commit()
        session.refresh(new_trip)
        return new_trip
    else:
        raise HTTPException(status_code=404, detail=f"Car with id {car_id} not found")