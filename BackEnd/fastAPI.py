from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from BackEnd.controllers import sentiment_controller, technical_controller, trading_controller
from BackEnd.tasks.trading import autonomous_trading_logic
from BackEnd.tasks.data_collection import daily_data_collection

load_dotenv()

scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    daily_data_collection()
    autonomous_trading_logic()

    scheduler.add_job(autonomous_trading_logic, 'interval', days=1)
    scheduler.add_job(daily_data_collection, 'interval', days=1)
    scheduler.start()

    try:
        yield
    finally:
        scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

# Configure CORS
origins = [
    "http://localhost:5173",  # The origin where your React app is running
    "http://localhost:8000",  # Commonly used dev server port (add if using this port)
    "https://btctrader.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow requests from specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include the router from the sentiment controller
app.include_router(sentiment_controller.router)
app.include_router(technical_controller.router)
app.include_router(trading_controller.router)

