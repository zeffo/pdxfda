from errors import APIError
from logging import getLogger

logger = getLogger("pdxfda")


def handle(exception):
    if isinstance(exception, KeyError):
        logger.debug(str(exception))
        return
    else:
        raise exception
