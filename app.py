from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from logger import Logger
from models import *

from json import load, loads
from requests import get
from typing import Optional

# imports

conf = load(open("confs/conf.json", encoding="utf-8"))

app = FastAPI()
mariamanager = MariaConnection(
    host=conf["db"]["conn"]["host"],
    port=conf["db"]["conn"]["port"],
    user=conf["db"]["conn"]["user"],
    password=conf["db"]["conn"]["password"],
    database=conf["db"]["conn"]["database"],
)

logger = Logger(filepath=conf["logger"]["app"])

templates = Jinja2Templates(directory=conf["fastapi"]["templates"])
static = StaticFiles(directory=conf["fastapi"]["static"])

app.mount("/static", static, "static")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "message": "Hello, FastAPI!"
        }
    )

@app.get("/api/users")
async def all_users(request: Request):
    return mariamanager.get_users()

@app.get("/api/users/{id}")
def get_user(
        request: Request,
        id
    ):
    data = mariamanager.get_user(id)
    if data != []:
        return data
    else:
        return []
    
@app.put("/api/users/{id}")
def put_user(
        request: Request,
        id,
        email: Optional[str] = None,
        login: Optional[str] = None,
        password: Optional[str] = None
    ):

    current_info = loads(get(f"http://127.0.0.1:8000/api/users/{id}").text)[0]

    if str(current_info) != []:

        if email != None:
            current_info["email"] = email
        if login != None:
            current_info["login"] = login
        if password != None:
            current_info["password"] = password
                

        mariamanager.update_user(
            id=id,
            login=current_info["login"],
            email=current_info["email"],
            password_unhashed=current_info["password"]
        )

@app.delete("/api/users/{id}")
def delete_user(
        request: Request,
        id
    ):
    
    mariamanager.delete_user(
        id=id,
    )