from __future__ import annotations

import json
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException, Query, Response, status
from pydantic import BaseModel, EmailStr, Field, field_validator


DATA_FILE = Path("students.json")

app = FastAPI(
    title="Student Management REST API",
    description="A simple FastAPI application for managing student records.",
    version="1.0.0",
)


class Student(BaseModel):
    id: int = Field(..., gt=0, description="Unique student ID")
    name: str = Field(..., min_length=1, description="Student name")
    age: int = Field(..., gt=0, le=120, description="Student age")
    email: EmailStr
    course: str = Field(..., min_length=1, description="Course name")
    marks: int = Field(..., ge=0, le=100, description="Marks between 0 and 100")

    @field_validator("name", "course")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Field cannot be empty")
        return cleaned


def load_students() -> List[Student]:
    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        save_students([])
        return []

    try:
        raw_students = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="students.json is invalid. Please fix or replace the JSON file.",
        ) from exc

    if raw_students in (None, ""):
        save_students([])
        return []

    if not isinstance(raw_students, list):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="students.json must contain a JSON array of students.",
        )

    try:
        return [Student.model_validate(student) for student in raw_students]
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="students.json contains invalid student records.",
        ) from exc


def save_students(students: List[Student]) -> None:
    DATA_FILE.write_text(
        json.dumps([student.model_dump() for student in students], indent=2),
        encoding="utf-8",
    )


def find_student_index(students: List[Student], student_id: int) -> int:
    for index, student in enumerate(students):
        if student.id == student_id:
            return index
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Student with ID {student_id} was not found.",
    )


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Student Management REST API is running."}


@app.post("/students", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(student: Student) -> Student:
    students = load_students()
    if any(existing_student.id == student.id for existing_student in students):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Student with ID {student.id} already exists.",
        )

    students.append(student)
    save_students(students)
    return student


@app.get("/students", response_model=List[Student])
def get_all_students() -> List[Student]:
    return load_students()


@app.get("/students/search", response_model=List[Student])
def search_students_by_course(course: str = Query(..., min_length=1)) -> List[Student]:
    course_name = course.strip().lower()
    if not course_name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Course query parameter cannot be empty.",
        )

    students = load_students()
    return [student for student in students if student.course.lower() == course_name]


@app.get("/students/{student_id}", response_model=Student)
def get_student_by_id(student_id: int) -> Student:
    students = load_students()
    return students[find_student_index(students, student_id)]


@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, updated_student: Student) -> Student:
    students = load_students()
    index = find_student_index(students, student_id)

    if updated_student.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student ID in the request body must match the URL student ID.",
        )

    students[index] = updated_student
    save_students(students)
    return updated_student


@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    response_model=None,
)
def delete_student(student_id: int):
    students = load_students()
    index = find_student_index(students, student_id)
    students.pop(index)
    save_students(students)
