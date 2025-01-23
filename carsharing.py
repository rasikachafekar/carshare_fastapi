import uvicorn
from fastapi import FastAPI, Request
from sqlmodel import SQLModel

from db import engine
from routers import cars, web, trips
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Car Sharing", lifespan=lifespan)
app.include_router(cars.router)
app.include_router(trips.router)
app.include_router(web.router)

@app.exception_handler(trips.BadTripException)
async def unicorn_exception_handler(request: Request, exc: trips.BadTripException):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Bad Trip"}
    )

if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)