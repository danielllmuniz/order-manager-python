from abc import ABC, abstractmethod
from order_service.src.infrastructure.api.controller.http_types.http_response import HttpResponse

class ControllerInterface(ABC):
    @abstractmethod
    def handle(self) -> HttpResponse:
        pass
