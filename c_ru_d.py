from fastapi import FastAPI, Path
from typing import Annotated
from fastapi import status, Body, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.templating import  Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug= True)


templates = Jinja2Templates(directory="templates")
#Create (POST): Создание новой записи.
# Метод POST отправляет данные на сервер для создания нового объекта.
#Read (GET): Получение данных.
# Метод GET используется для запроса информации,
# такой как получение списка всех задач или одной конкретной задачи.
#Update (PUT): Обновление данных.
# Метод PUT заменяет существующую запись на сервере на новую.
#Delete (DELETE): Удаление данных.
# Метод DELETE удаляет существующую запись.
users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int

@app.get('/', response_class=HTMLResponse)
async def get_user(request: Request):
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})



@app.get('/user/{user_id}', response_class=HTMLResponse)
async def get_list(request: Request, user_id: int):
    user = next((user for user in users if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("users.html", {"request": request, "user": user})

@app.post('/user/{username}/{age}')
async def post_user(username: str, age: int) -> User:
    user_id = (users[-1].id + 1) if users else 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user

    # user_id = str(int(max(users, key=int)) + 1)
    # users[user_id] = f'Имя: {username}, возраст: {age}'
    # return f'User {user_id} is registered!'

@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: str, age: int) -> User:
    try:
        for user in users:
            if user.id == user_id:
                user.username = username
                user.age = age
                return user

        # edit_user = users[user_id]
        # edit_user.username = user

    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


    # users[user_id] = f'Имя: {username}, возраст: {age}'
    # return f"The user {user_id} is updated"

@app.delete('/user/{user_id}')
async def delete_user(user_id: int) -> str:
    try:
        users.pop(user_id)
        return f"User id = {user_id} deleted"
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")

