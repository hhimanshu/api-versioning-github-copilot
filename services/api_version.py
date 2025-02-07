import logging
from enum import Enum
from datetime import datetime
from fastapi import Request, HTTPException

logger = logging.getLogger(__name__)


class VersionError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)


class DeprecatedVersionError(HTTPException):
    def __init__(self, detail: str, sunset_date: datetime = None):
        message = f"{
            detail} - This version will be sunset on {sunset_date}" if sunset_date else detail
        super().__init__(status_code=410, detail=message)


class ApiVersion(str, Enum):
    V2024_07_16 = ("2024-07-16", True, datetime(2025, 1, 24), False)
    V2025_01_24 = ("2025-01-24", False, None, False)
    V2025_03_01_PREVIEW = ("2025-03-01-preview", False, None, True)
    LATEST = V2025_01_24

    def __new__(cls, value, deprecated, sunset_date, preview):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.deprecated = deprecated
        obj.sunset_date = sunset_date
        obj.preview = preview
        return obj

    def __str__(self):
        return self.value

    @classmethod
    def is_valid_version(cls, version: str) -> bool:
        try:
            return version in [v.value for v in cls]
        except ValueError:
            return False

    @classmethod
    def from_string(cls, version: str) -> 'ApiVersion':
        """Convert a string to an ApiVersion enum value."""
        try:
            # Find the exact matching version
            return next(
                (v for v in cls if v.value == version),
                ApiVersion.LATEST
            )
        except Exception:
            raise VersionError(
                f"Invalid API version: {version}. Valid versions are: {
                    [v.value for v in cls]}"
            )

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)

    def validate(self):
        """Validate if the version can be used."""
        # Don't validate LATEST version
        if self == ApiVersion.LATEST:
            return True

        if self.deprecated:
            raise DeprecatedVersionError(
                f"API version {self.value} is deprecated",
                self.sunset_date
            )
        return True


async def get_api_version(request: Request) -> ApiVersion:
    """Get and validate API version from request state, defaulting to LATEST if not set."""
    version = getattr(request.state, "api_version", ApiVersion.LATEST)
    version.validate()
    return version
