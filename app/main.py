import pathlib
import os
import io
import uuid
from functools import lru_cache
from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    Request,
    File,
    UploadFile
    )
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    debug: bool = False
    echo_active: bool = False

    class Config:
        env_filed = ".env"

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
DEBUG=settings.debug

# Defining base directory of an app
BASE_DIR = pathlib.Path(__file__).parent

UPLOAD_DIR = BASE_DIR / "uploaded"

# Inititalizing FastaAPI app
app = FastAPI()
# Connecting templating engine
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse) # http GET -> JSON
def home_view(request: Request, settings:Settings = Depends(get_settings)):
    return templates.TemplateResponse("home.html", {"request": request, "abc": 123})

@app.post("/") # http POST
def home_detail_view():
    return {"hello": "world"}

@app.post("/img-echo/", response_class=FileResponse) # http POST
async def img_echo_view(file:UploadFile = File(...), settings:Settings = Depends(get_settings)):
    if not settings.echo_active:
        raise HTTPException(detail="Invalid endpoint", status_code=400)
    bytes_str = io.BytesIO(await file.read()) # getting bytes of an image
    fname = pathlib.Path(file.filename) # getting file name
    fext = fname.suffix # getting file extension
    destination = UPLOAD_DIR / f"{uuid.uuid1()}{fext}"
    with open(str(destination), 'wb') as out:
        out.write(bytes_str.read())
    return destination