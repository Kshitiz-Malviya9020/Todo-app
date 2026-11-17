from sys import prefix
from fastapi import FastAPI
from app.api.v1.router import api_router


app = FastAPI(
    title="Todo API",
    version="1.0.0",
    description="Backend API for the Todo Application",
)

app.include_router(api_router,prefix='/api/v1')
