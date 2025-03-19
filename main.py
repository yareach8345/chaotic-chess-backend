from fastapi import FastAPI
from app.routes.v1.router import api_router

app = FastAPI(
    title="Chaotic Chess",
    description="Chaotic Chess routes",
    version="0.0.0",
)

app.include_router(api_router, prefix="/routes/v1")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}