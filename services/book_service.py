from datetime import datetime, timezone
from typing import List, Optional
from exceptions.book_exceptions import (
    BookNotFoundException,
    InvalidBookDataException,
    BookAlreadyExistsException,
    InvalidBookOperationException
)
from repositories.book_repository import BookRepository
from models.book import Book, BookStatus

class BookService:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def _validate_book_data(self, book: Book) -> None:
        """Validate book data before creation or update"""
        if not book.title or len(book.title.strip()) < 1:
            raise InvalidBookDataException("Book title cannot be empty")
        if not book.author or len(book.author.strip()) < 1:
            raise InvalidBookDataException("Book author cannot be empty")
        if not book.isbn or len(book.isbn.strip()) < 10:
            raise InvalidBookDataException("Invalid ISBN format")
        if book.price and book.price < 0:
            raise InvalidBookDataException("Book price cannot be negative")

    async def create_book(self, book: Book) -> Book:
        """Create a new book with validation"""
        self._validate_book_data(book)
        
        # Set default values for new books
        book.status = BookStatus.ACTIVE
        book.created_date = datetime.now(tz=timezone.utc)
        book.updated_date = book.created_date

        try:
            return await self.book_repository.create(book)
        except ValueError as e:
            raise BookAlreadyExistsException(str(e))

    async def get_book(self, book_id: str) -> Book:
        """Get a book by ID with validation"""
        book = await self.book_repository.get_one(book_id)
        if not book:
            raise BookNotFoundException(f"Book with ID {book_id} not found")
        return book

    async def get_books(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[BookStatus] = BookStatus.ACTIVE
    ) -> List[Book]:
        """Get all books with optional filtering"""
        if skip < 0:
            raise InvalidBookDataException("Skip value cannot be negative")
        if limit < 1:
            raise InvalidBookDataException("Limit must be greater than 0")
        if limit > 100:
            limit = 100  # Enforce maximum limit
            
        return await self.book_repository.get_all(skip, limit, status)

    async def update_book(self, book_id: str, book_update: Book) -> Book:
        """Update a book with validation"""
        existing_book = await self.get_book(book_id)
        
        if existing_book.status == BookStatus.INACTIVE:
            raise InvalidBookOperationException(
                f"Cannot update inactive book with ID {book_id}"
            )

        self._validate_book_data(book_update)
        
        updated_book = await self.book_repository.update(book_id, book_update)
        if not updated_book:
            raise BookNotFoundException(f"Book with ID {book_id} not found")
        return updated_book

    async def delete_book(self, book_id: str) -> None:
        """Soft delete a book"""
        existing_book = await self.get_book(book_id)
        
        if existing_book.status == BookStatus.INACTIVE:
            raise InvalidBookOperationException(
                f"Book with ID {book_id} is already inactive"
            )

        success = await self.book_repository.soft_delete(book_id)
        if not success:
            raise BookNotFoundException(f"Book with ID {book_id} not found")
