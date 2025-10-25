from fastapi import FastAPI
from task_service.src.routes import router
app = FastAPI()

app.include_router(router)