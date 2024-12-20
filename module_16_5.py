from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.templating import Jinja2Templates
from typing import Annotated, List
from pydantic import BaseModel

# Создание объекта FastAPI
app = FastAPI()

# Создание объекта Jinja2Templates
templates = Jinja2Templates(directory="templates")

# Модель пользователя
class User(BaseModel):
    id: int
    username: str
    age: int

# Список пользователей
users: List[User] = []

# GET-запрос: Получение всех пользователей (главная страница)
@app.get("/")
async def get_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

# POST-запрос: Добавление нового пользователя
@app.post("/user/{username}/{age}")
async def create_user(
    username: Annotated[
        str,
        Path(title="Enter username", min_length=5, max_length=20, example="UrbanUser")
    ],
    age: Annotated[
        int,
        Path(title="Enter age", ge=18, le=120, example=24)
    ]
) -> User:
    # Определение нового id
    new_id = users[-1].id + 1 if users else 1
    # Создание нового пользователя
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user

# GET-запрос: Получение одного пользователя по ID
@app.get("/user/{user_id}")
async def get_user(request: Request, user_id: int):
    # Поиск пользователя по ID
    user = next((user for user in users if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("user.html", {"request": request, "user": user})

# PUT-запрос: Обновление информации о пользователе
@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
    user_id: Annotated[
        int,
        Path(title="Enter User ID", ge=1, example=1)
    ],
    username: Annotated[
        str,
        Path(title="Enter username", min_length=5, max_length=20, example="UrbanProfi")
    ],
    age: Annotated[
        int,
        Path(title="Enter age", ge=18, le=120, example=28)
    ]
) -> User:
    # Поиск пользователя по id
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    # Если пользователь не найден
    raise HTTPException(status_code=404, detail="User was not found")

# DELETE-запрос: Удаление пользователя
@app.delete("/user/{user_id}")
async def delete_user(
    user_id: Annotated[
        int,
        Path(title="Enter User ID", ge=1, example=2)
    ]
) -> User:
    # Поиск и удаление пользователя
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    # Если пользователь не найден
    raise HTTPException(status_code=404, detail="User was not found")
