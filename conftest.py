import asyncio
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient

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
