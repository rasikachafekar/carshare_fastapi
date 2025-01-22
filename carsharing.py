from schemas import CarOutput, load_cars, CarInput, save_db, TripInput, TripOutput
from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(title="Car Sharing")

db = load_cars("cars")
@app.get("/")
async def welcome(name):
    """Return a simple welcome message"""
    return {"message": f"Welcome {name}, to the Car Sharing Service"}

@app.get("/api/cars")
def get_cars(size: str|None = None, doors: int|None = None) -> list:
    res = db
    if size:
        res = [car for car in res if car["size"] == size]
    if doors:
        res = [car for car in res if car["doors"] >= doors]
    return res

@app.get("/api/cars/{id}")
def car_by_id(id: int) -> dict:
    res = [car for car in db if car.id == id]
    if res:
        return res[0].model_dump()
    else:
        raise HTTPException(status_code=404, detail=f"No car found with id = {id}")

@app.post("/api/cars")
def post_car(car: CarInput) -> CarOutput:
    car = CarOutput(id = len(db)+1, size=car.size, doors=car.doors,
                    fuel=car.fuel, transmission=car.transmission)
    db.append(car)
    save_db("cars", db)
    return car

@app.delete("/api/cars/id", status_code=204)
def remove_car(id: int) -> None:
    matches = [car for car in db if car.id == id ]
    if matches:
        car = matches[0]
        db.remove(car)
        save_db(db)
    else:
        raise HTTPException(status_code=404, detail=f"No car found with id = {id}")

@app.put("/api/cars/{id}")
def change_car(id: int, new_data: CarInput) -> CarOutput:
    matches = [car for car in db if car.id == id]
    if matches:
        car = matches[0]
        car.fuel = new_data.fuel
        car.size = new_data.size
        car.doors = new_data.doors
        car.transmission = new_data.transmission
        save_db(db)
        return car
    else:
        raise HTTPException(status_code=404, detail=f"Car with id={id} not found")

@app.post("/api/cars/{car_id}/trips")
def post_trip(car_id: int, trip: TripInput) -> TripOutput:
    car_match = [car for car in db if car.id == car_id]
    if car_match:
        car = car_match[0]
        trips = car.trips
        trip = TripOutput(id=len(trips)+1, 
                          start=trip.start, end=trip.end, 
                          description=trip.description)
        trips.append(trip)
        save_db("cars", db)
        return trip
    else:
        raise HTTPException(status_code=404, detail=f"Car with id {car_id} not found")

if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)