import json
from pydantic import BaseModel

class TripInput(BaseModel):
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


class TripOutput(TripInput):
    id: int


class CarInput(BaseModel): 
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

class CarOutput(CarInput):
    id: int
    trips: list[TripOutput] = []


def load_cars(file_name) -> list[CarOutput]:
    """ Helper function to load cars DB from a JSON file """
    with open(f"{file_name}.json")  as f:
        return [CarOutput.model_validate(obj) for obj in json.load(f)]


def save_db(file_name, cars):
    with open(f"{file_name}.json", "w") as f:
        json.dump([car.model_dump() for car in cars], f, indent=4)
