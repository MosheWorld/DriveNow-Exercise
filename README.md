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

**Why I chose PostgreSQL over NoSQL (e.g. MongoDB):**
I think PostgreSQL is a better choice than a NoSQL database for this project for a few simple reasons:

1. **Related Data:** A car rental system is relational. Rentals belong to specific cars. PostgreSQL makes sure the data connects correctly and avoids issues like renting a car that isn't available.
2. **Safe Transactions:** When multiple things happen at once (like renting a car), PostgreSQL ensures the database updates safely without any mix-ups.
3. **Easy Searching:** Using SQL makes it much easier to write queries that link different pieces of data together for reports in the future.

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

## How to Use the API

The easiest way to interact with the API is via the fully documented Swagger UI:

- **Swagger Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

## A Brief Architecture Description

This system is built using a decoupled, service-oriented architecture:

- **REST API:** Built with FastAPI, providing a clean interface for car and rental management.
- **Service Layer:** Contains core business logic, using Dependency Injection (Factories) for loose coupling and easy testing.
- **Asynchronous Processing:** Offloads metrics and events to a background worker via RabbitMQ, ensuring the primary API stays responsive and fast.
- **Data Persistence:** Relational data is managed via PostgreSQL and SQLAlchemy ORM for high integrity.

## Example usage

This section walks you through how to use the system step-by-step. You can do all of these steps directly in the Swagger UI.

### Step 1: Adding a new Car to the fleet

First, you need a car to rent out. Go to the **POST /cars** section and create a car. You just need to give it a model name (like "Kia") and a year (like 2021). When you click "Execute", the system will save the car and give it a unique ID.

### Step 2: Finding your Car's ID

To do anything with your car, you need its ID. Go to the **GET /cars** section and click "Execute". You will see a list of all your cars. Look for the car you just made and copy the "id" value. It looks like a long string of letters and numbers.

### Step 3: Updating car information

If you want to change the car's name or year, you can update it. Go to the **PUT /cars/{id}** section. Paste your car's ID into the box and enter the new information you want to save.

### Step 4: Starting a new Rental

Now it is time to rent the car to a customer. Go to the **POST /rentals** section. Paste the car's ID into the car_id box and type in the customer's name, for example: "Moshe Binieli". When you execute this, the car is officially rented.

### Step 5: Seeing that the car is "In Use"

The system is smart! If you go back to the **GET /cars** section and look at your car list again, you will see that the status of your car has automatically changed from "available" to "in use".

### Step 6: Finishing the Rental

When the customer returns the car, you need to end the rental. Go to the **PATCH /rentals/{car_id}/end-rental** section. Paste the car's ID and click "Execute". This tells the system the car is back.

### Step 7: Seeing that the car is "Available" again

If you check the **GET /cars** list one last time, you will see the status is back to "available". This means the car is ready for the next person to rent it.

## Testing

```bash
python -m pytest tests/ -v
```
