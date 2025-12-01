from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from api.core.config import settings
from api.core.logging import get_logger, setup_logging
from api.core.database import init_db, get_client, drop_db
from api.core.exceptions import (
    InternalServerException,
    TypedHTTPException,
    ValidationException,
)

setup_logging()

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info("Initializing database...")
    await init_db()

    if settings.SEED_IF_EMPTY and await User.count() == 0:
        logger.info("Seeding database...")
        await seed_db()

    # httpx client for external API services
    app.state.http_client = httpx.AsyncClient()

    yield

    # Shutdown
    logger.info("Application shutting down...")
    get_client().close()

    client: httpx.AsyncClient | None = getattr(app.state, "http_client", None)
    if client:
        await client.aclose()


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cases_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.exception_handler(RequestValidationError)
async def override_pydantic_validation_error(
    request: Request, exc: RequestValidationError
):
    raise ValidationException(detail=str(exc))


@app.exception_handler(TypedHTTPException)
async def typed_exception_handler(request: Request, exc: TypedHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "type": exc.type,
            "detail": exc.detail,
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Server error: {str(exc)}")
    raise InternalServerException
