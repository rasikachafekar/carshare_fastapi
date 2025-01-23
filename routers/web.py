from typing import Annotated
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from db import get_session
from routers.cars import get_cars

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request":request})

@router.post("/search", response_class=HTMLResponse)
def search(size: Annotated[str, Form()],
           doors: Annotated[int, Form()],
           request: Request,
           session: Session = Depends(get_session)):
    cars = get_cars(session=session, size=size, doors=doors)
    return templates.TemplateResponse("search_results.html", {"request":request, "cars":cars})
