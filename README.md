# FinTrack API

FinTrack is a Django REST API for personal finance tracking. It supports authenticated users, category and transaction management, financial summaries, and AI-backed transaction insights via OpenAI / Gemini.

## Tech Stack

- Python 3.14
- Django 6.0.4
- Django REST Framework
- PostgreSQL
- Django REST Framework Simple JWT
- django-filter
- python-decouple
- django-cors-headers
- OpenAI / Gemini integration for insights

## Features

- User registration and JWT authentication
- Category CRUD scoped to each user
- Transaction CRUD
- Monthly income, expense, and net balance summaries
- AI-generated financial insights using OpenAI/Gemini when configured

## Setup

1. Clone the repository:

   ```bash
   git clone <repo-url>
   cd "FinTrack API"
   ```

2. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Create a `.env` file from the example and fill in your values:

   ```powershell
   copy .env.example .env
   ```

5. Run database migrations:

   ```powershell
   python manage.py migrate
   ```

6. (Optional) Create a superuser:

   ```powershell
   python manage.py createsuperuser
   ```

7. Start the development server:

   ```powershell
   python manage.py runserver
   ```

8. Run tests:

   ```powershell
   python manage.py test
   ```

## Environment Variables

Create a `.env` file with the following keys. Do not commit secrets.

```env
# Django settings
DJANGO_SECRET_KEY=your_secret_key_here
DEBUG=False

# Database settings
DB_NAME=<YOUR_DB_NAME>
DB_USER=<YOUR_DB_USER>
DB_PASSWORD=<YOUR_DB_PASSWORD>
DB_HOST=localhost
DB_PORT=5432

# AI integration (optional)
OPENAI_API_KEY=
GEMINI_API_KEY=

# CORS
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOWED_ORIGINS=
```

## API Endpoints

For full request and response examples, see [API Reference](./API.md).

### Authentication

- `POST /api/user/register/`
  - Register a new user
- `POST /api/user/token/`
  - Obtain JWT access and refresh tokens
- `POST /api/user/token/refresh/`
  - Refresh the JWT access token

### Categories

- `GET /api/categories/`
  - List categories for the authenticated user
- `POST /api/categories/`
  - Create a new category
- `GET /api/categories/{id}/`
  - Retrieve a single category
- `PUT /api/categories/{id}/`
  - Update a category
- `DELETE /api/categories/{id}/`
  - Delete a category

### Transactions

- `GET /api/transactions/`
  - List user transactions
- `POST /api/transactions/`
  - Create a transaction
- `GET /api/transactions/{id}/`
  - Retrieve a specific transaction
- `PUT /api/transactions/{id}/`
  - Update a transaction
- `DELETE /api/transactions/{id}/`
  - Delete a transaction

### Insights

- `GET /api/transactions/insights/`
  - Generate a short finance insight for the authenticated user

### Summaries

- `GET /api/transactions/summary/?month=YYYY-MM`
  - Monthly summary for the authenticated user
- `GET /api/transactions/summary/total/`
  - Total transaction amount
- `GET /api/transactions/summary/total/income/`
  - Total income
- `GET /api/transactions/summary/total/expense/`
  - Total expense
- `GET /api/transactions/summary/net-balance/`
  - Current net balance

## Authentication

All protected endpoints require JWT authentication using the `Authorization` header:

```http
Authorization: Bearer <access_token>
```

## Notes

- Configure AI keys only if you want insight generation enabled.
- Keep `.env` out of version control.
- The default database is PostgreSQL.
