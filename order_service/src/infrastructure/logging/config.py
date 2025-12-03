import logging
import os
from dataclasses import dataclass


@dataclass
class LoggingConfig:
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    log_file: str = os.getenv("LOG_FILE", "logs/order_service.log")

    def get_log_level(self) -> int:
        levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        return levels.get(self.log_level.upper(), logging.INFO)

    def setup_logging(self) -> None:
        logger = logging.getLogger()
        logger.setLevel(self.get_log_level())

        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.get_log_level())
        console_formatter = logging.Formatter(self.log_format, self.date_format)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(self.get_log_level())
        file_formatter = logging.Formatter(self.log_format, self.date_format)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
