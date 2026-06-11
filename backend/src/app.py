from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def welcome_message():
    return {"message": "Hello!"}