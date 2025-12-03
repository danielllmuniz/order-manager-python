# Order Manager Python

A distributed order management system with event-driven microservices architecture.

## What is it?

A distributed application that manages orders through two integrated services:

- **Order Service**: REST API to create, retrieve, and update orders
- **Mail Service**: Event consumer that processes order notifications

Communication between services occurs via **RabbitMQ** (event-driven), with caching in **Redis** and persistence in **MongoDB**.

## How to Run

### Prerequisites
- Docker and Docker Compose

### Start

```bash
docker-compose up --build
```

This will start:
- **Order Service**: http://localhost:5000
- **RabbitMQ Management**: http://localhost:15672 (admin/admin)
- MongoDB, Redis, RabbitMQ

### Stop

```bash
docker-compose down
```

## Technologies

| Component | Technology |
|-----------|-----------|
| Web Framework | Flask 3.1.2 |
| Database | MongoDB 4.15.4 |
| Cache | Redis 7 |
| Message Broker | RabbitMQ 3.13 |
| Language | Python 3.12 |
| Testing | Pytest 9.0.1 |

## Architecture

- **Clean Architecture**: Separation between domain, application, and infrastructure layers
- **Event-Driven**: Asynchronous communication via RabbitMQ
- **Cache-Aside**: Redis for read caching
- **Dependency Injection**: Loose coupling of dependencies

## Unit Tests

```bash
# Run all tests
python -m pytest tests/ -v

# With coverage
python -m pytest tests/ --cov=order_service --cov-report=html
```

26 unit tests covering:
- Entities and Value Objects
- Use Cases
- Cache-Aside Pattern
- Order Status State Machine

## API Endpoints

### Create Order
```bash
POST /orders
```

### Get Order
```bash
GET /orders/{order_id}
```

### Update Status
```bash
PATCH /orders/{order_id}/status
```

### Health Check
```bash
GET /health
```

## Default Credentials

- **MongoDB**: admin / admin
- **RabbitMQ**: admin / admin
- **Redis**: password `redis_password`
