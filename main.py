import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.views import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App is starting up...")
    yield
    print("App is shutting down...")


app = FastAPI(lifespan=lifespan, title="BCS_APP")


app.include_router(auth_router)


origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
