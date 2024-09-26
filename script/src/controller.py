from fastapi import FastAPI, HTTPException
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

@app.put("/student")
async def add_student(student: Student):
    student = s.add_student(student.name, student.course_number, cursor, conn)
    if(student is not None):
        return student
    raise HTTPException(status_code=400, detail="Student not added")

@app.put("/discipline")
async def add_discipline(discipline: Discipline):
    discipline = s.add_discipline(discipline.discipline_name, discipline.day_of_week, discipline.lesson_number, discipline.course_number, cursor, conn)
    if(discipline is not None):
        return discipline
    raise HTTPException(status_code=400, detail="Discipline not added")

@app.delete("/student/{id}")
async def delete_student(id: int):
    student = s.get_student(id, cursor)
    if student is None:
        raise HTTPException(status_code=400, detail="Student not found")
    return s.delete_student(id, cursor, conn)

@app.delete("/discipline/{id}")
async def delete_discipline(id: int):
    discipline = s.get_discipline(id, cursor)
    if discipline is None:
        raise HTTPException(status_code=400, detail="Discipline not found")
    return s.delete_discipline(id, cursor, conn)
