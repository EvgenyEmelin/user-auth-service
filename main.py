from fastapi import FastAPI

from app.src.routes import router

app = FastAPI()

app.include_router(router)