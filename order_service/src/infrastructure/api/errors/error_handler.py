from order_service.src.infrastructure.api.controller.http_types.http_response import HttpResponse
from order_service.src.infrastructure.api.errors.error_types.http_bad_request import HttpBadRequestError
from order_service.src.infrastructure.api.errors.error_types.http_not_found import HttpNotFoundError
from order_service.src.infrastructure.api.errors.error_types.http_unprocessable_entity import HttpUnprocessableEntityError

def handle_errors(error: Exception):
    if isinstance(error, (HttpBadRequestError, HttpNotFoundError, HttpUnprocessableEntityError)):
        return HttpResponse(
            status_code=error.status_code,
            body={
                "errors": [{
                    "title": error.name,
                    "detail": error.message
                }]
            }
        )
    return HttpResponse(
        status_code=500,
        body={
            "errors": [{
                "title": "Server Error",
                "detail": str(error)
            }]
        }
    )
