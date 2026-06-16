# The Contractor Backend

A Django REST API for managing products, customer orders, and inventory for a contractor/building materials marketplace.

## Features

- User registration and authentication
- Custom user model with customer/admin roles
- Product management
- Categories and units management
- Product options with custom pricing
- Order creation and tracking
- Inventory management
- Customized Django Admin using Jazzmin
- RESTful API endpoints
- PostgreSQL database support
- Media upload support for product images

---

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Jazzmin Admin Theme
- Dynamic REST
- JWT / Token Authentication
- Gunicorn
- WhiteNoise

---

## Project Structure

```bash
.
├── app/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── media/
├── static/
├── requirements.txt
└── manage.py
```

---

## Main Entities

### User

Custom user model with:

- Username
- Full Name
- Phone Number
- Default Location
- Role (Customer / Admin)

### Product

- Name
- Image
- Category
- Unit
- Description
- Price Per Unit
- Available Quantity

### Category

Groups products into categories.

### Unit

Defines measurement units for products.

### Option

Additional product options with optional extra pricing.

### Order

Stores:

- Customer Information
- Delivery Location
- Order Notes
- Order Status

Available statuses:

- Pending
- Confirmed
- In Progress
- Delivered
- Cancelled

### Order Item

Stores ordered products and preserves pricing history.

---

## Installation

### Clone Repository

```bash
git clone https://github.com/hafsaMuhammad/The-Contractor.git
cd The-Contractor
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
DJANGO_SECRET_KEY=your_secret_key

DEBUG=True

SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=contractor
SQL_USER=postgres
SQL_PASSWORD=postgres
SQL_HOST=localhost
SQL_PORT=5432
```

---

## Database Setup

Run migrations:

```bash
python manage.py migrate
```

Create superuser:

```bash
python manage.py createsuperuser
```

---

## Run Development Server

```bash
python manage.py runserver
```

API:

```text
http://127.0.0.1:8000/
```

Admin Panel:

```text
http://127.0.0.1:8000/admin/
```

---

## API Endpoints

### Authentication

| Method | Endpoint |
|----------|----------|
| POST | /register/ |
| POST | /login/ |
| POST | /logout/ |
| GET | /me/ |

### Products

| Method | Endpoint |
|----------|----------|
| GET | /products/ |
| POST | /products/ |
| PUT | /products/{id}/ |
| DELETE | /products/{id}/ |

### Categories

| Method | Endpoint |
|----------|----------|
| GET | /categories/ |

### Units

| Method | Endpoint |
|----------|----------|
| GET | /units/ |

### Options

| Method | Endpoint |
|----------|----------|
| GET | /options/ |

### Orders

| Method | Endpoint |
|----------|----------|
| GET | /orders/ |
| POST | /orders/ |
| PUT | /orders/{id}/ |
| DELETE | /orders/{id}/ |

---

## Order Workflow

```text
Pending
   ↓
Confirmed
   ↓
In Progress
   ↓
Delivered
```

Cancelled orders automatically restore inventory quantities.

---

## Deployment

Production deployment can be done using:

- Gunicorn
- PostgreSQL
- WhiteNoise
- Render
- Railway
- VPS Hosting

---

## Author

Hafsa Mohamed

Junior Software Developer

GitHub:
https://github.com/hafsaMuhammad
