import pytest
from exceptions.book_exceptions import InvalidBookDataException
from models.book import Book, BookFormat, BookStatus

@pytest.mark.asyncio
async def test_create_valid_book(book_service, create_book_model):
    # Create a copy of the model to avoid modifying the fixture
    test_book = Book(**create_book_model.model_dump())
    
    # Act
    created_book = await book_service.create_book(test_book)
    
    # Assert
    assert created_book.title == test_book.title
    assert created_book.author == test_book.author
    assert created_book.status == BookStatus.ACTIVE
    assert created_book.created_date is not None
    assert created_book.updated_date is not None

@pytest.mark.asyncio
async def test_create_invalid_book_empty_title(book_service, create_book_model):
    # Arrange
    test_book = Book(**create_book_model.model_dump())
    test_book.title = ""
    
    # Act & Assert
    with pytest.raises(InvalidBookDataException) as exc_info:
        await book_service.create_book(test_book)
    assert "Book title cannot be empty" in str(exc_info.value)

@pytest.mark.asyncio
async def test_create_invalid_book_empty_author(book_service, create_book_model):
    # Arrange
    test_book = Book(**create_book_model.model_dump())
    test_book.author = "   "  # Empty string with spaces
    
    # Act & Assert
    with pytest.raises(InvalidBookDataException) as exc_info:
        await book_service.create_book(test_book)
    assert "Book author cannot be empty" in str(exc_info.value)

@pytest.mark.asyncio
async def test_create_invalid_book_invalid_isbn(book_service, create_book_model):
    # Arrange
    test_book = Book(**create_book_model.model_dump())
    test_book.isbn = "123"  # Invalid ISBN length
    
    # Act & Assert
    with pytest.raises(InvalidBookDataException) as exc_info:
        await book_service.create_book(test_book)
    assert "Invalid ISBN format" in str(exc_info.value)

@pytest.mark.asyncio
async def test_create_invalid_book_negative_price(book_service, create_book_model):
    # Arrange
    test_book = Book(**create_book_model.model_dump())
    test_book.price = -10.99
    
    # Act & Assert
    with pytest.raises(InvalidBookDataException) as exc_info:
        await book_service.create_book(test_book)
    assert "Book price cannot be negative" in str(exc_info.value)

