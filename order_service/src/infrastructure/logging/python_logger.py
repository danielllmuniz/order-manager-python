import logging

from ...domain.interfaces.logger import ILogger


class PythonLogger(ILogger):

    def __init__(self, name: str = __name__):
        self.logger = logging.getLogger(name)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def debug(self, message: str) -> None:
        self.logger.debug(message)
