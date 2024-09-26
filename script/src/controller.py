from fastapi import FastAPI
import script as s
from pydantic import BaseModel

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})
cursor, conn = s.connect()



class Student(BaseModel):
    id: int
    name: str
    course_number: int

class Discipline(BaseModel):
    id: int
    discipline_name: str
    day_of_week: str
    lesson_number: int
    course_number: int


@app.get("/student/{id}")
async def get_student_by_id(id: int):
    return s.get_student(id, cursor)

@app.get("/discipline/{course_number}")
async def get_disciplines_by_course_number(course_number: int):
    return s.get_discipline(course_number, cursor)

@app.get("/students_by_course/{course_number}")
async def get_students_by_course_number(course_number: int):
    return s.get_students_by_course(course_number, cursor)

@app.get("/discipline")
async def get_all_disciplines():
    return s.get_all_disciplines(cursor)

@app.post("/student")
async def add_student(student: Student):
    s.add_student(student.name, student.course_number, cursor, conn)
    return {"status": 201}, 201
