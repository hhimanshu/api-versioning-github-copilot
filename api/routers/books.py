from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from models.book import Book, BookStatus, PaginatedBooks
from services.api_version import ApiVersion, get_api_version
from services.book_service import BookService
from dependencies.service import get_book_service
from exceptions.book_exceptions import (
    BookNotFoundException,
    InvalidBookDataException,
    BookAlreadyExistsException,
    InvalidBookOperationException
)

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.post("/", response_model=Book, status_code=201)
async def create_book(
    book: Book,
    book_service: BookService = Depends(get_book_service),
    api_version: ApiVersion = Depends(get_api_version)
):
    """Create a new book"""
    try:
        return await book_service.create_book(book, api_version)
    except (InvalidBookDataException, BookAlreadyExistsException) as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[Book] | PaginatedBooks)
async def get_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, gt=0, le=100),
    status: Optional[BookStatus] = BookStatus.ACTIVE,
    book_service: BookService = Depends(get_book_service),
    api_version: ApiVersion = Depends(get_api_version)
):
    """Get a list of books with pagination"""
    try:
        return await book_service.get_books(skip, limit, status, api_version)
    except InvalidBookDataException as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{book_id}", response_model=Book)
async def get_book(
    book_id: str,
    book_service: BookService = Depends(get_book_service),
    api_version: ApiVersion = Depends(get_api_version)
):
    """Get a specific book by ID"""
    try:
        return await book_service.get_book(book_id, api_version)
    except BookNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{book_id}", response_model=Book)
async def update_book(
    book_id: str,
    book: Book,
    book_service: BookService = Depends(get_book_service),
    api_version: ApiVersion = Depends(get_api_version)
):
    """Update an existing book"""
    try:
        return await book_service.update_book(book_id, book, api_version)
    except BookNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (InvalidBookDataException, InvalidBookOperationException) as e:
        raise HTTPException(status_code=400, detail=str(e))
