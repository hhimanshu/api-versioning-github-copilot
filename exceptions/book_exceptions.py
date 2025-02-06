class BookServiceException(Exception):
    """Base exception for book service errors"""
    pass

class BookNotFoundException(BookServiceException):
    """Raised when a book is not found"""
    pass

class InvalidBookDataException(BookServiceException):
    """Raised when book data is invalid"""
    pass

class BookAlreadyExistsException(BookServiceException):
    """Raised when trying to create a book that already exists"""
    pass

class InvalidBookOperationException(BookServiceException):
    """Raised when trying to perform an invalid operation on a book"""
    pass
