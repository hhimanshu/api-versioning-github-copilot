from fastapi import FastAPI
from .routers import hello, books

app = FastAPI(
    title="BookHub API",
    description="A RESTful API for managing books",
    version="1.0.0"
)

# Include routers
app.include_router(hello.router)
app.include_router(books.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
