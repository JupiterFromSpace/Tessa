# Tessa Backend

Iran-focused car rental marketplace demo backend built with Django REST Framework.

## MVP

- Google Sign-In with JWT access/refresh tokens
- Renter accounts
- Provider verification workflow
- Vehicle listing and images
- Vehicle search/filter
- Date-based availability filtering
- Booking requests
- Provider approve/reject booking
- PostgreSQL
- Docker

Payments, chat/WebSockets, reviews, notifications, and advanced pricing are intentionally out of scope for the first demo.

## Run

```bash
cp .env.example .env
docker compose build
docker compose up -d
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
```

API base URL: `http://localhost:8000/api/v1/`

Admin: `http://localhost:8000/admin/`
