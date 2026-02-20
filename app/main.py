from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.api import router as main_router
from app.config.settings import settings
from app.utils.logger import setup_logger


setup_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url=settings.APP_DOCS_URL,
    redoc_url=settings.APP_REDOC_URL,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)
