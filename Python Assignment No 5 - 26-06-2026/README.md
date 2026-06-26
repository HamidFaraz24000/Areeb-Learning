# Student Management REST API

A simple FastAPI REST API for managing student records with JSON file persistence.

## Features

- Create a student
- Get all students
- Get a student by ID
- Update a student
- Delete a student
- Search students by course
- Store records in `students.json` so data remains after restart
- Validate empty names, invalid ages, invalid emails, marks outside `0-100`, duplicate IDs, missing students, invalid request bodies, and missing or empty JSON storage

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

Open the API docs at:

```text
http://127.0.0.1:8000/docs
```

## Example Request

```bash
curl -X POST "http://127.0.0.1:8000/students" \
  -H "Content-Type: application/json" \
  -d "{\"id\":1,\"name\":\"Ali Khan\",\"age\":22,\"email\":\"ali@example.com\",\"course\":\"Computer Science\",\"marks\":85}"
```

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/students` | Create a new student |
| `GET` | `/students` | Get all students |
| `GET` | `/students/{student_id}` | Get one student by ID |
| `PUT` | `/students/{student_id}` | Update a student |
| `DELETE` | `/students/{student_id}` | Delete a student |
| `GET` | `/students/search?course=Computer Science` | Search students by course |

## Example Student

```json
{
  "id": 1,
  "name": "Ali Khan",
  "age": 22,
  "email": "ali@example.com",
  "course": "Computer Science",
  "marks": 85
}
```
