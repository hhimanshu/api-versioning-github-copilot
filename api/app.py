from fastapi import FastAPI
from .routers import hello

app = FastAPI(
    title="My FastAPI Application",
    description="A simple FastAPI application with hello endpoint",
    version="1.0.0"
)

# Include routers
app.include_router(hello.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
