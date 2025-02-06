import asyncio
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from models.book import BookFormat, BookStatus
from repositories.book_repository import BookRepository
from services.book_service import BookService

TEST_DB = "test-db"


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    # Let pytest-asyncio handle loop cleanup


@pytest_asyncio.fixture(scope="session")
async def mongo_client():
    """Create a MongoDB client for the test database."""
    client = AsyncIOMotorClient(
        "mongodb://mongodb:27017/?replicaSet=rs0",
        serverSelectionTimeoutMS=5000
    )
    try:
        # Wait for MongoDB to be ready
        await client.admin.command('ping')
        yield client
    finally:
        await client.drop_database(TEST_DB)
        client.close()


@pytest_asyncio.fixture(scope="function")
async def book_repository(mongo_client):
    # Ensure we have a clean database for each test
    await mongo_client[TEST_DB].books.delete_many({})
    repo = BookRepository(mongo_client, TEST_DB)
    try:
        await repo.create_indexes()
    except Exception as e:
        print(f"Error creating indexes: {e}")
    return repo


@pytest_asyncio.fixture(scope="function")
async def book_service(book_repository):
    return BookService(book_repository)


@pytest_asyncio.fixture(scope="session")
async def create_book_model():
    from models.book import Book
    return Book(
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        description="A story of the fabulously wealthy Jay Gatsby",
        language="English",
        publisher="Charles Scribner's Sons",
        isbn="9780743273565",
        price=9.99,
        status=BookStatus.ACTIVE,
        cover_images=["https://example.com/cover1.jpg"],
        genres=["Fiction", "Classic"],
        book_format=BookFormat.PAPERBACK,
        published_date="1925-04-10"
    )
