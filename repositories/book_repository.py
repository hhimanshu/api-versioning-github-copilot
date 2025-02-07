from datetime import datetime, timezone
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from models.book import Book, BookStatus, PaginatedBooks

class BookRepository:
    def __init__(self, mongo_client: AsyncIOMotorClient, database_name: str):
        self.database = mongo_client[database_name]
        self.collection = self.database.books

    async def create_indexes(self):
        """Create necessary indexes for the books collection."""
        await self.collection.create_index("isbn", unique=True)
        await self.collection.create_index("title")
        await self.collection.create_index("author")
        await self.collection.create_index("status")

    async def create(self, book: Book) -> Book:
        """Create a new book in the database."""
        book_dict = book.model_dump(by_alias=True, exclude={"id"})
        try:
            result = await self.collection.insert_one(book_dict)
            book.id = str(result.inserted_id)
            return book
        except DuplicateKeyError:
            raise ValueError(f"Book with ISBN {book.isbn} already exists")

    async def get_one(self, book_id: str) -> Optional[Book]:
        """Retrieve a single book by its ID."""
        try:
            book_dict = await self.collection.find_one({"_id": ObjectId(book_id)})
            if book_dict:
                return Book.model_validate(book_dict)
            return None
        except Exception as e:
            raise ValueError(f"Invalid book ID: {book_id}") from e

    async def get_all(self, skip: int = 0, limit: int = 100, status: Optional[BookStatus] = None) -> List[Book]:
        """Retrieve all books with optional pagination and status filter."""
        query = {}
        if status:
            query["status"] = status

        cursor = self.collection.find(query).skip(skip).limit(limit)
        books = [Book.model_validate(book) async for book in cursor]
        return books

    async def update(self, book_id: str, book_update: Book) -> Optional[Book]:
        """Update an existing book."""
        try:
            update_data = book_update.model_dump(
                by_alias=True,
                exclude={"id", "created_date"},
                exclude_unset=True
            )
            update_data["updated_date"] = datetime.now(tz=timezone.utc)

            result = await self.collection.find_one_and_update(
                {"_id": ObjectId(book_id)},
                {"$set": update_data},
                return_document=True
            )
            
            if result:
                return Book.model_validate(result)
            return None
        except Exception as e:
            raise ValueError(f"Error updating book {book_id}: {str(e)}")

    async def soft_delete(self, book_id: str) -> bool:
        """Soft delete a book by setting its status to INACTIVE."""
        try:
            result = await self.collection.find_one_and_update(
                {"_id": ObjectId(book_id)},
                {
                    "$set": {
                        "status": BookStatus.INACTIVE,
                        "updated_date": datetime.now(tz=timezone.utc),
                        "inactive_date": datetime.now(tz=timezone.utc)
                    }
                },
                return_document=True
            )
            return bool(result)
        except Exception as e:
            raise ValueError(f"Error deleting book {book_id}: {str(e)}")
    
    async def get_books_paginated(self, skip: int = 0, limit: int = 10) -> PaginatedBooks:
        """Retrieve a paginated list of books."""
        total = await self.collection.count_documents({})
        cursor = self.collection.find().skip(skip).limit(limit)
        books = [Book.model_validate(book) async for book in cursor]
        return PaginatedBooks(books=books, total=total, skip=skip, limit=limit)  # noqa: F821
