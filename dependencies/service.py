from motor.motor_asyncio import AsyncIOMotorClient
from repositories.book_repository import BookRepository
from services.book_service import BookService
from config import MONGODB_URL, DATABASE_NAME

# MongoDB client instance
client = AsyncIOMotorClient(MONGODB_URL)

def get_book_repository() -> BookRepository:
    return BookRepository(client, DATABASE_NAME)

def get_book_service() -> BookService:
    repository = get_book_repository()
    return BookService(repository)
