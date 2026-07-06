# Inventory & Order Management System

A production-style backend application built with Python, FastAPI, SQLAlchemy, and MySQL. The system manages products, customers, and orders while enforcing inventory business rules such as stock reduction after order creation and stock restoration after cancellation.

## Features

- Add, update, delete, view, and search products.
- Add, update, delete, and view customers.
- Create, view, list, and cancel orders.
- Automatically calculate order totals.
- Prevent ordering more than available stock.
- Restore product stock when an order is cancelled.
- Validate empty fields, invalid emails, invalid phone numbers, duplicate emails, negative prices, negative quantities, and missing resources.

## Technologies Used

- Python 3.11+
- FastAPI
- SQLAlchemy 2
- MySQL
- PyMySQL
- Pydantic
- Uvicorn
- Pytest

## Installation Steps

1. Create and activate a virtual environment.

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Create the MySQL database.

```sql
CREATE DATABASE inventory_management;
```

4. Copy the environment template and update your database username and password.

```bash
copy .env.example .env
```

## Environment Variables

| Variable | Description | Example |
| --- | --- | --- |
| `APP_NAME` | Application name used in API docs | `Inventory & Order Management System` |
| `APP_ENV` | Environment name | `development` |
| `DATABASE_URL` | SQLAlchemy database connection string | `mysql+pymysql://root:password@localhost:3306/inventory_management` |

## How to Run

```bash
uvicorn inventory_management.main:app --reload
```

Open the Swagger UI at:

```text
http://127.0.0.1:8000/docs
```

## How to Test

```bash
pytest
```

The automated tests use an in-memory SQLite database so the endpoint behavior can be verified without changing your MySQL data.

## Folder Structure

```text
inventory_management/
├── routers/
│   ├── customers.py
│   ├── orders.py
│   └── products.py
├── models/
│   ├── customer.py
│   ├── order.py
│   └── product.py
├── schemas/
│   ├── customer.py
│   ├── order.py
│   └── product.py
├── services/
│   ├── customers.py
│   ├── orders.py
│   └── products.py
├── config.py
├── database.py
├── main.py
├── schema.sql
└── requirements.txt
```

## API Summary

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/products` | Add product |
| `GET` | `/products` | View/search products |
| `GET` | `/products/{product_id}` | View product |
| `PUT` | `/products/{product_id}` | Update product |
| `DELETE` | `/products/{product_id}` | Delete product |
| `POST` | `/customers` | Add customer |
| `GET` | `/customers` | View customers |
| `GET` | `/customers/{customer_id}` | View customer |
| `PUT` | `/customers/{customer_id}` | Update customer |
| `DELETE` | `/customers/{customer_id}` | Delete customer |
| `POST` | `/orders` | Create order |
| `GET` | `/orders` | View all orders |
| `GET` | `/orders/{order_id}` | View order |
| `PATCH` | `/orders/{order_id}/cancel` | Cancel order |

## Database Design

```mermaid
erDiagram
    CUSTOMERS ||--o{ ORDERS : places
    ORDERS ||--|{ ORDER_ITEMS : contains
    PRODUCTS ||--o{ ORDER_ITEMS : included_in

    CUSTOMERS {
        int id PK
        string full_name
        string email UK
        string phone_number
    }

    PRODUCTS {
        int id PK
        string name
        text description
        string category
        decimal unit_price
        int available_quantity
    }

    ORDERS {
        int id PK
        int customer_id FK
        datetime order_date
        decimal total_amount
        string status
    }

    ORDER_ITEMS {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal unit_price
        decimal line_total
    }
```

## Sample Order Request

```json
{
  "customer_id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}
```
