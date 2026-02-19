# DriveNow Vehicle Management System

## Quick Database Check

Run the following command to see the cars in the database:

```bash
docker exec -it drivenow-db-1 psql -U user -d drivenow -c "SELECT * FROM cars;"
```
