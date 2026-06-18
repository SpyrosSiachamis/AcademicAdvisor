from fastapi import FastAPI
from .modules.courses.router import router as courses_router
from .modules.users.router import router as users_router
from .modules.course_attempt.router import router as attempt_router
from .modules.university.router import router as uni_router

app = FastAPI()

@app.get("/")
def welcome_message():
    return {"message": "Hello!"}

app.include_router(courses_router)
app.include_router(users_router)
app.include_router(attempt_router)
app.include_router(uni_router)