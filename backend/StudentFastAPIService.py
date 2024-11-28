from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor
from typing import List
from fastapi.middleware.cors import CORSMiddleware

# FastAPI app instance
app = FastAPI()

# Allowing CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection configuration
DB_CONFIG = {
    "dbname": "FullStackProjectDb",
    "user": "my_postgres",
    "password": "ishank123",
    "host": "localhost",
    "port": "5432",
}

# Student model
class Student(BaseModel):
    roll_number: int
    name: str
    age: int
    grade: int

# Function to get a database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        return conn
    except OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

# CRUD operations

# 1. Create a new student
@app.post("/students/", response_model=Student)
def create_student(student: Student):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            query = """
            INSERT INTO student (roll_number, name, age, grade)
            VALUES (%s, %s, %s, %s) RETURNING *;
            """
            cur.execute(query, (student.roll_number, student.name, student.age, student.grade))
            new_student = cur.fetchone()
            conn.commit()
            return new_student
    except psycopg2.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Student with this roll_number already exists.")
    finally:
        conn.close()

# 2. Retrieve all students
@app.get("/students/", response_model=List[Student])
def get_all_students():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            query = "SELECT * FROM student;"
            cur.execute(query)
            students = cur.fetchall()
            return students
    finally:
        conn.close()

# 3. Retrieve a student by roll_number
@app.get("/students/{roll_number}", response_model=Student)
def get_student(roll_number: int):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            query = "SELECT * FROM student WHERE roll_number = %s;"
            cur.execute(query, (roll_number,))
            student = cur.fetchone()
            if not student:
                raise HTTPException(status_code=404, detail="Student not found.")
            return student
    finally:
        conn.close()

# 4. Update a student
@app.put("/students/{roll_number}", response_model=Student)
def update_student(roll_number: int, updated_student: Student):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            query = """
            UPDATE student
            SET name = %s, age = %s, grade = %s
            WHERE roll_number = %s RETURNING *;
            """
            cur.execute(query, (updated_student.name, updated_student.age, updated_student.grade, roll_number))
            student = cur.fetchone()
            if not student:
                raise HTTPException(status_code=404, detail="Student not found.")
            conn.commit()
            return student
    finally:
        conn.close()

# 5. Delete a student
@app.delete("/students/{roll_number}")
def delete_student(roll_number: int):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            query = "DELETE FROM student WHERE roll_number = %s RETURNING *;"
            cur.execute(query, (roll_number,))
            student = cur.fetchone()
            if not student:
                raise HTTPException(status_code=404, detail="Student not found.")
            conn.commit()
            return {"message": "Student deleted successfully."}
    finally:
        conn.close()
