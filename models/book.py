from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId


# Custom type for MongoDB ObjectId
PyObjectId = Annotated[str, BeforeValidator(str)]

class BookStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class BookFormat(str, Enum):
    PAPERBACK = "PAPERBACK"
    HARDCOVER = "HARDCOVER"
    EBOOK = "EBOOK"

class RatingStats(BaseModel):
    one_star: int = Field(default=0, ge=0)
    two_star: int = Field(default=0, ge=0)
    three_star: int = Field(default=0, ge=0)
    four_star: int = Field(default=0, ge=0)
    five_star: int = Field(default=0, ge=0)
    
@staticmethod
def _get_current_utc_time() -> datetime:
    return datetime.now(tz=timezone.utc)

class Book(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "description": "A story of the fabulously wealthy Jay Gatsby",
                "language": "English",
                "publisher": "Charles Scribner's Sons",
                "published_date": "1925-04-10",
                "isbn": "9780743273565",
                "price": 9.99,
                "status": "ACTIVE",
                "cover_images": ["https://example.com/cover1.jpg"],
                "genres": ["Fiction", "Classic"],
                "book_format": "PAPERBACK"
            }
        }
    )

    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    language: str = Field(..., min_length=2, max_length=50)
    publisher: str = Field(..., min_length=1, max_length=100)
    published_date: datetime
    isbn: str = Field(..., pattern=r'^(?:\d{10}|\d{13})$')
    price: float = Field(..., gt=0)
    status: BookStatus = Field(default=BookStatus.PENDING)
    created_date: datetime = Field(default_factory=_get_current_utc_time)
    updated_date: Optional[datetime] = None
    inactive_date: Optional[datetime] = None
    cover_images: List[str] = Field(default_factory=list)
    genres: List[str] = Field(..., min_length=1)
    book_format: BookFormat
    ratings: RatingStats = Field(default_factory=RatingStats)
    number_of_reviews: int = Field(default=0, ge=0)
