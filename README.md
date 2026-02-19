# DriveNow

## Setup

```bash
docker-compose up -d
pip install -r requirements.txt
python -m api.api
```

Server: `http://localhost:8000`
Docs: `http://localhost:8000/docs`

## Usage (Curl)

**Add Car**

```bash
curl -X POST "http://localhost:8000/cars" -H "Content-Type: application/json" -d "{\"model\": \"Kia\", \"year\": 2021}"
```

**Get Cars**

```bash
curl "http://localhost:8000/cars"
```

**Rent Car**
Replace `YOUR_CAR_ID` with an actual ID.

```bash
curl -X POST "http://localhost:8000/rentals" -H "Content-Type: application/json" -d "{\"car_id\": \"YOUR_CAR_ID\", \"customer_name\": \"Moshe Binieli\"}"
```

**Get Rentals**

```bash
curl "http://localhost:8000/rentals"
```

## Database Inspection

**Cars**

```bash
docker exec -it drivenow-db-1 psql -U user -d drivenow -c "SELECT * FROM cars;"
```

**Rentals**

```bash
docker exec -it drivenow-db-1 psql -U user -d drivenow -c "SELECT * FROM rentals;"
```
