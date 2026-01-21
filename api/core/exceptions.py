from fastapi import HTTPException, status


class TypedHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int,
        type: str,
        detail: str,
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.type = type


class NotFoundException(TypedHTTPException):
    """Base exception for resource not found errors."""

    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, type="not_found", detail=detail
        )


class AlreadyExistsException(TypedHTTPException):
    """Base exception for resource already exists errors."""

    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT, type="already_exists", detail=detail
        )


class UnauthorizedException(TypedHTTPException):
    """Base exception for unauthorized access errors."""

    def __init__(self, detail: str = "Unauthorized access"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, type="unauthorized", detail=detail
        )


class ForbiddenException(TypedHTTPException):
    """Base exception for forbidden access errors."""

    def __init__(self, detail: str = "Access forbidden"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, type="forbidden", detail=detail
        )


class LockedException(TypedHTTPException):
    """Base exception for when a resource is locked by another process or user."""

    def __init__(self, detail: str = "Resource is locked"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT, type="locked", detail=detail
        )


class ValidationException(TypedHTTPException):
    """Base exception for validation errors."""

    def __init__(self, detail: str = "Validation failed"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            type="validation",
            detail=detail,
        )


class BadRequestException(TypedHTTPException):
    """Base exception for bad request errors."""

    def __init__(self, detail: str = "Bad request"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, type="bad_request", detail=detail
        )


class InternalServerException(TypedHTTPException):
    """Base exception for internal server errors."""

    def __init__(
        self,
        detail: str = "An unexpected internal server error occurred.",
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            type="internal_server",
            detail=detail,
        )


class ServiceUnavailableException(TypedHTTPException):
    """Base exception for service unavailable errors."""

    def __init__(
        self,
        detail: str = "Service is temporarily unavailable.",
    ):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            type="service_unavailable",
            detail=detail,
        )
