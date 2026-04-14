# API Reference

This document lists all available API endpoints for the FinTrack API with example requests and responses.

## Authentication

### Register user

`POST /api/user/register/`

Create a new user account and return initial JWT tokens.

Request body:
```json
{
  "first_name" : "Test",
  "last_name" : "User",
  "username": "testuser",
  "email": "test@example.com",
  "password": "StrongPass123!"
}
```

Response:
```json
{
  "message": "Success! User registered successfully.",
  "user": {
    "id": "...",
    "first_name": "Test",
    "last_name": "User",
    "username": "testuser",
    "email": "test@example.com"
  },
  "data": {
    "username": "testuser",
    "access_token": "<jwt_access_token>",
    "refresh_token": "<jwt_refresh_token>"
  }
}
```

### Obtain token

`POST /api/user/token/`

Authenticate with username/password and return access and refresh tokens.

Request body:
```json
{
  "username": "testuser",
  "password": "StrongPass123!"
}
```

Response:
```json
{
  "message": "Success! Token generated successfully.",
  "data": {
    "username": "testuser",
    "access_token": "<jwt_access_token>",
    "refresh_token": "<jwt_refresh_token>"
  }
}
```

### Refresh token

`POST /api/user/token/refresh/`

Refresh an existing refresh token and return a new access token.

Request body:
```json
{
  "refresh": "<jwt_refresh_token>"
}
```

Response:
```json
{
  "message": "Success! Token refreshed successfully.",
  "data": {
    "username": "testuser",
    "access_token": "<new_jwt_access_token>",
    "refresh_token": "<new_jwt_refresh_token>"
  }
}
```

## Categories

All category endpoints require authentication.

### List categories

`GET /api/categories/`

Return all categories owned by the authenticated user.

Headers:
```http
Authorization: Bearer <access_token>
```

Response:
```json
[
  {
    "id": "...",
    "name": "Salary",
    "type": "income",
    "color": "#00FF00"
  },
  {
    "id": "...",
    "name": "Food",
    "type": "expense",
    "color": "#FF0000"
  }
]
```

### Create category

`POST /api/categories/`

Create a new category for the authenticated user.

Request body:
```json
{
  "name": "Groceries",
  "type": "expense",
  "color": "#FFA500"
}
```

Response:
```json
{
  "id": "...",
  "name": "Groceries",
  "type": "expense",
  "color": "#FFA500"
}
```

### Retrieve category

`GET /api/categories/{id}/`

Return details for a single category by ID.

Response:
```json
{
  "id": "...",
  "name": "Groceries",
  "type": "expense",
  "color": "#FFA500"
}
```

### Update category

`PUT /api/categories/{id}/`

Update an existing category's name, type, or color.

Request body:
```json
{
  "name": "Groceries",
  "type": "expense",
  "color": "#00AA00"
}
```

Response:
```json
{
  "id": "...",
  "name": "Groceries",
  "type": "expense",
  "color": "#00AA00"
}
```

### Delete category

`DELETE /api/categories/{id}/`

Remove a category owned by the authenticated user.

Response:
```http
204 No Content
```

## Transactions

### List transactions

`GET /api/transactions/`

Return all transactions for the authenticated user. Optional query parameters allow filtering by date range, category, and transaction type.

Query parameters:

- `start_date=YYYY-MM-DD` — include transactions on or after this date
- `end_date=YYYY-MM-DD` — include transactions on or before this date
- `category=<name>` — case-insensitive category name match
- `type=income|expense` — filter by transaction type

Example:

`GET /api/transactions/?start_date=2024-04-01&end_date=2024-04-30&type=expense&category=food`

Response:
```json
[
  {
    "id": "...",
    "category": "...",
    "amount": "1000.00",
    "type": "income",
    "description": "Salary deposit",
    "date": "2024-04-01",
    "created_at": "2024-04-01T12:00:00Z"
  },
  {
    "id": "...",
    "category": "...",
    "amount": "250.00",
    "type": "expense",
    "description": "Grocery shopping",
    "date": "2024-04-05",
    "created_at": "2024-04-05T08:30:00Z"
  }
]
```

### Create transaction

`POST /api/transactions/`

Create a new transaction record for the authenticated user.

Request body:
```json
{
  "amount": "500.00",
  "type": "expense",
  "category": "<category_uuid>",
  "description": "Grocery shopping",
  "date": "2024-04-12"
}
```

Response:
```json
{
  "id": "...",
  "user": "...",
  "category": "...",
  "amount": "500.00",
  "type": "expense",
  "description": "Grocery shopping",
  "date": "2024-04-12",
  "created_at": "2024-04-12T08:00:00Z"
}
```

### Retrieve transaction

`GET /api/transactions/{id}/`

Return details for a single transaction by ID.

Response:
```json
{
  "id": "...",
  "user": "...",
  "category": "...",
  "amount": "500.00",
  "type": "expense",
  "description": "Grocery shopping",
  "date": "2024-04-12",
  "created_at": "2024-04-12T08:00:00Z"
}
```

### Update transaction

`PUT /api/transactions/{id}/`

Update an existing transaction.

Request body:
```json
{
  "amount": "550.00",
  "type": "expense",
  "category": "<category_uuid>",
  "description": "Weekly groceries",
  "date": "2024-04-12"
}
```

Response:
```json
{
  "id": "...",
  "amount": "550.00",
  "type": "expense",
  "category": "...",
  "description": "Weekly groceries",
  "date": "2024-04-12",
  "created_at": "2024-04-12T08:00:00Z"
}
```

### Delete transaction

`DELETE /api/transactions/{id}/`

Delete a transaction by ID.

Response:
```http
204 No Content
```

## Insights

### Get financial insights

`GET /api/transactions/insights/`

Generate an AI-backed financial insight for the authenticated user.

Response:
```json
{
  "message": "Successfully generated financial insights",
  "data": {
    "user": "testuser",
    "total_income": 17000.0,
    "total_expense": 14650.0,
    "insights": "Your spending is under control, mostly in Salary."
  }
}
```

## Summaries

### Monthly summary

`GET /api/transactions/summary/?month=YYYY-MM`

Return the user's income, expenses, and net balance for a specific month.

Response:
```json
{
  "message": "Successfully calculated summary",
  "user": "testuser",
  "total_income": 8000.00,
  "total_expenses": 2000.00,
  "net_balance": 6000.00
}
```

### Total transactions

`GET /api/transactions/summary/total/`

Return the user's total transaction count and total transaction amount.

Response:
```json
{
  "message": "Successfully calculated total income and expense",
  "data": {
    "user": "testuser",
    "transaction_count": 5,
    "total": 10300.00
  }
}
```

### Total income

`GET /api/transactions/summary/total/income/`

Return the user's total income amount.

Response:
```json
{
  "message": "Successfully calculated total income",
  "data": {
    "user": "testuser",
    "total_income": 8000.00
  }
}
```

### Total expense

`GET /api/transactions/summary/total/expense/`

Return the user's total expense amount.

Response:
```json
{
  "message": "Successfully calculated total expense",
  "data": {
    "user": "testuser",
    "total_expense": 2000.00
  }
}
```

### Net balance

`GET /api/transactions/summary/net-balance/`

Return the user's current net balance and balance status.

Response:
```json
{
  "message": "Successfully calculated net balance",
  "data": {
    "user": "testuser",
    "net_balance": 6000.00,
    "balance_status": "Cheers! You are in surplus."
  }
}
```
