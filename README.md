# Employee Leave Management API

A REST API built with Node.js, Express, MySQL, and `mysql2` for employees to submit leave requests and managers to approve or reject them.

## Why `mysql2`?

`mysql2/promise` is used because it supports parameterized SQL queries (protecting against SQL injection), native async/await, connection pooling, and transactions while keeping the SQL explicit. This is a good fit for an assignment that specifically requires SQL joins and foreign-key behavior.

## Setup

1. Create the database and tables by running `database/schema.sql` in MySQL.
2. Copy `.env.example` to `.env` and enter your MySQL credentials.
3. Install packages: `npm install`
4. Run the API: `npm start`

The server starts at `http://localhost:3000` by default. Use `npm run dev` during development.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/api/employees` | Create an employee |
| GET | `/api/employees?department=Development` | List employees, optionally by department |
| GET | `/api/employees/:id` | Get an employee |
| PUT | `/api/employees/:id` | Update an employee |
| DELETE | `/api/employees/:id` | Delete employee and their leave requests |
| POST | `/api/leaves` | Create a pending leave request |
| GET | `/api/leaves?status=pending&department=Development&employeeId=1` | List leave requests with optional combined filters |
| GET | `/api/leaves/summary` | Return request totals by status |
| GET | `/api/leaves/department-summary` | Return request totals by department |
| GET | `/api/leaves/:id` | Get a leave request with employee data |
| PATCH | `/api/leaves/:id/status` | Approve or reject a pending request |
| DELETE | `/api/leaves/:id` | Delete a leave request |

## Key design notes

- The `leave_requests.employee_id` foreign key uses `ON DELETE CASCADE`, so deleting an employee also deletes all leave requests they submitted.
- The leave-list and leave-detail endpoints use an SQL `JOIN` to return employee name and department with each request.
- Leave creation always writes `pending`; only a manager can change it to `approved` or `rejected`, and a final decision cannot be changed.
- Input validation returns `{ "success": false, "message": "..." }` with 400 for invalid data and 404 for missing records. Duplicate email addresses are handled as a 400 response.

## Example decision request

```http
PATCH /api/leaves/1/status
Content-Type: application/json

{
  "managerId": 3,
  "status": "approved"
}
```
