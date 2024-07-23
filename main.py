import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from src.middleware.auth_middleware import auth_middleware
from src.api.v1.auth.router import router as auth_router
from src.api.v1.company.router import router as company_router
from src.api.v1.employee.router import router as employee_router
from src.api.v1.department.router import router as department_router
from src.api.v1.position.router import router as position_router
from src.api.v1.user.router import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App is starting up...")
    yield
    print("App is shutting down...")


app = FastAPI(lifespan=lifespan, title="BCS_APP")

app.include_router(auth_router)
app.include_router(company_router)
app.include_router(employee_router)
app.include_router(department_router)
app.include_router(position_router)
app.include_router(user_router)

app.middleware("http")(auth_middleware)


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


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Business Control System API",
        version="1.0.0",
        description="API for Business Control System",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"Bearer Auth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
