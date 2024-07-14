import sys

from loguru import logger


def configure_logger():
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>[{time:YYYY-MM-DD HH:mm:ss.SSS}]</green> <bold><level>[{level}]</level></bold> {message}",
        colorize=True,
    )
