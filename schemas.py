import json
from sqlmodel import Relationship, SQLModel, Field

class TripInput(SQLModel):
    start: int
    end: int
    description: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "start": 0,
                "end": 20,
                "description": "Airport drop"
            }
        }
    }


class Trip(TripInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    car_id: int = Field(foreign_key="car.id")
    car: "Car" = Relationship(back_populates="trips")


class TripOutput(TripInput):
    id: int


class CarInput(SQLModel): 
    size: str
    fuel: str | None = "electric"
    doors: int
    transmission: str | None = "auto"

    model_config = {
        "json_schema_extra": {
            "example": [
                {
                    "size": "xl",
                    "transmission": "manual",
                    "doors": 6,
                    "fuel": "hybrid"
                }
            ]
        }
    }


class Car(CarInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    trips: list[Trip] = Relationship(back_populates="car")

class CarOutput(CarInput):
    id: int
    trips: list[TripOutput] = []
