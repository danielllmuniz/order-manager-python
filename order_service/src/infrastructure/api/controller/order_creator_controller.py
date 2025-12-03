
from order_service.src.infrastructure.api.controller.interfaces.controller_interface import ControllerInterface
from order_service.src.infrastructure.api.controller.http_types.http_response import HttpResponse
from order_service.src.application.use_cases.interfaces.create_order_use_case import CreateOrderUseCase
from order_service.src.application.ports.logger import ILogger

class OrderCreatorController(ControllerInterface):
    def __init__(self, usecase: CreateOrderUseCase, logger: ILogger | None = None) -> None:
        self._usecase = usecase
        self._logger = logger

    def handle(self) -> HttpResponse:
        if self._logger:
            self._logger.debug("OrderCreatorController.handle() called")

        body_respone = self._usecase.execute()

        if self._logger:
            self._logger.debug("Use case executed successfully, building response")

        return HttpResponse(status_code=201, body=body_respone)
