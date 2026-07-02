CREATE DATABASE IF NOT EXISTS student_management;

USE student_management;

CREATE TABLE IF NOT EXISTS students (
  id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  age INT NOT NULL,
  email VARCHAR(255) NOT NULL,
  course VARCHAR(100) NOT NULL,
  marks INT NOT NULL,
  PRIMARY KEY (id),
  INDEX ix_students_course (course)
);
