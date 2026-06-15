from fastapi import FastAPI
app = FastAPI()
from .modules.courses.router import router as courses_router
from .modules.users.router import router as users_router
@app.get("/")
def welcome_message():
    return {"message": "Hello!"}

app.include_router(courses_router)
app.include_router(users_router)