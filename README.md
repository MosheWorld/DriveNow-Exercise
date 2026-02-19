# DriveNow

## Setup

```bash
docker-compose up -d
pip install -r requirements.txt
python -m api.api
```

Docs: `http://localhost:8000/docs`

## Database Inspection

**Cars**

```bash
docker exec -it drivenow-db-1 psql -U user -d drivenow -c "SELECT * FROM cars;"
```

**Rentals**

```bash
docker exec -it drivenow-db-1 psql -U user -d drivenow -c "SELECT * FROM rentals;"
```

## Tasks

1. Add appropriate exception handling at both the endpoint level and within the code.
2. Add proper input validation at the beginning of the functions.
3. Create a configuration class and inject it where needed, instead of accessing the configuration from various places throughout the project.
4. Review the SOLID principles and ensure the code meets the standards.
