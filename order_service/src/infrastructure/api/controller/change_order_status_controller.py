
from order_service.src.infrastructure.api.controller.interfaces.controller_interface import ControllerInterface
from order_service.src.infrastructure.api.controller.http_types.http_request import HttpRequest
from order_service.src.infrastructure.api.controller.http_types.http_response import HttpResponse
from order_service.src.application.use_cases.change_order_status_use_case import ChangeOrderStatusUseCase
from order_service.src.application.ports.logger import ILogger

class ChangeOrderStatusController(ControllerInterface):
    def __init__(self, usecase: ChangeOrderStatusUseCase, logger: ILogger | None = None) -> None:
        self._usecase = usecase
        self._logger = logger

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        if self._logger:
            self._logger.debug("ChangeOrderStatusController.handle() called")

        order_id = http_request.param.get("order_id")

        if self._logger:
            self._logger.debug(f"Changing status for order ID: {order_id}")

        response = self._usecase.execute(order_id)

        if self._logger:
            self._logger.debug("Use case executed successfully, building response")

        return HttpResponse(status_code=200, body=response)
