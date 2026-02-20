import sys

from loguru import logger

from app.config.paths import LOGS_FILE
from app.config.settings import settings


def setup_logger(
    is_file_log: bool = settings.IS_FILE_LOG,
    is_console_log: bool = settings.IS_CONSOLE_LOG,
):
    logger.remove()

    if is_console_log:
        logger.add(
            sys.stdout,
            level=settings.LOG_LEVEL,
            colorize=True,
        )

    if is_file_log:
        logger.add(
            LOGS_FILE,
            level=settings.LOG_LEVEL,
            rotation=settings.LOG_ROTATION,
            compression=settings.LOG_COMPRESSION,
            enqueue=True,
            # colorize=True,
        )
