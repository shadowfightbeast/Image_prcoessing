from fastapi import FastAPI
from app.database import init_db
from app.routers import upload

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    init_db()

app.include_router(upload.router)
