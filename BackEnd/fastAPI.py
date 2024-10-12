from fastapi import FastAPI
from BackEnd.controllers import sentiment_controller

app = FastAPI()

# Include the router from the sentiment controller
app.include_router(sentiment_controller.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
