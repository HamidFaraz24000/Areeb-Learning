from __future__ import annotations

import os
from typing import Generator, List

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from sqlalchemy import Column, Integer, String, create_engine, func, select
from sqlalchemy.engine import URL
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


load_dotenv()


def build_database_url() -> URL | str:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    return URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        database=os.getenv("MYSQL_DATABASE", "student_management"),
    )


engine = create_engine(build_database_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


class StudentRecord(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String(255), nullable=False)
    course = Column(String(100), nullable=False, index=True)
    marks = Column(Integer, nullable=False)


app = FastAPI(
    title="Student Management REST API",
    description="A simple FastAPI application for managing student records in MySQL.",
    version="1.0.0",
)


class Student(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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


@app.on_event("startup")
def create_tables() -> None:
    try:
        Base.metadata.create_all(bind=engine)
    except OperationalError as exc:
        raise RuntimeError(
            "Could not connect to MySQL. Check MYSQL_HOST, MYSQL_USER, "
            "MYSQL_PASSWORD, and MYSQL_DATABASE."
        ) from exc


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_student_or_404(db: Session, student_id: int) -> StudentRecord:
    student = db.get(StudentRecord, student_id)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} was not found.",
        )
    return student


def commit_or_500(db: Session) -> None:
    try:
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while saving the student record.",
        ) from exc


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Student Management REST API is running with MySQL."}


@app.post("/students", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(student: Student, db: Session = Depends(get_db)) -> StudentRecord:
    student_record = StudentRecord(**student.model_dump())
    db.add(student_record)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Student with ID {student.id} already exists.",
        ) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while creating the student.",
        ) from exc

    db.refresh(student_record)
    return student_record


@app.get("/students", response_model=List[Student])
def get_all_students(db: Session = Depends(get_db)) -> List[StudentRecord]:
    return list(db.scalars(select(StudentRecord).order_by(StudentRecord.id)).all())


@app.get("/students/search", response_model=List[Student])
def search_students_by_course(
    course: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
) -> List[StudentRecord]:
    course_name = course.strip().lower()
    if not course_name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Course query parameter cannot be empty.",
        )

    statement = (
        select(StudentRecord)
        .where(func.lower(StudentRecord.course) == course_name)
        .order_by(StudentRecord.id)
    )
    return list(db.scalars(statement).all())


@app.get("/students/{student_id}", response_model=Student)
def get_student_by_id(
    student_id: int,
    db: Session = Depends(get_db),
) -> StudentRecord:
    return get_student_or_404(db, student_id)


@app.put("/students/{student_id}", response_model=Student)
def update_student(
    student_id: int,
    updated_student: Student,
    db: Session = Depends(get_db),
) -> StudentRecord:
    if updated_student.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student ID in the request body must match the URL student ID.",
        )

    student = get_student_or_404(db, student_id)
    for field, value in updated_student.model_dump().items():
        setattr(student, field, value)

    commit_or_500(db)
    db.refresh(student)
    return student


@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    response_model=None,
)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = get_student_or_404(db, student_id)
    db.delete(student)
    commit_or_500(db)
