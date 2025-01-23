import uvicorn
from fastapi import FastAPI
from sqlmodel import SQLModel

from db import engine
from routers import cars, web

async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Car Sharing", lifespan=lifespan)
app.include_router(cars.router)
app.include_router(web.router)

if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)