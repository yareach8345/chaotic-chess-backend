import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.middle_ware.cookie_check_middleware import CookieCheckMiddleware
from app.routes.v1.router import api_router

app = FastAPI(
    title="Chaotic Chess",
    description="Chaotic Chess routes",
    version="0.0.0",
)

app.include_router(api_router, prefix="/api/v1")
app.add_middleware(CookieCheckMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

if __name__ == "__main__":
    uvicorn.run(app, port=8000)