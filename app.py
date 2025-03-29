import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

data = []
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/demo")
async def demo_name(name: str, age: int):
    if age < 0:
        return {"error": "Age cannot be negative"}
    return {"message": f"Hello {name} - {age} "}

class Books(BaseModel):
    id: int
    title: str
    author: str
    description: str
    price: float
    publisher: str

@app.post("/books")
async def create_book(book: Books):
    data.append(book)
    return {"message": "Book added successfully", "book": book}

@app.get("/books")
def read_books():           
    return {"books": data}

@app.get("/books/{book_id}")
def read_book(book_id: int):
    for book in data:
        if book.id == book_id:
            return {"book": book}
    return {"error": "Book not found"}  

@app.put("/books/{book_id}")
async def update_book(book_id: int, book: Books):
    for i, b in enumerate(data):
        if b.id == book_id:
            data[i] = book
            return {"message": "Book updated successfully", "book": book}
    return {"error": "Book not found"}

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i, b in enumerate(data):
        if b.id == book_id:
            del data[i]
            return {"message": "Book deleted successfully"}
    return {"error": "Book not found"}


class Student(BaseModel):
    id: int
    name: str
    age: int
    subjects: List[str] = []

@app.post("/students")
async def create_student(student: Student):
    data.append(student)
    return {"message": "Student added successfully", "student": student}

@app.get("/students")
def read_students():                  
    return {"students": data}

@app.get("/students/{student_id}")
def read_student(student_id: int):
    for student in data:
        if student.id == student_id:
            return {"student": student}
    return {"error": "Student not found"}   

@app.put("/students/{student_id}")
async def update_student(student_id: int, student: Student):
    for i, s in enumerate(data):
        if s.id == student_id:
            data[i] = student
            return {"message": "Student updated successfully", "student": student}
    return {"error": "Student not found"}

@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
    for i, s in enumerate(data):
        if s.id == student_id:
            del data[i]
            return {"message": "Student deleted successfully"}
    return {"error": "Student not found"}

test_studets = [
    Student(id=1, name="John Doe", age=20, subjects=["Math", "Science"]),
    Student(id=2, name="Jane Smith", age=22, subjects=["English", "History"]),
    Student(id=3, name="Alice Johnson", age=19, subjects=["Art", "Music"]),
]

async def test_api_student():
    for student in test_studets:
        response = await create_student(student)
        print(response)
    print("All test students added successfully")

@app.get("/hello/{name}", response_class=HTMLResponse)
async def read_item(request: Request, name:str):
    return templates.TemplateResponse("hello.html", {"request": request, "name": name})