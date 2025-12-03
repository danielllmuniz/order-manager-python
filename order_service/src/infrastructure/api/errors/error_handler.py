from order_service.src.infrastructure.api.controller.http_types.http_response import HttpResponse
from order_service.src.infrastructure.api.errors.error_types.http_bad_request import HttpBadRequestError
from order_service.src.infrastructure.api.errors.error_types.http_not_found import HttpNotFoundError
from order_service.src.infrastructure.api.errors.error_types.http_unprocessable_entity import HttpUnprocessableEntityError
from order_service.src.infrastructure.logging.config import LoggingConfig
from order_service.src.infrastructure.logging.python_logger import PythonLogger

# Setup logging
logging_config = LoggingConfig()
logging_config.setup_logging()
logger = PythonLogger(__name__)

def handle_errors(error: Exception):
    if isinstance(error, (HttpBadRequestError, HttpNotFoundError, HttpUnprocessableEntityError)):
        logger.warning(f"HTTP error handled - {error.name}: {error.message} (Status: {error.status_code})")
        return HttpResponse(
            status_code=error.status_code,
            body={
                "errors": [{
                    "title": error.name,
                    "detail": error.message
                }]
            }
        )
    logger.error(f"Unhandled exception: {type(error).__name__} - {str(error)}")
    return HttpResponse(
        status_code=500,
        body={
            "errors": [{
                "title": "Server Error",
                "detail": str(error)
            }]
        }
    )
