
from order_service.src.infrastructure.api.controller.interfaces.controller_interface import ControllerInterface
from order_service.src.infrastructure.api.controller.http_types.http_request import HttpRequest
from order_service.src.infrastructure.api.controller.http_types.http_response import HttpResponse
from order_service.src.application.use_cases.get_order_use_case import GetOrderUseCase
from order_service.src.application.dtos.order_dto import GetOrderRequest
from order_service.src.application.ports.logger import ILogger

class GetOrderController(ControllerInterface):
    def __init__(self, usecase: GetOrderUseCase, logger: ILogger | None = None) -> None:
        self._usecase = usecase
        self._logger = logger

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        if self._logger:
            self._logger.debug("GetOrderController.handle() called")

        order_id = http_request.param.get("order_id")

        if self._logger:
            self._logger.debug(f"Fetching order with ID: {order_id}")

        request = GetOrderRequest(order_id=order_id)
        response = self._usecase.execute(request)

        if self._logger:
            self._logger.debug("Use case executed successfully, building response")

        return HttpResponse(status_code=200, body=response)
