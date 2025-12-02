
from order_service.src.infrastructure.api.controller.interfaces.controller_interface import ControllerInterface

from order_service.src.infrastructure.api.controller.http_types.http_response import HttpResponse
from order_service.src.application.use_cases.interfaces.create_order_use_case import CreateOrderUseCase

class OrderCreatorController(ControllerInterface):
    def __init__(self, usecase: CreateOrderUseCase) -> None:
        self._usecase = usecase

    def handle(self) -> HttpResponse:
        body_respone = self._usecase.execute()

        return HttpResponse(status_code=201, body=body_respone)
