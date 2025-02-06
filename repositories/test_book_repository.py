from datetime import datetime, timezone

import pytest
from bson import ObjectId
from models.book import Book, BookFormat, BookStatus


@pytest.fixture
def sample_book():
    return Book(
        title="The Test Book",
        author="Test Author",
        description="A book for testing purposes",
        language="English",
        publisher="Test Publisher",
        published_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
        isbn="1234567890",
        price=29.99,
        genres=["Test", "Programming"],
        book_format=BookFormat.PAPERBACK
    )


@pytest.mark.asyncio
async def test_create_book(book_repository, sample_book):
    # Test creating a new book
    created_book = await book_repository.create(sample_book)
    assert created_book.id is not None
    assert created_book.title == sample_book.title
    assert created_book.isbn == sample_book.isbn
    assert created_book.status == BookStatus.PENDING


@pytest.mark.asyncio
async def test_create_duplicate_book(book_repository, sample_book):
    # Test creating a book with duplicate ISBN
    await book_repository.create(sample_book)
    with pytest.raises(ValueError, match=f"Book with ISBN {sample_book.isbn} already exists"):
        await book_repository.create(sample_book)


@pytest.mark.asyncio
async def test_get_one_book(book_repository, sample_book):
    # Test retrieving a single book
    created_book = await book_repository.create(sample_book)
    retrieved_book = await book_repository.get_one(created_book.id)
    assert retrieved_book is not None
    assert retrieved_book.id == created_book.id
    assert retrieved_book.title == sample_book.title


@pytest.mark.asyncio
async def test_get_one_book_not_found(book_repository):
    # Test retrieving a non-existent book
    non_existent_id = str(ObjectId())
    book = await book_repository.get_one(non_existent_id)
    assert book is None


@pytest.mark.asyncio
async def test_get_all_books(book_repository, sample_book):
    # Test retrieving all books with pagination and filtering
    # Create multiple books
    book1 = await book_repository.create(sample_book)
    book2 = await book_repository.create(sample_book.model_copy(update={'isbn': '0987654321'}))

    # Test pagination
    books = await book_repository.get_all(skip=0, limit=1)
    assert len(books) == 1

    # Test getting all books
    all_books = await book_repository.get_all()
    assert len(all_books) == 2

    # Test status filter
    active_books = await book_repository.get_all(status=BookStatus.PENDING)
    assert len(active_books) == 2


@pytest.mark.asyncio
async def test_update_book(book_repository, sample_book):
    # Test updating a book
    created_book = await book_repository.create(sample_book)
    update_data = sample_book.model_copy()
    update_data.title = "Updated Title"
    update_data.price = 39.99

    updated_book = await book_repository.update(created_book.id, update_data)
    assert updated_book is not None
    assert updated_book.title == "Updated Title"
    assert updated_book.price == 39.99
    assert updated_book.updated_date is not None


@pytest.mark.asyncio
async def test_update_nonexistent_book(book_repository, sample_book):
    # Test updating a non-existent book
    non_existent_id = str(ObjectId())
    updated_book = await book_repository.update(non_existent_id, sample_book)
    assert updated_book is None


@pytest.mark.asyncio
async def test_soft_delete_book(book_repository, sample_book):
    # Test soft deleting a book
    created_book = await book_repository.create(sample_book)
    result = await book_repository.soft_delete(created_book.id)
    assert result is True

    # Verify the book is marked as inactive
    deleted_book = await book_repository.get_one(created_book.id)
    assert deleted_book.status == BookStatus.INACTIVE
    assert deleted_book.inactive_date is not None


@pytest.mark.asyncio
async def test_soft_delete_nonexistent_book(book_repository):
    # Test soft deleting a non-existent book
    non_existent_id = str(ObjectId())
    result = await book_repository.soft_delete(non_existent_id)
    assert result is False
