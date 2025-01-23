from fastapi import APIRouter
from fastapi.responses import FileResponse, HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Carsharing Simple App to demo FastAPI</title>
        </head>
        <body>
            <h1>Welcome to Car Sharing service</h1>
            <p>No more fluff, because we care more about FastAPI.</p>
        </body>
    </html>
    """

@router.get("/home", response_class=FileResponse)
def home():
    return FileResponse("routers/home.html")

@router.get("/home1", response_class=HTMLResponse)
def home():
    with open("routers/home.html") as f:
        return f.read()