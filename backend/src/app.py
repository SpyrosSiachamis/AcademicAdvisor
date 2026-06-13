from fastapi import FastAPI
app = FastAPI()
from .modules.courses.router import router as courses_router
@app.get("/")
def welcome_message():
    return {"message": "Hello!"}

app.include_router(courses_router)