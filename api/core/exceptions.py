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

    def __init__(self, type: str = "not_found", detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, type=type, detail=detail
        )


class AlreadyExistsException(TypedHTTPException):
    """Base exception for resource already exists errors."""

    def __init__(
        self, type: str = "already_exists", detail: str = "Resource already exists"
    ):
        super().__init__(status_code=status.HTTP_409_CONFLICT, type=type, detail=detail)


class UnauthorizedException(TypedHTTPException):
    """Base exception for unauthorized access errors."""

    def __init__(self, type: str = "unauthorized", detail: str = "Unauthorized access"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, type=type, detail=detail
        )


class ForbiddenException(TypedHTTPException):
    """Base exception for forbidden access errors."""

    def __init__(self, type: str = "forbidden", detail: str = "Access forbidden"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, type=type, detail=detail
        )


class LockedException(TypedHTTPException):
    """Base exception for when a resource is locked by another process or user."""

    def __init__(self, type: str = "locked", detail: str = "Resource is locked"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, type=type, detail=detail)


class ValidationException(TypedHTTPException):
    """Base exception for validation errors."""

    def __init__(
        self, type: str = "validation_error", detail: str = "Validation failed"
    ):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, type=type, detail=detail
        )


class BadRequestException(TypedHTTPException):
    """Base exception for bad request errors."""

    def __init__(self, type: str = "bad_request", detail: str = "Bad request"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, type=type, detail=detail
        )


class InternalServerException(TypedHTTPException):
    """Base exception for internal server errors."""

    def __init__(
        self,
        type: str = "internal_server_error",
        detail: str = "An unexpected internal server error occurred.",
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, type=type, detail=detail
        )


class ServiceUnavailableException(TypedHTTPException):
    """Base exception for service unavailable errors."""

    def __init__(
        self,
        type: str = "service_unavailable",
        detail: str = "Service is temporarily unavailable.",
    ):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, type=type, detail=detail
        )
