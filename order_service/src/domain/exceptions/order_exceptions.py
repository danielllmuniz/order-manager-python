class DomainException(Exception):
    pass


class OrderNotFoundException(DomainException):
    def __init__(self, order_id: str) -> None:
        self.order_id = order_id
        super().__init__(f"Order with ID {order_id} not found")


class InvalidOrderStatusTransitionException(DomainException):
    def __init__(self, current_status: str, new_status: str) -> None:
        self.current_status = current_status
        self.new_status = new_status
        super().__init__(
            f"Invalid status transition from {current_status} to {new_status}"
        )


class OrderAlreadyExistsException(DomainException):
    def __init__(self, order_id: str) -> None:
        self.order_id = order_id
        super().__init__(f"Order with ID {order_id} already exists")


class InvalidOrderDataException(DomainException):
    def __init__(self, message: str) -> None:
        super().__init__(f"Invalid order data: {message}")
