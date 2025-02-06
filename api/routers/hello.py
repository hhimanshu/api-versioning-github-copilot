from fastapi import APIRouter

router = APIRouter(
    prefix="/hello",
    tags=["hello"]
)

@router.get("/")
async def hello_world():
    """
    Returns a simple hello world message
    """
    return {"message": "Hello, World!"}
