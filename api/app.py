from fastapi import FastAPI

from api.middleware.custom_openapi import custom_openapi
from api.middleware.version_middleware import APIVersionMiddleware
from .routers import hello, books

app = FastAPI(
    title="BookHub API",
    description="A RESTful API for managing books",
    version="1.0.0"
)

# Include routers
app.include_router(hello.router)
app.include_router(books.router)

# Include middleware
app.add_middleware(APIVersionMiddleware)

app.openapi = custom_openapi(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
