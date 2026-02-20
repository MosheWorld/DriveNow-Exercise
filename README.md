# DriveNow - Vehicle Management System

## Graphic Flow of Design Architecture

### 1. Project Architecture

```text
       [Dependency Injection (Factories)]
                  | injects into
                  v
[API Controllers / Routers]
                  |
                  v
         [Business Services] -----> (Publishes Event to Queue)
                  |
                  v
           [Repositories]
                  |
                  v
        [PostgreSQL Database]
```

### 2. Message Queue Flow

```text
[Business Services]
       |
       | (Publishes Event)
       v
   [RabbitMQ]
   (Message Queue)
       |
       | (Listens & Consumes)
       v
[Metrics Worker] ---> Updates -> [Prometheus Gauges]
```

### 3. Docker-Compose Interaction Flow

```text
                      [Client]
                         |
                 (HTTP)  |  Port 8000
                         v
       +------------------------------------+
       |          drivenow_api              |
       +------------------------------------+
         |                 |             ^
  (SQL)  |          (AMQP) |             | (HTTP) Fetch Metrics
         v                 v             |
 [drivenow_db]     [drivenow_rabbitmq]   |
                           ^             |
                   (AMQP)  |             |
                           |             v
       +------------------------------------+
       |        drivenow_metrics_worker     |
       +------------------------------------+
```

### 4. Database Schema

```text
 +-------------------+           +--------------------------+
 |       cars        |           |         rentals          |
 +-------------------+           +--------------------------+
 | id (UUID)         |<----------| car_id (UUID)            |
 | model (String)    |  1 to N   | id (UUID)                |
 | year (Integer)    |           | customer_name (String)   |
 | status (Enum)     |           | start_date (Date)        |
 | created_at (Date) |           | end_date (Date)          |
 | updated_at (Date) |           | created_at (Date)        |
 +-------------------+           | updated_at (Date)        |
                                 +--------------------------+
```

## How to Run the Project

```bash
docker-compose up -d
```

All dependencies, the database, the message broker, the metrics worker, and the core API will automatically build and start inside docker containers.

## How to Use the API or CLI

The easiest way to interact with the API is via the fully documented Swagger UI:

- **Swagger Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

### Real-Time Aggregate Metrics

You can call the `/metrics` endpoint to see all real-time metrics.
This custom endpoint automatically aggregates and combines Prometheus data spanning both the core API HTTP metrics and the asynchronous queue worker metrics service.

```bash
curl http://localhost:8000/metrics
```

## A Brief Architecture Description

This system is built using a decoupled, service-oriented architecture:

- **REST API:** Built with FastAPI, providing a clean interface for car and rental management.
- **Service Layer:** Contains core business logic, using Dependency Injection (Factories) for loose coupling and easy testing.
- **Asynchronous Processing:** Offloads metrics and events to a background worker via RabbitMQ, ensuring the primary API stays responsive and fast.
- **Data Persistence:** Relational data is managed via PostgreSQL and SQLAlchemy ORM for high integrity.

## Database Choice

**Why I chose PostgreSQL over NoSQL (e.g. MongoDB):**
I think PostgreSQL is a better choice than a NoSQL database for this project for a few simple reasons:

1. **Related Data:** A car rental system is relational. Rentals belong to specific cars. PostgreSQL makes sure the data connects correctly and avoids issues like renting a car that isn't available.
2. **Safe Transactions:** When multiple things happen at once (like renting a car), PostgreSQL ensures the database updates safely without any mix-ups.
3. **Easy Searching:** Using SQL makes it much easier to write queries that link different pieces of data together for reports in the future.

## Testing

```bash
python -m pytest tests/ -v
```
