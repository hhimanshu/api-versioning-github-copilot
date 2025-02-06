# Versioned API

A FastAPI application demonstrating API versioning.

## Running the Application

1. Install dependencies:
```bash
uv sync
```

2. Run the FastAPI application:
```bash
uvicorn src.api.app:app --reload
```

3. To Upgrade all dependencies:

```bash
uv lock --upgrade
uv sync
```

The application will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Interactive API documentation at `http://localhost:8000/docs`
- Alternative API documentation at `http://localhost:8000/redoc`

## Available Endpoints

- `GET /hello` - Returns a hello world message
