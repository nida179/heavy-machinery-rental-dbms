# Heavy Machinery Rental Management System

A web-based system that digitalizes an offline heavy machinery / earth-moving equipment rental business in Karachi. Customers can browse and book machinery online, while the owner manages inventory, bookings, and payments from one place.

**Course:** Database Management Systems (CS-452), Dr. S.M. Khalid

**University:** UBIT, University of Karachi

**Team:** Nida Hafeez and Fatima Fahad

---

## Features

**Customer**
- Browse available machinery by category
- View machinery details and availability
- Book machinery for a chosen rental period
- View rental history

**Owner / Admin**
- Manage categories and machinery inventory
- Approve or reject bookings
- Log payments against bookings
- Dashboard with revenue and overdue-rental reports

**System rules**
- Booking-conflict validation (no double-booking of the same machine)
- JWT-based authentication with role-based access
- Public (unauthenticated) machinery browsing

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend / API | Django, Django REST Framework |
| Frontend | Next.js |
| Database | PostgreSQL (SQLite used during local development) |
| Auth | JWT |
| Filtering | django-filter |
| CORS | django-cors-headers |

---

## Database Design

The schema is normalized to **3NF** with five core entities:

| Entity | Description |
|---|---|
| Category | Type of machinery (e.g. bulldozer, grader, loader) |
| Machinery | Individual machines, linked to a Category |
| Customer | Registered customers |
| Booking | A rental of a Machinery by a Customer for a date range |
| Payment | Payment record, one-to-one with a Booking |

**Relationships:** Machinery → Category, Booking → Customer + Machinery, Payment → Booking (1:1).

---

## Project Structure

```
DBMS_PROJECT/
├── myproject/          # Django project
│   ├── myproject/      # settings, root urls
│   ├── rental/         # main app: models, serializers, views, urls, admin, tests
│   └── manage.py
└── frontend/           # Next.js app
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Git

### Backend

```bash
cd myproject
python -m venv venv
venv\Scripts\activate          # Windows
pip install django djangorestframework django-filter django-cors-headers djangorestframework-simplejwt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The API runs at `http://127.0.0.1:8000/`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The app runs at `http://localhost:3000/`. Make sure the backend is running and `http://localhost:3000` is listed in `CORS_ALLOWED_ORIGINS` in the Django settings.

### Run Tests

```bash
cd myproject
python manage.py test
```

---

## API Overview

| Endpoint | Description |
|---|---|
| `/api/machinery/` | List machinery (public), manage machinery (admin) |
| `/api/categories/` | Machinery categories |
| `/api/customers/` | Customer records |
| `/api/bookings/` | Create and manage bookings |
| `/api/payments/` | Payment records |

---

## Project Status

- Database design and normalized schema: done
- Backend (models, serializers, views, URLs, JWT auth, CORS, tests): complete
- Frontend: in progress (machinery listing page connected to the live API)
- Polishing: planned

## Out of Scope

- Real-time GPS tracking
- Live payment gateway integration
- Multi-branch support

---

## Contributors

- Nida Hafeez
- Fatima Fahad
