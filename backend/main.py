from fastapi import FastAPI

app = FastAPI(
    title="DCN Secure Web Application",
    description="Secure backend API for DCN Project",
    version="1.0.0"
)

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