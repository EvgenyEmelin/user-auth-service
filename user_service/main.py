from fastapi import FastAPI

from user_service.src.routes import router

app = FastAPI()

app.include_router(router)