from fastapi import FastAPI
from database.connection import engine, Base
from backend import models
from backend.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DCN Secure Web Application",
    description="Secure backend API for DCN Project",
    version="1.0.0"
)
app.include_router(router)
@app.get("/")
def home():
    return {
        "message": "DCN Backend is running successfully!"
    }

@app.get("/health")
def health():
    return {
        "status": "OK"
    }