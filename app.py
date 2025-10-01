from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from logger import Logger
from db import *

from json import load, loads
from typing import Optional, List, Tuple

import requests

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

app.mount("/static", static, name="static")

# configures

@app.get("/api/users")
async def all_users(request: Request) -> Tuple[List[User], int]:
    try:
        users = mariamanager.get_users()
        if users and users[0] == "404":
            return [], 404
        return users, 200
    except Exception as e:
        logger.log(status="e", message=f"Error getting users: {e}")
        return [], 500

@app.get("/api/users/{id}")
async def get_user(request: Request, id: str) -> List[User]:
    try:
        data = mariamanager.get_user(id)
        if data and data[0] == "404":
            raise HTTPException(status_code=404, detail="User not found")
        return data
    except HTTPException:
        raise
    except Exception as e:
        logger.log(status="e", message=f"Error getting user {id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/api/users/")
async def put_user(
        request: Request,
        email: str,
        login: str,
        password: str,
    ) -> Tuple[str, int]:

    try:
        status = mariamanager.create_user(
            email=email,
            login=login,
            password_unhashed=password
        )

        if status and status[0] == "400":
            raise HTTPException(status_code=400, detail="Bad Request")
        
        return "OK", 201
    except HTTPException:
        raise
    except Exception as e:
        logger.log(status="e", message=f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.patch("/api/users/{id}")
async def patch_user(
        request: Request,
        id: str,
        email: Optional[str] = None,
        login: Optional[str] = None,
        password: Optional[str] = None
    ):

    try:
        user_info = mariamanager.get_user(id)
        if not user_info or user_info[0] == "404":
            raise HTTPException(status_code=404, detail="User not found")

        current_info = user_info[0]
        
        if email is not None:
            current_info["email"] = email
        if login is not None:
            current_info["login"] = login
        if password is not None:
            current_info["password"] = password

        update_status = mariamanager.update_user(
            id=id,
            login=current_info["login"],
            email=current_info["email"],
            password_unhashed=current_info["password"]
        )

        if update_status and update_status[0] == "400":
            raise HTTPException(status_code=400, detail="Bad Request")

        return {"message": "User updated successfully"}, 200

    except HTTPException:
        raise
    except Exception as e:
        logger.log(status="e", message=f"Error updating user {id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.delete("/api/users/{id}")
async def delete_user(request: Request, id: str):
    try:
        user_info = mariamanager.get_user(id)
        if not user_info or user_info[0] == "404":
            raise HTTPException(status_code=404, detail="User not found")

        delete_status = mariamanager.delete_user(id=id)

        if delete_status and delete_status[0] == "400":
            raise HTTPException(status_code=400, detail="Bad Request")

        return {"message": "User deleted successfully"}, 200

    except HTTPException:
        raise
    except Exception as e:
        logger.log(status="e", message=f"Error deleting user {id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/posts")
async def get_posts(request: Request):
    try:
        posts = mariamanager.get_posts()
        return posts
    except Exception as e:
        logger.log(status="e", message=f"Error getting posts: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    

@app.get("/api/posts/{id}")
async def get_post(request: Request, id: str):
    try:
        data = mariamanager.get_post(id)
        if data and data[0] == "404":
            raise HTTPException(status_code=404, detail="Post not found")
        return data
    except HTTPException:
        raise
    except Exception as e:
        logger.log(status="e", message=f"Error getting post {id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/users")
async def all_users(request: Request) -> Tuple[List[User], int]:
    try:
        users = mariamanager.get_users()
        if users and users[0] == "404":
            return [], 404
        return users, 200
    except Exception as e:
        logger.log(status="e", message=f"Error getting users: {e}")
        return [], 500

@app.get("/api/users/{id}")
async def get_user(request: Request, id: str) -> List[User]:
    try:
        data = mariamanager.get_post(id)
        if data and data[0] == "404":
            raise HTTPException(status_code=404, detail="Post not found")
        return data
    except HTTPException:
        raise
    except Exception as e:
        logger.log(status="e", message=f"Error getting post {id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.put("/api/posts")
async def put_post(
        request: Request,
        authorId: str,
        title: str,
        content: str           
    ) -> Tuple[str, int]:

    try:
        # Check if author exists
        author_info = mariamanager.get_user(authorId)
        if not author_info or author_info[0] == "404":
            raise HTTPException(status_code=400, detail="Author does not exist")

        status = mariamanager.create_post(
            author_id=authorId,
            title=title,
            content=content
        )

        if status and status[0] == "400":
            raise HTTPException(status_code=400, detail="Bad Request")
        
        return "OK", 201
    except HTTPException:
        raise
    except Exception as e:
        logger.log(status="e", message=f"Error creating post: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
@app.delete("/api/posts/{id}")
async def delete_post(request: Request, id: str) -> Tuple[str, int]:
    try:
        status = mariamanager.delete_post(id)
        
        if status and status[0] == "400":
            raise HTTPException(status_code=400, detail="Bad Request")
            
        return "OK", 200
    except HTTPException:
        raise
    except Exception as e:
        logger.log(status="e", message=f"Error deleting post {id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.patch("/api/posts/{id}")
async def patch_post(
        request: Request,
        id: str,
        title: Optional[str] = None,
        content: Optional[str] = None,
    ):

    try:
        post_info = mariamanager.get_post(id)
        if not post_info or post_info[0] == "404":
            raise HTTPException(status_code=404, detail="Post not found")

        current_info = post_info[0]
        
        if title is not None:
            current_info["title"] = title
        if content is not None:
            current_info["content"] = content

        update_status = mariamanager.update_post(
            id=id,
            title=current_info["title"],
            content=current_info["content"]
        )

        if update_status and update_status[0] == "400":
            raise HTTPException(status_code=400, detail="Bad Request")

        return {"message": "Post updated successfully"}, 200

    except HTTPException:
        raise
    except Exception as e:
        logger.log(status="e", message=f"Error updating post {id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# api

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "message": "Hello, FastAPI!"
        }
    )

@app.get("/users")
def users(request: Request):
    try:
        all_users = requests.get("http://127.0.0.1:8000/api/users", timeout=5)
    except TimeoutError:
        return 404


    return templates.TemplateResponse(
        "users.html",{
            "request": request,
            "users": loads(all_users.text)[0]
        }
    )

@app.get("/users/{id}")
def user(request: Request, id):
    try:
        this_user = requests.get(f"http://127.0.0.1:8000/api/users/{id}", timeout=5)
    except TimeoutError:
        return 404
    
    return templates.TemplateResponse(
        "user.html",{
            "request": request,
            "user": loads(this_user.text)[0]
        }
    )

@app.get("/posts")
def posts(request: Request):
    try:
        all_posts = requests.get("http://127.0.0.1:8000/api/posts", timeout=5)
    except TimeoutError:
        return 404


    return templates.TemplateResponse(
        "posts.html",{
            "request": request,
            "posts": loads(all_posts.text)
        }
    )

@app.get("/posts/{id}")
def post(request: Request, id):
    try:
        this_post = requests.get(f"http://127.0.0.1:8000/api/posts/{id}", timeout=5)
    except TimeoutError:
        return 404
    
    return templates.TemplateResponse(
        "post.html",{
            "request": request,
            "post": loads(this_post.text)[0]
        }
    )

@app.patch("/api/posts/{id}")
async def patch_post(request: Request, id: str, title: str, content: str):
    try:
        status = mariamanager.update_post(id=id, title=title, content=content)
        if status and status[0] == "400":
            raise HTTPException(status_code=400, detail="Bad Request")
        return "OK", 200
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")